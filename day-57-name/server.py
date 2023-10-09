from flask import Flask, render_template
import requests

GENDER_URL = "https://api.genderize.io?"
AGE_URL = "https://api.agify.io?"
app = Flask(__name__)

@app.route("/guess/<string:name>")
def name_check(name):
    query_params = {
        'name': name,
    }

    response = requests.get(url= GENDER_URL, params=query_params)
    data = response.json()
    gender = data["gender"]

    response = requests.get(url=AGE_URL, params=query_params)
    data = response.json()
    age = data["age"]

    return render_template("name.html", name = name, gender = gender, age = age)
@app.route("/blog")
def blog():
    blog_url = 'https://www.npoint.io/docs/c790b4d5cab58020d391'
    response = requests.get(url=blog_url)
    data = response.json()
    print(data)
    return render_template('blog.html', posts = data)


if __name__ == "__main__":
    # app.run(debug=True)
    blog_url = 'https://www.npoint.io/docs/c790b4d5cab58020d391'
    response = requests.get(url=blog_url)
    # data = response.json()
    print(response.text)