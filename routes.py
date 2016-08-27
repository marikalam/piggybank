from flask import Flask, session, g, redirect, url_for, abort, render_template, flash
from flask import request
app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template('home.html')

if __name__ == "__main__":
    app.run()