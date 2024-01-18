#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ved Agrawal

DS 2500

10/18

Analyzing data from the Boston Marathon from the years 2010-2023. Calculating means of times
for different demographics and comparing it to their respective years.

"""

import os
import csv
import matplotlib.pyplot as plt
from collections import Counter
import statistics
from scipy import stats
import seaborn as sns

csv_directory = "marathon_data"

def read_data(directory):
    """
    Reads data from CSV files in the given directory and stores it in a dictionary.

    Args:
        directory (str): The directory containing CSV files.

    Returns:
        dict: A dictionary with file names as keys and data as values.
    """
    data = {}
    file_extensions = [".csv"]
    for filename in os.listdir(directory):
        if filename.endswith(tuple(file_extensions)):
            with open(os.path.join(directory, filename), 'r', newline='') as infile:
                
                csv_reader = csv.reader(infile)
                data[filename] = [row for row in csv_reader]
    return data

def structure_data(data_dict):
    """
    Structures the data from a dictionary of CSV data.

    Args:
        data_dict (dict): A dictionary with file names as keys and data as values.

    Returns:
        dict: Structured data with file names as keys and data dictionaries as values.
    """
    structured_data = {}
    for key, values in data_dict.items():
        headers, * data = values
        data_dict = {}
        for i, col in enumerate(headers):
            
            column_data = [row[i] for row in data]
            data_dict[col] = column_data
        structured_data[key] = data_dict
    
    return structured_data

# Function to convert time in HH:MM:SS format to seconds

def time_to_seconds(time_str):
    """
    Converts a time string in HH:MM:SS format to seconds.

    Args:
        time_str (str): Time in HH:MM:SS format.

    Returns:
        int: Time in seconds.
    """
   
    hours, minutes, seconds = map(int, time_str.split(':'))
    
    return hours * 3600 + minutes * 60 + seconds

# Function to convert seconds to HH:MM:SS format

def seconds_to_time(seconds):
    """
    Converts seconds to a time string in HH:MM:SS format.

    Args:
        seconds (int): Time in seconds.

    Returns:
        str: Time in HH:MM:SS format.
    """
   
    hours, remainder = divmod(seconds, 3600)
   
    minutes, seconds = divmod(remainder, 60)
   
    return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

# Call the read_data function to read the data

data_dict = read_data(csv_directory)

# Call the structure_data function to structure the data

structured_data = structure_data(data_dict)

# Question 1: In 2013, what was the mean finish time of the top 1000 runners in HH:MM:SS format?

year_2013_data = structured_data['boston_marathon_2013.csv']

finish_times_2013 = year_2013_data['OfficialTime']

# Convert finish times to seconds and calculate the mean

finish_times_seconds = [time_to_seconds(time) for time in finish_times_2013[:1000]]

mean_finish_time_seconds = statistics.mean(finish_times_seconds)

# Convert the mean finish time in seconds back to HH:MM:SS format

mean_finish_time_original_format = seconds_to_time(mean_finish_time_seconds)

# Question 2: What is the median age of the top 1000 runners in 2010?

year_2010_data = structured_data['boston_marathon_2010.csv']

ages_2010 = year_2010_data['AgeOnRaceDay']

median_age_2010 = statistics.median([int(age) for age in ages_2010[:1000]])

# Question 3: Apart from the US, which country had the most runners in 2023?

year_2023_data = structured_data['boston_marathon_2023.csv']

countries_2023 = year_2023_data['CountryOfResName']

# Remove the "United States" from the list of countries

filtered_countries_2023 = [country for country in countries_2023 if country != "United States of America"]

country_counts_2023 = Counter(filtered_countries_2023)

most_common_country_2023 = country_counts_2023.most_common(1)[0][0]

# Question 4: How many women finished in the top 1000 in 2021?

year_2021_data = structured_data['boston_marathon_2021.csv']

genders_2021 = year_2021_data['Gender']

women_count_2021 = genders_2021[:1000].count("F")

# Question 5: Correlation between year and mean finish time of women in the top 1000

mean_times_by_year = []

years = []

for year in range(2010, 2024):
    year_data = structured_data.get(f'boston_marathon_{year}.csv', None)
    if year_data:
        
        genders = year_data['Gender']
        finish_times = year_data['OfficialTime']
        
        women_finish_times = [time_to_seconds(time) for time, gender in zip(finish_times[:1000], genders[:1000]) if gender == 'F']
        
        if women_finish_times:
            
            mean_finish_time_seconds = statistics.mean(women_finish_times)
           
            mean_times_by_year.append(mean_finish_time_seconds)
            
            years.append(year)

# Calculate Pearson correlation coefficient

correlation_women, _ = stats.pearsonr(years, mean_times_by_year)

# Question 6: Correlation between year and mean finish time of American runners in the top 1000

mean_times_by_year = []

years = []

for year in range(2010, 2024):
    year_data = structured_data.get(f'boston_marathon_{year}.csv', None)
    if year_data:
        
        countries = year_data['CountryOfResName']
        finish_times = year_data['OfficialTime']
        
        american_finish_times = [time_to_seconds(time) for time, country in zip(finish_times[:1000], countries[:1000]) if country == 'United States of America']

        if american_finish_times:
            mean_finish_time_seconds = statistics.mean(american_finish_times)
            mean_times_by_year.append(mean_finish_time_seconds)
           
            years.append(year)

# Calculate the prediction for 2020 based on the correlation

x_mean = statistics.mean(years)

y_mean = statistics.mean(mean_times_by_year)

correlation_americans, _ = stats.pearsonr(years, mean_times_by_year)

slope = correlation_americans * (statistics.stdev(mean_times_by_year) / statistics.stdev(years))

intercept = y_mean - slope * x_mean

predicted_mean_time_2020 = slope * 2020 + intercept

# Create the linear regression plot

plt.figure(figsize=(10, 6))

sns.regplot(x=years, y=[time / 60 for time in mean_times_by_year], color='blue', label='Data')

slope, intercept, r_value, p_value, std_err = stats.linregress(years, [time / 60 for time in mean_times_by_year])

sns.lineplot(x=years, y=[slope * year + intercept for year in years], color='red', label='Linear Regression')

plt.title("Linear Regression: Year vs. Mean Finish Time of American Runners (Top 1000)")

plt.xlabel("Year")

plt.ylabel("Mean Finish Time (minutes)")

plt.legend()

plt.show()

# Extract median age and mean finish times for American runners in the top 1000

american_data = {}

for year in range (2010, 2024):
    year_data = structured_data.get(f'boston_marathon_{year}.csv', None)
    if year_data:
        
        countries = year_data['CountryOfResName']
        finish_times = year_data['OfficialTime']
        ages = year_data['AgeOnRaceDay']
        
        american_finish_times = [time_to_seconds(time) for time, country in zip(finish_times[:1000], countries[:1000]) if country == 'United States of America']
        american_ages = [int(age) for age in ages[:1000]]

        if american_finish_times and american_ages:
            mean_finish_time_seconds = statistics.mean(american_finish_times)
            median_age = statistics.median(american_ages)
           
            american_data[year] = {
                'mean_finish_time': mean_finish_time_seconds,
                'median_age': median_age
            }

# Normalize data using min-max scaling

min_age = min(american_data.values(), key=lambda x: x['median_age'])['median_age']

max_age = max(american_data.values(), key=lambda x: x['median_age'])['median_age']

min_time = min(american_data.values(), key=lambda x: x['mean_finish_time'])['mean_finish_time']

max_time = max(american_data.values(), key=lambda x: x['mean_finish_time'])['mean_finish_time']

normalized_data = {}
for year, values in american_data.items():
    normalized_data[year] = {
        'median_age': (values['median_age'] - min_age) / (max_age - min_age),
        'mean_finish_time': (values['mean_finish_time'] - min_time) / (max_time - min_time)
    }

years = list(normalized_data.keys())

median_ages = [values['median_age'] for values in normalized_data.values()]

mean_finish_times = [values['mean_finish_time'] for values in normalized_data.values()]

# Create the plot

plt.figure(figsize=(10, 6))

plt.plot(years, median_ages, label='Median Age')

plt.plot(years, mean_finish_times, label='Mean Finish Time ')

plt.title("Changes in Median Age and Mean Finish Times Over Time")

plt.xlabel("Year")

plt.ylabel("Median Age and Average Finish Time (Normalized Value)")

plt.legend()

plt.show()

# Print the answers to the questions
print(f"Question 1: In 2013, the mean finish time of the top 1000 runners was {mean_finish_time_original_format}.")
print(f"Question 2: The median age of the top 1000 runners in 2010 was {median_age_2010} years.")
print(f"Question 3: Apart from the US, {most_common_country_2023} had the most runners in 2023.")
print(f"Question 4: In 2021, {women_count_2021} women finished in the top 1000.")
print(f"Question 5: Correlation between year and mean finish time of women in the top 1000: {correlation_women:.4f}")
print(f"Question 6: Correlation between year and mean finish time of American runners in the top 1000: {correlation_americans:.4f}")
print(f"Predicted mean finish time of Americans in the top 1000 for 2020: {seconds_to_time(predicted_mean_time_2020)}")