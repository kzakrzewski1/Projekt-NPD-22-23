import pandas as pd
import numpy as np
import os
import DataExtraction as de


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
    countries.loc[countries['Country Name'] == 'ANGUILLA', 'Country Code'] = 'GBR'
    countries.loc[countries['Country Name'] == 'ANTIGUA & BARBUDA', 'Country Code'] = 'ATG'
    countries.loc[countries['Country Name'] == 'BAHAMAS', 'Country Code'] = 'BHS'
    countries.loc[countries['Country Name'] == 'BONAIRE, SAINT EUSTATIUS, AND SABA', 'Country Code'] = 'NLD'
    countries.loc[countries['Country Name'] == 'BOSNIA & HERZEGOVINA', 'Country Code'] = 'BIH'
    countries.loc[countries['Country Name'] == 'BRUNEI (DARUSSALAM)', 'Country Code'] = 'BRN'
    countries.loc[countries['Country Name'] == 'CAPE VERDE', 'Country Code'] = 'CPV'
    countries.loc[countries['Country Name'] == 'CHINA (MAINLAND)', 'Country Code'] = 'CHN'
    countries.loc[countries['Country Name'] == 'CHRISTMAS ISLAND', 'Country Code'] = 'AUS'
    countries.loc[countries['Country Name'] == 'CONGO', 'Country Code'] = 'COG'
    countries.loc[countries['Country Name'] == 'COOK ISLANDS', 'Country Code'] = 'NZL'
    countries.loc[countries['Country Name'] == 'COTE D IVOIRE', 'Country Code'] = 'CIV'
    countries.loc[countries['Country Name'] == 'CZECH REPUBLIC', 'Country Code'] = 'CZE'
    countries.loc[countries['Country Name'] == 'CZECHOSLOVAKIA', 'Country Code'] = 'CSK'
    countries.loc[countries['Country Name'] == 'DEMOCRATIC PEOPLE S REPUBLIC OF KOREA', 'Country Code'] = 'PRK'
    countries.loc[countries['Country Name'] == 'DEMOCRATIC REPUBLIC OF THE CONGO (FORMERLY ZAIRE)', 'Country Code'] = 'COD'
    countries.loc[countries['Country Name'] == 'DEMOCRATIC REPUBLIC OF VIETNAM', 'Country Code'] = 'VNM'
    countries.loc[countries['Country Name'] == 'EAST & WEST PAKISTAN', 'Country Code'] = 'PAK'
    countries.loc[countries['Country Name'] == 'EGYPT', 'Country Code'] = 'EGY'
    countries.loc[countries['Country Name'] == 'FAEROE ISLANDS', 'Country Code'] = 'FRO'
    countries.loc[countries['Country Name'] == 'FALKLAND ISLANDS (MALVINAS)', 'Country Code'] = 'GBR'
    countries.loc[countries['Country Name'] == 'FEDERAL REPUBLIC OF GERMANY', 'Country Code'] = 'DEU'
    countries.loc[countries['Country Name'] == 'FEDERATED STATES OF MICRONESIA', 'Country Code'] = 'FSM'
    countries.loc[countries['Country Name'] == 'FORMER DEMOCRATIC YEMEN', 'Country Code'] = 'YEM'
    countries.loc[countries['Country Name'] == 'FORMER GERMAN DEMOCRATIC REPUBLIC', 'Country Code'] = 'DEU'
    countries.loc[countries['Country Name'] == 'FORMER PANAMA CANAL ZONE', 'Country Code'] = 'PAN'
    countries.loc[countries['Country Name'] == 'FORMER YEMEN', 'Country Code'] = 'YEM'
    countries.loc[countries['Country Name'] == 'FRANCE (INCLUDING MONACO)', 'Country Code'] = 'FRA'
    countries.loc[countries['Country Name'] == 'FRENCH GUIANA', 'Country Code'] = 'FRA'
    countries.loc[countries['Country Name'] == 'GAMBIA', 'Country Code'] = 'GMB'
    countries.loc[countries['Country Name'] == 'GUADELOUPE', 'Country Code'] = 'FRA'
    countries.loc[countries['Country Name'] == 'GUINEA BISSAU', 'Country Code'] = 'GNB'
    countries.loc[countries['Country Name'] == 'HONG KONG SPECIAL ADMINSTRATIVE REGION OF CHINA', 'Country Code'] = 'HKG'
    countries.loc[countries['Country Name'] == 'ISLAMIC REPUBLIC OF IRAN', 'Country Code'] = 'IRN'
    countries.loc[countries['Country Name'] == 'ITALY (INCLUDING SAN MARINO)', 'Country Code'] = 'ITA'
    countries.loc[countries['Country Name'] == 'JAPAN (EXCLUDING THE RUYUKU ISLANDS)', 'Country Code'] = 'JPN'
    countries.loc[countries['Country Name'] == 'KUWAITI OIL FIRES', 'Country Code'] = 'KWT'
    countries.loc[countries['Country Name'] == 'KYRGYZSTAN', 'Country Code'] = 'KGZ'
    countries.loc[countries['Country Name'] == 'LAO PEOPLE S DEMOCRATIC REPUBLIC', 'Country Code'] = 'LAO'
    countries.loc[countries['Country Name'] == 'LEEWARD ISLANDS', 'Country Code'] = 'GBR'
    countries.loc[countries['Country Name'] == 'LIBYAN ARAB JAMAHIRIYAH', 'Country Code'] = 'LBY'
    countries.loc[countries['Country Name'] == 'MACAU SPECIAL ADMINSTRATIVE REGION OF CHINA', 'Country Code'] = 'MAC'
    countries.loc[countries['Country Name'] == 'MACEDONIA', 'Country Code'] = 'MKD'
    countries.loc[countries['Country Name'] == 'MARTINIQUE', 'Country Code'] = 'FRA'
    countries.loc[countries['Country Name'] == 'MONTSERRAT', 'Country Code'] = 'GBR'
    countries.loc[countries['Country Name'] == 'MYANMAR (FORMERLY BURMA)', 'Country Code'] = 'MMR'
    countries.loc[countries['Country Name'] == 'NETHERLAND ANTILLES', 'Country Code'] = 'NLD'
    countries.loc[countries['Country Name'] == 'NETHERLAND ANTILLES AND ARUBA', 'Country Code'] = 'NLD'
    countries.loc[countries['Country Name'] == 'NIUE', 'Country Code'] = 'NZL'
    countries.loc[countries['Country Name'] == 'PACIFIC ISLANDS (PALAU)', 'Country Code'] = 'PLW'
    countries.loc[countries['Country Name'] == 'PENINSULAR MALAYSIA', 'Country Code'] = 'MYS'
    countries.loc[countries['Country Name'] == 'PLURINATIONAL STATE OF BOLIVIA', 'Country Code'] = 'BOL'
    countries.loc[countries['Country Name'] == 'REPUBLIC OF CAMEROON', 'Country Code'] = 'CMR'
    countries.loc[countries['Country Name'] == 'REPUBLIC OF KOREA', 'Country Code'] = 'KOR'
    countries.loc[countries['Country Name'] == 'REPUBLIC OF MOLDOVA', 'Country Code'] = 'MDA'
    countries.loc[countries['Country Name'] == 'REPUBLIC OF SOUTH SUDAN', 'Country Code'] = 'SSD'
    countries.loc[countries['Country Name'] == 'REPUBLIC OF SOUTH VIETNAM', 'Country Code'] = 'VNM'
    countries.loc[countries['Country Name'] == 'REPUBLIC OF SUDAN', 'Country Code'] = 'SDN'
    countries.loc[countries['Country Name'] == 'REUNION', 'Country Code'] = 'FRA'
    countries.loc[countries['Country Name'] == 'SAINT HELENA', 'Country Code'] = 'GBR'
    countries.loc[countries['Country Name'] == 'SAINT LUCIA', 'Country Code'] = 'LCA'
    countries.loc[countries['Country Name'] == 'SAINT MARTIN (DUTCH PORTION)', 'Country Code'] = 'SXM'
    countries.loc[countries['Country Name'] == 'SAO TOME & PRINCIPE', 'Country Code'] = 'STP'
    countries.loc[countries['Country Name'] == 'SLOVAKIA', 'Country Code'] = 'SVK'
    countries.loc[countries['Country Name'] == 'ST. KITTS-NEVIS', 'Country Code'] = 'KNA'
    countries.loc[countries['Country Name'] == 'ST. PIERRE & MIQUELON', 'Country Code'] = 'FRA'
    countries.loc[countries['Country Name'] == 'ST. VINCENT & THE GRENADINES', 'Country Code'] = 'VCT'
    countries.loc[countries['Country Name'] == 'SWAZILAND', 'Country Code'] = 'SWZ'
    countries.loc[countries['Country Name'] == 'TANGANYIKA', 'Country Code'] = 'TZA'
    countries.loc[countries['Country Name'] == 'TIMOR-LESTE (FORMERLY EAST TIMOR)', 'Country Code'] = 'TLS'
    countries.loc[countries['Country Name'] == 'TURKEY', 'Country Code'] = 'TUR'
    countries.loc[countries['Country Name'] == 'UNITED REPUBLIC OF TANZANIA', 'Country Code'] = 'TZA'
    countries.loc[countries['Country Name'] == 'UNITED STATES OF AMERICA', 'Country Code'] = 'USA'
    countries.loc[countries['Country Name'] == 'USSR', 'Country Code'] = 'SUN'
    countries.loc[countries['Country Name'] == 'VENEZUELA', 'Country Code'] = 'VEN'
    countries.loc[countries['Country Name'] == 'VIET NAM', 'Country Code'] = 'VNM'
    countries.loc[countries['Country Name'] == 'WALLIS AND FUTUNA ISLANDS', 'Country Code'] = 'FRA'
    countries.loc[countries['Country Name'] == 'YEMEN', 'Country Code'] = 'YEM'
    countries.loc[countries['Country Name'] == 'YUGOSLAVIA (FORMER SOCIALIST FEDERAL REPUBLIC)', 'Country Code'] = 'YUG'
    countries.loc[countries['Country Name'] == 'YUGOSLAVIA (MONTENEGRO & SERBIA)', 'Country Code'] = 'SCG'
    countries.loc[countries['Country Name'] == 'ZANZIBAR', 'Country Code'] = 'TZA'


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
