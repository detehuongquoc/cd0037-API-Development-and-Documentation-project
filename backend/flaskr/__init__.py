import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(db_URI="", test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.debug = True
    app.app_context().push()
    if db_URI:
        setup_db(app, db_URI)
    else:
        setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        categoriesDict = {}
        for category in categories:
            categoriesDict[category.id] = category.type
        return jsonify({
            'success': True,
            'categories': categoriesDict
        })

    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        per_page = 10

        try:
            questions = Question.query.paginate(page=page, per_page=per_page)

            if not questions.items:
                abort(404)

            formatted_questions = [question.format()
                                   for question in questions.items]

            categories = Category.query.all()
            categoriesDict = {}
            for category in categories:
                categoriesDict[category.id] = category.type
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': questions.total,
                'current_page': page,
                'categories': categoriesDict
            })

        except Exception as e:
            abort(404)

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question:
            question.delete()
            return jsonify({"success": True, "message": "Question deleted successfully"})
        else:
            return abort(404)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        if 'question' not in body or 'answer' not in body or 'category' not in body or 'difficulty' not in body:
            abort(400)
        # Extract the required fields from the request body
        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')
        try:
            # Create a new Question instance
            new_question = Question(
                question=question, answer=answer, category=category, difficulty=difficulty)

            # Insert the question into the database
            new_question.insert()

            # Return a success response
            return jsonify({
                'success': True,
                'message': 'Question created successfully',
                'question': new_question.format()
            }), 201
        except Exception as e:
            # Return an error response if an exception occurs
            return jsonify({
                'success': False,
                'error': 'Failed to create question',
                'message': str(e)
            }), 500

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_term = request.json.get('searchTerm', '')

        try:
            # Perform the search query
            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            print(search_term, "neeeeeeeeeeeee")
            # Format the questions
            formatted_questions = [question.format() for question in questions]

            # Return the questions
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions)
            }), 200
        except Exception as e:
            abort(500)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            category = Category.query.get(category_id)

            if category is None:
                abort(404)

            # Retrieve questions based on the provided category ID
            questions = Question.query.filter_by(category=category_id).all()

            # Format the questions
            formatted_questions = [question.format() for question in questions]

            # Return the questions
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions)
            }), 200
        except Exception as e:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        body = request.get_json()
        quiz_category = body.get('quiz_category', None)
        previous_questions = body.get('previous_questions', [])

        try:
            # Query questions based on the category and exclude previous questions
            if quiz_category:
                category_id = int(quiz_category.get('id'))
                category = Category.query.get(category_id)

                if category is None:
                    abort(404)

                questions = Question.query.filter(
                    Question.category == category_id,
                    Question.id.notin_(previous_questions)
                ).all()
            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)
                ).all()

            # Randomly select a question from the available questions
            if questions:
                question = random.choice(questions).format()
            else:
                question = None

            return jsonify({
                'success': True,
                'question': question
            }), 200
        except Exception as e:
            print(e)
            abort(404)


# Error handlers ************************

# 400 Bad Request


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    # 404 Not Found
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    # 405 Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    # 500 Internal Server Error
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
