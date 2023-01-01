import pandas as pd
import numpy as np
import os
import argparse
import DataOperations as do
import DataExtraction as de


parser = argparse.ArgumentParser(description = "The goal of this program is to analyze data on CO2 emissions, gross domestic product and population")
cwd = os.getcwd()

parser.add_argument("-f", "--first_year", type = int, default = 0,
                    required = False, help = "Ignore all the data before this year")

parser.add_argument("-l", "--last_year", type = int, default = 5000,
                    required = False, help = "Ignore all the data after this year")


parser.add_argument("emission_path", default = os.path.join(cwd, 'fossil-fuel-co2-emissions-by-nation_csv.csv'),
                     nargs = "?", help = "Path to csv file containing CO2 emission data")

parser.add_argument("gdp_path", default = os.path.join(cwd, 'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv'),
                     nargs = "?", help = "Path to csv file containing GDP data")

parser.add_argument("population_path", default = os.path.join(cwd, 'API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv'),
                     nargs = "?", help = "Path to csv file containing population data")


args = parser.parse_args()


if (args.last_year - args.first_year) < 0:
    parser.error('Please select a valid time interval')


co2, gdp, pop = do.get_data(args.emission_path, args.gdp_path, args.population_path)
gdp, pop = do.combine_countries(gdp, pop)

countries = de.get_countries(co2, gdp)
start, end = de.get_interval(args.first_year, args.last_year, co2, gdp, pop)

co2 = do.crop_data(co2, start, end)
data = do.merge_data(co2, gdp, pop, countries)


highest_emission = de.n_highest_emissions_pc(data).reset_index(drop = True)

print("\nFollowing table contains list of 5 countries with highest CO2 per capita emission in every considered year: \n")
print(highest_emission)

highest_gdp = de.n_highest_gdps_pc(data).reset_index(drop = True)

print("\nFollowing table contains list of 5 countries with highest GDP per capita in every considered year: \n")
print(highest_gdp)

if (end == start):
    print("\nAvailable data comes from only one year. Per capita CO2 emission reduction table cannot be created")
else:
    highest_reduction = de.n_highest_reductions(data, start, end, 5).reset_index(drop=True)
    if (end - 10) < start:
        print(
            f"\nAvailable data goes back for only {end - start} years. Following table contains list of 5 countries with highest reduction of CO2 per capita emission in the last {end - start} years: \n")
    else:
        print(("\nFollowing table contains list of 5 countries with highest reduction of CO2 per capita emission in the last 10 years:\n"))
    print(highest_reduction)
