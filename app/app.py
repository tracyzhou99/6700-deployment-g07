from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

# add get and post method to our app
@app.route('/', methods=['GET','POST'])

def index():
    # get the html request type to differentiate the output
    request_type = request.method
    if request_type == 'GET':
        path = 'static/example.png'
        return render_template('index.html',href=path)
    else:
        text = request.form['text']
        path = 'static/example.png'
        return render_template('index.html',href=path)


if __name__ == '__main__':
    app.run(debug=True)
