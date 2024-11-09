from transformers import BertTokenizer, BertModel
import docx
import torch

# Load a pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Path to your text file containing song lyrics
file_path = 'lyrics.txt'

# Read lyrics from the Word document
lyrics = read_txt(file_path)

# Tokenize the lyrics into subword tokens using BERT tokenizer
tokens = tokenizer.tokenize(lyrics)

print(tokens)
# Convert tokens to token IDs
token_ids = tokenizer.convert_tokens_to_ids(tokens)
print("Token IDs:", token_ids)

# Token IDs for the full sequence including special tokens
input_ids = tokenizer.encode(text, add_special_tokens=True)
print("Token IDs with special tokens:", input_ids)