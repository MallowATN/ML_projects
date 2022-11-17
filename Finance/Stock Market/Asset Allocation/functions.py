import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

pca = PCA()

def pcWeights(X_train):
    #principal components (pc) weights for each 28 pc
    weights = pd.DataFrame()
    pca = PCA()
    pcomp = pca.fit(X_train)
    for i in range(len(pca.components_)):
        weights['weights_{}'.format(i)] = pca.components_[i] / sum(pca.components_[i])
    weights = weights.values.T
    return weights

# To find the best Eigen Portfolio, we use Sharpe ratio. Higher Sharpe Ratio means higher Returns and/or lower volatility for a specified portfolio
def Sharpe_ratio(ts_returns, trading_days_per_year=252): #total of 252 trading days per year
    n_years = ts_returns.shape[0]/trading_days_per_year
    annualized_return = np.power(np.prod(1+ts_returns),(1/n_years))-1
    annualized_volatility = ts_returns.std() * np.sqrt(trading_days_per_year)
    annualized_Sharpe = annualized_return/annualized_volatility
    return annualized_return, annualized_volatility, annualized_Sharpe

def final_port(rs_df,X_train_clean):
    num_port = len(pca.components_)
    annual_ret = np.array([0.] * num_port)
    sharpe_ratio = np.array([0.] * num_port)
    annual_vol = np.array([0.] * num_port)
    max_sharpe = 0

    stock_tickers = rs_df.columns.values
    # num_ticks = len(stock_tickers)
    principal_comps = pca.components_

    for i in range(num_port):
        pc_weight = principal_comps[i] / sum(principal_comps[i])
        eigen_portfolio = pd.DataFrame(data={'weights': pc_weight.squeeze()*100}, index=stock_tickers)
        eigen_portfolio.sort_values(by=['weights'], ascending=False, inplace=True)

        eigen_portfolio_ret = np.dot(X_train_clean.loc[:,eigen_portfolio.index],pc_weight)
        eigen_portfolio_ret = pd.Series(eigen_portfolio_ret.squeeze(), index=X_train_clean.index)
        ar, av, aS = Sharpe_ratio(eigen_portfolio_ret)
        annual_ret[i] = ar
        annual_vol[i] = av
        sharpe_ratio[i] = aS

        sharpe_ratio = np.nan_to_num(sharpe_ratio)

    max_sharpe = np.argmax(sharpe_ratio)

    print('The best Eigen portfolio is number #%d... The return is %.2f%%, the volatility is %.2f%%, and the Sharpe ratio is %.2f'%
        (max_sharpe, annual_ret[max_sharpe]*100, annual_vol[max_sharpe]*100, sharpe_ratio[max_sharpe]))

def Backtest(eigen, X_test_clean, X_test, stock_ticks):
    '''Plots Principle components returns against real returns.'''
    eigen_prtfi = pd.DataFrame(data ={'weights': eigen.squeeze()}, index = stock_ticks)
    eigen_prtfi.sort_values(by=['weights'], ascending=False, inplace=True)    

    eigen_prti_returns = np.dot(X_test_clean.loc[:, eigen_prtfi.index], eigen)
    eigen_portfolio_returns = pd.Series(eigen_prti_returns.squeeze(), index=X_test_clean.index)
    returns, vol, sharpe = Sharpe_ratio(eigen_portfolio_returns)  
    print('Current Eigen-Portfolio:\nReturn = %.2f%%\nVolatility = %.2f%%\nSharpe = %.2f' % (returns*100, vol*100, sharpe))
    equal_weight_return=(X_test_clean * (1/len(pca.components_))).sum(axis=1)    
    df_plot = pd.DataFrame({'EigenPorfolio Return': eigen_portfolio_returns, 'Equal Weight Index': equal_weight_return}, index=X_test.index)
    np.cumprod(df_plot + 1).plot(title='Returns of the equal weighted index vs. eigen-portfolio' , 
                          figsize=(12,6), linewidth=3)
    plt.show()