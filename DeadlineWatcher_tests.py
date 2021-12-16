import unittest
import DeadlineWatcher

class watcherTest(unittest.TestCase):
    def test_words_counter_one_str(self):
        self.assertEqual(DeadlineWatcher.count_words("Going to the street"), 4)
    def test_words_counter_many_str(self):
        self.assertEqual(DeadlineWatcher.count_words("Я иду на\n улицу 5-ый\n раз на дню"), 8)

if __name__ == "__main__":
    unittest.main()
