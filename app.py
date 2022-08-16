# Main streamlit application for the Covid19 analytics dashboard

import pandas as pd
import streamlit as st
import plotly.express as px
import constants as const
from fetch_covid_data import fetch_covid_data

# Set page width to wide
st.set_page_config(layout='wide')

# Create sidebar
st.sidebar.markdown('# COVID 19 Dashboard')
st.sidebar.markdown("### Author: Guillermo Chumaceiro")
st.sidebar.markdown("This dashboard shows the most important worldwide and countrywise parameters regarding the COVID19 pandemic from January 1st, 2020 until today using Python and Streamlit.")
st.sidebar.markdown("To get started")
st.sidebar.markdown("1. Select the date range")
st.sidebar.markdown("2. Select the countries/continents")
st.sidebar.markdown("3. Select the Y-axis")
st.sidebar.markdown("The dashboard fetchs the data once when it starts. If you want to update the data to include the lastest dates, press the update data button.")
st.sidebar.markdown("All the data is public and was obtain from [Our World in Data](https://ourworldindata.org/).")
st.sidebar.markdown("Data on COVID-19 (coronavirus) by Our World in Data: https://covid.ourworldindata.org/")

# fetch data from the website
with st.spinner(text='Fetching data...'):
    df = fetch_covid_data()

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Select date range to show on plot
date_range = st.date_input("Select date range to show data",value=[const.min_date, const.max_date], min_value=const.min_date, max_value=const.max_date)

# Select countries
all_countries = df['location'].unique()
countries = st.multiselect('Select countries', options=all_countries, default=['World', 'Europe', 'Africa', 'Asia', 'North America', 'South America'])

# Select Y axis
y_axis = st.selectbox('Select Y-axis', options=const.plot_y_axis_options, index=6)

# Subset data using selected parameters
date_mask = (df['date'] >= str(date_range[0])) & (df['date'] <= str(date_range[1]))
df_plot = df.loc[date_mask]
df_plot = df_plot[df_plot['location'].isin(countries)]

# Make plotly line chart
fig = px.line(df_plot, x='date', y=str(y_axis), color='location', title='COVID 19 information line chart', height=800)
st.plotly_chart(fig, use_container_width=True)

# Button to update data
if st.button('Update Data'): # Trigger something
    with st.spinner(text='Fetching data...'):
        df = fetch_covid_data()
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
