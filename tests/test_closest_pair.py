import math
import random
import unittest

from divide_conquer.closest_pair import closest_pair, brute_force, benchmark


class TestClosestPairEdgeCases(unittest.TestCase):

    def test_empty_list(self):
        self.assertIsNone(closest_pair([]))

    def test_single_point(self):
        self.assertIsNone(closest_pair([(1, 1)]))

    def test_two_points(self):
        d, pair = closest_pair([(0, 0), (3, 4)])
        self.assertEqual(d, 5.0)
        self.assertEqual(set(pair), {(0, 0), (3, 4)})

    def test_three_points_base_case(self):
        self.assertEqual(closest_pair([(0, 0), (10, 10), (11, 10)])[0], 1.0)

    def test_duplicate_points(self):
        d, pair = closest_pair([(1, 1), (5, 5), (1, 1), (9, 2), (7, 7)])
        self.assertEqual(d, 0.0)
        self.assertEqual(pair, ((1, 1), (1, 1)))

    def test_only_duplicates(self):
        self.assertEqual(closest_pair([(2, 2)] * 6)[0], 0.0)

    def test_all_points_on_vertical_line(self):
        pts = [(5, y * 3) for y in range(20)] + [(5, 31)]
        self.assertEqual(closest_pair(pts)[0], 1.0)

    def test_all_points_on_horizontal_line(self):
        pts = [(x * 4, 7) for x in range(20)] + [(41, 7)]
        self.assertEqual(closest_pair(pts)[0], 1.0)

    def test_negative_coordinates(self):
        self.assertAlmostEqual(closest_pair([(-5, -5), (-4, -5), (10, 10), (20, -20)])[0], 1.0)

    def test_float_coordinates(self):
        self.assertAlmostEqual(closest_pair([(0.0, 0.0), (0.5, 0.0), (9.9, 9.9)])[0], 0.5)


class TestClosestPairCorrectness(unittest.TestCase):

    def test_closest_pair_straddles_the_dividing_line(self):
        # The nearest pair has one point on each side of the median split.
        pts = [(0, 0), (0, 50), (10, 100), (49, 20), (51, 21), (90, 60), (100, 0), (100, 100)]
        d, pair = closest_pair(pts)
        self.assertAlmostEqual(d, math.hypot(2, 1))
        self.assertEqual(set(pair), {(49, 20), (51, 21)})

    def test_returned_distance_matches_returned_pair(self):
        rng = random.Random(4)
        pts = [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(200)]
        d, (a, b) = closest_pair(pts)
        self.assertAlmostEqual(d, math.hypot(a[0] - b[0], a[1] - b[1]))
        self.assertIn(a, pts)
        self.assertIn(b, pts)

    def test_matches_brute_force_on_random_inputs(self):
        rng = random.Random(3)
        for _ in range(200):
            pts = [(rng.randint(0, 50), rng.randint(0, 50)) for _ in range(rng.randint(2, 60))]
            self.assertAlmostEqual(closest_pair(pts)[0], brute_force(pts)[0])

    def test_matches_brute_force_on_float_inputs(self):
        rng = random.Random(5)
        for _ in range(50):
            pts = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(rng.randint(2, 120))]
            self.assertAlmostEqual(closest_pair(pts)[0], brute_force(pts)[0])

    def test_input_is_not_modified(self):
        pts = [(5, 5), (1, 1), (2, 2), (9, 9)]
        copy = list(pts)
        closest_pair(pts)
        self.assertEqual(pts, copy)


class TestBruteForce(unittest.TestCase):

    def test_fewer_than_two_points(self):
        self.assertIsNone(brute_force([]))
        self.assertIsNone(brute_force([(1, 1)]))

    def test_known_answer(self):
        d, _ = brute_force([(0, 0), (6, 8), (1, 1)])
        self.assertAlmostEqual(d, math.sqrt(2))


class TestBenchmark(unittest.TestCase):

    def test_rows_have_expected_shape_and_agree(self):
        rows = benchmark(sizes=(50, 200))
        self.assertEqual([r[0] for r in rows], [50, 200])
        for n, t_brute, t_dc, same in rows:
            self.assertTrue(same)
            self.assertGreaterEqual(t_brute, 0)
            self.assertGreaterEqual(t_dc, 0)


if __name__ == "__main__":
    unittest.main()