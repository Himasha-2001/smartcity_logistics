import math
import random
import unittest

from divide_conquer.closest_pair import closest_pair, brute_force


class TestClosestPairEdgeCases(unittest.TestCase):

    def test_empty_list(self):
        self.assertIsNone(closest_pair([]))

    def test_two_points(self):
        d, pair = closest_pair([(0, 0), (3, 4)])
        self.assertEqual(d, 5.0)
        self.assertEqual(set(pair), {(0, 0), (3, 4)})

    def test_duplicate_points(self):
        d, pair = closest_pair([(1, 1), (5, 5), (1, 1), (9, 2), (7, 7)])
        self.assertEqual(d, 0.0)
        self.assertEqual(pair, ((1, 1), (1, 1)))

    def test_all_points_on_vertical_line(self):
        pts = [(5, y * 3) for y in range(20)] + [(5, 31)]
        self.assertEqual(closest_pair(pts)[0], 1.0)

    def test_negative_coordinates(self):
        self.assertAlmostEqual(closest_pair([(-5, -5), (-4, -5), (10, 10), (20, -20)])[0], 1.0)


class TestClosestPairCorrectness(unittest.TestCase):

    def test_closest_pair_straddles_the_dividing_line(self):
        # The nearest pair has one point on each side of the median split.
        pts = [(0, 0), (0, 50), (10, 100), (49, 20), (51, 21), (90, 60), (100, 0), (100, 100)]
        d, pair = closest_pair(pts)
        self.assertAlmostEqual(d, math.hypot(2, 1))
        self.assertEqual(set(pair), {(49, 20), (51, 21)})

    def test_matches_brute_force_on_random_inputs(self):
        rng = random.Random(3)
        for _ in range(200):
            pts = [(rng.randint(0, 50), rng.randint(0, 50)) for _ in range(rng.randint(2, 60))]
            self.assertAlmostEqual(closest_pair(pts)[0], brute_force(pts)[0])


if __name__ == "__main__":
    unittest.main()