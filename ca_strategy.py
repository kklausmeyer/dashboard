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






table_dir = os.path.join(os.getcwd(), 'tables')
in_table = os.path.join(table_dir, 'CA_strategy_dashboard_metrics_v1.2_Apr_2022.xlsx')
in_points = os.path.join(table_dir, 'ca_strategy_points_{}.csv'.format(date))

# Read in strategy table
df = pd.read_excel(in_table, sheet_name='CA_strategy_outcomes')
df = df.astype(str)
df = df.replace(['nan'],np.NaN)
df = df.dropna(how='any', thresh=6).reset_index()
df['unique_id'] = df.program + "_" + df.strategy + "_" + df.outcome

# Read in point table
dfp1 = pd.read_csv(in_points)
dfp = pd.merge(dfp1, df, on='unique_id', how='outer')
dfp.loc[dfp['name'].isna(), 'name'] = " "
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
                 hover_data={'outcome':False,
                             'area_acres':':,.0f',
                             },
                 
                 orientation='h',
                 height=40,
                 width=500,
                 color='name',
                 #color_discrete_sequence=px.colors.qualitative.Dark2,
                 color_discrete_sequence=["olive", 'green', 'darkolivegreen', 'forestgreen', 'yellowgreen', 'olivedrab'],
                 )
    fig.update_traces(#marker_color='rgb(55,127,49)',
                      marker_line_width=0,
                      marker_line_color='rgb(40,110,30)',
                      width=100,
                      #hovertext="name",
                      #hovertemplate = '%{y}, %{x:.0f} acres',
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
                      modebar_remove=['zoom', 'pan', 'select', 'autoScale', 'resetScale', 'zoomIn', 'zoomOut','lasso', 'toImage'],
                      #modebar_display=False,
                      showlegend=False,
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
        

#px.set_mapbox_access_token(open(".mapbox_token").read())
dfm = dfp.dropna(subset=['area_acres'])
fig_map = px.scatter_mapbox(dfm,
                         title="Initial map of locations",
                            lat="latitude",
                            lon="longitude",
                            color="strategy",
                            size="area_acres",
                            hover_name="name",
                            color_discrete_sequence=["green"],
                            hover_data={'latitude':False,
                                        'longitude':False,
                                        'program':True,
                                        'outcome':True,
                                        
                                        'area_acres':':,.0f',
                             },
                         width=1000,
                         height=1000,
                            #color_continuous_scale=px.colors.cyclical.IceFire,
                            #size_max=15,
                            zoom=5,
                            )
fig_map.update_layout(mapbox_style="open-street-map")
#fig_map.update_geos(fitbounds="locations")

st.plotly_chart(fig_map)
#st.map(dfp1)
#st.dataframe(dfp)


