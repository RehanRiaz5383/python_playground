from tiktoken import encoding_for_model

encoding = encoding_for_model("gpt-3.5-turbo")


#encoded = encoding.encode("Hello, how are you?")

decoded = encoding.decode([9906, 11, 1268, 527, 499, 30])
print(decoded)