import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    cities = ["chicago", "new york city", "washington"]
    while True:
        city = input(
            "Please enter the city (chicago, new york city, washington): ").lower()

        if city in cities:
            break

    # get user input for month (all, january, february, ... , june)
    months = ["januray", "february", "march", "april", "may", "june"]

    while True:
        month = input(
            "Please enter a specific month (januray, february, march, april, may, june) or all if you don't want to filter the months: ").lower()
        if month in months:
            break
        if month == "all":
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["saturday", "sunday", "monday",
            "tuesday", "wednesday", "thursday", "friday"]

    while True:
        day = input(
            "Please enter a specific day or all if you don't want to filter the days: ").lower()
        if day in days:
            break
        if day == "all":
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()

    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hours'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month.capitalize())
        # filter by month to create the new dataframe
        df = df[df['month'] == months[month]]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month = df['month'].value_counts().idxmax()
    print('The most common month is: \n', month)

    # TO DO: display the most common day of week
    day = df['day_of_week'].value_counts().idxmax()
    print('The most common day is: \n', day)

    # TO DO: display the most common start hour
    hour = df['hours'].value_counts().idxmax()
    print('The most common hour is: \n', hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print('The most common used start station: \n', start_station)

    # TO DO: display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print('The most common used end station: \n', end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['combination of start and end station'] = df['Start Station'] + \
        [' and ']+df['End Station']
    comb = df['combination of start and end station'].value_counts().idxmax()
    print('frequent combination of start station and end station trip: \n', comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_time = df.groupby(['User Type'])['Trip Duration'].sum()
    print('The total time spent: \n', travel_time)

    # TO DO: display mean travel time

    travel_mean = df.groupby(['User Type'])['Trip Duration'].mean()
    print('The mean travel time:\n', travel_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # ATTENTION HEERREE DONT FORGET TO CHECK THIS FUNCTION WITH A !!!!!!!!


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    Users = df['User Type'].value_counts()
    print('User types are: \n', Users)

    # TO DO: Display counts of gender
    Gender = df['Gender'].value_counts()
    print('Genders are: \n', Gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    print("\nThe most recent:{} \nThe earlist:{} \nThe most common: {} ".format(
        df['Birth Year'].max(), df['Birth Year'].min(), df['Birth Year'].value_counts().idxmax()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        view_data = input(
            '\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').lower()
        start_loc = 0
        while (view_data == "yes"):
            print(df.iloc[0:5])
            start_loc += 5
            view_display = input('\nDo you wish to conyinue?: ').lower()

            if(view_display == "no"):
                break
            else:
                continue

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
