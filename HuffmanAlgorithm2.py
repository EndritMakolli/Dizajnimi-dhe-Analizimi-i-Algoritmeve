import heapq
from collections import Counter
import time
import os

##This class defines a node in the Huffman Tree.
class Node:
    def __init__(self, char, freq):
        self.char = char         # Character (None for internal nodes)
        self.freq = freq         # Frequency of the character
        self.left = None         # Left child
        self.right = None        # Right child

    # Define comparison operators for priority queue, This ensures that nodes are compared by their frequency when building the tree.
    def __lt__(self, other):
        return self.freq < other.freq

# Step 1: Build frequency dictionary
# Example: "aabbbcccc" → {'a': 2, 'b': 3, 'c': 4}
def build_frequency_table(text):
    return Counter(text)

# Step 2 & 3: Build Huffman Tree
def build_huffman_tree(freq_table): 
    heap = [Node(char, freq) for char, freq in freq_table.items()] # Every character becomes a Node with its frequency.
    heapq.heapify(heap)

    while len(heap) > 1: # Constructs the Huffman Tree by merging two least frequent nodes.
        node1 = heapq.heappop(heap) # Remove node with lowest frequency
        node2 = heapq.heappop(heap) # Remove next lowest frequency node
        merged = Node(None, node1.freq + node2.freq) # New internal node
        merged.left = node1 
        merged.right = node2
        heapq.heappush(heap, merged) # Push back into heap
    return heap[0] 

# Step 4: Generate codes
def generate_codes(root, current_code="", codes=None): # Generate binary codes for each character
    if codes is None:
        codes = {}

    if root.left is None and root.right is None:
        if current_code == "": # Single character case
            codes[root.char] = "0"
        else:
            codes[root.char] = current_code
        return codes

    generate_codes(root.left, current_code + "0", codes)
    generate_codes(root.right, current_code + "1", codes)

    return codes

# Step 5: Encode the input text
def encode_text(text, codes): # Encode input using Huffman codes
    return ''.join(codes[char] for char in text)

# Optional: Decode the encoded text
def decode_text(encoded_text, root):
    if root.left is None and root.right is None:
        return root.char * len(encoded_text)
    
    result = ""
    current = root
    for bit in encoded_text:
        current = current.left if bit == '0' else current.right
        if current.char is not None:
            result += current.char
            current = root
    return result

# Read file content
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Test Huffman coding on provided file
def test_huffman_on_file(file_path):
    print(f"\nTesting file: {file_path}")  # Print which file is being tested

    text = read_file(file_path)  # Read the content of the file
    original_size = os.path.getsize(file_path) / 1024  # Get original file size in KB

    # ---------- Encoding Phase ----------
    start_time = time.time()  # Start the timer for encoding

    freq_table = build_frequency_table(text)  # Count frequency of each character
    huffman_tree = build_huffman_tree(freq_table)  # Build Huffman tree from frequencies
    codes = generate_codes(huffman_tree)  # Generate binary codes for each character
    encoded = encode_text(text, codes)  # Encode the entire text using Huffman codes

    encoding_time = (time.time() - start_time) * 1000  # Calculate encoding time in milliseconds

    # Compute the compressed size (encoded bits → bytes → KB)
    compressed_size = len(encoded) / 8 / 1024  

    # ---------- Decoding Phase ----------
    start_time = time.time()  # Start the timer for decoding

    decoded = decode_text(encoded, huffman_tree)  # Decode the binary string back to original text

    decoding_time = (time.time() - start_time) * 1000  # Calculate decoding time in milliseconds

    # ---------- Validation ----------
    assert text == decoded, "Decoded text does not match original!"  # Ensure correctness

    # ---------- Results ----------
    print(f"Original Size: {original_size:.2f} KB")  # Show original size
    print(f"Compressed Size: {compressed_size:.2f} KB")  # Show compressed size
    print(f"Compression Ratio: {original_size/compressed_size:.2f}:1 "
          f"({(compressed_size/original_size)*100:.2f}%)")  # Show compression effectiveness
    print(f"Encoding Time: {encoding_time:.2f} ms")  # Time taken to compress
    print(f"Decoding Time: {decoding_time:.2f} ms")  # Time taken to decompress


    assert text == decoded, "Decoded text does not match original!"

    print(f"Original Size: {original_size:.2f} KB")
    print(f"Compressed Size: {compressed_size:.2f} KB")
    print(f"Compression Ratio: {original_size/compressed_size:.2f}:1 ({(compressed_size/original_size)*100:.2f}%)")
    print(f"Encoding Time: {encoding_time:.2f} ms")
    print(f"Decoding Time: {decoding_time:.2f} ms")

# Main execution to test multiple files
if __name__ == "__main__":
    test_files = [
        "english_text.txt",
        "source_code.py",
        "log_file.log"
    ]

    for file_path in test_files:
        test_huffman_on_file(file_path)
