import math
import os
import random
import string
import unittest
from collections import Counter

from greedy.huffman import (build_tree, build_codes, encode, decode,
                            compression_stats, Node)

MANIFEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "sample_manifest.txt")


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


def internal_nodes(node):
    if node is None or node.is_leaf:
        return []
    return [node] + internal_nodes(node.left) + internal_nodes(node.right)


class TestBuildTree(unittest.TestCase):
    def test_empty_text_gives_no_tree(self):
        self.assertIsNone(build_tree(""))

    def test_single_symbol_is_one_leaf(self):
        root = build_tree("aaaa")
        self.assertTrue(root.is_leaf)
        self.assertEqual((root.char, root.freq), ("a", 4))

    def test_root_frequency_equals_text_length(self):
        text = "hello world"
        self.assertEqual(build_tree(text).freq, len(text))

    def test_leaves_match_symbol_frequencies(self):
        text = "abracadabra"
        found = {leaf.char: leaf.freq for leaf in leaves(build_tree(text))}
        self.assertEqual(found, dict(Counter(text)))

    def test_internal_nodes_have_two_children_and_summed_frequency(self):
        for node in internal_nodes(build_tree("mississippi river")):
            self.assertIsNotNone(node.left)
            self.assertIsNotNone(node.right)
            self.assertEqual(node.freq, node.left.freq + node.right.freq)
            self.assertIsNone(node.char)

    def test_number_of_leaves_equals_distinct_symbols(self):
        text = "the quick brown fox"
        self.assertEqual(len(leaves(build_tree(text))), len(set(text)))

    def test_construction_is_deterministic(self):
        text = "deterministic tie breaking test abcabcabc"
        self.assertEqual(build_codes(build_tree(text)), build_codes(build_tree(text)))

    def test_node_is_leaf_property(self):
        self.assertTrue(Node("x", 1).is_leaf)
        self.assertFalse(Node(None, 2, Node("a", 1), Node("b", 1)).is_leaf)


class TestBuildCodes(unittest.TestCase):
    def test_empty_tree_gives_empty_codes(self):
        self.assertEqual(build_codes(None), {})

    def test_single_symbol_gets_code_zero(self):
        self.assertEqual(build_codes(build_tree("aaaa")), {"a": "0"})

    def test_two_symbols_get_one_bit_each(self):
        codes = build_codes(build_tree("aab"))
        self.assertEqual(sorted(codes.values()), ["0", "1"])

    def test_every_symbol_has_a_code_of_zeros_and_ones(self):
        text = "SmartCity Logistics 123"
        codes = build_codes(build_tree(text))
        self.assertEqual(set(codes), set(text))
        for code in codes.values():
            self.assertTrue(code and set(code) <= {"0", "1"})

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

    def test_known_code_lengths(self):
        # a:4 b:2 c:1  ->  a gets 1 bit, b and c get 2 bits
        codes = build_codes(build_tree("aaaabbc"))
        self.assertEqual(len(codes["a"]), 1)
        self.assertEqual(len(codes["b"]), 2)
        self.assertEqual(len(codes["c"]), 2)

    def test_kraft_equality_for_full_tree(self):
        codes = build_codes(build_tree("abracadabra alakazam"))
        self.assertAlmostEqual(sum(2 ** -len(c) for c in codes.values()), 1.0)


class TestOptimality(unittest.TestCase):
    def test_classic_textbook_example_costs_224_bits(self):
        # Frequencies a:5 b:9 c:12 d:13 e:16 f:45 -> optimal cost 224 bits
        text = "a" * 5 + "b" * 9 + "c" * 12 + "d" * 13 + "e" * 16 + "f" * 45
        bits = encode(text, build_codes(build_tree(text)))
        self.assertEqual(len(bits), 224)

    def test_never_worse_than_fixed_length_code(self):
        rng = random.Random(4)
        for _ in range(20):
            text = "".join(rng.choice("abcdefgh") for _ in range(rng.randint(10, 300)))
            k = len(set(text))
            fixed = max(1, math.ceil(math.log2(k))) * len(text)
            _, bits = roundtrip(text)
            self.assertLessEqual(len(bits), fixed)

    def test_uniform_four_symbols_use_two_bits_each(self):
        text = "abcd" * 10
        _, bits = roundtrip(text)
        self.assertEqual(len(bits), 2 * len(text))


