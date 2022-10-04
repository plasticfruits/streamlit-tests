import time

from dataclasses import replace
from select import select
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# import data
df = pd.read_csv('./data/dummy_data.csv')

# conver date to datetime
df.date = pd.to_datetime(df["date"])

####################
# Streamlit App
####################



# event selector
select_event = st.selectbox(
    'Choose an event',
     df['eventName'].unique())
    # TODO: add select multiple and all
    
event_df = df[df.eventName.isin([select_event])]
event_df['month'] = event_df.date.dt.month.astype(int)
event_df['year'] = event_df.date.dt.year

# total count
metric_count = event_df['eventName'].count()
metric_users = event_df['userId'].nunique()

with st.container():
    col1, col2 = st.columns(2)
    col1.metric("Avg. Monthly Clicks", metric_count, -12)
    col2.metric("Monthly Users", metric_users, "11")  





# 2-cols layout
col1, col2 = st.columns(2)
# OS Pie Chart
#df.query(f"eventName == '{select_event}'")
fig = px.pie(event_df, values='userId', names='operatingSystem')
col1.plotly_chart(fig, use_container_width=True)

# Event Count Timeseries
daily_events = df.groupby(['date', 'eventName'])['eventName'].count().rename('count').to_frame().reset_index()
fig2 = px.line(daily_events.query(f"eventName == '{select_event}'"), x="date", y="count")
st.plotly_chart(fig2, use_container_width=True)

daily_events = event_df.groupby(['screenName', 'month'])['eventName'].count().rename('count').to_frame().reset_index()
daily_events = daily_events.pivot_table(index='month', columns='screenName', values='count')
st.area_chart(daily_events)

""" chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.area_chart(chart_data) """