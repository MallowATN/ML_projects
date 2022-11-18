import pytest
import pandas as pd
import pytest_check as check
from src.data.preprocess import preprocessing
from src.util.data_prep import split_train_test_data
from src.model.train_model import gradient_boost_reg
from src.model.predict_model import pred_test


@pytest.fixture
def data_preparation():
    preprocessing()
    return split_train_test_data()

@pytest.fixture
def gradient_boost_reg_prediction(data_preparation):
    X_train, y_train, X_test, y_test = data_preparation
    GBR = gradient_boost_reg(X_train, y_train)
    y_pred = pred_test(GBR, X_test)
    return X_test, y_pred

def test_data_leak(data_preparation):
    X_train, y_train, X_test, y_test = data_preparation
    concat_df = pd.concat([X_train, X_test])
    concat_df.drop_duplicates(inplace=True)
    assert concat_df.shape[0] == X_train.shape[0] + X_test.shape[0]

# example...
def test_output_shape(gradient_boost_reg_prediction):
    print("Gradient Boost Regression")
    X_test, y_pred = gradient_boost_reg_prediction
    check.equal(y_pred.shape, (X_test.shape[0],1))
    # assert y_pred.shape == (X_test.shape[0],1)
