import random
import unittest
from divide_conquer.closest_pair import closest_pair, brute_force


class TestClosestPair(unittest.TestCase):
    def test_edge_cases(self):
        self.assertIsNone(closest_pair([]))
        self.assertIsNone(closest_pair([(1, 1)]))
        self.assertEqual(closest_pair([(0, 0), (3, 4)])[0], 5.0)

    def test_duplicates(self):
        d, _ = closest_pair([(1, 1), (5, 5), (1, 1), (9, 2), (7, 7)])
        self.assertEqual(d, 0.0)

    def test_matches_brute_force(self):
        rng = random.Random(3)
        for _ in range(50):
            pts = [(rng.randint(0, 50), rng.randint(0, 50)) for _ in range(rng.randint(2, 60))]
            self.assertAlmostEqual(closest_pair(pts)[0], brute_force(pts)[0])

    def test_vertical_line(self):
        pts = [(5, y * 3) for y in range(20)] + [(5, 31)]
        self.assertEqual(closest_pair(pts)[0], 1.0)


if __name__ == "__main__":
    unittest.main()
