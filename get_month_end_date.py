from datetime import datetime
import calendar

# Function to get the last day of a month
def get_last_day_of_month(year, month):
    # Get the last day of the month using calendar.monthrange
    _, last_day = calendar.monthrange(year, month)
    return datetime(year, month, last_day).strftime('%d-%b-%Y').lower()

# Generate last days for months from nov-2024 to jan-2014
def generate_last_days():
    start_year = 2017
    start_month = 11  # November
    end_year = 2014
    end_month = 1  # January

    current_year = start_year
    current_month = start_month

    last_days = []

    # Iterate over the months from November 2024 to January 2014
    while current_year > end_year or (current_year == end_year and current_month >= end_month):
        last_day = get_last_day_of_month(current_year, current_month)
        last_days.append(last_day)

        # Move to the previous month
        if current_month == 1:
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1

    return last_days

# # Example usage
# last_days = generate_last_days()
# for date in last_days:
#     print(date)
