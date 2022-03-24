import streamlit as st
import pandas as pd
import numpy as np
import ulmo
from ulmo import cdec

st.title('Mill Creek Flows')

sensor = 'MCH' # Mill Creek below highway 99


@st.cache
def load_data(start_date, end_date):
    data_url = ('https://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations=MCH&SensorNums=20&dur_code=H&Start={}&End={}'.format(start_date, end_date))
    df = pd.read_csv(data_url)
    #df = ulmo.cdec.historical.get_data(station_ids=[sensor], sensor_ids=[20], start=start_date, end=end_date)
    #df = df[sensor]['FLOW']
    #df.columns = map(str.upper, df.columns)
    df["VALUE"] = df["VALUE"].replace(['---','BRT','ART','-1', 'nan'],np.NaN)
    df[['VALUE']] = df[['VALUE']].apply(pd.to_numeric)
    df['DATE TIME'] = pd.to_datetime(df['DATE TIME'])
    df = df.set_index('DATE TIME')
    return df

# Create a text element and let the reader know the data is loading
data_load_state = st.text('Loading data...')

# Load 10,000 rows of data into the dataframe
data= load_data('2019-01-01', '2022-03-23')

#Notify the reader that the data was successfully loaded.
data_load_state.text('Done! (using st.cache)')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Hydrograph')
st.line_chart(data[['VALUE']])

##st.subheader('Number of pickups by hour')
##hist_values = np.histogram(
##    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
##st.bar_chart(hist_values)
##
##hour_to_filter = st.slider('hour', 0, 23, 17)
##filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
##st.subheader(f'Map of all pickups at {hour_to_filter}:00')
##st.map(filtered_data)


