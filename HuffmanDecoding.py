def huffman_decode(encoded_text, huffman_codes):
    reverse_codes = {code: char for char, code in huffman_codes.items()}
    
    decoded_text = ""
    temp_code = ""
    
    for bit in encoded_text:
        temp_code += bit
        
        if temp_code in reverse_codes:
            decoded_text += reverse_codes[temp_code]
            temp_code = ""
    
    return decoded_text

encoded_text = "101101110"
huffman_codes = {'a': '1', 'b': '01', 'c': '00', 'd': '110'}

decoded_result = huffman_decode(encoded_text, huffman_codes)

print("Encoded Text:", encoded_text)
print("Decoded Text:", decoded_result)