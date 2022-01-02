# Reminda
Project for Reminda: Application to help you study

Basically, Reminda allows you to create an exam/test called questionnaire with 3 different kinds of questions:
- Questions where you have to provide the answer
- Questions with 4 possible answers but only 1 correct answer (you can only pick one)
- Questions with 4 possible answers but only 2 correct answers (you have to pick two)

Once you have create the questions for your questionnaire, you can load it and answer the questions one by one. However, questions will be presented in a different order.
The innovation comes for the fact that in this application you can choose the following parameters:
- Time you have to answer a question -> When that time is over, the question will disappear
- Time between questions -> After you answered the question or the time to answer it is over, the application will disappear and a new question will appear after the time we set in this parameter

The idea is to help you study in this 3 ways:
- You have to transform the topic you are studying into these 3 kinds of questions, helping you study the material in a different way
- You can see how you have done by the end (also if you would pass or not)
- Also, you can take the exam all at once or use a very interesting way of studying the material, you can set a bigger time between questions so you can be working on another thing while from time to time a question will pop up and will help you remind those questions you always seem to forget

In order to execute this application you need:
- Python 3.8
- In the project folder, execute the following command: pip3 install -r requirements.txt (or pip install -r requirements.txt)

To execute this application, in the project folder just run: python3 main.py