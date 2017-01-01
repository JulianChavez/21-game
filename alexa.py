import logging
import os 
from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():

    welcome_msg = "Let's play twenty one. Ready?"

    return question(welcome_msg)


@ask.intent("YesIntent")
def next_round():

    # Make two random numbers from 1 to 11    
    numbers = [randint(1, 11) for _ in range(2)]
    AlexaNumber1 = randint(1, 11)

    session.attributes['numbers'] = numbers
    session.attributes['AlexaNumber1'] = AlexaNumber1
    round_msg = render_template('round', numbers=numbers, AlexaNumber1=AlexaNumber1)
    return question(round_msg)

@ask.intent("StandIntent")
def standIntent(): 
    AlexaNumber2 = randint(1, 11)
    #create list of numbers for Alexa
    session.attributes["AlexaNumbers"] = [session.attributes["AlexaNumber1"]]
    session.attributes["AlexaNumbers"].append(AlexaNumber2)
    usernumbers = session.attributes['numbers']
    usersum = sum(usernumbers)

    #check alexa's sum, make sure it is over 16
    alexasum = sum(session.attributes["AlexaNumbers"])
    ####
    while alexasum <= 16:
        AlexaNumbers = randint(1, 11)
        session.attributes['AlexaNumbers'].append(AlexaNumbers)
        alexasum = sum(session.attributes["AlexaNumbers"])
        






    ####

    AllAlexaNumbers = session.attributes["AlexaNumbers"]

    if alexasum > 21 and usersum > 21:
        msg = render_template('draw', AlexaNumbers=AllAlexaNumbers, alexasum=alexasum, usersum=usersum)
        return statement(msg)
    elif  alexasum > 21 and usersum <= 21:
        msg= render_template('win', AlexaNumbers=AllAlexaNumbers, alexasum=alexasum, usersum=usersum)
        return statement(msg)
    elif alexasum <= 21 and usersum > 21:
        msg= render_template('lose', AlexaNumbers=AllAlexaNumbers, alexasum=alexasum, usersum=usersum)
        return statement(msg)
    elif alexasum <= 21 and usersum <=21:
        if alexasum > usersum:
            msg= render_template('lose', AlexaNumbers=AllAlexaNumbers, alexasum=alexasum, usersum=usersum)
            return statement(msg)
        elif alexasum < usersum:
            msg= render_template('win', AlexaNumbers=AllAlexaNumbers, alexasum=alexasum, usersum=usersum)
            return statement(msg)
        elif alexasum == usersum:
            msg = render_template('draw', AlexaNumbers=AllAlexaNumbers, alexasum=alexasum, usersum=usersum)
            return statement(msg)


@ask.intent("HitIntent")
def HitIntent():
    numbers = randint(1, 11) 
    session.attributes['numbers'].append(numbers)

    msg = render_template('new round', numbers=numbers)
    return question(msg)

# @ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
# def answer(first, second, third):

#     winning_numbers = session.attributes['numbers']

#     if [first, second, third] == winning_numbers:

#         msg = render_template('win')

#     else:

#         msg = render_template('lose')

#     return statement(msg)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
