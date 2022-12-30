import pandas as pd
import numpy as np
import os



# create file containing countries present in emission data and some of their alpha-3 codes
def get_countries(co2, gdp):
    countries = pd.DataFrame(co2['Country'].drop_duplicates())        
    countries.columns = ['Country Name']

    countries = pd.merge(countries, gdp[['Country Name', 'Country Code']], 
                     on='Country Name', how='left').sort_values(by = 'Country Name')

    countries.to_csv('countries.csv')

    countries = pd.read_csv('countries2.csv')       # missing alpha-3 codes have been added manually

    return countries



# find years for which all of the required data is available
def get_interval(start, end, co2, gdp, pop):        
    return [1960, 2014]



# return population of a given country in a given year
def get_population(pop, year, country_code):      
    if  pop[pop['Country Code'] == country_code].loc[:, str(year)].values:
        return pop[pop['Country Code'] == country_code].loc[:, str(year)].values[0]
    else:
        return np.nan


#  return gdp of a given country in a given year
def get_gdp(gdp, year, country_code):        
    if  gdp[gdp['Country Code'] == country_code].loc[:, str(year)].values:
        return gdp[gdp['Country Code'] == country_code].loc[:, str(year)].values[0]
    else:
        print(country_code)
        return np.nan



# calculate co2 emission per capita 
def per_capita(total, population):       
    return 1000 * total/population


# calculate GDP per capita
def GDP_per_capita(gdp, population):
    return gdp/population



# create table containing n countries with highest co2 emission per capita in each year
def n_highest_emissions_pc(co2, n = 5):
    return co2.sort_values(by = ['Year', 'Per Capita'],
                           ascending = [True, False]).groupby(['Year']).head(n)[['Year',
                                                                                 'Country Name', 
                                                                                 'Per Capita', 
                                                                                 'Total']]


# create table containing n countries with highest co2 emission per capita in a given year
def n_highest_emissions_pc_year(co2, start, end, year, n = 5):
    try:
        assert (co2 >= start and year <= end)
        return co2[co2['Year'] == year].sort_values(by = 'Per Capita',
                                                    ascending = False).head(n)[['Year', 
                                                                                'Country Name', 
                                                                                'Per Capita', 
                                                                                'Total']]
    except AssertionError:
        print('No data available for this year')


# create table containing n countries with highest GDP per capita in each year
def n_highest_gdps_pc(co2, n = 5):
    return co2.sort_values(by = ['Year', 'GDP Per Capita'],
                                 ascending = [True, False]).groupby(['Year']).head(n)[['Year',
                                                                                       'Country Name', 
                                                                                       'GDP Per Capita', 
                                                                                       'GDP']]


# create table containing n countries with highest GDP per capita in a given year
def n_highest_gdps_pc_year(co2, start, end, year, n = 5):
    try:
        assert (year >= start and year <= end)
        return co2[co2['Year'] == year].sort_values(by = 'GDP Per Capita',
                                                    ascending = False).head(n)[['Year', 
                                                                                'Country Name', 
                                                                                'GDP Per Capita', 
                                                                                'GDP']]
    except AssertionError:
        print('No data available for this year')



# calculate reduction of co2 per capita reduction between given years
def get_reduction(co2, country_name, start, end):
    if  (co2[(co2['Country Name'] == country_name) & (co2['Year'] == start)]['Per Capita'].values and
         co2[(co2['Country Name'] == country_name) & (co2['Year'] == end)]['Per Capita'].values): 
        return (co2[(co2['Country Name'] == country_name) & (co2['Year'] == start)]['Per Capita'].values[0] 
              - co2[(co2['Country Name'] == country_name) & (co2['Year'] == end)]['Per Capita'].values[0])
    else:
        return np.nan
    

# create table containing n countries with higest reduction of co2 per capita emission between given years
def n_highest_reductions(co2, start, end, year, n):
    try:
        assert (year > start and year <= end)
        if (year - 10 < start):
                print(f"Available data goes back only for {year - start} years. Following table shows countries with highest reduction in the last {year - start} years. \n")

        begin = max(year - 10, start)

        country_list =  pd.DataFrame(co2["Country Name"].unique())
        country_list.columns = ['Country Name']
        country_list['Reduction'] = country_list[['Country Name']].apply(lambda x: get_reduction(co2, x['Country Name'], begin, year), axis = 1)

        return country_list.sort_values(by = 'Reduction', ascending = False).dropna().head(n)
        
    except AssertionError:
        if (start == end):
            print("The available data comes from only one year")
        else:
            print(f"Required data is not available for this year. Please select a year between {start + 1} and {end}")