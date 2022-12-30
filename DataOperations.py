import pandas as pd
import numpy as np
import os
import DataExtraction as de


# load emission, gdp and population data from csv files
def get_data(emissions, gdp, population):

    co2 = pd.read_csv(emissions, on_bad_lines = 'skip')

    gdp = pd.read_csv(gdp, skiprows = 4)
    gdp = gdp.dropna(how='all', axis='columns')        # reading from given csv leaves empty column at the end of the data

    pop = pd.read_csv(population, skiprows = 4)
    pop = pop.dropna(how='all', axis='columns')                  


    gdp['Country Name'] = gdp['Country Name'].str.upper()       # changing country names to uppercase for compatibility with co2 emission data
    pop['Country Name'] = pop['Country Name'].str.upper()

    return [co2, gdp, pop]

# delete data outside of the considered time interval
def crop_data(co2, start, end):       
    try:
        assert start <= end
        co2 = co2[co2['Year'].isin(range(start, end + 1))]
        return co2

    except AssertionError:
        print('No data available for the chosen time period')


# merge emission, gdp and population data
def merge_data(co2, gdp, pop, countries):
    co2 = pd.merge(co2, countries, on = 'Country')      # adding alpha-3 codes to emission data

    co2 = co2.groupby(['Year', 'Country Code'], as_index = False).sum(numeric_only = True)      # summing emissions for territories assigned the same alpha-3 code

    co2 = pd.merge(co2, gdp[['Country Name', 'Country Code']],
                   on = 'Country Code').sort_values(['Year', 'Country Code'])       # assigning country names used in gdp and population data

    co2.drop('Per Capita', axis =  1, inplace = True)       # deleting corrupted per capita data, it will be recalculated using population data
    

    co2['Population'] = co2[['Year', 'Country Code']].apply(lambda x:
                                                            de.get_population(pop, x['Year'], x['Country Code']), axis = 1)

    co2['GDP'] = co2[['Year', 'Country Code']].apply(lambda x:
                                                     de.get_gdp(gdp, x['Year'], x['Country Code']), axis = 1)

    co2["Per Capita"] = co2[['Total', 'Population']].apply(lambda x:
                                                           de.per_capita(x['Total'], x['Population']), axis = 1)

    co2['GDP Per Capita'] = co2[['GDP', 'Population']].apply(lambda x:
                                                             de.GDP_per_capita(x['GDP'], x['Population']), axis = 1)


    return co2[co2['Per Capita'].notna()]