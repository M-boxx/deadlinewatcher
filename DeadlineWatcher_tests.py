import unittest
from unittest import mock
import DeadlineWatcher

class watcherTest(unittest.TestCase):
    def test_words_counter_one_str(self):
        self.assertEqual(DeadlineWatcher.count_words("Going to the street"), 4)
    def test_words_counter_many_str(self):
        self.assertEqual(DeadlineWatcher.count_words("Я иду на\n улицу 5-ый\n раз на дню"), 8)
    def test_start(self):
        update = unittest.mock.Mock()
        context = unittest.mock.Mock()
        update.message.text = 'Установить дедлайн'
        update.effective_chat.id = 1
        DeadlineWatcher.text(update)
        context.bot.send_message.assert_called_with(
            chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == "__main__":
    unittest.main()
