from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import re
from markupsafe import Markup
app = Flask(__name__)

es = Elasticsearch(["http://localhost:9200"])
model = SentenceTransformer('all-MiniLM-L6-v2')
index_name = "philosopher_quotes"


@app.template_filter('highlight')
def highlight_filter(text, query):
    if not query:
        return text

    # Sort words by length, longest first
    words = sorted(query.split(), key=len, reverse=True)

    # Compile a single regex pattern for all words
    pattern = '|'.join(re.escape(word) for word in words)
    regex = re.compile(f'({pattern})', re.IGNORECASE)

    # Replace all matches with highlighted version
    highlighted = regex.sub(lambda m: f'<span class="highlight">{m.group()}</span>', text)

    # Mark the result as safe HTML
    return Markup(highlighted)

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        query_vector = model.encode(query).tolist()

        search_result = es.search(index=index_name, body={
            "size": 10,  # Limit to top 10 results
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'content_vector') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            },
            "min_score": 1.2,  # Set a minimum relevance threshold
            "sort": [{"_score": "desc"}]  # Sort by score in descending order
        })

        results = []
        for hit in search_result['hits']['hits']:
            results.append({
                'score': hit['_score'],
                'author': hit['_source']['author'],
                'quote': hit['_source']['quote']
            })

        return render_template('search.html', results=results, query=query)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)