import math
import random
import unittest

from divide_conquer.merge_sort import merge_sort, merge_sort_counted


class TestMergeSort(unittest.TestCase):

    def test_normal_list(self):
        self.assertEqual(merge_sort([45, 12, 30, 8, 25]), [8, 12, 25, 30, 45])

    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_duplicates(self):
        self.assertEqual(merge_sort([4, 2, 4, 1, 2]), [1, 2, 2, 4, 4])

    def test_already_sorted_and_reverse_sorted(self):
        data = list(range(50))
        self.assertEqual(merge_sort(data), data)
        self.assertEqual(merge_sort(data[::-1]), data)

    def test_matches_builtin_sorted_on_random_lists(self):
        rng = random.Random(1)
        for _ in range(200):
            data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 80))]
            self.assertEqual(merge_sort(data), sorted(data))

    # --- the actual use case: packages sorted by delivery deadline ---
    def test_sort_packages_by_deadline_with_key(self):
        packages = [{"id": "A", "deadline": 9}, {"id": "B", "deadline": 3},
                    {"id": "C", "deadline": 6}]
        result = merge_sort(packages, key=lambda p: p["deadline"])
        self.assertEqual([p["id"] for p in result], ["B", "C", "A"])

    def test_sort_is_stable_for_equal_deadlines(self):
        packages = [("a", 3), ("b", 1), ("c", 3), ("d", 1)]
        result = merge_sort(packages, key=lambda p: p[1])
        self.assertEqual([p[0] for p in result], ["b", "d", "a", "c"])


class TestComparisonCounting(unittest.TestCase):

    def test_comparisons_never_exceed_n_log2_n(self):
        rng = random.Random(2)
        for n in (16, 100, 1000, 4096):
            data = rng.sample(range(10 ** 6), n)
            self.assertLessEqual(merge_sort_counted(data)[1], n * math.log2(n))


if __name__ == "__main__":
    unittest.main()