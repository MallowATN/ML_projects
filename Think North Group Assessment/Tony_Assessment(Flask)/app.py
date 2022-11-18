from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
from views import views

# with open('Tony_Assessment/Total_Rev.pkl','rb') as f:
#     model = pickle.load()

app = Flask(__name__)
model = pickle.load(open('retired/Total_Rev.pkl', 'rb'))

app.register_blueprint(views, url_prefix="/")

# @app.route('/')
# def home():
#     return render_template('index.html')
    
@app.route('/predict', methods=['POST'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0],2)
    return render_template('index.html', prediction_text='Total Revenue is around... ${}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)

