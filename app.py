# Main streamlit application for the Covid19 analytics dashboard

# Load modules
import pandas as pd
import streamlit as st
import plotly.express as px
import constants as const
from fetch_covid_data import fetch_covid_data

# Page configuration
st.set_page_config(page_title="Covid 19 Dashboard",  page_icon="🦠", layout='wide')

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

# Header 
st.markdown("# Covid 19 Dashboard 📈")
last_update = df[df['location'] == 'World'].iloc[-1, :]['date']
st.markdown(f'Last update: {last_update.date()}')

world_population = df[df['location'] == 'World'].iloc[-1, :]['population']

st.markdown("### General metrics")

# Separated in three columns
col1, col2, col3 = st.columns(3)

total_cases = df[df['location'] == 'World'].iloc[-1, :]['total_cases']

with col1:
    st.write(f'#### Total Cases')
    st.write(f'#### {int(total_cases):,}')
    st.write(f'{(total_cases*100/world_population):.2f}% of the population')

total_deaths = df[df['location'] == 'World'].iloc[-1, :]['total_deaths']

with col2:
    st.write(f'#### Total Deaths')
    st.write(f'#### {int(total_deaths):,}')
    st.write(f'{(total_deaths*100/world_population):.2f}% of the population')

total_vaccines = df[df['location'] == 'World'].iloc[-1, :]['total_vaccinations']

with col3:
    st.write(f'Total Vaccines')
    st.write(f'#### {int(total_vaccines):,}')

st.markdown("### General trends")

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
fig = px.line(df_plot, x='date', y=str(y_axis), color='location', title='COVID 19 information line chart')
st.plotly_chart(fig, use_container_width=True)

# Button to update data
if st.button('Update Data'): # Trigger something
    with st.spinner(text='Fetching data...'):
        df = fetch_covid_data()
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
