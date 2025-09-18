import tiktoken
from token import *


#creating encoder object
enc = tiktoken.encoding_for_model("gpt-4o")

#My actual text
text = "Hello , I am Mohd Gulam!!"

# Tokens for above text

tokens = enc.encode(text) #Output:  [13225, 1366, 357, 939, 31564, 67, 94801, 313, 2618]

#how to get text from tokens

original_text = enc.decode([13225, 1366, 357, 939, 31564, 67, 94801, 313, 2618])

print(original_text)
