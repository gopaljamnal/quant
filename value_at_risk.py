import numpy as np
import yfinance as yf
from scipy.stats import norm
import pandas as pd
import datetime
import matplotlib.pyplot as plt

pd.set_option('display.max_colwidth', None)

stocks = ['AAPL', 'WMT', 'TSLA', 'GE', 'AMZN', 'DB']

start_date = '2012-01-01'
end_date = '2017-01-01'

NUM_TRADING_DAYS = 252
NUM_PORTFOLIOS = 10000
def download_data():
    stock_data = {}
    for stock in stocks:
        ticker = yf.Ticker(stock)
        stock_data[stock] = ticker.history(start=start_date, end=end_date)['Close']
    return pd.DataFrame(stock_data)

def show_data(data):
    data.plot(figsize=(10, 5))
    plt.show()

def calculate_return(data) :
    log_return = np.log(data/data.shift(1))
    return log_return[1:]

def show_statistics(returns):
    print(returns.mean() * NUM_TRADING_DAYS)
    print(returns.cov() * NUM_TRADING_DAYS)

def show_mean_variance(returns, weights):
    portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
    portfolio_volability = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights)))
    print("Expected portfolio mean (return): ", portfolio_return)
    print("Expected portfolio volatility (standard deviation): ", portfolio_volability)


def show_portfolio(returns, volatilities):
    plt.figure(figsize=(10, 5))
    plt.scatter(volatilities, returns, c= returns/volatilities, marker='o')
    plt.grid(True)
    plt.xlabel("Expected Volatility")
    plt.ylabel("Expected Return")
    plt.colorbar(label="Sharpe Ratio")
    plt.show()
def generate_portfolio(returns):

    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = []

    for _ in range(NUM_PORTFOLIOS):
        w =  np.random.random(len(stocks))
        w /= np.sum(w)
        portfolio_weights.append(w)
        portfolio_means.append(np.sum(returns.mean() * w ) * NUM_TRADING_DAYS)
        portfolio_risks.append(np.sqrt(np.dot(w.T, np.dot(returns.cov() * NUM_TRADING_DAYS, w))))

    return np.array(portfolio_weights), np.array(portfolio_means), np.array(portfolio_risks)
#this is how we calculate the VaR tomorrow(n=1)
def calculate_var(position, c,mu, sigma):
    var = position * (mu - sigma * norm.ppf(1-c))
    return var


from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key=)

## everything
def get_news(newsapi):
    all_articles =newsapi.get_everything(q='bitcoin', sources='bbc-news, the-verge', from_param="2025-01-01", to_param="2025-01-31", language='en', sort_by='relevance', page=2)
    return all_articles

# top headlines
source = newsapi.get_sources()



if __name__ == '__main__':

    # start = datetime.datetime(2014,1,1)
    # end = datetime.datetime(2018,1,1)
    # stock_data = download_data('C', start, end)
    #
    # stock_data['return'] = np.log(stock_data['C'] / stock_data['C'].shift(1))
    # print(stock_data)
    dataset = download_data()
    show_data(dataset)
    log_daily_return = calculate_return(dataset)
    show_statistics(log_daily_return)

    weights, means, risks = generate_portfolio(log_daily_return)
    show_portfolio(means, risks)
