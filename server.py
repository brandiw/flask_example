# Import the flask module, and any others needed
from flask import Flask, jsonify, redirect, render_template, request
import my_secrets
from pymongo import MongoClient

# Declare app variable
app = Flask(__name__, static_folder='static', static_url_path='')

# Set up mongo database
client = MongoClient()
db = client.test_heroes # Name of new or existing database
collection = db.heroes # Name of new or existing collection

# Declare the desired route's path
# Then, declare a function for that route to use
@app.route('/')
def home():
    heroes = db.heroes.find()
    return render_template('home.html', name=my_secrets.firstname, heroes=heroes)

# Define say_hi route (this has an optional param called num)
@app.route('/say_hi')
@app.route('/say_hi/<num>')
def hello(num):
    return 'Hello, ' + my_secrets.firstname + '! I see you\'re drinking ' + my_secrets.drink + ' and you like ' + num

@app.route('/hero/<name>', methods=['GET'])
def gimmieOneHero(name):
    heroes = [{'person': 'Superman', 'age': 1000}, {'person': 'Batman', 'age': 36}, {'person': 'Thor'}, {'person': 'Wonder Woman'}]
    names = [hero for hero in heroes if hero['person'] == name]

    # NOTE: Empty lists are FALSEY!!!
    if names:
        return jsonify({'hero': names[0]})
    else:
        return "Hero not found"

@app.route('/heroes', methods=['POST'])
def create():
    person = request.form['person']
    age = request.form['age']

    new_hero = {
        'person': person,
        'age': age
    }

    db.heroes.insert_one(new_hero)
    return redirect('/')

# Make sure the program is listening for connections
# Default port is 5000
if __name__ == '__main__':
    app.run(debug=True)
