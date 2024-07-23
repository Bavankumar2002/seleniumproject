import streamlit as st
import pandas as pd
import sqlite3

st.title("Bus Route Information")

# Connect to the SQLite database
conn = sqlite3.connect('test1.db')
cursor = conn.cursor()

# Read data from the database
data = pd.read_sql_query("SELECT * FROM data_bus", conn)

# Display the data in a table
#st.dataframe(data)

# Seat type selection
seat_type = st.selectbox("Select the Seat Type", data['bus_type'].unique())

# star rating selection
star_ratings = st.selectbox("Select the Ratings", data['star_rating'].unique())

# Allow users to filter the data based on the bus name
selected_route = st.selectbox("Select a Route", data['route_name'].unique())

# Filter the data based on the selected bus and other criteria
filtered_data = data[(data['route_name'] == selected_route) &
                     (data['bus_type'] == seat_type) ]

# Display the filtered data in a table
st.dataframe(filtered_data)

# Close the database connection
conn.close()