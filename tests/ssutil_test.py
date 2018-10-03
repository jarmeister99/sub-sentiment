import unittest

from ssutil import *
from prawcore import OAuthException


class TestStringMethods(unittest.TestCase):
    def test_clean(self):
        s1 = "Hi, Guys!"
        e1 = "hi guys"
        self.assertEqual(e1, clean(s1))

        s2 = "hi guys"
        e2 = "hi guys"
        self.assertEqual(e2, clean(s2))

        s3 = "What do you mean, Candy?!"
        e3 = "what do you mean candy"
        self.assertEqual(e3, clean(s3))

        s4 = "money9"
        e4 = "money9"
        self.assertEqual(e4, clean(s4))

    def test_soft_clean(self):
        s1 = "Hello I'm bob"
        e1 = "Hello I`m bob"
        self.assertEqual(e1, soft_clean(s1))


class TestRedditMethods(unittest.TestCase):
    def test_connection(self):
        settings1 = {'client_id': 'mWvMZYAgcZz2_Q', 'client_secret': 'QQckU5bMih7t3Mz3FYpkwBWvlDs',
                     'client_password': '1longtime###ERRORINPASSOWRD###',
                     'user_agent': 'a script that determines general sentiment on a specified subreddit',
                     'client_username': 'jarmeister',
                     'comment_progress_updates': 'True',
                     'comment_progress_interval': '10',
                     'db_path': 'db/{sub}'}
        settings2 = {'client_id': 'mWvMZYAgcZz2_Q', 'client_secret': 'QQckU5bMih7t3Mz3FYpkwBWvlDs',
                     'client_password': '1longtime',
                     'user_agent': 'a script that determines general sentiment on a specified subreddit',
                     'client_username': 'jarmeister',
                     'comment_progress_updates': 'True',
                     'comment_progress_interval': '10',
                     'db_path': 'db/{sub}'}
        try:
            with self.assertRaises(OAuthException):
                get_reddit(settings1)
            self.assertIsInstance(get_reddit(settings2), praw.Reddit)
        except SystemExit:
            pass


if __name__ == '__main__':
    unittest.main(exit = False)
