import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from decouple import config


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        # edit create to test
        self.database_path = config('DATABASE_PATH')

        self.app = create_app(self.database_path)
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test case for get categories : pass and fail *********************

    def test_get_categories_success(self):
        """Test GET /categories endpoint - Success"""
        res = self.app.test_client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']) > 0)

    def test_get_categories_failure(self):
        """Test GET /categories endpoint - Failure"""
        res = self.app.test_client().get('/categories/nonexistent')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    # # Test case for get questions : pass and fail *********************

    def test_get_questions_success(self):
        """Test GET /questions endpoint - Success"""
        res = self.app.test_client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)

    def test_get_questions_failure(self):
        """Test GET /questions endpoint - Failure"""
        res = self.app.test_client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    #  # Test case for delete questions : pass and fail *********************

    def test_delete_question_success(self):
        """Test DELETE /questions/<int:question_id> endpoint - Success"""
        # create new Question
        question_payload = {
            'question': 'What is the capital of France?',
            'answer': 'Paris',
            'category': 3,
            'difficulty': 2
        }
        res = self.app.test_client().post('/questions', json=question_payload)
        data = res.get_json()

        # Get id From that question
        question_id = data['question']['id']

        # start delete it
        res = self.app.test_client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question deleted successfully')

    def test_delete_question_failure(self):
        """Test DELETE /questions/<int:question_id> endpoint - Failure"""
        # Assuming question_id = 9999 does not exist in the database
        question_id = 9999
        res = self.app.test_client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    #  # Test case for create questions : pass and fail *********************

    def test_create_question_success(self):
        """Test POST /questions endpoint - Success"""
        # Assuming a valid question payload
        question_payload = {
            'question': 'What is the capital of France?',
            'answer': 'Paris',
            'category': 3,
            'difficulty': 2
        }
        res = self.app.test_client().post('/questions', json=question_payload)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question created successfully')
        self.assertTrue(data['question'])

    def test_create_question_failure(self):
        """Test POST /questions endpoint - Failure"""
        # Assuming an invalid question payload missing 'question' field
        question_payload = {
            'answer': 'Paris',
            'category': 3,
            'difficulty': 2
        }
        res = self.app.test_client().post('/questions', json=question_payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

    # # Test case for search questions : pass and fail *********************

    def test_search_questions_success(self):
        """Test POST /questions/search endpoint - Success"""
        # Assuming a valid search term
        search_payload = {
            'searchTerm': 'what'
        }
        res = self.app.test_client().post('/questions/search', json=search_payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['total_questions'], int)

    # # Test case for get questions by category : pass and fail *********************

    def test_get_questions_by_category_success(self):
        """Test GET /categories/<int:category_id>/questions endpoint - Success"""
        # Assuming a valid category ID
        category_id = 1
        res = self.app.test_client().get(
            f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['total_questions'], int)

    def test_get_questions_by_category_failure(self):
        """Test GET /categories/<int:category_id>/questions endpoint - Failure"""
        # Assuming an invalid category ID
        category_id = 1000
        res = self.app.test_client().get(
            f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    # # Test case for get post_quizz by category : pass and fail *********************

    def test_play_quiz_success(self):
        """Test POST /quizzes endpoint - Success"""
        # Assuming a valid previous question ID and category ID
        previous_question_id = 1
        category_id = 1

        payload = {
            'previous_question': previous_question_id,
            'quiz_category': {
                'id': category_id
            }
        }

        res = self.app.test_client().post('/quizzes', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_play_quiz_failure(self):
        """Test POST /quizzes endpoint - Failure"""
        # not pass id in quiz_category
        previous_question_id = 1000
        tye_question = "Science"

        payload = {
            'quiz_category': {
                'type': tye_question
            }
        }

        res = self.app.test_client().post('/quizzes', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
