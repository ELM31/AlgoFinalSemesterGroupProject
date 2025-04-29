import heapq
from collections import defaultdict
from bitarray import bitarray

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def generate_huffman_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node:
        if node.char is not None:
            code_map[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", code_map)
        generate_huffman_codes(node.right, prefix + "1", code_map)
    return code_map

def compress_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()

    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1

    root = build_huffman_tree(frequency)
    huffman_codes = generate_huffman_codes(root)

    encoded_text = bitarray()
    for char in text:
        encoded_text.extend(huffman_codes[char])

    compressed_path = input_path + ".bin"
    with open(compressed_path, 'wb') as file:
        file.write(encoded_text.tobytes())

    return compressed_path, huffman_codes

def decompress_file(compressed_path, huffman_codes, output_path):
    reverse_codes = {v: k for k, v in huffman_codes.items()}

    with open(compressed_path, 'rb') as file:
        bit_str = bitarray()
        bit_str.fromfile(file)

    decoded_text = ""
    buffer = ""
    for bit in bit_str.to01():
        buffer += bit
        if buffer in reverse_codes:
            decoded_text += reverse_codes[buffer]
            buffer = ""

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(decoded_text)
