import math
import random
import unittest

from divide_conquer.merge_sort import merge_sort, merge_sort_counted, empirical_check


class TestMergeSort(unittest.TestCase):

    def test_normal_list(self):
        self.assertEqual(merge_sort([45, 12, 30, 8, 25]), [8, 12, 25, 30, 45])

    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_single_item(self):
        self.assertEqual(merge_sort([10]), [10])

    def test_two_items(self):
        self.assertEqual(merge_sort([2, 1]), [1, 2])

    def test_duplicates(self):
        self.assertEqual(merge_sort([4, 2, 4, 1, 2]), [1, 2, 2, 4, 4])

    def test_all_equal(self):
        self.assertEqual(merge_sort([7, 7, 7, 7]), [7, 7, 7, 7])

    def test_already_sorted_and_reverse_sorted(self):
        data = list(range(50))
        self.assertEqual(merge_sort(data), data)
        self.assertEqual(merge_sort(data[::-1]), data)

    def test_negative_numbers(self):
        self.assertEqual(merge_sort([3, -1, 0, -5, 2]), [-5, -1, 0, 2, 3])

    def test_input_is_not_modified(self):
        original = [3, 1, 2]
        merge_sort(original)
        self.assertEqual(original, [3, 1, 2])

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

    def test_returns_sorted_list_and_count(self):
        result, comps = merge_sort_counted([3, 1, 2])
        self.assertEqual(result, [1, 2, 3])
        self.assertIsInstance(comps, int)

    def test_empty_and_single_need_zero_comparisons(self):
        self.assertEqual(merge_sort_counted([])[1], 0)
        self.assertEqual(merge_sort_counted([5])[1], 0)

    def test_two_items_need_exactly_one_comparison(self):
        self.assertEqual(merge_sort_counted([2, 1])[1], 1)

    def test_comparisons_never_exceed_n_log2_n(self):
        rng = random.Random(2)
        for n in (16, 100, 1000, 4096):
            data = rng.sample(range(10 ** 6), n)
            self.assertLessEqual(merge_sort_counted(data)[1], n * math.log2(n))

    def test_comparisons_grow_like_n_log_n(self):
        # Doubling n should slightly more than double the comparisons.
        rng = random.Random(3)
        small = merge_sort_counted(rng.sample(range(10 ** 6), 1000))[1]
        large = merge_sort_counted(rng.sample(range(10 ** 6), 2000))[1]
        self.assertGreater(large / small, 2.0)
        self.assertLess(large / small, 2.4)      # a quadratic sort would give ~4

    def test_empirical_check_ratio_is_bounded(self):
        rows = empirical_check(sizes=(100, 1000, 10000))
        for n, comps, bound, ratio in rows:
            self.assertGreater(ratio, 0.5)
            self.assertLessEqual(ratio, 1.0)


if __name__ == "__main__":
    unittest.main()