import pandas as pd
import numpy as np
import scipy as sp
import chart_studio.plotly as py
import chart_studio.plotly as py
import plotly.figure_factory as ff
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

df = pd.read_csv("https://linked.aub.edu.lb/pkgcube/data/17501924270e0cf53d2db144d41c3f01_20240905_174938.csv")

st.title('Demography')

if st.checkbox('Show Demographic Data'):
 st.subheader('Demographic Data')
 st.write(df)

# Drop rows where "Percentage of Women" or "Percentage of Men" are NaN or 0
df_clean = df[(df['Percentage of Women'].notna()) & (df['Percentage of Men'].notna()) &
              (df['Percentage of Women'] != 0) & (df['Percentage of Men'] != 0)]

df_top25 = df_clean.head(25)

# Define bars for Women and Men
Women_Percentage = go.Bar(x=df_top25.Town,
                     y=df_top25['Percentage of Women'],
                     name='Women',
                     marker=dict(color='#ffcdd2'))

Men_Percentage = go.Bar(x=df_top25.Town,
                   y= df_top25['Percentage of Men'],
                   name='Men',
                   marker=dict(color='#74B3D1'))

# Combine Bars into a list
data = [Women_Percentage, Men_Percentage]

# Define layout of the plot
layout = go.Layout(title="Gender Percentages",
                   xaxis=dict(title='Town'),
                   yaxis=dict(title='Percentage'))

# Create a figure and display it inline
fig = go.Figure(data=data, layout=layout)

chart_mode = st.radio("Select Chart Mode", ['Group', 'Stack'])
fig.update_layout(barmode='group' if chart_mode == 'Group' else 'stack')

st.subheader('Barchart using options')

st.plotly_chart(fig)

st.subheader('Barchart using st.bar_chart')

# Extract relevant data
city_data = df_top25[['Town', 'Percentage of Women', 'Percentage of Men']].set_index('Town')

st.subheader("Gender Percentages")
# Streamlit bar chart
st.bar_chart(city_data)

st.subheader('Line Chart of Family sizes')
# Extract relevant columns and drop rows with missing values
df_line = df_top25[['Town', 'Average family size - 1 to 3 members',
                 'Average family size - 4 to 6 members',
                 'Average family size - 7 or more members ']].dropna()

# Set 'Town' as the index for better plotting
df_line.set_index('Town', inplace=True)

# Streamlit line chart: it automatically makes the chart interactive
st.line_chart(df_line)

st.subheader('Comparison of Elderly and Youth Percentages Across Towns')

# Handle missing values by filling them with 0
df_top25.fillna(0, inplace=True)

# Extract the relevant columns for visualization
age_percentages = df_top25[['Town', 'Percentage of Eldelry - 65 or more years ', 'Percentage of Youth - 15-24 years']]

# Set the index to 'Town' for better area chart representation
age_percentages.set_index('Town', inplace=True)

# Create an area chart using Streamlit's st.area_chart
st.area_chart(age_percentages)