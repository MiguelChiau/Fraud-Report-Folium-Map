import streamlit as st
import pandas as pd

APP_TITLE = 'Fraud and Identity Theft Report'
APP_SUB_TITTLE = 'Source: Federal Trade Comission'


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITTLE)

    # Load the Dataset
    df = pd.read_csv('data/AxS-Fraud Box_Full Data_data.csv')

    year = 2022
    quarter = 1
    state_name = 'Texas'
    report_type = 'Fraud'
    field_name = 'State Fraud/Other Count'
    metric_title = f'\# of {report_type} Reports'

    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)
            & (df['Report Type'] == report_type)]
    if state_name:
        df = df[(df['State Name'] == state_name)]
    # dropping duplicate values
    df.drop_duplicates(inplace=True)

    # when no state is selected display the sum of frauds in all states
    total = df[field_name].sum()
    st.metric(metric_title, total)

    st.write(df.shape)
    st.write(df.head())
    st.write(df.columns)

    # Display filters and Map

    # Display Metrics


if __name__ == '__main__':
    main()
