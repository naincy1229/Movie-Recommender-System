import pickle
import gzip

# Compress movie_dict.pkl
with open('movie_dict.pkl', 'rb') as f_in:
    data = pickle.load(f_in)

with gzip.open('movie_dict_compressed.pkl.gz', 'wb') as f_out:
    pickle.dump(data, f_out)

print("movie_dict.pkl compressed successfully.")

# Compress similarity.pkl
with open('similarity.pkl', 'rb') as f_in:
    data = pickle.load(f_in)

with gzip.open('similarity_compressed.pkl.gz', 'wb') as f_out:
    pickle.dump(data, f_out)

print("similarity.pkl compressed successfully.")
