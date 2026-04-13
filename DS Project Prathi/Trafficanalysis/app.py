import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("🚦 Traffic Flow Analysis Dashboard")

# Load dataset
df = pd.read_csv("traffic.csv")

# Convert datetime
df['date_time'] = pd.to_datetime(df['date_time'])

# Feature Engineering
df['Hour'] = df['date_time'].dt.hour
df['Day'] = df['date_time'].dt.day_name()

# Sidebar filters
st.sidebar.header("Filter Data")

selected_day = st.sidebar.multiselect(
    "Select Day",
    options=df['Day'].unique(),
    default=df['Day'].unique()
)

selected_weather = st.sidebar.multiselect(
    "Select Weather",
    options=df['weather_type'].unique(),
    default=df['weather_type'].unique()
)

# Apply filters
filtered_df = df[
    (df['Day'].isin(selected_day)) &
    (df['weather_type'].isin(selected_weather))
]

# Show data
st.subheader("Dataset Preview")
st.write(filtered_df.head())

# ---- Graph 1: Traffic by Hour ----
st.subheader("⏰ Traffic by Hour")

traffic_hour = filtered_df.groupby('Hour')['traffic_volume'].mean()

fig1, ax1 = plt.subplots()
traffic_hour.plot(kind='bar', ax=ax1)
ax1.set_title("Average Traffic by Hour")
ax1.set_xlabel("Hour")
ax1.set_ylabel("Traffic Volume")
st.pyplot(fig1)

# ---- Graph 2: Traffic vs Weather ----
st.subheader("🌦️ Traffic vs Weather")

fig2, ax2 = plt.subplots()
sns.boxplot(x='weather_type', y='traffic_volume', data=filtered_df, ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)

# ---- Graph 3: Day-wise Traffic ----
st.subheader("📅 Traffic by Day")

fig3, ax3 = plt.subplots()
sns.barplot(x='Day', y='traffic_volume', data=filtered_df, ax=ax3)
plt.xticks(rotation=45)
st.pyplot(fig3)

# ---- Graph 4: Correlation ----
st.subheader("🔥 Correlation Heatmap")

fig4, ax4 = plt.subplots()
sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, ax=ax4)
st.pyplot(fig4)