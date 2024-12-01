import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime 
# import date_input
import io

# Header of Dashboard
st.header('Dashboard for  Bike Sharing Data Analysis :sparkles:')

# Load the dataset
url = "combined_dataset_dayhour.csv"  
data = pd.read_csv(url)


with st.sidebar: 
    # Sidebar for user interaction

    st.title("Last Project - Simião S.")
    # st.sidebar.title("")
    st.header("Bike Sharing Data Analysis")
    st.markdown("""
        **Bike sharing systems** are part of the modern transportation infrastructure. 
        These systems allow users to rent and return bikes at various locations, making urban mobility more flexible and sustainable. 
        With over 500 bike-sharing programs around the world, these systems have been pivotal in addressing traffic, environmental, and health challenges. 
        This dashboard provides insights into bike rental patterns, weather conditions, and other key factors influencing bike sharing.
    """)


    # Show basic information about the dataset
if st.sidebar.checkbox("Show Dataset Information"):
    st.subheader("Dataset Information")
    st.write("""
        This dataset represents bike-sharing data collected from a bike-sharing system. 
        The dataset includes information about rentals, weather conditions, and time-related factors.
        - **`season`**: Season (1: Spring, 2: Summer, 3: Fall, 4: Winter)
        - **`yr`**: Year (0: 2011, 1: 2012)
        - **`mnth`**: Month (1 to 12)
        - **`hr`**: Hour (0 to 23) [Available in hourly dataset]
        - **`holiday`**: Whether the day is a holiday
        - **`weekday`**: Day of the week
        - **`workingday`**: If the day is a working day
        - **`weathersit`**: Weather situation (1 to 4)
        - **`temp`**: Normalized temperature in Celsius
        - **`atemp`**: Normalized feeling temperature in Celsius
        - **`hum`**: Normalized humidity
        - **`windspeed`**: Normalized wind speed
        - **`casual`**: Count of casual users
        - **`registered`**: Count of registered users
        - **`cnt`**: Total count of rental bikes (casual + registered)
    """)

    # st.write(data.info())
    # Capture the output of data.info() into a string
    st.subheader("Dataset Info")
    buffer = io.StringIO()
    data.info(buf=buffer)
    s = buffer.getvalue()

    # Display the captured output in Streamlit
    # st.subheader("Dataset Information")
    st.text(s)  # Use st.text() to display the info output

    
    st.subheader("Dataset Head")
    st.write(data.head())
    st.subheader("Dataset Description")
    st.write(data.describe())



# Plot Temperature vs Total Bike Rentals
st.subheader("Temperature vs Total Bike Rentals")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='temp', y='cnt', data=data, ax=ax)
ax.set_title('Temperature vs Total Bike Rentals')
ax.set_xlabel('Normalized Temperature')
ax.set_ylabel('Total Bike Rentals')
st.pyplot(fig)

# Plot Bike Rentals by Hour of the Day
st.subheader("Bike Rentals by Hour of the Day")
data['hour'] = pd.to_datetime(data['dteday']).dt.hour  # Extract the hour from the datetime column
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='hour', y='cnt', data=data, ax=ax)
ax.set_title('Bike Rentals by Hour')
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Total Bike Rentals')
st.pyplot(fig)

# Weather Effects on Bike Rentals
st.subheader("Effect of Weather on Bike Rentals")
weather_mapping = {1: 'Clear/Few Clouds', 2: 'Mist/Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
data['weather'] = data['weathersit'].map(weather_mapping)

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='weather', y='cnt', data=data, ax=ax)
ax.set_title('Effect of Weather on Bike Rentals')
ax.set_xlabel('Weather Situation')
ax.set_ylabel('Total Bike Rentals')
st.pyplot(fig)

# Bike Rentals by Season
st.subheader("Bike Rentals by Season")
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
data['season_name'] = data['season'].map(season_mapping)

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='season_name', y='cnt', data=data, ax=ax)
ax.set_title('Bike Rentals by Season')
ax.set_xlabel('Season')
ax.set_ylabel('Total Bike Rentals')
st.pyplot(fig)

# Alternative RFM-like Analysis: Frequency by Weather, Season, and Hour
st.subheader("Rental Frequency Analysis by Weather, Season, and Hour")

# Frequency analysis by weather situation
weather_frequency = data.groupby('weather')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weather', y='cnt', data=weather_frequency, ax=ax)
ax.set_title('Rental Frequency by Weather Situation')
ax.set_xlabel('Weather Situation')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)

# Frequency analysis by season
season_frequency = data.groupby('season_name')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season_name', y='cnt', data=season_frequency, ax=ax)
ax.set_title('Rental Frequency by Season')
ax.set_xlabel('Season')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)

# Frequency analysis by hour
hour_frequency = data.groupby('hour')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='hour', y='cnt', data=hour_frequency, ax=ax)
ax.set_title('Rental Frequency by Hour')
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)


st.caption('Copyright (c) S.Salvador 2024')