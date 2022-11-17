import pandas as pd
import yfinance as yf
from lxml import etree
from io import StringIO
import zipfile
import json
from datetime import date


tickers = ['AAPL','ADBE','AMD','AMC','AMZN','JPM','GOOG','GME','INTC','NFLX','TSLA']

def get_tick_data():
    start = '2008-01-01'
    end = '2019-01-01'
    df_ticker_return = pd.DataFrame()
    for ticker in tickers:
        ticker_yf = yf.Ticker(ticker)
        if df_ticker_return.empty:
            df_ticker_return = ticker_yf.history(start=start, end=end)
            df_ticker_return['ticker']=ticker
        else:
            data_temp = ticker_yf.history(start=start, end=end)
            data_temp['ticker']=ticker
            df_ticker_return = df_ticker_return.append(data_temp)
    df_ticker_return.to_csv(r'data\returnData.csv')

def jsonParser(json_data):
    xml_data = json_data['content']

    tree = etree.parse(StringIO(xml_data), parser=etree.HTMLParser())
    headlines = tree.xpath("//h4[contains(@class, 'media-heading')]/a/text()")
    assert len(headlines) == json_data['count']

    main_tickers = list(map(lambda x: x.replace('/symbol/',''), tree.xpath("//div[contains(@class, 'media-left')]//a/@href")))
    final_headlines = [''.join(f.xpath('.//text()')) for f in tree.xpath("//div[contains(@class, 'media-body')]/ul/li[1]")]
    if len(final_headlines) == 0:
        final_headlines = [''.join(f.xpath('.//text()')) for f in tree.xpath("//div[contains(@class, 'media-body')]")]
        final_headlines = [f.replace(h, '').split('\xa0')[0].strip() for f,h in zip (final_headlines, headlines)]
    return main_tickers, final_headlines

data_df_news = []
def jsonextractor():
    data = None
    with zipfile.ZipFile('Data/Raw Headline Data.zip','r') as z:
        for filename in z.namelist():
            try:
                with z.open(filename) as f:
                    data = f.read()
                    json_data = json.loads(data)
                if json_data.get('count',0) > 10:
                    #1) Parse the News JSONS files
                    main_tickers, final_headlines = jsonParser(json_data)
                    if len(final_headlines) != json_data['count']:
                        continue
                    #2) Prepare Future and event return and assign their return for each tickers
                    file_date = filename.split('/')[-1].replace('.json','')
                    file_date = date(int(file_date[:4]), int(file_date[5:7]), int(file_date[8:]))
                    #3) Merge
                    df_dict = {'ticker': main_tickers,
                            'headline': final_headlines,
                            'date': [file_date]*len(main_tickers)}
                    df_f = pd.DataFrame(df_dict)
                    data_df_news.append(df_f)
            except:
                pass


def add_features(df_ticker_return):
    #compute return
    df_ticker_return['ret_curr'] = df_ticker_return['Close'].pct_change()
    #compute event return
    df_ticker_return['eventRet'] = df_ticker_return['ret_curr'] + df_ticker_return['ret_curr'].shift(-1) + df_ticker_return['ret_curr'].shift(1)
    df_ticker_return.reset_index(level=0, inplace=True)
    df_ticker_return['date'] = pd.to_datetime(df_ticker_return['Date']).apply(lambda x: x.date())