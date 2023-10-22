from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

class FlaskTests(TestCase):

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertIn('board_state', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('num_plays'))
            self.assertIn("IT'S BOGGLE TIME!", html)
            self.assertIn("Start Game!", html)

    def test_gamepage(self):
        """Make sure elements of the game page are displayed"""
        with app.test_client() as client:
            client.get('/')
            response = client.get('/game')
            html = response.get_data(as_text=True)

            self.assertIn("New Game", html)
            self.assertIn("Score:", html)
            self.assertIn("Time:", html)
            self.assertIn("<tr>", html)
            self.assertIn("<td>", html)
            self.assertIn('<form id="player-input-form">', html)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board_state'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = client.get('/validate-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""
        with app.test_client() as client:
            client.get('/')
            response = client.get('/validate-word?word=impossible')
            self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""
        with app.test_client() as client:
            client.get('/')
            response = client.get(
                '/validate-word?word=fsjdakfkldsfjdslkfjdlksf')
            self.assertEqual(response.json['result'], 'not-word')