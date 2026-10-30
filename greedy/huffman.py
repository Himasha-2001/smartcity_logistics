"""Compress text using Huffman coding without losing information.

    Frequently used characters get shorter binary codes, while
    less frequently used characters get longer codes. This
    helps reduce the total number of bits needed to store text.

    Steps:
        1. Count how many times each character appears.
        2. Store characters in a min heap based on frequency.
        3. Combine the two characters or nodes with the lowest
            frequencies until one tree remains.
        4. Assign 0 to left branches and 1 to right branches.
        5. Use the codes to encode and decode the text.

    Prefix free coding ensures that the encoded text can be
    decoded without confusion.

    Time Complexity:O(n + k log k), where n is the text length and k is
                    the number of distinct characters.

    Space Complexity:O(k) for storing the Huffman tree and character codes.
"""


import heapq
import itertools
from collections import Counter


class Node:
    """Represents a node in the Huffman tree.

        A leaf node stores a character and its frequency.
        An internal node stores the total frequency of its two children.
    """

    __slots__ = ("char", "freq", "left", "right")

    def __init__(self, char, freq, left=None, right=None):
        self.char, self.freq, self.left, self.right = char, freq, left, right

    @property
    def is_leaf(self):
        return self.left is None and self.right is None


def build_tree(text):
    """Build a Huffman tree using the given text.

    Creates nodes for each character and combines the two
    nodes with the lowest frequencies until one tree remains.

    A tie breaker is used when nodes have the same frequency
    to avoid comparing Node objects and keep the result consistent.

    Returns:The root of the Huffman tree, or None if the text is empty.
    """
    if not text:
        return None
    tie = itertools.count()
    heap = [(f, next(tie), Node(c, f)) for c, f in sorted(Counter(text).items())]
    heapq.heapify(heap)
    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)
        f2, _, b = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, next(tie), Node(None, f1 + f2, a, b)))
    return heap[0][2]


def build_codes(root):
    """Generate binary codes for each character from the Huffman tree.

    Moving left adds 0, and moving right adds 1 to the code.

    Returns:A dictionary containing each character and its binary code.
            Returns an empty dictionary if the tree is empty.
            Assigns "0" if the tree contains only one character.
"""
    if root is None:
        return {}
    if root.is_leaf:
        return {root.char: "0"}
    codes = {}

    def walk(node, prefix):
        if node.is_leaf:
            codes[node.char] = prefix
            return
        walk(node.left, prefix + "0")
        walk(node.right, prefix + "1")

    walk(root, "")
    return codes


def encode(text, codes):
    """Convert text into a binary string using Huffman codes.

    Replaces each character with its corresponding binary code
    and joins all the codes together.

    Returns:A string containing only 0s and 1s.
    KeyError: If a character does not have a code.
    """
    return "".join(codes[c] for c in text)


def decode(bits, root):
    """Convert a binary string back into the original text using the Huffman tree.

    Moves left for 0 and right for 1.
    When a character is found, adds it to the result and
    returns to the root to decode the next character.

    Returns:The decoded original text.
    Incomplete codes at the end are ignored.
    """
    if root is None:
        return ""
    if root.is_leaf:
        return root.char * len(bits)
    out, node = [], root
    for b in bits:
        node = node.left if b == "0" else node.right
        if node.is_leaf:
            out.append(node.char)
            node = root
    return "".join(out)


def compression_stats(text, encoded):
    """Compare the original text size with the Huffman-compressed size.

    Calculates the original size using 8 bits per character
    and compares it with the compressed size.

    Returns:
        A dictionary containing:
            original_bits: Original text size in bits.
            compressed_bits: Compressed text size in bits.
            ratio: Compression ratio. Higher means better compression.
            savings_pct: Percentage of space saved.

        Returns 0.0 for ratio and savings if the input is empty.
    """
    original = 8 * len(text)
    compressed = len(encoded)
    return {"original_bits": original, "compressed_bits": compressed,
            "ratio": original / compressed if compressed else 0.0,
            "savings_pct": 100 * (1 - compressed / original) if original else 0.0}