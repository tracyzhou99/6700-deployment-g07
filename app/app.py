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
            # save the data into a dataframe
            test_df = pd.DataFrame([test_data], columns=[' Age (yrs)', 'Weight (Kg)', 'Height(Cm) ', 'Blood Group',
                'Pulse rate(bpm) ', 'RR (breaths/min)', 'Hb(g/dl)', 'Cycle(R/I)',
                'Cycle length(days)', 'Marraige Status (Yrs)', 'Pregnant(Y/N)',
                'No. of aborptions', '  I   beta-HCG(mIU/mL)', 'II    beta-HCG(mIU/mL)',
                'FSH(mIU/mL)', 'LH(mIU/mL)', 'Hip(inch)', 'Waist:Hip Ratio',
                'TSH (mIU/L)', 'AMH(ng/mL)', 'PRL(ng/mL)', 'Vit D3 (ng/mL)',
                'PRG(ng/mL)', 'RBS(mg/dl)', 'Weight gain(Y/N)', 'hair growth(Y/N)',
                'Skin darkening (Y/N)', 'Hair loss(Y/N)', 'Pimples(Y/N)',
                'Fast food (Y/N)', 'Reg.Exercise(Y/N)', 'BP _Systolic (mmHg)',
                'BP _Diastolic (mmHg)', 'Follicle No. (L)', 'Follicle No. (R)',
                'Avg. F size (L) (mm)', 'Avg. F size (R) (mm)', 'Endometrium (mm)'])
            # perform the model testing part
            with open('TrainedModel/stackedmodel.pkl', 'rb') as file:
                pickle_model = pickle.load(file)
                class_label = pickle_model.predict(test_df)[0]
            # save the result as a variable
            if class_label == 0:
                result = 'NOT PCOS'
            else:
                result = 'PCOS'
            # define the return message
            message = f"The diagnosis result of the patient's data is {result}."
        except:
            message = f"Invalid Input. Please check your data and type."
        
        # print the result to the HTML page
        path = 'static/mean_importances.svg'
        return render_template('index.html',href=path,message=message)


if __name__ == '__main__':
    app.run(debug=True)
