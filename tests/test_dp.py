import random
import unittest
from dynamic_programming.knapsack_01 import knapsack_2d, knapsack_1d, knapsack_bruteforce
from dynamic_programming.shortest_path_dp import shortest_path, bellman_ford


class TestKnapsack(unittest.TestCase):
    def test_known(self):
        items = [(1, 1), (3, 4), (4, 5), (5, 7)]
        best, chosen, _ = knapsack_2d(items, 7)
        self.assertEqual(best, 9)
        self.assertEqual(sum(items[i][0] for i in chosen), 7)

    def test_edges(self):
        self.assertEqual(knapsack_1d([], 10), 0)
        self.assertEqual(knapsack_1d([(5, 10)], 4), 0)
        self.assertEqual(knapsack_2d([(5, 10)], 0)[0], 0)
        with self.assertRaises(ValueError):
            knapsack_1d([(1, 1)], -1)

    def test_all_versions_agree(self):
        rng = random.Random(5)
        for _ in range(30):
            items = [(rng.randint(1, 10), rng.randint(1, 50)) for _ in range(rng.randint(0, 10))]
            cap = rng.randint(0, 30)
            a = knapsack_2d(items, cap)[0]
            self.assertEqual(a, knapsack_1d(items, cap))
            self.assertEqual(a, knapsack_bruteforce(items, cap))


class TestShortestPath(unittest.TestCase):
    EDGES = [("S", "A", 4), ("S", "B", 2), ("B", "A", 1), ("A", "T", 5), ("B", "T", 8)]

    def test_path(self):
        self.assertEqual(shortest_path(self.EDGES, "S", "T", directed=True), (8, ["S", "B", "A", "T"]))

    def test_unreachable_and_same_node(self):
        self.assertEqual(shortest_path(self.EDGES, "T", "S", directed=True)[0], float("inf"))
        self.assertEqual(shortest_path(self.EDGES, "S", "S"), (0, ["S"]))

    def test_negative_edge_ok_negative_cycle_raises(self):
        self.assertEqual(shortest_path([("S", "A", 5), ("A", "B", -3)], "S", "B", directed=True)[0], 2)
        with self.assertRaises(ValueError):
            bellman_ford([("S", "A", 1), ("A", "B", -3), ("B", "A", 1)], "S")


if __name__ == "__main__":
    unittest.main()
