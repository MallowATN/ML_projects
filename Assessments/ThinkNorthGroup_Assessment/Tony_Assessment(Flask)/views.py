from flask import Blueprint, render_template, request
import numpy as np
import pickle
from flask_login import login_required, current_user

views = Blueprint("views", __name__)
model = pickle.load(open('retired/Total_Rev.pkl', 'rb'))

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/predict', methods=['POST'])
@login_required
def predict():
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0],2)
    return render_template('home.html', prediction_text='Total Revenue is around... ${}'.format(output), user=current_user)