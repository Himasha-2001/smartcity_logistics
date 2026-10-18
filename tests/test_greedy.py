import unittest
from greedy.activity_selection import activity_selection
from greedy.fractional_knapsack import fractional_knapsack


class TestActivitySelection(unittest.TestCase):
    def test_edges(self):
        self.assertEqual(activity_selection([]), [])
        self.assertEqual(activity_selection([(1, 2)]), [(1, 2)])

    def test_classic(self):
        w = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
        self.assertEqual(len(activity_selection(w)), 4)

    def test_touching_allowed(self):
        self.assertEqual(len(activity_selection([(1, 2), (2, 3), (3, 4)])), 3)


class TestFractionalKnapsack(unittest.TestCase):
    def test_classic(self):
        total, _ = fractional_knapsack([("a", 10, 60), ("b", 20, 100), ("c", 30, 120)], 50)
        self.assertAlmostEqual(total, 240)

    def test_edges(self):
        self.assertEqual(fractional_knapsack([], 10)[0], 0)
        self.assertEqual(fractional_knapsack([("a", 5, 10)], 0)[0], 0)

    def test_greedy_fails_for_01(self):
        # same items, indivisible: greedy-by-ratio takes a+b = 160, optimum is b+c = 220
        from dynamic_programming.knapsack_01 import knapsack_1d
        self.assertEqual(knapsack_1d([(10, 60), (20, 100), (30, 120)], 50), 220)


if __name__ == "__main__":
    unittest.main()
