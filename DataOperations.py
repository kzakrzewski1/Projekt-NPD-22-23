import pandas as pd
import numpy as np
import os
import DataExtraction as de
from CodeAssignments import AssignCodes


# load emission, gdp and population data from csv files
def get_data(emissions, gdp, population):

    co2 = pd.read_csv(emissions, on_bad_lines = 'skip')

    gdp = pd.read_csv(gdp, skiprows = 4)        # data starts at line 5
    gdp = gdp.dropna(how='all', axis='columns')        # reading from given csv leaves empty column at the end of the data

    pop = pd.read_csv(population, skiprows = 4)
    pop = pop.dropna(how='all', axis='columns')                  

    gdp['Country Name'] = gdp['Country Name'].str.upper()       # changing country names to uppercase for compatibility with co2 emission data
    pop['Country Name'] = pop['Country Name'].str.upper()

    return [co2, gdp, pop]



# create dataframe containing countries present in emission data and their alpha-3 codes
def get_countries(co2, gdp):
    countries = pd.DataFrame(co2['Country'].drop_duplicates())        
    countries.columns = ['Country Name']

    countries = pd.merge(countries, gdp[['Country Name', 'Country Code']], 
                         on = 'Country Name', how = 'left').sort_values(by = 'Country Name')

   # manually assign missing codes
    countries = AssignCodes(countries)

    countries.columns = ['Country', 'Country Code']

    return countries



# add san marino gdp and population to italy, monaco to france
def combine_countries(gdp, pop):
    if gdp[gdp['Country Name'] == "SAN MARINO"].index.array.size == 1:
        sm_ix_gdp = gdp[gdp['Country Name'] == "SAN MARINO"].index.item()
    else:
        sm_ix_gdp = None

    if pop[pop['Country Name'] == "SAN MARINO"].index.array.size == 1:
        sm_ix_pop = pop[pop['Country Name'] == "SAN MARINO"].index.item()
    else:
        sm_ix_pop = None

    if gdp[gdp['Country Name'] == "MONACO"].index.array.size == 1:
        mc_ix_gdp = gdp[gdp['Country Name'] == "MONACO"].index.item()
    else:
        mc_ix_gdp = None

    if pop[pop['Country Name'] == "MONACO"].index.array.size == 1:
        mc_ix_pop = pop[pop['Country Name'] == "MONACO"].index.item()
    else:
        mc_ix_pop = None

    if sm_ix_gdp is not None:
        gdp.at[sm_ix_gdp, 'Country Name'] = "ITALY"
        gdp.at[sm_ix_gdp, 'Country Code'] = "ITA"

    if mc_ix_gdp is not None:
        gdp.at[mc_ix_gdp, 'Country Name'] = "FRANCE"
        gdp.at[mc_ix_gdp, 'Country Code'] = "FRA"

    if sm_ix_pop is not None:
        pop.at[sm_ix_pop, 'Country Name'] = "ITALY"
        pop.at[sm_ix_pop, 'Country Code'] = "ITA"

    if mc_ix_pop is not None:
        pop.at[mc_ix_pop, 'Country Name'] = "FRANCE"
        pop.at[mc_ix_pop, 'Country Code'] = "FRA"

    gdp = gdp.groupby(['Country Name', 'Country Code',
                       'Indicator Name', 'Indicator Code'], as_index=False).agg(sum)

    pop = pop.groupby(['Country Name', 'Country Code',
                       'Indicator Name', 'Indicator Code'], as_index=False).agg(sum)

    return [gdp, pop]



# delete data outside of the considered time interval
def crop_data(co2, start, end):       
        co2 = co2[co2['Year'].isin(range(start, end + 1))]

        return co2
    


# merge emission, gdp and population data
def merge_data(co2, gdp, pop, countries):
    co2 = pd.merge(co2, countries, on = 'Country')      # adding alpha-3 codes to emission data

    co2 = co2.groupby(['Year', 'Country Code'], as_index = False).sum(numeric_only = True)      # summing emissions for territories assigned the same alpha-3 code

    co2 = pd.merge(co2, gdp[['Country Name', 'Country Code']],
                   on = 'Country Code').sort_values(['Year', 'Country Code'])       # assigning country names used in gdp and population data

    co2.drop('Per Capita', axis =  1, inplace = True)       # deleting corrupted per capita data, it will be recalculated using population data

    assert (not co2.empty), "Provided emission data is not compatible with gdp and population data"
    

    co2['Population'] = co2[['Year', 'Country Code']].apply(lambda x:
                                                            de.get_population(pop, x['Year'], x['Country Code']), axis = 1)

    co2['GDP'] = co2[['Year', 'Country Code']].apply(lambda x:
                                                     de.get_gdp(gdp, x['Year'], x['Country Code']), axis = 1)

    co2["Per Capita"] = co2[['Total', 'Population']].apply(lambda x:
                                                           de.CO2_per_capita(x['Total'], x['Population']), axis = 1)

    co2['GDP Per Capita'] = co2[['GDP', 'Population']].apply(lambda x:
                                                             de.GDP_per_capita(x['GDP'], x['Population']), axis = 1)

    
    return co2[co2['Per Capita'].notna()]
    
