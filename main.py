from flask import Flask, render_template
app = Flask(__name__)

posts = [
  {
    'user': 'John',
    'title': 'Post 1',
    'content': 'Help',
    'date': 'March 3, 2023'
  },
  {
    'user': 'Tim',
    'title': 'Post 2',
    'content': 'Help',
    'date': 'March 4, 2023'
  }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

app.run(host='0.0.0.0', port=81)