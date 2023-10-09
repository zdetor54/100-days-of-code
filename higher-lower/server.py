from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def hello():
    return('<h1>Guess a number between 0 and 9</h1>'
           '<img src = "https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif"/>')
@app.route("/<int:guessed_num>")
def check_guess(guessed_num):
    if guessed_num < number:
        return (f'<p>{guessed_num} is too low</p>'
                '<img src = "https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"/>')
    elif guessed_num > number:
        return (f'<p>{guessed_num} is too high</p>'
                '<img src = "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"/>')
    else:
        return (f'<p>{guessed_num} is just right</p>'
                '<img src = "https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"/>')

if __name__ == "__main__":
    number = random.randint(0,9)
    print(number)
    app.run(debug=True)

