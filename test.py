from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        # to complete before each test
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_homepage(self):
        # enusre session information in HTML displays
        # use self.client
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('high_score'))
            self.assertIsNone(session.get('numplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):  
        # test if word is valid by modifyinh the session board
        with self.client as client:
            with client.session_transaction() as sess:
                sess["board"] =  [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
                
        response = self.client.get("/check-word?word=cat")
        self.assertEqual(response.json["result"], "ok")

    def test_invalid_word(self):
        # test if word is in dict
        self.client.get("/")
        response = self.client.get("/check-word?word=impossible")
        self.assertEqual(response.json["result"], "not-on-board")
        
    def non_english_word(self):
        # test if word is on board
        self.client.get("/")
        response = self.client.get("/check-word?word=qworeywreytieyeuytritur")
        self.assertEqual(response.json["result"], "not-word")
        
