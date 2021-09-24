import unittest
import assignment1
import requests

from unittest import mock
from unittest.mock import patch

class Test_assignment(unittest.TestCase):
    def test_top_movie(self):
        self.assertRaises(TypeError,assignment1.movies_id_func("https://www.imdb"))

    def test_api_fetch(self):
        self.assertRaises(TypeError, assignment1.fetch_api_data(123))
    
    def test_synopsis_func(self):
        self.assertRaises(TypeError, assignment1.movies_synopsis_func(123))

    def test_bag_of_words(self):
        self.assertEqual(assignment1.bag_of_words('ram is shyam'),'ram shyam')

    def test_fetch_data(self):
        with mock.patch('builtins.input', return_value="Drama"):
            assert assignment1.fetch_movies_data() == ['The Shawshank Redemption', 'The Godfather', 'The Godfather: Part II', 'The Dark Knight', '12 Angry Men']


if __name__ == "__main__":
    unittest.main()