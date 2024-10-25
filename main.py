import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Upload CSV file
st.title("Simple Data Filtering App")
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    
    # Let user filter the data
    column_to_filter = st.selectbox('Select column to filter by', df.columns)
    unique_values = df[column_to_filter].unique()
    selected_value = st.selectbox('Select value', unique_values)
    
    # Display filtered data
    filtered_df = df[df[column_to_filter] == selected_value]
    st.write(filtered_df)
    
    # Plot filtered data
    st.subheader(f'Data Distribution by {column_to_filter}')
    fig, ax = plt.subplots()
    filtered_df.hist(ax=ax)
    st.pyplot(fig)