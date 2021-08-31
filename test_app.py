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

            # import pdb
            # pdb.set_trace()

            #Use pdb to see res.data
            #have to use b-string to check inside res.data
            self.assertIn(b'id="score-para">Your Score:', res.data)
            self.assertIn(b'id="guess-form">\n<bu', res.data)
            self.assertIn(b'<button id="guess-button">Guess', res.data)

            #These shouldn't be in session yet on a new server
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('times_played'))

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


    def test_session(self):
        with app.test_client() as client:

            with client.session_transaction() as change_session:
                change_session['times_played'] = 57
                change_session['highscore'] = 6
 
            res = client.post('/check-score', json={'score':4})
            self.assertEqual(res.status_code, 200)

            self.assertEqual(session['times_played'], 58)
            self.assertEqual(session['highscore'], 6)
