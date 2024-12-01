import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import io
sns.set(style='dark')

# Main Header
st.header("🚴 Bike Sharing Data Analysis Dashboard")

# Create daily bike count DataFrame
def create_daily_bike_count_data(data):
    daily_bike_count_data = data.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    })
    daily_bike_count_data = daily_bike_count_data.reset_index()
    daily_bike_count_data.rename(columns={
        "cnt": "total_bike_count",
        "casual": "casual_bike_count",
        "registered": "registered_bike_count"
    }, inplace=True)
    
    return daily_bike_count_data

# Create bike count by weather type DataFrame
def create_bike_count_by_weather_data(data):
    bike_count_by_weather_data = data.groupby("weather")["cnt"].sum().reset_index()
    bike_count_by_weather_data.rename(columns={
        "cnt": "total_bike_count"
    }, inplace=True)
    
    return bike_count_by_weather_data

# Create bike count by hour DataFrame
def create_bike_count_by_hour_data(data):
    bike_count_by_hour_data = data.groupby("hr")["cnt"].sum().reset_index()
    bike_count_by_hour_data.rename(columns={
        "cnt": "total_bike_count"
    }, inplace=True)
    
    return bike_count_by_hour_data

# Create bike count by season DataFrame
def create_bike_count_by_season_data(data):
    bike_count_by_season_data = data.groupby("season")["cnt"].sum().reset_index()
    bike_count_by_season_data.rename(columns={
        "cnt": "total_bike_count"
    }, inplace=True)
    
    return bike_count_by_season_data

def create_bike_count_by_weather_season_data(data):
    # Mapping of season numbers to weather types
    season_to_weather = {
        1: 'Clear/Few Clouds',  # Example mapping
        2: 'Mist/Cloudy',
        3: 'Rain/Snow',
        4: 'Thunderstorm'
    }
    
    # Replace season numbers with weather descriptions
    data['weather'] = data['season'].map(season_to_weather)
    
    # Group by the new 'weather' column and aggregate the bike counts
    bike_count_by_weather_season_data = data.groupby("weather")["cnt"].sum().reset_index()
    bike_count_by_weather_season_data.rename(columns={
        "cnt": "total_bike_count"
    }, inplace=True)
    
    return bike_count_by_weather_season_data

# Create bike count by month DataFrame
def create_bike_count_by_month_data(data):
    bike_count_by_month_data = data.groupby("mnth")["cnt"].sum().reset_index()
    bike_count_by_month_data.rename(columns={
        "cnt": "total_bike_count"
    }, inplace=True)
    
    return bike_count_by_month_data



# Load Data
data = pd.read_csv("merged_data.csv")

# Convert datetime columns
data['dteday'] = pd.to_datetime(data['dteday'])

# Filter Data for selected time period
min_date = data['dteday'].min()
max_date = data['dteday'].max()


with st.sidebar:
   
    # Sidebar for user interaction

    st.title("Last Project - Simião S.")
    st.title("📊 Dashboard Options")
    # st.sidebar.title("")
    st.header("Bike Sharing Data Analysis")
  

    #  Date range filter
    st.header("Filter Data by Date")
    min_date = data['dteday'].min()
    max_date = data['dteday'].max()

    start_date, end_date = st.date_input(
        label = "Select Date Range",
        min_value = min_date,
        max_value = max_date, 
        value=[min_date, max_date])
    
    # Filter data based on selected dates
    filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]


# Show basic information about the dataset
if st.sidebar.checkbox("Show Dataset Information"):
    st.subheader("Dataset Information")
    st.markdown("""
        **Bike sharing systems** are part of the modern transportation infrastructure. 
        These systems allow users to rent and return bikes at various locations, making urban mobility more flexible and sustainable. 
        With over 500 bike-sharing programs around the world, these systems have been pivotal in addressing traffic, environmental, and health challenges. 
        This dashboard provides insights into bike rental patterns, weather conditions, and other key factors influencing bike sharing.
    """)
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





# Filter Data based on selected date range
main_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]

# Prepare various DataFrames
daily_bike_count_data = create_daily_bike_count_data(main_data)
bike_count_by_weather_data = create_bike_count_by_weather_data(main_data)
bike_count_by_hour_data = create_bike_count_by_hour_data(main_data)
bike_count_by_season_data = create_bike_count_by_season_data(main_data)
bike_count_by_month_data = create_bike_count_by_month_data(main_data)
bike_count_by_weather_season_data = create_bike_count_by_weather_season_data(main_data)


# Visualize Daily Bike Counts
st.subheader(f"📈 Analysis for Selected Dates: {start_date} to {end_date}")
st.subheader('Daily Bike Counts')
col1, col2 = st.columns(2)

with col1:
    total_bikes = daily_bike_count_data.total_bike_count.sum()
    st.metric("Total Bikes Rented", value=total_bikes)

with col2:
    total_registered_bikes = daily_bike_count_data.registered_bike_count.sum()
    st.metric("Total Registered Bikes", value=total_registered_bikes)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_bike_count_data["dteday"],
    daily_bike_count_data["total_bike_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Visualize Bike Counts by Weather Type
st.subheader("Bike Count by Weather")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="total_bike_count", y="weather", data=bike_count_by_weather_data, palette="coolwarm", ax=ax)
ax.set_title("Total Bike Count by Weather", fontsize=18)
st.pyplot(fig)

# Visualize Bike Counts by Hour
st.subheader("Bike Count by Hour")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x="hr", y="total_bike_count", data=bike_count_by_hour_data, marker='o', color="b", ax=ax)
ax.set_title("Bike Count by Hour", fontsize=18)
st.pyplot(fig)

# Visualize Bike Counts by Season
st.subheader("Bike Count by Season")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="weather", y="total_bike_count", data=bike_count_by_weather_season_data, palette="viridis", ax=ax)
ax.set_title("Total Bike Count by Season", fontsize=18)
st.pyplot(fig)

# Visualize Bike Counts by Month
st.subheader("Bike Count by Month")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="mnth", y="total_bike_count", data=bike_count_by_month_data, palette="Blues", ax=ax)
ax.set_title("Total Bike Count by Month", fontsize=18)
st.pyplot(fig)

# Caption for the app
st.caption('Copyright (c) S.Salvador 2024')