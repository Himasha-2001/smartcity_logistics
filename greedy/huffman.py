import heapq
import itertools
from collections import Counter


class Node:
    __slots__ = ("char", "freq", "left", "right")

    def __init__(self, char, freq, left=None, right=None):
        self.char, self.freq, self.left, self.right = char, freq, left, right

    @property
    def is_leaf(self):
        return self.left is None and self.right is None


def build_tree(text):
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
    return "".join(codes[c] for c in text)


def decode(bits, root):
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
    original = 8 * len(text)
    compressed = len(encoded)
    return {"original_bits": original, "compressed_bits": compressed,
            "ratio": original / compressed if compressed else 0.0,
            "savings_pct": 100 * (1 - compressed / original) if original else 0.0}
