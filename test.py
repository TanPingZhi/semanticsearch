import fitz  # PyMuPDF
import sys


def read_pdf_memory_usage(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Initialize an empty string to hold all text
    all_text = ""

    # Iterate through each page and concatenate its text
    for page in doc:
        all_text += page.get_text()

    # Calculate the memory usage of the concatenated text
    memory_usage = sys.getsizeof(all_text)

    # Close the document
    doc.close()

    return memory_usage


pdf_path = 'aa.pdf'
memory_usage = read_pdf_memory_usage(pdf_path)
print(f"The memory usage of the content read from '{pdf_path}' is {memory_usage} bytes.")
import pandas as pd
import sys
import random
import string

def get_size(obj):
    return sys.getsizeof(obj)

# Generate a large string dataset
n_strings = 100000
string_length = 100
data = [''.join(random.choices(string.ascii_letters, k=string_length)) for _ in range(n_strings)]

# Calculate size of raw string list
raw_size = get_size(data)
for s in data:
    raw_size += get_size(s)

# Create DataFrame with different dtypes
df_object = pd.DataFrame({'text': data})
df_string = df_object.astype({'text': 'string'})
df_category = df_object.astype({'text': 'category'})

# Calculate sizes
df_object_size = df_object.memory_usage(deep=True).sum()
df_string_size = df_string.memory_usage(deep=True).sum()
df_category_size = df_category.memory_usage(deep=True).sum()

# Calculate ratios
object_ratio = df_object_size / raw_size
string_ratio = df_string_size / raw_size
category_ratio = df_category_size / raw_size

print(f"Raw string list size: {raw_size / 1024 / 1024:.2f} MB")
print(f"DataFrame size (object dtype): {df_object_size / 1024 / 1024:.2f} MB")
print(f"DataFrame size (string dtype): {df_string_size / 1024 / 1024:.2f} MB")
print(f"DataFrame size (category dtype): {df_category_size / 1024 / 1024:.2f} MB")
print(f"\nMemory usage ratio (object dtype): {object_ratio:.2f}")
print(f"Memory usage ratio (string dtype): {string_ratio:.2f}")
print(f"Memory usage ratio (category dtype): {category_ratio:.2f}")