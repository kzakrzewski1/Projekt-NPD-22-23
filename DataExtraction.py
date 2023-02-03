import pandas as pd
import numpy as np
import os



# find years for which all of the required data is available
def get_interval(first, last, co2, gdp, pop):        
    start = max(int(gdp.select_dtypes('number').columns.min()),
                int(pop.select_dtypes('number').columns.min()),
                co2['Year'].values.min(),
                first)
    
    end = min(int(gdp.select_dtypes('number').columns.max()),
               int(pop.select_dtypes('number').columns.max()),
               co2['Year'].values.max(),
               last)


    start_in = max(int(gdp.select_dtypes('number').columns.min()),
                   int(pop.select_dtypes('number').columns.min()),
                   co2['Year'].values.min())

    end_in = min(int(gdp.select_dtypes('number').columns.max()),
                  int(pop.select_dtypes('number').columns.max()),
                  co2['Year'].values.max())

    if(start_in >= end_in):
        msg = f"supplied files provide overlapping data only between years {start_in} and {end_in}"
    else:
        msg = f"supplied files don't provide overlapping data in any year."
               

    assert start <= end, f"no data available for chosen time interval. {msg}"

    return [start, end]



# return population of a given country in a given year
def get_population(pop, year, country_code):
    return pop.at[pop[pop['Country Code'] == country_code].index.item(), str(year)]
        

#  return gdp of a given country in a given year
def get_gdp(gdp, year, country_code):        
    return gdp.at[gdp[gdp['Country Code'] == country_code].index.item(), str(year)]



# calculate co2 emission per capita 
def CO2_per_capita(total, population):       
    if population == 0:
        return np.nan
    else:
        return 1000 * total/population


# calculate GDP per capita
def GDP_per_capita(gdp, population):
    if population == 0:
        return np.nan
    else:
        return gdp/population



# create table containing n countries with highest co2 emission per capita in each year
def n_highest_emissions_pc(data, n = 5):
    return data.sort_values(by = ['Year', 'Per Capita'],
                            ascending = [True, False]).groupby(['Year']).head(n)[['Year',
                                                                                  'Country Name', 
                                                                                  'Per Capita', 
                                                                                  'Total']]


# create table containing n countries with highest GDP per capita in each year
def n_highest_gdps_pc(data, n = 5):
    return data.sort_values(by = ['Year', 'GDP Per Capita'],
                                  ascending = [True, False]).groupby(['Year']).head(n)[['Year',
                                                                                        'Country Name', 
                                                                                        'GDP Per Capita', 
                                                                                        'GDP']]



# calculate reduction of co2 per capita emission between given years
def get_reduction(data, country_name, first, last):
    if  (data[(data['Country Name'] == country_name) & (data['Year'] == first)]['Per Capita'].values and
         data[(data['Country Name'] == country_name) & (data['Year'] == last)]['Per Capita'].values): 
        return (data[(data['Country Name'] == country_name) & (data['Year'] == first)]['Per Capita'].values[0] 
              - data[(data['Country Name'] == country_name) & (data['Year'] == last)]['Per Capita'].values[0])
    else:
        return np.nan
        
    

# create table containing n countries with higest reduction of co2 per capita emission in the last 10 years
def n_highest_reductions_increases(data, start, end, n):
        begin = max(end - 10, start)

        country_list =  pd.DataFrame(data["Country Name"].unique())
        country_list.columns = ['Country Name']
        country_list['Reduction'] = country_list[['Country Name']].apply(lambda x: 
                                                                         get_reduction(data, x['Country Name'], begin, end), axis = 1)
        country_list['Increase'] = country_list[['Reduction']].apply(lambda x: x*(-1), axis = 1)                                                    


        return [country_list[['Country Name', 'Reduction']].sort_values(by = 'Reduction', 
                                                                        ascending = False).dropna().head(n),
                country_list[['Country Name', 'Increase']].sort_values(by = 'Increase', 
                                                                       ascending = False).dropna().head(n)]