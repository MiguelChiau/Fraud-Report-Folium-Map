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
    st_map = st_folium(map, width=700, height=450)

    st.write(df.shape)
    st.write(df.head())
    st.write(df.columns)


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
