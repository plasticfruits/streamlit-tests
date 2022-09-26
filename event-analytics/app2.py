import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st

dataset_url = "https://www.dropbox.com/s/qh7z695q5vajpb6/dummy_data.csv"
dataset_path = "./data/dummy_data.csv"

# page config --> first st element!!
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Streamlit | Simple Analytics Viewer")

# read csv from a URL
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_path)

df = get_data()
df.date = pd.to_datetime(df["date"])


# top-level filters
event_filter = st.selectbox("Select the event", pd.unique(df["eventName"]))

# dataframe filter
df = df[df["eventName"] == event_filter]
df['month'] = df.date.dt.month

# create three columns
kpi1, kpi2, kpi3 = st.columns(3)

# define KPI metrics
m_count = df['eventName'].count()
m_users = df['userId'].nunique()
m_monthly_users = df.groupby('month')['userId'].nunique().mean()



# fill in those three columns with respective metrics or KPIs
kpi1.metric(
    label="Avg. Monthly Users ⏳",
    value=round(m_monthly_users),
    delta=round(m_users),
)

kpi2.metric(
    label="Total Users 💍",
    value=int(m_users),
    delta=-10 + m_users,
)

kpi3.metric(
    label="Total Clicks 📈",
    value=round(m_count),
    delta=round(m_count) - 10,
)


# create two columns for charts
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### First Chart")
    fig = px.density_heatmap(
        df, y="screenName", x="context"
    )
    #st.write(fig)
    st.plotly_chart(fig, use_container_width=True)
   
with fig_col2:
    st.markdown("### Second Chart")
    fig2 = px.line(df, x="date", y="operatingSystem", color="operatingSystem")
    st.plotly_chart(fig2, use_container_width=True)
    

# create two columns for charts
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### First Chart")
    fig = px.pie(
        data_frame=df, values='userId', names='operatingSystem'
    )
    st.plotly_chart(fig, use_container_width=True)
   
with fig_col2:
    st.markdown("### Second Chart")
    fig2 = px.histogram(data_frame=df, x="operatingSystem")
    st.plotly_chart(fig2, use_container_width=True)