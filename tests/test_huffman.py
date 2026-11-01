import random
import string
import unittest
from collections import Counter

from greedy.huffman import build_tree, build_codes, encode, decode, compression_stats

def roundtrip(text):
    root = build_tree(text)
    bits = encode(text, build_codes(root))
    return decode(bits, root), bits


def leaves(node):
    if node is None:
        return []
    if node.is_leaf:
        return [node]
    return leaves(node.left) + leaves(node.right)


class TestBuildTree(unittest.TestCase):
    def test_empty_text_gives_no_tree(self):
        self.assertIsNone(build_tree(""))

    def test_leaves_match_symbol_frequencies(self):
        text = "abracadabra"
        found = {leaf.char: leaf.freq for leaf in leaves(build_tree(text))}
        self.assertEqual(found, dict(Counter(text)))


class TestBuildCodes(unittest.TestCase):

    def test_codes_are_prefix_free(self):
        codes = list(build_codes(build_tree("mississippi river banks")).values())
        for a in codes:
            for b in codes:
                if a != b:
                    self.assertFalse(b.startswith(a), f"{a} is a prefix of {b}")

    def test_more_frequent_symbols_never_get_longer_codes(self):
        text = "a" * 50 + "b" * 20 + "c" * 10 + "d" * 5 + "e" * 1
        codes = build_codes(build_tree(text))
        freq = Counter(text)
        for x in freq:
            for y in freq:
                if freq[x] > freq[y]:
                    self.assertLessEqual(len(codes[x]), len(codes[y]))


class TestOptimality(unittest.TestCase):
    def test_classic_textbook_example_costs_224_bits(self):
        # Frequencies a:5 b:9 c:12 d:13 e:16 f:45 -> optimal cost 224 bits
        text = "a" * 5 + "b" * 9 + "c" * 12 + "d" * 13 + "e" * 16 + "f" * 45
        bits = encode(text, build_codes(build_tree(text)))
        self.assertEqual(len(bits), 224)


class TestEncode(unittest.TestCase):

    def test_unknown_character_raises_key_error(self):
        codes = build_codes(build_tree("abc"))
        with self.assertRaises(KeyError):
            encode("abcz", codes)


class TestRoundTrip(unittest.TestCase):
    def check(self, text):
        decoded, _ = roundtrip(text)
        self.assertEqual(decoded, text)

    def test_simple_strings(self):
        for text in ["", "a", "aaaa", "ab", "abracadabra", "mississippi"]:
            with self.subTest(text=text):
                self.check(text)

    def test_random_texts(self):
        rng = random.Random(99)
        alphabet = string.ascii_letters + string.digits + " |-:\n"
        for _ in range(100):
            text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 400)))
            self.check(text)


class TestCompressionStats(unittest.TestCase):
    def test_exact_values(self):
        text = "aaaabbc"
        _, bits = roundtrip(text)
        s = compression_stats(text, bits)
        self.assertEqual(s["original_bits"], 56)
        self.assertEqual(s["compressed_bits"], 10)
        self.assertAlmostEqual(s["ratio"], 5.6)
        self.assertAlmostEqual(s["savings_pct"], 100 * (1 - 10 / 56))


if __name__ == "__main__":
    unittest.main()