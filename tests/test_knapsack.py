import random
import unittest

from dynamic_programming.knapsack_01 import knapsack_2d, knapsack_1d, knapsack_bruteforce

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

    def test_zero_capacity(self):
        self.assertEqual(knapsack_1d([(5, 10)], 0), 0)
        self.assertEqual(knapsack_2d([(5, 10)], 0)[0], 0)

    def test_negative_capacity_raises(self):
        for solver in (knapsack_1d, lambda i, c: knapsack_2d(i, c)):
            with self.assertRaises(ValueError):
                solver([(1, 1)], -1)


if __name__ == "__main__":
    unittest.main()