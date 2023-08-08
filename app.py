import streamlit as st
import pandas as pd
import plotly.express as px
import json


APP_TITLE = 'Electricity Generation in Canada'
APP_SUB_TITLE = 'Source: Stats Canada'

def display_map(df, year,prov):
    #st.write(df)
    df = df.groupby(['GEO'])['VALUE'].sum().reset_index()
    with open('./Canada_ShapeFile.geojson', 'r') as geo:
        mp = json.load(geo)

    fig = px.choropleth_mapbox(data_frame=df, geojson=mp, featureidkey="properties.prov_name_en",
                        locations='GEO', color='VALUE',
                        color_continuous_scale="Viridis",
                        #range_color=(0, 14223942),
                        mapbox_style = 'open-street-map',
                        center=dict(lat=59.959354, lon=-101.990312),
                        zoom=2.55,opacity=0.5,width=1000, height=500
                        #colorbar={"orientation": "h", "x": 0.5, "yanchor": "middle", "y": 0.1}
                    )


    #fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    coloraxis_colorbar=dict(
                    x=0.01,  # Adjust the x-coordinate (0.0 to 1.0) for horizontal position
                    y=0.5,  # Adjust the y-coordinate (0.0 to 1.0) for vertical position
                    len=0.7,  # Adjust the length of the color bar
                    )
                )

    #fig.show()
    st.plotly_chart(fig,use_container_width=False)

def display_treemap(df):
    df = df.groupby(['Type of electricity generation'])['VALUE'].sum().reset_index()
    fig = px.treemap(df, 
                 names='Type of electricity generation', 
                 parents=['']*(df.shape[0]), 
                 values='VALUE',width=1000, height=500)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig,use_container_width=False)


def main():
    st.set_page_config(layout="wide",page_title=APP_TITLE)
    #st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    df = pd.read_csv('./Canada-Energy-2016_onwards.csv')

    #st.write(df.shape)
    #st.write(df.head())
    #st.write(df.columns)

    #year = 2022

    year_list = list(df['year'].unique())
    year_list.sort(reverse=True)

    prov_list =  list(df['GEO'].unique())
    prov_list.sort()
    prov_list = ['All'] + prov_list

    year = st.sidebar.selectbox('Year',year_list)
    prov = st.sidebar.selectbox('Provience',prov_list)

    df=df[df['year']==year]
    if prov in df['GEO'].unique():
        df=df[df['GEO']==prov]

    display_map(df, year, prov)
    display_treemap(df)

if __name__ == '__main__':
    main()