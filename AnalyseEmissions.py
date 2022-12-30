import pandas as pd
import numpy as np
import os
import argparse
import DataOperations as do
import DataExtraction as de


parser = argparse.ArgumentParser()

cwd = os.getcwd()

parser.add_argument("starting_year", type = int, default = 0, nargs = "?", help = "Ignore all the data before this year")
parser.add_argument("ending_year", type = int, default = 3000, nargs = "?", help = "Ignore all the data after this year")

parser.add_argument("emission_path", default = os.path.join(cwd, 'fossil-fuel-co2-emissions-by-nation_csv.csv'),
                     nargs = "?", help = "path to csv file containing co2 emission data")

parser.add_argument("gdp_path", default = os.path.join(cwd, 'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv'),
                     nargs = "?", help = "path to csv file containing GDP data")

parser.add_argument("population_path", default = os.path.join(cwd, 'API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv'),
                     nargs = "?", help = "path to csv file containing population data")

args = parser.parse_args()


if (args.ending_year - args.starting_year) < 0:
    parser.error('Please select a valid time interval')


co2, gdp, pop = do.get_data(args.emission_path, args.gdp_path, args.population_path)

countries = de.get_countries(co2, gdp)
start, end = de.get_interval(args.starting_year, args.ending_year, co2, gdp, pop)

co2 = do.crop_data(co2, start, end)
co2 = do.merge_data(co2, gdp, pop, countries)


highest_emission = de.n_highest_emissions_pc(co2).reset_index(drop = True)

print("\nFollowing table contains list of 5 countries with highest co2 per capita emission in every considered year: \n")
print(highest_emission)

highest_gdp = de.n_highest_gdps_pc(co2).reset_index(drop = True)

print("\nFollowing table contains list of 5 countries with highest GDP per capita in every considered year: \n")
print(highest_gdp)

highest_reduction = de.n_highest_reductions(co2, start, end, end, 5).reset_index(drop = True)

print("\nFollowing table contains list of 5 countries with highest reduction of co2 per capita emission in the last 10 years: \n")
print(highest_reduction)