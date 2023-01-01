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

    countries = pd.read_csv('country_codes.csv')       # missing alpha-3 codes have been added manually

    return countries



# find years for which all of the required data is available
def get_interval(start, end, co2, gdp, pop):        
    first = max(int(gdp.select_dtypes('number').columns.min()),
                int(pop.select_dtypes('number').columns.min()),
                co2['Year'].values.min(),
                start)
    
    last = min(int(gdp.select_dtypes('number').columns.max()),
               int(pop.select_dtypes('number').columns.max()),
               co2['Year'].values.max(),
               end)


    first_in = max(int(gdp.select_dtypes('number').columns.min()),
                   int(pop.select_dtypes('number').columns.min()),
                   co2['Year'].values.min())

    last_in = min(int(gdp.select_dtypes('number').columns.max()),
                  int(pop.select_dtypes('number').columns.max()),
                  co2['Year'].values.max())

    if(last_in >= first_in):
        msg = f"supplied files provide overlapping data only between years {first_in} and {last_in}"
    else:
        msg = f"supplied files don't provide overlapping data in any year."
               

    assert first <= last, f"no data available for chosen time interval. {msg}"

    return [first, last]



# return population of a given country in a given year
def get_population(pop, year, country_code):
    return pop.at[pop[pop['Country Code'] == country_code].index.item(), str(year)]
        

#  return gdp of a given country in a given year
def get_gdp(gdp, year, country_code):        
    return gdp.at[gdp[gdp['Country Code'] == country_code].index.item(), str(year)]



# calculate co2 emission per capita 
def CO2_per_capita(total, population):       
    return 1000 * total/population


# calculate GDP per capita
def GDP_per_capita(gdp, population):
    return gdp/population



# create table containing n countries with highest co2 emission per capita in each year
def n_highest_emissions_pc(data, n = 5):
    return data.sort_values(by = ['Year', 'Per Capita'],
                            ascending = [True, False]).groupby(['Year']).head(n)[['Year',
                                                                                 'Country Name', 
                                                                                 'Per Capita', 
                                                                                 'Total']]


# create table containing n countries with highest co2 emission per capita in a given year
def n_highest_emissions_pc_year(data, start, end, year, n = 5):
    try:
        assert (data >= start and year <= end)
        return data[data['Year'] == year].sort_values(by = 'Per Capita',
                                                      ascending = False).head(n)[['Year', 
                                                                                'Country Name', 
                                                                                'Per Capita', 
                                                                                'Total']]
    except AssertionError:
        print('No data available for this year')


# create table containing n countries with highest GDP per capita in each year
def n_highest_gdps_pc(data, n = 5):
    return data.sort_values(by = ['Year', 'GDP Per Capita'],
                                  ascending = [True, False]).groupby(['Year']).head(n)[['Year',
                                                                                       'Country Name', 
                                                                                       'GDP Per Capita', 
                                                                                       'GDP']]


# create table containing n countries with highest GDP per capita in a given year
def n_highest_gdps_pc_year(data, start, end, year, n = 5):
    try:
        assert (year >= start and year <= end)
        return data[data['Year'] == year].sort_values(by = 'GDP Per Capita',
                                                      ascending = False).head(n)[['Year', 
                                                                                'Country Name', 
                                                                                'GDP Per Capita', 
                                                                                'GDP']]
    except AssertionError:
        print('No data available for this year')



# calculate reduction of co2 per capita reduction between given years
def get_reduction(data, country_name, first, last):
    if  (data[(data['Country Name'] == country_name) & (data['Year'] == first)]['Per Capita'].values and
         data[(data['Country Name'] == country_name) & (data['Year'] == last)]['Per Capita'].values): 
        return (data[(data['Country Name'] == country_name) & (data['Year'] == first)]['Per Capita'].values[0] 
              - data[(data['Country Name'] == country_name) & (data['Year'] == last)]['Per Capita'].values[0])
    else:
        return np.nan
    

# create table containing n countries with higest reduction of co2 per capita emission in the last 10 years
def n_highest_reductions(data, start, end, n):
    try:
        assert (end > start)

        begin = max(end - 10, start)

        country_list =  pd.DataFrame(data["Country Name"].unique())
        country_list.columns = ['Country Name']
        country_list['Reduction'] = country_list[['Country Name']].apply(lambda x: 
                                                                         get_reduction(data, x['Country Name'], begin, end), axis = 1)

        return country_list.sort_values(by = 'Reduction', ascending = False).dropna().head(n)
        
    except AssertionError:
        if (start == end):
            print("The available data comes from only one year")
        else:
            print(f"Required data is not available for this year. Please select a year between {start + 1} and {end}")
