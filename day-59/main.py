from flask import Flask,render_template
import requests
import json

app = Flask("__name__")

URL = 'https://api.npoint.io/5bac95d077d22575d565'
response = requests.get(url=URL)

data = response.json()
print(data)


@app.route("/")
def get_all_posts():
    return render_template("index.html", posts = data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:id>")
def post(id):
    post = data[id-1]
    return render_template("post.html", post = post)

if __name__ == "__main__":
    app.run(debug=True)