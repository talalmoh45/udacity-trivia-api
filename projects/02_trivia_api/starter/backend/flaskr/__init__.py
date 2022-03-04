import json
import os
import re
from select import select
from tkinter import N
from unicodedata import category
from flask import Flask, request, abort, jsonify
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import time
time_func = time.time

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
#helper methode
def paginate(request,selection):
  page = request.args.get('page',1,int)
  start=(page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions=[q.format() for q in selection]
  current_questions = questions[start:end]
  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # CORS(app,resources={r"/questions/*",{'origins': '*'}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','content-type')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, PUT, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories',methods=['GET'])
  def get_Categories():
    selection = Category.query.order_by(Category.id).all()
    categories=paginate(request,selection)
  
    return jsonify({
      'categories' : categories
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''


  @app.route('/questions')
  def get_Questions():
    questions = Question.query.order_by(Question.id).all()

    formatted_questions=paginate(request,questions)
    all_categories = Category.query.order_by(Category.id).all()
    formatted_Categories= [category.format() for category in all_categories]

    if len(formatted_questions)==0:
      abort(404)

    else:
      
      return jsonify({
        'success':True,
        'questions' : formatted_questions,
        'total_questions' : len(questions),
        'categories' : formatted_Categories,
        'currentCategory' : formatted_Categories
      })



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''


  @app.route('/questions/<int:id>',methods=['DELETE'])
  def delete_question(id):
    try:
      question=Question.query.filter(Question.id==id).one_or_none()

      if question is None:
        abort(404)

      Question.delete(question)
      selection = Question.query.order_by(Question.id).all()
      curreen_questions = paginate(request,selection)
      return jsonify({
        'success' : True,
        'deleted' : id,
        'curreen_questions':curreen_questions,
        'total_questions' : len(Question.query.all())
      })

    except:
      abort(422)

    


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''


  @app.route('/questions',methods=['POST'])
  def add_new_question():
   body = request.get_json()

   new_question = body.get('question',None)
   new_answer = body.get('answer',None)
   new_category = body.get('category',None)
   new_difficulty = body.get('difficulty',None)
   searchTerm = body.get('searchTerm',None)

   if searchTerm:
      try:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(searchTerm))).all()
        result=paginate(request,selection)

        if searchTerm is None:
          abort(404)

        else:
          return jsonify({
            'success':True,
            'questions':result,
            'totalQuestions':len(Question.query.all()),
            'currentCategory' : result,
            'total_question_found':len(result)
          })
      except:
        abort(405)

   else:

      try:

        if new_question is None:
          abort(500)

        else:
          newQuestion = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
          Question.insert(newQuestion)
          questions= Question.query.order_by(Question.id).all() 
          current_questions = paginate(request,questions)

        return jsonify({
          "success":True,
          "created" : newQuestion.id,
          "current_questions" : current_questions,
          "total_questions" : len(Question.query.all())
        })

      except:
          abort(405)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
 


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  @app.route('/categories/<int:category>/questions',methods=['GET'])
  def get_category_question(category):
    cat=Category.query.filter(Category.id==category).one_or_none()
    question=Question.query.filter(category==Question.category).all()
    current_questions=paginate(request,question)
    if cat is None:
      abort(404)
    else:
      return jsonify({
        'success':True,
        'category' : category,
        'questions' : current_questions
      })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''


  @app.route('/quizzes',methods=['POST'])
  def quizes():
   if request.data:
    search_data = json.loads(request.data)

    if search_data['quiz_category']['id']==0:
        questions_query =Question.query.filter(
          Question.id.notin_(search_data["previous_questions"])
          ).all()
        length_of_available_question = len(Question.query.all())

        return jsonify({
                "success": True,
                "question": Question.format(questions_query[random.randrange(0,length_of_available_question)])
            })

    if (('quiz_category' in search_data)
              and 'previous_questions' in search_data):
          questions_query = Question.query.filter_by(
              category=search_data['quiz_category']['id']
          ).filter(
              Question.id.notin_(search_data["previous_questions"])
          ).all()
          length_of_available_question = len(questions_query)
          if length_of_available_question > 0:
              result = {
                  "success": True,
                  "question": Question.format(questions_query[random.randrange(0,length_of_available_question)])
              }
        
          else:
            result = {
                "success": True,
                "question": None
            }
            
          return jsonify(result)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404



  @app.errorhandler(422)
  def Unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable"
        }), 422



  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400



  @app.errorhandler(405)
  def methode_not_allowed(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "methode not allowed"
        }), 422



  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "internal server error"
        }), 500






  
  return app
