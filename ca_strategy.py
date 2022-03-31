import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import os
import plotly.express as px

st.title('California Strategies: 2030 Outcomes')
col1, col2 = st.columns([2,2])

outer_dir = os.path.split(os.getcwd())[0]
in_table = os.path.join(outer_dir, 'CA_strategy_dashboard_metrics_v1.2_Apr_2022.xlsx')
df = pd.read_excel(in_table, sheet_name='CA_strategy_outcomes')
df = df.astype(str)
df = df.replace(['nan'],np.NaN)
df = df.dropna(how='any', thresh=6).reset_index()
df['unique_id'] = df.program + "_" + df.strategy + "_" + df.outcome

with col2:
    st.map()
    st.dataframe(df)

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

# Create a horizontal bar chart
def strategy_chart(unique_id):
    df1 = df.loc[df.unique_id == unique_id]
    df1['2025 progress estimate'] = df1['2025 progress estimate'].astype(float)
    fig = px.bar(df1, x="2025 progress estimate", y="outcome", orientation='h', height=40, width=500)
    fig.update_traces(marker_color='rgb(55,127,49)',
                      marker_line_width=0,
                      width=100,
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




unique_ids = df.unique_id.unique().tolist()
with col1:

    # Add program and strategy to containers
    prev_prog = ""
    prev_strat = ""
    for index, row in df.iterrows():
        prog = row['program']
        strat = row['strategy']
        if prog != prev_prog:
            prog_cont = st.container()
            with prog_cont:
                st.header(prog)
        with prog_cont:
            if strat != prev_strat:
                container = st.container()
                with container:
                    st.subheader(strat)
            with container:
                st.plotly_chart(strategy_chart(row['unique_id']), use_container_width=True)

        prev_prog = prog
        prev_strat = strat
        



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


