This project aims to analyse data on CO2 emissions, gross domestic product and populations.

Data that has been used for this analysis can be downloaded from this repository in the form of csv files. It comes from two different sources,
which sometimes use different names for the same countries or treat some territories in a different way (for example in the gdp and population 
data monaco is treated as a separate entity, whereas in the emission data it is counted together with france). In order to make it possible to
combine this data, all the countries present in emission data have been manually assigned alpha-3 code (see country_codes.csv). As these codes
are already present in gdp and population data, we can use them to merge all available informations. To assign codes, following rules have been
used:

- dependencies, unless appearing as a separate entity in the gpd/population data (e.g. Aruba) have been assigned alpha-3 codes of their controlling 
  states (e.g. Martinique has been assigned alpha-3 code "FRA", which means that its CO2 emissions will be later on added to the CO2 emissions of
  France).
  
- countries that used to be divided in two parts have been assigned codes of the state that has been created after their union (e.g. East and West
  Germany have been both assigned code "DEU")
  
- Monaco has been assigned code "FRA"

- San Marino has been assigned code "ITA"

- Historical countries, e.g. USSR, Yugoslavia, Czechoslovakia have been assigned their official alpha-3 codes. Data pertaining those countries is 
  not available in the csv files accessible in this repository, but if it was added, the program should be able to use it without any modifications.
  
- Few countries, due to their unclear situation, have been deleted from country_codes.csv file, which means that their data will not be used at all.
  This list includes:
  - Malaysia and Singapore Federation
  - Ryukyu Islands
  - Palestine
  - Taiwan
  - United Korea
  - former colonial territories: French Indochina, Rhodesia-Nyasaland, Ruanda-Urundi etc.
