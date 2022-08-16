'''
This file will fetch all the COVID 19 from the Our World in Data github repository
Link to the data: https://covid.ourworldindata.org/data/owid-covid-data.csv
'''

import pandas as pd 

def fetch_covid_data():
    '''
    This function will fetch all the COVID 19 data in csv format 
    from the Our World in Data github repository and create an pandas dataframe
    '''
    df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
    #df.to_csv('coviddata.csv', index=False)
    return df

# Run it in the command line
if __name__ == '__main__':
    fetch_covid_data()