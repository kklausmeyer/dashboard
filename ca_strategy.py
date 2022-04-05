import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import os
from os.path import exists
import plotly.express as px
from datetime import date
from PIL import Image
#date = date.today().strftime("%Y%m%d")
date = '20220331'






outer_dir = os.path.split(os.getcwd())[0]
in_table = os.path.join(os.getcwd(), 'tables', 'CA_strategy_dashboard_metrics_v1.2_Apr_2022.xlsx')
in_points = os.path.join(outer_dir, 'ca_strategy_points_{}.csv'.format(date))

# Read in strategy table
df = pd.read_excel(in_table, sheet_name='CA_strategy_outcomes')
df = df.astype(str)
df = df.replace(['nan'],np.NaN)
df = df.dropna(how='any', thresh=6).reset_index()
df['unique_id'] = df.program + "_" + df.strategy + "_" + df.outcome

# Read in point table
dfp1 = pd.read_csv(in_points)
dfp = pd.merge(dfp1, df, on='unique_id', how='outer')
#dfp['latitude'] = dfp['latitude'].astype(float)
#dfp['longitude'] = dfp['longitude'].astype(float)




def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

# Create a horizontal bar chart
@st.cache
def strategy_chart(unique_id):
    df1 = dfp.loc[dfp.unique_id == unique_id]
    #df1['2025 progress estimate'] = df1['2025 progress estimate'].astype(float)
    fig = px.bar(df1,
                 x="area_acres",
                 y="outcome",
                 #hover_name="name",
                 #hovertext="name",
                 orientation='h',
                 height=40,
                 width=500,
                 )
    fig.update_traces(marker_color='rgb(55,127,49)',
                      marker_line_width=1,
                      marker_line_color='rgb(40,110,30)',
                      width=100,
                      hovertext="name",
                      )
    fig.update_yaxes(ticklabelposition="inside",
                     title=None,
                     tickfont_family="Arial",
                     )
    fig.update_xaxes(range=[0, float(df1.iloc[0]['2030 outcome target'])],
                     title=None,
                     showgrid=False,
                     showticklabels=False,
                     )
    fig.update_layout(plot_bgcolor='rgb(128,123,120)',
                      margin_l = 0,
                      margin_r = 0,
                      margin_t = 10,
                      margin_b = 0,
                      modebar_remove=['zoom', 'pan', 'select', 'autoScale', 'resetScale', 'zoomIn', 'zoomOut','lasso'],
                      #modebar_display=False,
                      )
    annotation = "{} {}".format(human_format(float(df1.iloc[0]['2030 outcome target'])), df1.iloc[0]['units'])
    fig.add_annotation(text=annotation,
                       font = dict(
                           family="Arial",
                           color="#ffffff",
                           ),
                       xref="paper",
                       yref="paper",
                       x=1,
                       y=0.5,
                       showarrow=False,
                       )
    return fig






st.title('California Strategies: 2030 Outcomes')


col1, col2, col3, col4 = st.columns(4)

# Add program and strategy to containers
prev_prog = ""
prev_strat = ""
i = 1
for index, row in df.iterrows():
    prog = row['program']
    strat = row['strategy']
    if prog != prev_prog:
        exec('prog_col = col{}'.format(i))
        i += 1
        with prog_col:
            st.header(prog)
            
    with prog_col:
        
        if strat != prev_strat:
            container = st.container()
            with container:
                img_path = os.path.join(os.getcwd(),'graphics','{}.png'.format(strat))
                if exists(img_path):
                    image = Image.open(img_path)
                    st.image(image, width = 300)
                else:
                    st.subheader(strat)
        with container:
            st.plotly_chart(strategy_chart(row['unique_id']), use_container_width=True)

    prev_prog = prog
    prev_strat = strat
        
st.map(dfp1)
st.dataframe(dfp1)


#st.write(df)

##@st.cache
##def load_data(nrows):
##    data = pd.read_csv(DATA_URL, nrows=nrows)
##    lowercase = lambda x: str(x).lower()
##    data.rename(lowercase, axis='columns', inplace=True)
##    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
##    return data
##
### Create a text element and let the reader know the data is loading
##data_load_state = st.text('Loading data...')
##
### Load 10,000 rows of data into the dataframe
##data= load_data(10000)
##
###Notify the reader that the data was successfully loaded.
##data_load_state.text('Done! (using st.cache)')
##
##if st.checkbox('Show raw data'):
##    st.subheader('Raw data')
##    st.write(data)
##
##st.subheader('Number of pickups by hour')
##hist_values = np.histogram(
##    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
##st.bar_chart(hist_values)
##
##hour_to_filter = st.slider('hour', 0, 23, 17)
##filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
##st.subheader(f'Map of all pickups at {hour_to_filter}:00')
##st.map(filtered_data)


