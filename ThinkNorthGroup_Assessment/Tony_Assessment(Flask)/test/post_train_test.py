import numpy as np
import pytest
import pytest_check as check

from src.data.preprocess import preprocessing
from src.model.train_model import gradient_boost_reg
from src.util.data_prep import split_train_test_data

@pytest.fixture
def data_preparation():
    preprocessing()
    return split_train_test_data()

@pytest.fixture
def return_models(data_preparation):
    X_train, y_train, X_test, y_test = data_preparation
    GBR = gradient_boost_reg(X_train, y_train)
    return [GBR]

# Add rules under here...
