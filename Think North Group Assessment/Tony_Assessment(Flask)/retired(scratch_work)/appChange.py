from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np


# with open('Tony_Assessment/Total_Rev.pkl','rb') as f:
#     model = pickle.load()

app = Flask(__name__)
model = pickle.load(open('model/Total_Rev.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('indexTrue.html')
    
@app.route('/predict', methods=['POST'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0],2)
    return render_template('indexTrue.html', prediction_text='Total Revenue is around... ${}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)
