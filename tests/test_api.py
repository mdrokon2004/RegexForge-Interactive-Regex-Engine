"""
RegexForge API Integration Tests
Tests /api/analyze and /api/match endpoints with Flask test client.
"""

import sys
import os
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


class TestRegexForgeAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_api_examples(self):
        res = self.client.get('/api/examples')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 1)

    def test_api_analyze_valid(self):
        res = self.client.post('/api/analyze', json={'regex': '(a|b)*abb'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('tokens', data)
        self.assertIn('ast', data)
        self.assertIn('nfa', data)
        self.assertIn('dfa', data)
        self.assertIn('stats', data)
        self.assertEqual(data['stats']['dfa_states'], len(data['dfa']['states']))

    def test_api_analyze_invalid_lexical(self):
        res = self.client.post('/api/analyze', json={'regex': 'a#b'})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error']['error_type'], 'Lexical Error')

    def test_api_analyze_invalid_syntax(self):
        res = self.client.post('/api/analyze', json={'regex': '(a|b'})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error']['error_type'], 'Parse Error')

    def test_api_match_endpoint(self):
        res = self.client.post('/api/match', json={
            'regex': '(a|b)*abb',
            'test_strings': ['aaabb', 'abb', 'ababa']
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['results']), 3)

        results_map = {r['string']: r['is_match'] for r in data['results']}
        self.assertTrue(results_map['aaabb'])
        self.assertTrue(results_map['abb'])
        self.assertFalse(results_map['ababa'])


if __name__ == '__main__':
    unittest.main()
