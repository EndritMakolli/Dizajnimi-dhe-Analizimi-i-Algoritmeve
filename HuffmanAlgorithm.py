import heapq
from collections import Counter

# Node class for Huffman Tree
class Node:
    def __init__(self, char, freq): # __lt__ essential to compare Nodes by frequency.
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Define comparison operators for priority queue
    def __lt__(self, other):
        return self.freq < other.freq

# Step 1: Build frequency dictionary
# Example: "aabbbcccc" → {'a': 2, 'b': 3, 'c': 4}
def build_frequency_table(text):
    return Counter(text)

# Step 2 & 3: Build Huffman Tree
def build_huffman_tree(freq_table): 
    heap = [Node(char, freq) for char, freq in freq_table.items()] #Every character becomes a Node with its frequency.
    heapq.heapify(heap)

    while len(heap) > 1: # This loop constructs the Huffman Tree by always merging the two least frequent nodes.
        node1 = heapq.heappop(heap) # Remove the node with the lowest frequency from the heap
        node2 = heapq.heappop(heap) # Remove the node with the lowest frequency from the heap
        merged = Node(None, node1.freq + node2.freq)   #  Creates a new internal node with combined frequency
        #Set the two nodes as children of the merged node
        merged.left = node1 
        merged.right = node2
        heapq.heappush(heap, merged) #Push the merged node back into the heap
        # The process continues until only one node remains, which becomes the root of the Huffman Tree.
    return heap[0] 

# Step 4: Generate codes
def generate_codes(root, current_code="", codes={}): # generates a binary code (string of 0s and 1s) for each character depending if it is left or right by traversing the Huffman Tree.
    # If no dictionary was provided, create a new one.
    if codes is None:
        codes = {}

    # Check if this node is a leaf (it has no children), which means:
    # 1) It's a regular leaf in a larger Huffman tree, OR
    # 2) It is the ONLY node in the entire tree (in the case of a single unique character).
    if root.left is None and root.right is None:
        # If 'current_code' is empty, we are dealing with the single-character case.
        # In that scenario, we assign a default code "0" to avoid having an empty code string.
        if current_code == "":
            codes[root.char] = "0"
        else:
            codes[root.char] = current_code
        return codes

    # If the node is not a leaf, recurse down the left child with an added "0" bit.
    generate_codes(root.left, current_code + "0", codes)

    # Then recurse down the right child with an added "1" bit.
    generate_codes(root.right, current_code + "1", codes)

    # The 'codes' dictionary accumulates all character-code mappings during recursion.
    return codes

# Step 5: Encode the input text
def encode_text(text, codes): # takes original input and replaces every character with its corresponding Huffman binary code using the codes dictionary that was built earlier.
    return ''.join(codes[char] for char in text)

# Optional: Decode the encoded text
def decode_text(encoded_text, root):
    # If the tree has only one node (meaning one unique character),
    # then every bit in 'encoded_text' corresponds to the same character.
    if root.left is None and root.right is None:
        # Repeat the single character for however many bits we have.
        return root.char * len(encoded_text)
    
    result = ""
    current = root
    for bit in encoded_text:
        if bit == '0':
            current = current.left
        else:
            current = current.right
        if current.char is not None:
            result += current.char
            current = root
    return result

# Example usage
if __name__ == "__main__":
    text = "Huffman Coding" # The input string that we want to compress using Huffman Coding
    freq_table = build_frequency_table(text) # Calls the function to count how often each character appears in the text
    huffman_tree = build_huffman_tree(freq_table) # Uses a min-heap to build the Huffman Tree by merging the lowest-frequency characters step by step
    codes = generate_codes(huffman_tree) # Traverses the tree to assign binary codes to each character based on its position in the tree

    encoded = encode_text(text, codes) # Replaces each character in the original text with its corresponding binary Huffman code
    decoded = decode_text(encoded, huffman_tree) # Uses the Huffman tree to turn the encoded binary back into the original text.

    print("Original:", text)
    print("Encoded:", encoded) # shows the binary string
    print("Decoded:", decoded) # shows the final result after decoding (should match original!)
    print("Codes:", codes) # shows the Huffman code for each character
