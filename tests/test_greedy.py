import itertools
import random
import unittest

from greedy.activity_selection import activity_selection
from greedy.fractional_knapsack import fractional_knapsack


def non_overlapping(windows):
    ordered = sorted(windows, key=lambda w: (w[1], w[0]))
    return all(a[1] <= b[0] for a, b in zip(ordered, ordered[1:]))


def optimal_count(windows):
    """Brute force: size of the largest non-overlapping subset."""
    return max((len(c) for k in range(len(windows) + 1)
                for c in itertools.combinations(windows, k) if non_overlapping(c)), default=0)


class TestActivitySelection(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(activity_selection([]), [])

    def test_classic_textbook_example(self):
        w = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
        self.assertEqual(activity_selection(w), [(1, 4), (5, 7), (8, 11), (12, 16)])

    def test_touching_windows_are_compatible(self):
        self.assertEqual(len(activity_selection([(1, 2), (2, 3), (3, 4)])), 3)

    def test_identical_windows_pick_one(self):
        self.assertEqual(activity_selection([(2, 5)] * 4), [(2, 5)])

    def test_earliest_finish_beats_earliest_start(self):
        # Taking the job that starts first, (0, 10), would block the other two.
        self.assertEqual(activity_selection([(0, 10), (1, 2), (3, 4)]), [(1, 2), (3, 4)])

    def test_greedy_is_optimal_against_brute_force(self):
        rng = random.Random(7)
        for _ in range(300):
            n = rng.randint(0, 9)
            w = [(s := rng.randint(0, 12), s + rng.randint(0, 5)) for _ in range(n)]
            self.assertEqual(len(activity_selection(w)), optimal_count(w))


class TestFractionalKnapsack(unittest.TestCase):
    ITEMS = [("a", 10, 60), ("b", 20, 100), ("c", 30, 120)]

    def test_classic_example(self):
        total, taken = fractional_knapsack(self.ITEMS, 50)
        self.assertAlmostEqual(total, 240)
        self.assertEqual([name for name, _ in taken], ["a", "b", "c"])
        self.assertAlmostEqual(taken[-1][1], 2 / 3)

    def test_zero_capacity(self):
        self.assertEqual(fractional_knapsack([("a", 5, 10)], 0)[0], 0)

    def test_negative_capacity_raises(self):
        with self.assertRaises(ValueError):
            fractional_knapsack(self.ITEMS, -1)

    def test_capacity_larger_than_total_weight_takes_everything(self):
        total, taken = fractional_knapsack(self.ITEMS, 1000)
        self.assertAlmostEqual(total, 280)
        self.assertTrue(all(frac == 1.0 for _, frac in taken))

    def test_single_item_is_split(self):
        total, taken = fractional_knapsack([("a", 10, 100)], 4)
        self.assertAlmostEqual(total, 40)
        self.assertAlmostEqual(taken[0][1], 0.4)

    def test_weight_loaded_never_exceeds_capacity(self):
        rng = random.Random(2)
        for _ in range(100):
            items = [(f"i{k}", rng.randint(1, 20), rng.randint(1, 100)) for k in range(rng.randint(0, 10))]
            cap = rng.randint(0, 60)
            _, taken = fractional_knapsack(items, cap)
            weight = {n: w for n, w, _ in items}
            self.assertLessEqual(sum(weight[n] * f for n, f in taken), cap + 1e-9)


if __name__ == "__main__":
    unittest.main()