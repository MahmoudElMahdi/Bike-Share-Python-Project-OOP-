import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
cities = ["new york city", "chicago", "washington"]
months = ["january", "february", "march", "april", "may", "june", "all"]
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]

print('Hello! Let\'s explore some US bike share data!\n')


def ask_user_selection(options, prompt_message):
    answer = ""
    while len(answer) == 0:
        answer = input(prompt_message)
        answer = answer.strip().lower()

        if answer in options:
            return answer
        else:
            answer = ""
            print("Please enter one of the offered options.\n")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ask_user_selection(
        cities,
        "Please enter: 'new york city', 'chicago' or 'washington' > ")

    # get user input for month (all, january, february, ... , june)
    month = ask_user_selection(
        months,
        "Please enter month: 'january', 'february', 'march', 'april', 'may', 'june' or 'all' > ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ask_user_selection(
        days,
        "Please enter day: 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' or 'all' > ")

    print('-' * 40)
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
    # loading the data file into a dataframe
    df = pd.read_csv(CITY_DATA[city], index_col=0)
    df['Start Time'] = pd.to_datetime(df['Start Time'])  # Casting "Start Time" to datetime.
    df["month"] = df['Start Time'].dt.month  # Get the weekday out of the "Start Time" value.
    df["week_day"] = df['Start Time'].dt.day_name()  # Month-part from "Start Time" value.
    df["start_hour"] = df['Start Time'].dt.hour  # Hour-part from "Start Time" value. 
    df["start_end"] = df['Start Station'].astype(str) + ' to ' + df['End Station']

    if month != 'all':
        month_index = months.index(month) + 1  # Get the list-index of the month.
        df = df[df["month"] == month_index]  # Establish a filter for month.

    if day != 'all':
        df = df[df["week_day"] == day.title()]  # Establish a filter for week day.

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_index = df["month"].mode()[0] - 1
    most_common_month = months[month_index].title()

    print("Most common month: ", most_common_month)

    # display the most common day of week
    most_common_day = df["week_day"].mode()[0]
    print("Most common day: ", most_common_day)

    # display the most common start hour
    most_common_hour = df["start_hour"].mode()[0]
    print("Most common hour: ", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_used_start = df['Start Station'].mode()[0]
    print("Most used start: ", most_used_start)

    # display most commonly used end station
    most_used_end = df['End Station'].mode()[0]
    print("Most used end: ", most_used_end)

    # display most frequent combination of start station and end station trip
    most_common_combination = df["start_end"].mode()[0]
    print("Most common used combination concerning start- and end-station: ",
          most_common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    # resubmission part --  display raw data taken from the csv file
    x = 1
    while True:
        raw = input('\nWould you like to see some raw data? Enter yes or no.\n')
        if raw.lower() == 'yes':
            print(df[x:x + 5])
            x += 5
            print('If you do not like to see some raw data again Enter no...')
        else:
            break


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total time of travel: ", total_travel_time)

    # display mean travel time
    average_time = df["Trip Duration"].mean()
    print("The average travel-time: ", average_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bike share users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Count of user types: ",
          df["User Type"].value_counts())

    # Display counts of gender
    if "Gender" in df:
        print("\nCounts concerning client`s gender")
        print("Male persons: ", df.query("Gender == 'Male'").Gender.count())
        print("Female persons: ", df.query("Gender == 'Female'").Gender.count())

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print("\nEarliest year of birth: ", int(df["Birth Year"].min()))
        print("Most recent year of birth: ", int(df["Birth Year"].max()))
        print("Most common year of birth: ", int(df["Birth Year"].value_counts().idxmax()))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('GoodBye')
            break


if __name__ == "__main__":
    main()
