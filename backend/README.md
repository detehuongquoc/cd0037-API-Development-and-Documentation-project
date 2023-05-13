# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

# get categories end point

`GET '/categories'`

- Description: Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key-value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

# get questions end point

- `GET '/questions'`

- Description: Fetches a paginated list of questions.
- Request Arguments:
  - page (optional): The page number of the questions to retrieve. Defaults to 1.
- Returns: An object with the following properties:
  - success: Boolean value indicating the success status of the request.
  - questions: An array of formatted question objects.
  - total_questions: The total number of questions available.
  - current_page: The current page number.
  - categories: An object of id: category_string key-value pairs.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_page": 1,
  "questions": [
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 55
}
```

# delete question end point

`DELETE '/questions/int:question_id'`

- Description: Deletes a question with the given question ID.
- Request Arguments: None
- Returns: An object with the following properties:
  success: Boolean value indicating the success status of the request.
  message: A success message indicating that the question was deleted successfully.

```json
{
    "message": "Question deleted successfully",
    "success": true
}
```

# create question end point

`POST '/questions'`

- Description: Creates a new question.
- Request Arguments: None
- Request Body: A JSON object containing the following properties:
  - question: The text of the question.
  - answer: The answer to the question.
  - category: The ID of the category the question belongs to.
  - difficulty: The difficulty level of the question.
- Returns: An object with the following properties:
  - success: Boolean value indicating the success status of the request.
  - message: A success message indicating that the question was created successfully.
  - question: The formatted question object that was created.
```json
{
    "message": "Question created successfully",
    "question": {
        "answer": "Question 2",
        "category": 1,
        "difficulty": 1,
        "id": 105,
        "question": "Question 2"
    },
    "success": true
}
```

# search question end point

`POST '/questions/search'`

- Description: Searches for questions based on a search term.
- Request Arguments: None
- Request Body: A JSON object containing the following properties:
  - searchTerm: The search term to match against question texts.
- Returns: An object with the following properties:
  - success: Boolean value indicating the success status of the request.
  - questions: An array of formatted question objects that match the search term.
  - total_questions: The total number of matching questions.


```json
{
    "questions": [
        {
            "answer": "Vollbyelball",
            "category": 6,
            "difficulty": 5,
            "id": 24,
            "question": "What is your favorirest game"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

# get question by catergory id

`GET '/categories/int:category_id/questions'`

- Description: Fetches a list of questions that belong to the specified category.
- Request Arguments: None
- Request Body: A JSON object containing the following properties:
  - searchTerm: The search term to match against question texts.
- Returns: An object with the following properties:
  - success: Boolean value indicating the success status of the request.
  - questions: An array of formatted question objects that belong to the category.
  - total_questions: The total number of questions in the category.


```json
{
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "total_questions": 4
}
```

# get quizz to play game

`POST '/quizzes'`

- Description: Retrieves a random question for a quiz.
- Request Arguments: None
- Request Body: A JSON object containing the following properties:
  - quiz_category: An object with the properties id (the ID of the quiz category) and type (the string name of the category).
  - previous_questions: An array of question IDs that have been asked previously in the quiz, we not choose it into next      question.
- Returns: An object with the following properties:
  - success: Boolean value indicating the success status of the request.
  - questions: An array of formatted question objects that match the search term.


```json
{
    "question": {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
````
