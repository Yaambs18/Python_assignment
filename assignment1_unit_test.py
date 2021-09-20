import unittest
import assignment1
import requests

from unittest import mock
from unittest.mock import patch

class Test_assignment(unittest.TestCase):

    def test_api_fetch(self):
        self.assertRaises(TypeError, assignment1.fetch_api_data(123))
    
    def test_synopsis_func(self):
        self.assertRaises(TypeError, assignment1.movies_synopsis_func(123))

    def test_fetch_data(self):
        with mock.patch('builtins.input', return_value="Drama"):
            assert assignment1.fetch_movies_data() == [{'movie_id': 'tt0111161', 'Synopsis': "Chronicles experiences formerly successful banker prisoner gloomy jailhouse Shawshank found guilty crime commit film portrays man 's unique way dealing new torturous life along way befriends number fellow prisoners notably wise longterm inmate named Red —JSGolden", 'Genre': 'Drama', 'Actors': 'Tim Robbins, Morgan Freeman, Bob Gunton'}]


if __name__ == "__main__":
    unittest.main()