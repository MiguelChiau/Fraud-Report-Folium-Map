import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


APP_TITLE = 'Fraud and Identity Theft Report'
APP_SUB_TITTLE = 'Source: Federal Trade Comission'


def display_fraud_facts(df, year, quarter, state_name, report_type, field_name, metric_title, number_format='${:,}', is_median=False):
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)
            & (df['Report Type'] == report_type)]
    if state_name:
        df = df[(df['State Name'] == state_name)]
    # dropping duplicate values
    df.drop_duplicates(inplace=True)

    if is_median:
        total = df[field_name].sum() / len(df) if len(df) else 0
    else:
        total = df[field_name].sum()
    # when no state is selected display the sum of frauds in all states
    # total = df[field_name].sum()
    st.metric(metric_title, number_format.format(round(total)))


def display_map(df, year, quarter):
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]

    map = folium.Map(location=[38, -96.5], zoom_start=4,
                     scrollWheelZoom=False, tiles='CartoDB positron')

# Highlighting the borders around the US map and styling the map
    choropleth = folium.Choropleth(
        geo_data='data/us-state-boundaries.geojson',
        data=df,
        columns=['State Name', 'State Total Reports Quarter'],
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)

    df = df.set_index('State Name')
    state_name = 'North Carolina'
    # st.write(df.loc[state_name, 'State Pop'][0])


# To access the population the state details on highlight
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name']
        feature['properties']['population'] = 'Population: ' + str('{:,}'.format(df.loc[state_name, 'State Pop'][0])
                                                                   if state_name in list(df.index) else 'N/A')
        feature['properties']['per_100k'] = 'Reports/100K Population: ' + str('{:,}'.format(round(df.loc[state_name, 'Reports per 100K-F&O together'][0]))
                                                                              if state_name in list(df.index) else 'N/A')

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            ['name', 'population', 'per_100k'], labels=False)
    )

    # Displaying the map on streamlit
    st_map = st_folium(map, width=700, height=450)


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITTLE)

    # LOADING THE DATASET
    df_continental = pd.read_csv('data/AxS-Continental_Full Data_data.csv')
    df_fraud = pd.read_csv('data/AxS-Fraud Box_Full Data_data.csv')
    df_median = pd.read_csv('data/AxS-Median Box_Full Data_data.csv')
    df_loss = pd.read_csv('data/AxS-Losses Box_Full Data_data.csv')

    year = 2022
    quarter = 1
    state_name = ''
    report_type = 'Fraud'

    # Display filters and Map
    display_map(df_continental, year, quarter)

    # Display Metrics
    st.subheader(f'{state_name}{report_type} Facts')
    col1, col2, col3 = st.columns(3)
    with col1:
        display_fraud_facts(df_fraud, year, quarter, state_name,
                            report_type, 'State Fraud/Other Count', f'\# of {report_type} Reports', number_format='{:,}')

    with col2:
        display_fraud_facts(df_median, year, quarter, state_name,
                            report_type, 'Overall Median Losses Qtr', 'Median $ Loss', is_median=True)
    with col3:
        display_fraud_facts(df_loss, year, quarter, state_name,
                            report_type, 'Total Losses', 'Total $ Loss')


if __name__ == '__main__':
    main()
