import pandas as pd
import numpy as np
import pytest
import DataOperations as do
import DataExtraction as de
from pytest import MonkeyPatch


# always load data from the files attached to the project
def mock_get_data(v1, v2, v3):
    pop = pd.read_csv('API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv', skiprows=4)
    pop = pop.dropna(how='all', axis='columns')

    gdp = pd.read_csv('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv', skiprows=4)
    gdp = gdp.dropna(how='all', axis='columns')

    co2 = pd.read_csv('fossil-fuel-co2-emissions-by-nation_csv.csv')


    pop['Country Name'] = pop['Country Name'].str.upper()
    gdp['Country Name'] = gdp['Country Name'].str.upper()

    return [co2, gdp, pop]



# check if the get_interval function correctly identifies available data interval for attached files
def test_get_interval(monkeypatch):
    monkeypatch.setattr("DataOperations.get_data", mock_get_data)

    co2, gdp, pop = do.get_data(1, 2, 3)

    assert de.get_interval(0, 5000, co2, gdp, pop) == [1960, 2014],      \
        "get_interval returns incorrect values"
    assert de.get_interval(0, 5000, co2[co2["Year"] <= 2010], gdp, pop) == [1960, 2010],    \
        "get_interval returns incorrect values"
    assert de.get_interval(2000, 5000, co2, gdp, pop) == [2000, 2014],      \
        "get_interval returns incorrect values when first year is specified"
    assert de.get_interval(0, 2005, co2, gdp, pop) == [1960, 2005],      \
        "get_interval returns incorrect values when last year is specified"

    with pytest.raises(AssertionError) as AErr:
        de.get_interval(3000, 2000, co2, gdp, pop)
    assert "no data available for chosen time interval" in str(AErr.value),      \
        "get_interval doesn't return error when given incompatible data"

    with pytest.raises(AssertionError) as AErr:
        de.get_interval(0, 5000, co2[co2["Year"] <= 1800], gdp, pop)
    assert "no data available for chosen time interval" in str(AErr.value),      \
        "get_interval doesn't return error when given incompatible data"



# check correctness of get_gdp, get_population, and combine_countries functions
def test_population_gdp(monkeypatch):
    monkeypatch.setattr("DataOperations.get_data", mock_get_data)

    co2, gdp, pop = do.get_data(1, 2, 3)

    assert de.get_population(pop, 2000, 'FRA') == 60912500,     \
        "get_population returns incorrect population values"
    assert de.get_gdp(gdp, 2000, 'FRA') == 1365639660792.16,     \
        "get_gdp returns incorrect gdp values"

    gdp, pop = do.combine_countries(gdp, pop)

    assert de.get_population(pop, 2000, 'FRA') == 60912500 + 32148,     \
        "combine_countries doesn't properly add monaco population to france"
    assert de.get_gdp(gdp, 2000, 'FRA') == 1365639660792.16 + 2647885848.5351,      \
        "combine_countries doesn't properly add monaco gdp to france"

    gdp2, pop2 = do.combine_countries(gdp, pop)

    assert gdp.equals(gdp2), "combine countries performs unnecessary operations on table without monaco and san marino"
    assert pop.equals(pop2), "combine countries performs unnecessary operations on table without monaco and san marino"



# check if get_reduction correctly calculates reduction of CO2 per capita emission
def test_get_reduction(monkeypatch):
    monkeypatch.setattr("DataOperations.get_data", mock_get_data)

    co2, gdp, pop = do.get_data(1, 2, 3)
    co2.rename(columns = {'Country':'Country Name'}, inplace = True)

    assert de.get_reduction(co2, "UNITED KINGDOM", 1960, 1970) == 3.02 - 3.19,      \
        "get_reduction incorrectly calculates CO2 per capita emission reduction"
