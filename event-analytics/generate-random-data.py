import pandas as pd
import numpy as np
import datetime


####################
# Make Dummy Data
####################


events = pd.read_csv('./data/single_events.csv')

# sample
event_df = pd.concat([events, events.sample(n=1000, replace=True)]).reset_index()

# generate full month dates
test_date = datetime.datetime.strptime("01-8-2022", "%d-%m-%Y")
date_generated = pd.date_range(test_date, periods=31)

# create dummy df
build_df = pd.DataFrame({
    'userId':np.random.randint(1000, 9999, size=1050).astype(str),
    'sessionId':np.random.randint(11111111111, 111111111111, size=1050).astype(str),
    'date':np.random.choice(date_generated.strftime("%d-%m-%Y"), 1050),
    'operatingSystem':np.random.choice(['Android', 'iOS'], 1050),
}).reset_index()

# concat df's
df = pd.concat((event_df, build_df), axis=1)
df = df.drop('index', axis=1) 

df.to_csv('./data/dummy_data.csv', index=False)