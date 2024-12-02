import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
# from babel.numbers import format_currency
import io, calendar
import os
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
    # Mapping Weather Description
    weather_desc = {
        1: 'Clear/Few Clouds',  
        2: 'Mist/Cloudy',
        3: 'Rain/Snow',
        4: 'Thunderstorm'
    }
    # Replace Weather  numbers with weather descriptions
    data['weathersit'] = data['weathersit'].map( weather_desc)

    bike_count_by_weather_data = data.groupby("weathersit")["cnt"].sum().reset_index()
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

def create_bike_count_by_season_data(data):
    # Mapping of season numbers to weather types
    season_name = {
        1: 'Springer',  # Example mapping
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    }
    
    # Replace season numbers with weather descriptions
    data['season'] = data['season'].map(season_name)
    
    # Group by the new 'weather' column and aggregate the bike counts
    bike_count_by_season_data = data.groupby("season")["cnt"].sum().reset_index()
    bike_count_by_season_data.rename(columns={
        "cnt": "total_bike_count"
    }, inplace=True)
    
    return bike_count_by_season_data

# Create bike count by month DataFrame
def create_bike_count_by_month_data(data):
    
    bike_count_by_month_data = data.groupby("mnth")["cnt"].sum().reset_index()
    # Map month numbers to month names
    month_mapping = {
        1: "January", 2: "February", 3: "March", 4: "April", 
        5: "May", 6: "June", 7: "July", 8: "August", 
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    bike_count_by_month_data["mnth"] = bike_count_by_month_data["mnth"].map(month_mapping)
    # bike_count_by_month_data["mnth"] = bike_count_by_month_data["mnth"].apply(lambda x: calendar.month_name[x])

    bike_count_by_month_data.rename(columns={
        "cnt": "total_bike_count"
    }, inplace=True)
    
    return bike_count_by_month_data



# Load Data
absolute_path = os.path.join(os.getcwd(), "merged_data.csv")
data = pd.read_csv(absolute_path)

# Convert datetime columns
data['dteday'] = pd.to_datetime(data['dteday'])

# Filter Data for selected time period
min_date = data['dteday'].min()
max_date = data['dteday'].max()


with st.sidebar:
   
    # Sidebar for user interaction

    st.title(" Simião S.")
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
# bike_count_by_weather_season_data = create_bike_count_by_weather_season_data(main_data)


# Visualize Daily Bike Counts
# st.subheader(f"📈 Analysis for Selected Dates: {start_date} to {end_date}")
# Format the dates to "Day Month Year" format
formatted_start_date = start_date.strftime("%d %B %Y")
formatted_end_date = end_date.strftime("%d %B %Y")


st.subheader('Daily Bike Counts')
# Update the subheader with the formatted dates
st.write(f"📈 Analysis for Selected Dates: {formatted_start_date} to {formatted_end_date}")
col1, col2 = st.columns(2)

with col1:
    total_bikes = daily_bike_count_data.total_bike_count.sum()
    formatted_total_bikes = f"{total_bikes:,}"
    st.metric("Total Bikes Rented", value=formatted_total_bikes)

with col2:
    total_registered_bikes = daily_bike_count_data.registered_bike_count.sum()
    formated_total_registered_bikes = f"{total_registered_bikes:,}"
    st.metric("Total Registered Bikes", value=formated_total_registered_bikes)

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
sns.barplot(x="total_bike_count", y="weathersit", data=bike_count_by_weather_data, palette="coolwarm", ax=ax)

ax.set_xlabel("Total Bikes", fontsize=12)
ax.set_ylabel("Weather", fontsize=12)
ax.set_title("Total Bike Count by Weather", fontsize=18)
st.pyplot(fig)

# Visualize Bike Counts by Hour
st.subheader("Bike Count by Hour")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x="hr", y="total_bike_count", data=bike_count_by_hour_data, marker='o', color="b", ax=ax)

ax.set_xlabel("Hour", fontsize=12)
ax.set_ylabel("Total Bikes", fontsize=12)
ax.set_title("Bike Count by Hour", fontsize=18)
st.pyplot(fig)

# Visualize Bike Counts by Season
st.subheader("Bike Count by Season")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="season", y="total_bike_count", data=bike_count_by_season_data, palette="viridis", ax=ax)

# Update axis labels and title
ax.set_xlabel("Season", fontsize=12)
ax.set_ylabel("Total Bikes", fontsize=12)
ax.set_title("Total Bike Count by Season", fontsize=18)
st.pyplot(fig)


# Visualize Bike Counts by Month
st.subheader("Bike Count by Month")
# fig, ax = plt.subplots(figsize=(10, 6))
# sns.barplot(x="mnth", y="total_bike_count", data=bike_count_by_month_data, palette="Blues", ax=ax)
# ax.set_title("Total Bike Count by Month", fontsize=18)
# st.pyplot(fig)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="mnth", 
    y="total_bike_count", 
    data=bike_count_by_month_data, 
    palette="Blues", 
    ax=ax
)

# Update axis labels and title
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Total Bikes", fontsize=12)
ax.set_title("Total Bike Count by Month", fontsize=18)

# Adjust tick labels for better readability
ax.tick_params(axis='x', labelsize=9)
ax.tick_params(axis='y', labelsize=9)

st.pyplot(fig)


# Caption for the app
st.caption('Copyright (c) S.Salvador 2024')