from flask import session
from app import app
from unittest import TestCase


# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleTestCase(TestCase):

    def test_homepage(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Click to play Boggle!</h1>', html)

    def test_boggle(self):
        with app.test_client() as client:
            res = client.get('/boggle')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Boggle!</h1>', html)
            self.assertIn('board', session)

    def test_check_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [["D", "A", "G", "A", "P"], 
                                 ["D", "I", "G", "T", "S"], 
                                 ["D", "D", "G", "B", "R"], 
                                 ["D", "G", "G", "G", "Q"], 
                                 ["D", "O", "G", "J", "Z"]]

        res = client.get('/check-guess?word=dog')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['result'], 'ok')

        res = client.get('/check-guess?word=doa')
        self.assertEqual(res.json['result'], 'not-word')

        res = client.get('/check-guess?word=cat')
        self.assertEqual(res.json['result'], 'not-on-board')



    def test_check_score(self):
        with app.test_client() as client:
            res = client.post('/check-score', json={'score':10})
            self.assertEqual(res.status_code, 200)

            self.assertEqual(session['times_played'], 1)
            self.assertEqual(session['highscore'], 10)

