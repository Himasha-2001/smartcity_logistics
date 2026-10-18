
import unittest

from divide_conquer.merge_sort import merge_sort


class TestMergeSort(unittest.TestCase):

    def test_normal_list(self):
        self.assertEqual(
            merge_sort([45, 12, 30, 8, 25]),
            [8, 12, 25, 30, 45]
        )

    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_single_item(self):
        self.assertEqual(merge_sort([10]), [10])

    def test_duplicates(self):
        self.assertEqual(
            merge_sort([4, 2, 4, 1, 2]),
            [1, 2, 2, 4, 4]
        )

    def test_input_is_not_modified(self):
        original = [3, 1, 2]
        merge_sort(original)
        self.assertEqual(original, [3, 1, 2])


if __name__ == "__main__":
    unittest.main()
