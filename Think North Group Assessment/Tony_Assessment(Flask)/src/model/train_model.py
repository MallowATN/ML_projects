from sklearn.ensemble import GradientBoostingRegressor

def gradient_boost_reg(X_train, y_train):
    GBR = GradientBoostingRegressor()
    GBR.fit(X_train, y_train)
    return GBR