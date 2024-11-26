---
layout: post
title: Country Indicators and Their Correlation
subtitle: How population, GDP, life expectancy, access to electricity, and literacy rates across the world's countries relate 
---

# World Bank Analysis

This blog post will discuss my use of the World Bank API and the country indicator which I chose, in an attempt to find correlation and relationships between certain variables.

## Indicators

I used the default `population`, `GDP`, and `life expectancy` indicators, as they would likely have a lot of data and complete information. In addition, I also chose `access to electricity` and `literacy rates`, under the assumption that the three other indicators (GDP, population, and life expectancy) would be correlated. A poorer country (lower gdp) would likely have worse education (lower literacy rates) and less people with electricity. I thought a similar trend would also exist in terms of population and life expectancy.

Each indicator had a corresponding id, which was used to call the api, so I made a dictionary containing the five indicators and their ids. This also made it easier to change the indicators if I ever wanted to because the rest of the code just referred to generic keys and values of the dictionary.

```python 
INDICATORS = {
    "Population": "SP.POP.TOTL",
    "Gdp": "NY.GDP.PCAP.CD",
    "Life_Expectancy": "SP.DYN.LE00.IN",
    "Electricity": "EG.ELC.ACCS.ZS",
    "Literacy": "SE.ADT.1524.LT.ZS",
}
```

## CountryYear Class

To store the data I received from the API, I made a `CountryYear` class with a variable for each indicator as a well as ones for the country `name`, `year`, and `3 digit code` (EX. Afghanistan: AFG). 

```python
class CountryYear:
    def __init__(self, name, country_iso3, year):
        self.name = name
        self.country_iso3 = country_iso3
        self.year = year
        self.indicators = {}

    def __str__(self):
        indicators_str = ','.join(f"{value}" for value in self.indicators.values())
        return f"{self.name},{self.country_iso3},{self.year},{indicators_str}"
```

The class takes in the indicators as a json, so I can change them more easily and add more if I ever need to. When a `CountryYear` object is printed out, it returns the variables in CSV format which makes creating the final CSV with all the data much simpler and easier.

## API Call

When you make a get request to the World Bank API (using the indicator endpoint), it returned a json with the data for every country and the corresponding indicator value. I wanted to initialize the CountryYear objects with all of indicator data, but there was no endpoint for calling multiple indicators on one country. Instead, I had to call the endpoint for each of the indicators and add the data to a CountryYear object that I had already made. 

The base format of the requested data is in xml, so I had to change it to JSON using the param: `{"format": "json"}`. The other parameter I used was per_page and set it to 17024 (the total number of country year entries), so I only had to call the endpoint once per indicator. 

```python
BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/"
DEFAULT_PARAMS = {"format": "json", "per_page": 17024}

def get_world_bank_data(indicator):
    try:
        response = requests.get(BASE_URL + indicator, params=DEFAULT_PARAMS)
        response.raise_for_status()
        data = response.json()[1]
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not retrieve data - {e}")
```

I needed the line `data = response.json()[1]` because the data returned was an array with the first element detailing the metadata about the request (number of entries, number of pages, etc.). I only wanted the main data about the countries and years which was stored in the second element of the array (index 1).

## Storing the Data

The previous function only got the data by making a call to the api. Now, I needed to store the data in a CountryYear object, to later construct the CSV and find the correlations between the indicators. Like I said, I couldn't just call one endpoint for multiple indicators, which made creating the objects a bit harder, so I had to make a json with all the objects and make a key that could let me access to needed object again later. When process_indicator is called the first time, the CountryYear object is created. Every future function call just adds the indicator value to the existing object.

```python
def process_indicator(indicator, id, results):
    data = get_world_bank_data(id)
    if data:
        data = data[3136:]
        for row in data:
            key = (row['countryiso3code'], row['date'])
            if key not in results:
                results[key] = CountryYear(
                    row['country']['value'], row['countryiso3code'], row['date'])
            results[key].indicators[indicator] = row['value']
```

I had to skip the first 3136 entries in the data, which seems like a completely magic number. However, when I first printed out the CSV, I noticed that many of the countries in the beginning weren't really countries but rather regions or types of countries (Ex. high income, fragile, etc.). I didn't want to include these pseudo-countries, as I thought they might distort the data, so I skipped every entry up until Afghanistan (when the real countries started alphabetically). I would have liked to make the skip number a variable that is correlated with the number of entries in the json, but there wasn't any indicator in the json or data that would tell me how many pseudo-countries existed. As a result, I settled on simply hard-coding the number.

Some years (like 2023) didn't have very complete data, but I didn't think it was worth filtering out, as many countries also had incomplete data. I could see how recording values for indicators in smaller or dangerous countries could be difficult, so I wasn't too worried about this empty data.

## Making the CSV

The next step of the program was to create the final csv. I just ran the `process_indicator` function for each indicator and then printed out the corresponding CountryYearObjects.

```python
def create_country_data(indicators):
    results = {}
    for indicator_name, indicator_id in indicators.items():
        process_indicator(indicator_name, indicator_id, results)
    return list(results.values())

print(f"Name, Iso3, Year, {list(INDICATORS)[0]}, {list(INDICATORS)[1]}, {list(INDICATORS)[2]}, {list(INDICATORS)[3]}, {list(INDICATORS)[4]}")
countries = create_country_data(INDICATORS)
for country in countries:
    print(country)
```

The print line before `create_country_data` is called serves as the header for the CSV. 

Once you run `python3 lab3.py > countries.csv`, you should get the complete csv file.

Here is the <a href="../assets/lab3.py" download>full python file</a>