class TestEncode(unittest.TestCase):
    def test_empty_text_encodes_to_empty_string(self):
        self.assertEqual(encode("", {}), "")

    def test_encode_uses_the_code_table(self):
        self.assertEqual(encode("abba", {"a": "0", "b": "10"}), "0" + "10" + "10" + "0")

    def test_encoded_length_is_sum_of_code_lengths(self):
        text = "aaaabbc"
        codes = build_codes(build_tree(text))
        self.assertEqual(len(encode(text, codes)), sum(len(codes[c]) for c in text))
        self.assertEqual(len(encode(text, codes)), 10)

    def test_unknown_character_raises_key_error(self):
        codes = build_codes(build_tree("abc"))
        with self.assertRaises(KeyError):
            encode("abcz", codes)


class TestDecode(unittest.TestCase):
    def test_empty_tree_decodes_to_empty_string(self):
        self.assertEqual(decode("", None), "")

    def test_empty_bits_decode_to_empty_string(self):
        self.assertEqual(decode("", build_tree("abc")), "")

    def test_single_symbol_decoding(self):
        self.assertEqual(decode("00000", build_tree("a")), "aaaaa")

    def test_truncated_bits_drop_only_the_incomplete_symbol(self):
        text = "abcabc"
        root = build_tree(text)
        bits = encode(text, build_codes(root))
        self.assertEqual(decode(bits[:-1], root), text[:-1])


class TestRoundTrip(unittest.TestCase):
    def check(self, text):
        decoded, _ = roundtrip(text)
        self.assertEqual(decoded, text)

    def test_simple_strings(self):
        for text in ["", "a", "aaaa", "ab", "abracadabra", "mississippi"]:
            with self.subTest(text=text):
                self.check(text)

    def test_whitespace_newlines_and_punctuation(self):
        self.check("PKG001 | Electronics | Zone-A\n\tDeliver 09:00\n\n")

    def test_unicode_text(self):
        self.check("héllo wörld ñandú 配送 🚚🚚")

    def test_every_printable_ascii_character(self):
        self.check(string.printable * 3)

    def test_skewed_frequencies(self):
        self.check("a" * 1000 + "b" * 10 + "c")

    def test_random_texts(self):
        rng = random.Random(99)
        alphabet = string.ascii_letters + string.digits + " |-:\n"
        for _ in range(100):
            text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 400)))
            self.check(text)

    def test_sample_manifest_file_if_present(self):
        if not os.path.exists(MANIFEST):
            self.skipTest("sample_manifest.txt not found")
        with open(MANIFEST, encoding="utf-8") as f:
            self.check(f.read())


class TestCompressionStats(unittest.TestCase):
    def test_exact_values(self):
        text = "aaaabbc"
        _, bits = roundtrip(text)
        s = compression_stats(text, bits)
        self.assertEqual(s["original_bits"], 56)
        self.assertEqual(s["compressed_bits"], 10)
        self.assertAlmostEqual(s["ratio"], 5.6)
        self.assertAlmostEqual(s["savings_pct"], 100 * (1 - 10 / 56))

    def test_empty_text_does_not_divide_by_zero(self):
        s = compression_stats("", "")
        self.assertEqual(s, {"original_bits": 0, "compressed_bits": 0,
                             "ratio": 0.0, "savings_pct": 0.0})

    def test_single_symbol_text_uses_one_bit_per_character(self):
        text = "aaaa"
        _, bits = roundtrip(text)
        s = compression_stats(text, bits)
        self.assertEqual(s["compressed_bits"], 4)
        self.assertAlmostEqual(s["ratio"], 8.0)

    def test_uniform_four_symbols_ratio_is_four(self):
        text = "abcd" * 10
        _, bits = roundtrip(text)
        self.assertAlmostEqual(compression_stats(text, bits)["ratio"], 4.0)

    def test_repetitive_manifest_text_compresses(self):
        text = "PKG001 | Electronics | Zone-A | Deliver 09:00\n" * 20
        _, bits = roundtrip(text)
        s = compression_stats(text, bits)
        self.assertGreater(s["ratio"], 1.0)
        self.assertGreater(s["savings_pct"], 0)

    def test_compressed_never_exceeds_ascii_size(self):
        rng = random.Random(8)
        for _ in range(20):
            text = "".join(rng.choice(string.ascii_letters) for _ in range(rng.randint(1, 200)))
            _, bits = roundtrip(text)
            self.assertLessEqual(len(bits), 8 * len(text))


if __name__ == "__main__":
    unittest.main()