import unittest
from training import load_data

class TestModel(unittest.TestCase):
    def test_load_data(self):
        df = load_data()
        self.assertIsNotNone(df)
        self.assertEqual(len(df.columns), 14)  # 13 features + 1 target

if __name__ == '__main__':
    unittest.main()