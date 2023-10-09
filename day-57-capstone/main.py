from flask import Flask, render_template
import requests
from post import Post

blog_url = 'https://api.npoint.io/5980e7d6ccee3d92d16b'
response = requests.get(url=blog_url)
blog_data = response.json()

ls_blog = []

for blog in blog_data['blogs']:
    my_post = Post(id = blog['id'], body=blog['body'], title=blog['title'], subtitle=blog['subtitle'])
    ls_blog.append(my_post)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", posts = ls_blog )

@app.route('/post/<int:id>')
def blog_post(id):
    return render_template("post.html", post = ls_blog[id-1])

if __name__ == "__main__":
    app.run(debug=True)
