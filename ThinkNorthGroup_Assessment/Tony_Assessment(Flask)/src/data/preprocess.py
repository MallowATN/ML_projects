import logging
from src.util.data_prep import load_raw_data, save_processed_data

def preprocessing(): #We'll just test this out for short, since this isn't one of the big projects that I work with, just an assessment, BUT insightful.
    logger = logging.getLogger(__name__)
    logger.info('creating final dataset from raw data')
    #load the data
    df = load_raw_data()
    #drop these columns... we'll just test this out for short, since this isn't one of the big projects that I work with, just an assessment, BUT insightful.
    df = df.drop(['Days Since Most Recent Deal Close','Employees','Billing Country','Industry',
            'Owner ID','Annual Revenue','Account Type','Average Age','Account Source',
            'Top Product Family','Days Since First Deal Close','Account ID', 'Account Name',
            'Created Date','Billing State/Province','Customer Priority','First Deal Date',
            'Number of Locations','Top Product Name'
            ],axis=1)
    save_processed_data(df)
    return

if __name__ == '__main__':
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)
    preprocessing()