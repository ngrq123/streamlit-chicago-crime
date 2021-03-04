import streamlit as st

import pandas as pd

from bokeh.plotting import figure
import matplotlib.pyplot as plt


@st.cache
def load_data(url):
    data = pd.read_csv(url, index_col=0)
    data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y %H:%M:%S %p')
    data = data.loc[data['Date'].dt.year <= 2016]
    return data

def groupby_year_month(data_df):
    df_copy = data_df.copy()
    df_copy = df_copy.groupby(['Date'])['ID'] \
        .count() \
        .rename('Sample Count')
    return df_copy.resample('1Y').sum()

##### Config ######

DATA_FILE_PATH = './data/Crimes_2001_to_present_sample.csv'

###### Sidebar #####

years_slider = st.sidebar.slider('Select a range of years:', 
    2001, 2016, 
    (2001, 2016))

##### Dashboard

st.title('Sampled Chicago Crimes \n (Samples from 2001-2016)')

data_load_state = st.text('Status: Loading data...')
data = load_data(DATA_FILE_PATH)
data = data.loc[(data['Date'].dt.year >= years_slider[0]) & (data['Date'].dt.year <= years_slider[1])]
data_load_state.text("Status: Data loaded and filtered! (using st.cache)")

if st.checkbox('Show raw data sample'):
    st.dataframe(data.sample(100))

st.header('Sample Crimes per Year')

sample_crimes_per_year_df = groupby_year_month(data)

col1, col2 = st.beta_columns([2, 1])

with col1:
    plotting_lib = st.radio(
        "Select plotting library",
        ('Default (Altair)', 'Bokeh', 'Matplotlib'))

    if plotting_lib == 'Matplotlib':
        fig, ax = plt.subplots()
        ax.plot(sample_crimes_per_year_df.index, sample_crimes_per_year_df.values)
        st.pyplot(fig)
    elif plotting_lib == 'Bokeh':
        p = figure(x_axis_label='x', y_axis_label='y')
        p.line(sample_crimes_per_year_df.index, sample_crimes_per_year_df.values)
        st.bokeh_chart(p, use_container_width=True)
    else:
        st.line_chart(sample_crimes_per_year_df)

with col2:
    st.write('Data table')
    st.dataframe(sample_crimes_per_year_df)