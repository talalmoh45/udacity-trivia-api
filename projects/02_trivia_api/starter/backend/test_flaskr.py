import os
from re import T
from telnetlib import TTYLOC
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','1234','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question ={
            'question':'What is the whether today',
                        'answer':'sunny',
                        'category':'2',
                        'difficulty':1
                        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_pagenated_questions_and_categories(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['questions']),10)




    def test_delete_question(self):
        res = self.client().delete('/questions/15')
        data = json.loads(res.data)
        query = Question.query.filter(Question.id==15).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted',15])
        self.assertEqual(query,None)




    def test_post_new_question(self):
        response = self.client().post('/questions',json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_questions"])




    def test_search_question(self):
        res = self.client().post('/questions',json={'searchTerm':'title'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])
        self.assertEqual(data['total_question_found'],1)




    def test_get_questions_based_on_category(self):
        res = self.client().get('/categories/2/questions')
        data=json.loads(res.data)

        self.assertEqual(data['success'],True)
        self.assertTrue(data['category'])
        self.assertTrue(data['questions'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()