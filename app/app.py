from flask import Flask, render_template, request, flash
import numpy as np
import pandas as pd
import secrets
import joblib

app = Flask(__name__)
app.secret_key = secrets.token_hex()

# define the available models for the app
available_models = ['lg', 'NB', 'KNN', 'Tree', 'Random Forest', 'Bagging', 'XGB', 'GBM', 'Stacked Model',]

# add get and post method to our app
@app.route('/', methods=['GET','POST'])

def index():
    # get the html request type to differentiate the output
    request_type = request.method
    if request_type == 'GET':
        path = 'static/mean_importances.svg'
        flash(f"Please input data and submit!", "welcome")
        return render_template('index.html',href=path,available_models=available_models)
    else:
        # use try except to make sure the input value is valid
        try:
            # collect the input values from the input form
            # change the datatype into float
            test_data = [float(value) for key, value in request.form.items() if key != "model"]
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
            test_dict = test_df.to_dict(orient='records')[0]
            # perform the model testing part
            selected_model = request.form.get('model')
            model_path = f"app/TrainedModel/{selected_model}.joblib"
            joblib_model = joblib.load(model_path)
            class_label = joblib_model.predict(test_df)[0]
            # save the result as a variable
            if class_label == 0:
                result = 'NOT PCOS'
            else:
                result = 'PCOS'
            # define the return message
            flash(f"The diagnosis result of the patient's data is {result}.", "result")
        except Exception as e:
            selected_model = None
            test_dict=None
            flash(f'Invalid Input. Please check your selected model, data, and types!', 'danger')
        
        # print the result to the HTML page
        path = 'static/mean_importances.svg'
        return render_template('index.html',href=path,available_models=available_models,selected_model=selected_model,input_table=test_dict)


if __name__ == '__main__':
    app.run(debug=True)
