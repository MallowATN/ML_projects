import pandas as pd 

def pred_test(model, x_test):
    y_test = model.predict(x_test)
    filename = str(model.__class__.__name__)+"pred_output.csv"
    prediction = pd.DataFrame(y_test)
    pd.DataFrame(y_test).to_csv("data/test_model/"+filename)
    return prediction