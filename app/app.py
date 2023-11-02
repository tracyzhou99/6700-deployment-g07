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
        path = 'static/mean_importances.svg'
        return render_template('index.html',href=path,message=None)
    else:
        # use try except to make sure the input value is valid
        try:
            # collect the input values from the input form
            # change the datatype into float
            test_data = [float(value) for key, value in request.form.items()]
            # perform the model testing part
            with open('stackedmodel.pkl', 'rb') as file:
                pickle_model = pickle.load(file)
            class_label = pickle_model.predict([test_data])[0]
           
            # save the result as a variable
            if class_label == '0':
               result = 'NOT PCOS'
            else:
               result = 'PCOS'
           
            # define the return message
            #message = f"The diagnosis result of the patient's data is {result}."
            message = f"The diagnosis result of the patient's data is {test_data}."
        except:
            message = f"Invalid Input. Please check your data and type."
        
        # print the result to the HTML page
        path = 'static/mean_importances.svg'
        return render_template('index.html',href=path,message=message)


if __name__ == '__main__':
    app.run(debug=True)

