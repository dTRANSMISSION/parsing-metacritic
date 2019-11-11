#!/usr/bin/env python3

import unittest
import json
from metacritic_parse import MetacriticData, app


class TestData(unittest.TestCase):
    def setUp(self):
        self.metacritic_data = MetacriticData().generate_data()

    def test_data_present(self):
        """Assert that we have data returned"""
        self.data = json.JSONDecoder().decode(self.metacritic_data)
        self.assertGreater(len(self.data), 0)

    def test_object_keys(self):
        """Assert that the data has the correct keys"""
        j = json.loads(self.metacritic_data)
        keys = []
        for dict in j:
            keys.append(dict.keys())
        self.assertTrue(keys, ['title', 'score'])

    def test_title_type(self):
        """Assert that the values in the 'title' key are strings"""
        j = json.loads(self.metacritic_data)
        all_titles = []
        for dict in j:
            all_titles.append(dict['title'])
        result = checktype_str(all_titles)
        self.assertTrue(result, True)

    def test_score_type(self):
        """Assert that the values in the 'score' key are integers"""
        j = json.loads(self.metacritic_data)
        all_scores = []
        for dict in j:
            all_scores.append(dict['score'])
        result = checktype_int(all_scores)
        self.assertTrue(result, True)


class TestApp(unittest.TestCase):
    def setUp(self):
        app.debug = True
        self.test_app = app.test_client()

    def test_root_endpoint(self):
        """Assert that the / endpoint correctly loads"""
        response = self.test_app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_games_endpoint(self):
        """Assert that the /games endpoint returns data"""
        response = self.test_app.get('/games')
        self.assertEqual(response.status_code, 308)


def checktype_str(obj):
    return all(isinstance(elem, str) for elem in obj)


def checktype_int(obj):
    return all(isinstance(elem, int) for elem in obj)


if __name__ == '__main__':
    unittest.main()
