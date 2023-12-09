import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

day_df = pd.read_csv('./day.csv')
hour_df = pd.read_csv('./hour.csv')

st.set_option('deprecation.showPyplotGlobalUse', False)

day_df['dteday'] = pd.to_datetime(day_df['dteday'])

min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

def count_total_users(df):
    sum_users_df = df.groupby(by="dteday").cnt.sum().sort_values(ascending=False).reset_index()

    return sum_users_df

def count_users_over_seasonss(df):
    count_user_seasonss_df = df.groupby(by="season").cnt.sum().reset_index()

    count_user_seasonss_df['season'].replace({
        1: "Spring",
        2: "Summer",
        3: "Autumn",
        4: "Winter"
    }, inplace=True)

    return count_user_seasonss_df

def count_summer_in_week(df):
    summer_df = df[(df['dteday'].dt.month >= 6) & (df['dteday'].dt.month <= 8)]
    summer_in_mean = summer_df.groupby(summer_df['dteday'].dt.to_period("W-Mon"))["cnt"].mean()

    summer_in_mean_df = summer_in_mean.reset_index()
    summer_in_mean_df.columns = ["Week starting from Monday", "Mean Count"]

    summer_in_mean_df = summer_in_mean_df.sort_values(by="Week starting from Monday")

    return summer_in_mean_df

def count_users_hour(df):
    weekend_data = df[(df['dteday'].dt.day > 5) & (df['dteday'].dt.day <= 7)]
    weekend_bike_user = weekend_data.groupby("hr").cnt.mean().reset_index()

    return weekend_bike_user
    
# def count_summer_in_week():
#     summer_df = day_df[(day_df['dteday'].dt.month >= 6) & (day_df['dteday'].dt.month <= 8)]
#     summer_in_mean = summer_df.groupby(summer_df['dteday'].dt.to_period("W-Mon"))["cnt"].mean()

#     summer_in_mean = summer_in_mean.sort_index()

#     print(summer_in_mean)

# count_summer_in_week()


"""Calling function"""

count_summer_in_week(day_df)
master_day = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]
master_hour = hour_df[(hour_df['dteday'] >= str(start_date)) & (hour_df['dteday'] <= str(end_date))]
master_hour['dteday'] = pd.to_datetime(master_hour['dteday'])

count_total_users = count_total_users(master_day)
count_users_over_seasons = count_users_over_seasonss(master_day)
count_users_in_summer_weekday = count_summer_in_week(master_day)
count_bike_users_hour = count_users_hour(master_hour)

"""Streamlit Dashboard"""

st.header("Bike User Dashboard :smile:")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Dimulai" ,value=f"{start_date}")

with col2:
    st.metric(label="Berakhir", value=f"{end_date}")

with col3:
    total_users = count_total_users.cnt.sum()
    st.metric(label="Users", value=total_users)

st.subheader("Amount of Users based on Season")

total_users_in_season = count_users_over_seasons.cnt.sum()

plt.barh(
    count_users_over_seasons.season,
    count_users_over_seasons.groupby(by="season").cnt.sum(),   
    color="grey"
)

plt.title("Grafik Pengguna Bike Selama 4 Season")
plt.xlabel("Number of users")
plt.ylabel("Season")

st.pyplot()

st.subheader("Average Bike Users in Summer Season in A Week")

fig, ax = plt.subplots(figsize=(20, 16))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    data=count_users_in_summer_weekday,
    x="Week starting from Monday",
    y="Mean Count",
    palette=colors,
    ax=ax   
)

ax.set_title("Average Bike Users in Summer Season Each Week", fontsize=50)
ax.set_xlabel('Week starting from Monday')
ax.set_ylabel('Mean Count')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# print(weekend_bike_user)
st.subheader("Average of Bike User per hour in weekend")

plt.figure(figsize=(12, 5))
plt.plot(
    count_bike_users_hour['hr'],
    count_bike_users_hour['cnt'],
    marker='o',
    linewidth=2,
    color="grey"
)

plt.grid(True)
plt.title("Average Number of Bike Users per Hour on Weekends")
plt.xlabel("Hour of the Day")
plt.ylabel("Average Number of Bike Users")
plt.xticks(count_bike_users_hour['hr'])
st.pyplot()




