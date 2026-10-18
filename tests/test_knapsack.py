import unittest
from greedy.huffman import build_tree, build_codes, encode, decode, compression_stats


class TestHuffman(unittest.TestCase):
    def roundtrip(self, text):
        root = build_tree(text)
        bits = encode(text, build_codes(root))
        self.assertEqual(decode(bits, root), text)
        return bits

    def test_roundtrip(self):
        self.roundtrip("abracadabra")
        self.roundtrip("PKG001 | Electronics | Zone-A\n" * 5)

    def test_edges(self):
        self.roundtrip("")
        self.roundtrip("aaaa")
        self.roundtrip("a")

    def test_prefix_free(self):
        codes = list(build_codes(build_tree("mississippi river")).values())
        for a in codes:
            for b in codes:
                if a != b:
                    self.assertFalse(b.startswith(a))

    def test_compresses(self):
        text = "aaaaaaaabbbc"
        s = compression_stats(text, self.roundtrip(text))
        self.assertGreater(s["ratio"], 1)


if __name__ == "__main__":
    unittest.main()
