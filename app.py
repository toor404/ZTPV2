from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/profile/<username>')
def show_profile(username):
    return render_template ('profile.html', username=username)