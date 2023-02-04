import pandas as pd
import numpy as np
import os
import argparse
import DataOperations as do
import DataExtraction as de


parser = argparse.ArgumentParser(description = "The goal of this program is to analyze data on CO2 emissions, gross domestic product and population")
cwd = os.getcwd()

parser.add_argument("-s", "--save", action = 'store_true',
                    help = "Save results as csv files")


parser.add_argument("-f", "--first_year", type = int, default = 0,
                    required = False, help = "Ignore all data before this year")

parser.add_argument("-l", "--last_year", type = int, default = 5000,
                    required = False, help = "Ignore all data after this year")


parser.add_argument("emission_path", default = os.path.join(cwd, 'fossil-fuel-co2-emissions-by-nation_csv.csv'),
                     nargs = "?", help = "Path to csv file containing CO2 emission data")

parser.add_argument("gdp_path", default = os.path.join(cwd, 'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv'),
                     nargs = "?", help = "Path to csv file containing GDP data")

parser.add_argument("population_path", default = os.path.join(cwd, 'API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv'),
                     nargs = "?", help = "Path to csv file containing population data")


args = parser.parse_args()


if (args.last_year - args.first_year) < 0:
    parser.error('Please select a valid time interval')



# reorganize data before analysis
co2, gdp, pop = do.get_data(args.emission_path, args.gdp_path, args.population_path)
gdp, pop = do.combine_countries(gdp, pop) 

start, end = de.get_interval(args.first_year, args.last_year, co2, gdp, pop)
co2 = do.crop_data(co2, start, end)

countries = do.get_countries(co2, gdp)
data = do.merge_data(co2, gdp, pop, countries)


# perform analysis on table 'data'
highest_emissions = de.n_highest_emissions_pc(data).reset_index(drop = True)

print("\nFollowing table contains list of 5 countries with highest CO2 per capita emission in every considered year: \n")
print(highest_emissions)


highest_gdps = de.n_highest_gdps_pc(data).reset_index(drop = True)

print("\nFollowing table contains list of 5 countries with highest GDP per capita in every considered year: \n")
print(highest_gdps)


if (end == start):
    print("\nAvailable data comes from only one year. Per capita CO2 emission reduction/increase table cannot be created")
else:
    high_low = de.n_highest_reductions_increases(data, start, end, 5)
    highest_reductions = high_low[0].reset_index(drop=True)
    highest_increases = high_low[1].reset_index(drop=True)

    if (end - 10) < start:
        print(
            (f"\nAvailable data goes back for only {end - start} years."
             f" Following tables contain lists of 5 countries with highest reduction/increase of CO2 per capita emission in the last {end - start} years: \n"))
    else:
        print(("\nFollowing tables contain lists of 5 countries with highest reduction/increase of CO2 per capita emission in the last 10 years:\n"))
    print(highest_reductions, end = '\n\n')
    print(highest_increases, end = '\n')



# save results if requested
if (args.save == True):
    highest_emissions.to_csv('highest_emissions.csv')
    highest_gdps.to_csv('highest_gdps.csv')
    if (end != start):
        highest_reductions.to_csv("highest_reductions.csv")
        highest_increases.to_csv('highest_increases.csv')
