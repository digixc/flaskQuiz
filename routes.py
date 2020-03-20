from flask import Flask
from sqlalchemy.orm import sessionmaker, lazyload, joinedload
from flask import Flask, flash, redirect, render_template, request, session, abort

from models import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, ForeignKey
import datetime
import random

@app.route('/', methods=["GET", "POST"])
def mainpage():
        return render_template("mainpage.html")

# route decorator for the default path
@app.route('/login')
def login():
    if session.get('logged_in'):
        return redirect('quiz')
    else:
        users = [] 
        if request.form and session['admin']:
            try:
                users = User.query.all()
            except Exception as e:
                print("Failed to fetch users")
        return render_template("login.html", users=users)



# route decorator for the login path
@app.route('/do_login', methods=['GET', 'POST'])
def do_login():
    print('hahaha password!')
    POST_USERNAME = str(request.form.get('username'))
    POST_PASSWORD = str(request.form.get('password'))
     
    result = User.query.first()
    
    if result:
        session['logged_in'] = True
        session['loggedinUser'] = POST_USERNAME
        session['userID'] = result.id

        if result.username == 'teacher':
            session['admin'] = True
            
            users = User.query.all()
        return redirect('quiz')

    else:
        print('wrong password!')
        return render_template("login.html")

@app.route('/questions', methods=['GET', 'POST'])
def questions():
        quizID = str(request.form.get('quizID'))
        session['quizID'] = quizID

        quiz =   Quiz.query.filter_by(id=quizID).first()
    
        qsIDs=[]

        for q in quiz.questions:
            qsIDs.append(str(q.id))
        session['questionsIDs'] = qsIDs
        # for q in quiz.questions:
        #     print(type(q.options))
        return render_template("questions.html", questions = quiz.questions, quizid = quizID)

@app.route('/score', methods=['GET', 'POST'])
def score():
        questionsIDs = session.get("questionsIDs")
        userChoices =[]
        score = 0
        # get the user picked choice IDs for each question ID
        for i in range(len(questionsIDs)):
            userChoices.append(request.form.get("userChoice['"+ questionsIDs[i]+"']"))        

        for i in range(len(questionsIDs)):
            print("choices: ", questionsIDs[i], " - ", userChoices[i])
            qid = int(questionsIDs[i])
            cid = int(userChoices[i])
            choice = Choices.query.filter_by(id=cid).first()
            if choice.correct == 'True':
                score += 1

        if score >= 0:
            try:
                result = Results(user_id=session.get('userID'), quiz_id=session.get("quizID"), score=score, quiz_date=datetime.datetime.now())
                db.session.add(result)
                db.session.commit()
            except Exception as e:
                print("Failed to add score to results table")
                print(e)

        return render_template("scores.html", score=score)


@app.route('/progress')
def progress():

    reports={}
    colorStr =''
    chartsGroupDate ={}

    # change this to query results from the quiz table
    qIDs = {'1': 'Test', '2': 'Internet'}

    for qID in qIDs.keys():
        topic = qIDs[qID]
        dates = []
        scores = []
        backgroundColors = []
        res = Results.query.filter_by(user_id=session.get('userID'), quiz_id=int(qID)).order_by(Results.quiz_date).all()
        if len(res) > 0:
            for r in res:
                dates.append((r.quiz_date).strftime("%m/%d/%Y, %H:%M"))
                scores.append(r.score)

            print("Total records: ", len(res), " in topic ", topic)

            for i in range(len(res)):
                rColor = random.randrange(256)
                gColor = random.randrange(256)
                bColor = random.randrange(256)

                colorStr = 'rgba('+ str(rColor) + ','+ str(gColor) + ',' + str(bColor) + ', 0.5)'
                backgroundColors.append(colorStr)
          
            reports = {
           'dates': dates,
            'scores': scores,
            'backgroundColor': backgroundColors
            }

            chartsGroupDate[topic]=reports
    return render_template("progress.html", chartData = chartsGroupDate)
        
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    quiz = []
    errMsg=''
    userID = ''
    if session.get('logged_in'):
        userID = int(session.get('userID'))
        quiz = Quiz.query.all()
    elif len(quiz) == 0 :
        errMsg = 'No quiz found on DB'
    return render_template("quiz.html", quiz = quiz, msg = errMsg)

@app.route('/logout')
def logout():
    if session['logged_in']:
        session['logged_in'] = False
        session['admin'] = False
        session['loggedinUser'] = None
        return redirect("/")


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
    session['logged_in'] = False
