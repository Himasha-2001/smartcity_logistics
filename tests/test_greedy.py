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

    def test_single_window(self):
        self.assertEqual(activity_selection([(1, 2)]), [(1, 2)])

    def test_classic_textbook_example(self):
        w = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
        self.assertEqual(activity_selection(w), [(1, 4), (5, 7), (8, 11), (12, 16)])

    def test_touching_windows_are_compatible(self):
        self.assertEqual(len(activity_selection([(1, 2), (2, 3), (3, 4)])), 3)

    def test_all_overlapping_picks_exactly_one(self):
        self.assertEqual(len(activity_selection([(1, 10), (2, 9), (3, 8), (4, 7)])), 1)

    def test_identical_windows_pick_one(self):
        self.assertEqual(activity_selection([(2, 5)] * 4), [(2, 5)])

    def test_zero_length_window(self):
        self.assertEqual(len(activity_selection([(3, 3), (1, 2), (4, 5)])), 3)

    def test_earliest_finish_beats_earliest_start(self):
        # Taking the job that starts first, (0, 10), would block the other two.
        self.assertEqual(activity_selection([(0, 10), (1, 2), (3, 4)]), [(1, 2), (3, 4)])

    def test_input_order_does_not_matter(self):
        w = [(8, 11), (1, 4), (5, 7), (3, 5), (12, 16)]
        self.assertEqual(activity_selection(w), activity_selection(list(reversed(w))))

    def test_input_is_not_modified(self):
        w = [(5, 7), (1, 4), (3, 5)]
        copy = list(w)
        activity_selection(w)
        self.assertEqual(w, copy)

    def test_result_is_valid_and_in_time_order(self):
        rng = random.Random(1)
        w = [(s := rng.randint(0, 50), s + rng.randint(1, 6)) for _ in range(60)]
        chosen = activity_selection(w)
        self.assertEqual(chosen, sorted(chosen, key=lambda x: x[1]))
        self.assertTrue(non_overlapping(chosen))
        self.assertTrue(all(job in w for job in chosen))

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

    def test_empty_items(self):
        self.assertEqual(fractional_knapsack([], 10), (0.0, []))

    def test_zero_capacity(self):
        self.assertEqual(fractional_knapsack([("a", 5, 10)], 0)[0], 0)

    def test_negative_capacity_raises(self):
        with self.assertRaises(ValueError):
            fractional_knapsack(self.ITEMS, -1)

    def test_capacity_larger_than_total_weight_takes_everything(self):
        total, taken = fractional_knapsack(self.ITEMS, 1000)
        self.assertAlmostEqual(total, 280)
        self.assertTrue(all(frac == 1.0 for _, frac in taken))

    def test_exact_fit(self):
        total, taken = fractional_knapsack([("a", 10, 60), ("b", 20, 100)], 30)
        self.assertAlmostEqual(total, 160)
        self.assertTrue(all(frac == 1.0 for _, frac in taken))

    def test_highest_ratio_taken_first(self):
        total, taken = fractional_knapsack([("low", 10, 10), ("high", 10, 90)], 10)
        self.assertEqual(taken, [("high", 1.0)])
        self.assertAlmostEqual(total, 90)

    def test_single_item_is_split(self):
        total, taken = fractional_knapsack([("a", 10, 100)], 4)
        self.assertAlmostEqual(total, 40)
        self.assertAlmostEqual(taken[0][1], 0.4)

    def test_item_heavier_than_capacity_is_partially_taken(self):
        total, _ = fractional_knapsack([("sofa", 100, 500)], 20)
        self.assertAlmostEqual(total, 100)

    def test_zero_weight_item_is_free(self):
        total, taken = fractional_knapsack([("free", 0, 50), ("a", 5, 10)], 3)
        self.assertAlmostEqual(total, 56)
        self.assertEqual(taken[0], ("free", 1.0))

    def test_zero_weight_item_is_free_even_at_zero_capacity(self):
        self.assertAlmostEqual(fractional_knapsack([("free", 0, 50), ("a", 5, 10)], 0)[0], 50)

    def test_weight_loaded_never_exceeds_capacity(self):
        rng = random.Random(2)
        for _ in range(100):
            items = [(f"i{k}", rng.randint(1, 20), rng.randint(1, 100)) for k in range(rng.randint(0, 10))]
            cap = rng.randint(0, 60)
            _, taken = fractional_knapsack(items, cap)
            weight = {n: w for n, w, _ in items}
            self.assertLessEqual(sum(weight[n] * f for n, f in taken), cap + 1e-9)

    def test_greedy_beats_every_other_filling_order(self):
        rng = random.Random(3)
        for _ in range(30):
            items = [(f"i{k}", rng.randint(1, 15), rng.randint(1, 80)) for k in range(5)]
            cap = rng.randint(1, 50)
            best = fractional_knapsack(items, cap)[0]
            for order in itertools.permutations(items):
                room, value = cap, 0.0
                for _, w, v in order:
                    take = min(1.0, room / w)
                    value += v * take
                    room -= w * take
                self.assertLessEqual(value, best + 1e-9)


class TestWhyGreedyFailsFor01(unittest.TestCase):

    def test_ratio_greedy_is_not_optimal_for_indivisible_items(self):
        # Greedy (a, b) = 160, but the best whole-item choice (b, c) = 220.
        from dynamic_programming.knapsack_01 import knapsack_1d
        self.assertEqual(knapsack_1d([(10, 60), (20, 100), (30, 120)], 50), 220)
        self.assertLess(160, 220)


if __name__ == "__main__":
    unittest.main()