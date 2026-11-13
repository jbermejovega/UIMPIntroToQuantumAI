import unittest
from quazris_mpi_distribution import distribute, check_horn_candidate

class TestQuazrisDistribution(unittest.TestCase):
    def test_exact_cover(self):
        for size in (1, 2, 3, 4, 9, 12):
            d = distribute(size)
            names = [name for rank in d for name in d[rank]]
            self.assertEqual(len(names), 9)
            self.assertEqual(len(set(names)), 9)
            self.assertEqual(set(names), {f"{i:02}.ipynb" for i in range(1, 10)})

    def test_deterministic(self):
        self.assertEqual(distribute(3), distribute(3))

    def test_invalid_size(self):
        with self.assertRaises(ValueError):
            distribute(0)

    def test_horn_not_proof(self):
        self.assertFalse(check_horn_candidate()["kan_filler_certified"])

if __name__ == "__main__":
    unittest.main()
