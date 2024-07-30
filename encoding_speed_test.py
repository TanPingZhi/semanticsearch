import string
import random

from sentence_transformers import SentenceTransformer
import pandas as pd
import time

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def gen_random_string(n):
    chars = string.ascii_letters + ' '
    return ''.join(random.choice(chars) for _ in range(n))

def main():
    # i want to test the encoding speed of model to encode 1MB
    duration = 0

    nfiles = 2 ** 5
    for file_size in [2 ** 10, 2 ** 11, 2 ** 12, 2 ** 13, 2 ** 14, 2 ** 15, 2 ** 16, 2 ** 17, 2 ** 18, 2 ** 19, 2 ** 20]:
        for i in range(nfiles):
            s = gen_random_string(file_size)

            start = time.time()
            vector = model.encode(s)
            end = time.time()
            duration += end - start

        time_per_file = duration / nfiles
        encoding_rate = file_size/time_per_file
        print("file size: {:d} bytes".format(file_size))
        print("total time: {:.2f} s".format(duration))
        print("time per file: {:.2f} s".format(time_per_file))
        print("encoding rate: {:.2f}KB/s".format(encoding_rate / 2 ** 10))
        print()



if __name__ == "__main__":
    main()