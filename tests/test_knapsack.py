import random
import unittest

from dynamic_programming.knapsack_01 import (knapsack_2d, knapsack_1d, knapsack_bruteforce,
                                             table_to_text, benchmark, memory_comparison)

ITEMS = [(1, 1), (3, 4), (4, 5), (5, 7)]
CAP = 7


class TestKnapsackCorrectness(unittest.TestCase):

    def test_known_answer_all_three_versions(self):
        self.assertEqual(knapsack_2d(ITEMS, CAP)[0], 9)
        self.assertEqual(knapsack_1d(ITEMS, CAP), 9)
        self.assertEqual(knapsack_bruteforce(ITEMS, CAP), 9)

    def test_hand_traced_table(self):
        _, _, table = knapsack_2d(ITEMS, CAP)
        self.assertEqual(table, [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 4, 5, 5, 5, 5],
            [0, 1, 1, 4, 5, 6, 6, 9],
            [0, 1, 1, 4, 5, 7, 8, 9],
        ])

    def test_table_shape(self):
        _, _, table = knapsack_2d(ITEMS, CAP)
        self.assertEqual(len(table), len(ITEMS) + 1)
        self.assertTrue(all(len(row) == CAP + 1 for row in table))

    def test_first_row_and_column_are_zero(self):
        _, _, table = knapsack_2d(ITEMS, CAP)
        self.assertEqual(table[0], [0] * (CAP + 1))
        self.assertTrue(all(row[0] == 0 for row in table))

    def test_table_never_decreases_with_more_items_or_capacity(self):
        _, _, t = knapsack_2d([(3, 5), (2, 4), (6, 9), (4, 7)], 12)
        for i in range(1, len(t)):
            for c in range(len(t[0])):
                self.assertGreaterEqual(t[i][c], t[i - 1][c])
                if c:
                    self.assertGreaterEqual(t[i][c], t[i][c - 1])

    def test_chosen_items_fit_and_add_up_to_best_value(self):
        best, chosen, _ = knapsack_2d(ITEMS, CAP)
        self.assertEqual(chosen, [1, 2])
        self.assertLessEqual(sum(ITEMS[i][0] for i in chosen), CAP)
        self.assertEqual(sum(ITEMS[i][1] for i in chosen), best)

    def test_each_item_used_at_most_once(self):
        # One item of weight 1, value 10, capacity 5: must give 10, not 50.
        self.assertEqual(knapsack_1d([(1, 10)], 5), 10)
        self.assertEqual(knapsack_2d([(1, 10)], 5)[0], 10)

    def test_greedy_counterexample(self):
        items = [(10, 60), (20, 100), (30, 120)]
        self.assertEqual(knapsack_1d(items, 50), 220)      # greedy by ratio gives 160

    def test_all_versions_agree_on_random_inputs(self):
        rng = random.Random(5)
        for _ in range(100):
            items = [(rng.randint(0, 12), rng.randint(0, 60)) for _ in range(rng.randint(0, 11))]
            cap = rng.randint(0, 40)
            a = knapsack_2d(items, cap)
            self.assertEqual(a[0], knapsack_1d(items, cap))
            self.assertEqual(a[0], knapsack_bruteforce(items, cap))
            self.assertLessEqual(sum(items[i][0] for i in a[1]), cap)
            self.assertEqual(sum(items[i][1] for i in a[1]), a[0])


class TestKnapsackEdgeCases(unittest.TestCase):

    def test_no_items(self):
        self.assertEqual(knapsack_1d([], 10), 0)
        self.assertEqual(knapsack_2d([], 10)[0], 0)

    def test_zero_capacity(self):
        self.assertEqual(knapsack_1d([(5, 10)], 0), 0)
        self.assertEqual(knapsack_2d([(5, 10)], 0)[0], 0)

    def test_item_too_heavy(self):
        self.assertEqual(knapsack_1d([(9, 100)], 8), 0)

    def test_exact_fit(self):
        self.assertEqual(knapsack_1d([(4, 7), (6, 9)], 10), 16)

    def test_all_items_fit(self):
        self.assertEqual(knapsack_1d([(1, 5), (2, 6), (3, 7)], 100), 18)

    def test_zero_weight_item_is_free(self):
        self.assertEqual(knapsack_1d([(0, 7), (3, 4)], 2), 7)
        self.assertEqual(knapsack_2d([(0, 7), (3, 4)], 2)[0], 7)

    def test_negative_capacity_raises(self):
        for solver in (knapsack_1d, lambda i, c: knapsack_2d(i, c)):
            with self.assertRaises(ValueError):
                solver([(1, 1)], -1)

    def test_non_integer_inputs_raise_value_error(self):
        with self.assertRaises(ValueError):
            knapsack_1d([(2.5, 10)], 5)
        with self.assertRaises(ValueError):
            knapsack_2d([(1, 1)], 5.5)

    def test_negative_weight_raises(self):
        with self.assertRaises(ValueError):
            knapsack_1d([(-3, 10)], 5)

    def test_input_is_not_modified(self):
        items = [(3, 4), (2, 3)]
        copy = list(items)
        knapsack_2d(items, 5)
        knapsack_1d(items, 5)
        self.assertEqual(items, copy)


class TestSpaceOptimisation(unittest.TestCase):

    def test_1d_uses_far_less_memory_than_2d(self):
        peak_2d, peak_1d = memory_comparison(n=60, capacity=600)
        self.assertLess(peak_1d * 5, peak_2d)

    def test_memory_gap_grows_with_n(self):
        small = memory_comparison(n=20, capacity=300)
        large = memory_comparison(n=80, capacity=300)
        self.assertGreater(large[0] / large[1], small[0] / small[1])


class TestHelpers(unittest.TestCase):

    def test_table_text_has_one_line_per_row_plus_header(self):
        text = table_to_text(ITEMS, CAP)
        self.assertEqual(len(text.splitlines()), len(ITEMS) + 2)

    def test_benchmark_rows_agree(self):
        rows = benchmark(sizes=(5, 8), capacity=30)
        self.assertEqual([r[0] for r in rows], [5, 8])
        self.assertTrue(all(r[4] for r in rows))


if __name__ == "__main__":
    unittest.main()