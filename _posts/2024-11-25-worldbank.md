---
layout: post
title: Country Indicators and Their Correlation
subtitle: How population, GDP, life expectancy, access to electricity, and literacy rates across the world's countries relate 
---

# World Bank Analysis

This blog post will discuss my use of the World Bank API and the country indicator which I chose, in an attempt to find correlation and relationships between certain variables.

## Indicators

I used the default `population`, `GDP`, and `life expectancy` indicators, as they would likely have a lot of data and complete information. In addition, I also chose `access to electricity` and `literacy rates`, under the assumption that the three other indicators (GDP, population, and life expectancy) would be correlated. A poorer country (lower GDP) would likely have worse education (lower literacy rates) and less people with electricity. I thought a similar trend would also exist in terms of population and life expectancy.

Each indicator had a corresponding id, which was used to call the api, so I made a dictionary containing the five indicators and their ids. This also made it easier to change the indicators if I ever wanted to because the rest of the code just referred to the generic keys and values of the dictionary.

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

Once you run `python3 lab3.py > countries.csv`, you should get the complete <a href="../assets/countries.csv" download>csv file</a>.

# What's Next?

Now that we have all of our data and the values for our indicators, we can start to look for correlation between the different indicators. The way we would accomplish this is by isolating two of the variables (labelling one as the independent and the other as the dependent variable) and finding the corresponding p-value. 

The p-value is a number, calculated from a statistical test, that describes how likely you are to have found a particular set of observations if the null hypothesis were true ([scribbr.com](https://www.scribbr.com/statistics/p-value/#:~:text=A%20p%2Dvalue%2C%20or%20probability,to%20perform%20your%20statistical%20test.)). Usually p-values are used to determine the statistical significance of data, or how strong the correlation is. A p-value of 0.05 indicates that the results of your test could only occur randomly 5% of the time (it is very likely your data is correlated). 

To find the p-values between my indicators, I used Ms.Feng's pythonanywhere api, which could return a p-value based on two lists of data. After making a POST request with all of my data using the https://ifenghm.pythonanywhere.com/upload endpoint, I could simply reference any two of my indicators and make a GET request to the https://ifenghm.pythonanywhere.com/analyze endpoint to determine the p-value.

Here is my implementation of this: 

```python
def upload_data(dataset, indicators, api_key):
    payload = {indicator: [country.indicators.get(indicator) for country in dataset]
               for indicator in indicators}
    
    response = requests.post('https://ifenghm.pythonanywhere.com/upload', headers={"apikey": api_key}, json=payload)
    response.raise_for_status()
    data = response.json()

    return data


def analyze_data(file_id, indicators, api_key):
    results = {}

    for i in range(len(indicators)):
        for j in range(i + 1, len(indicators)):
            key = (indicators[i], indicators[j])

            response = requests.get('https://ifenghm.pythonanywhere.com/analyze', headers={"apikey": api_key}, params={
                "independent": indicators[i],
                "dependent": indicators[j],
                "id": file_id,
            })
            response.raise_for_status()
            data = response.json()
            results[key] = data

    return results


file_id = upload_data(countries, INDICATORS.keys(), API_KEY)
results = analyze_data(file_id['id'], list(INDICATORS.keys()), API_KEY)
for result in results:
    print(f"{result}: {results[result]}")
```

With this capability in mind, there were, seemingly, two ways to approach finding correlation in the data.

## National Correlation

Since we have data spanning many years for most if not every country, we can isolate two of our indicators over the time range for a country and potentially find a correlation between, say, literacy and gdp in any given country we would like. 

We also could perform this action for each of the countries in the dataset and view how correlations may shift or change for data in different countries. While we know that the GDP in the US is higher than that of Yemen or Angola, we could also determine how much the US's GDP is correlated with life expectancy or literacy rates compared to either of those two countries.

The only issue with isolating the indicators by country is that many of the countries don't have data for the more niche statistics like access to electricity or literacy rates. This would make many of our p-values null or simply useless due to a lack of data.

Thus, there is an alternative, more general approach to finding correlation.

## International Correlation

This could also be titled Worldwide or Global Correlation, as we aren't gonna be comparing two countries in particular, but rather the data for every country in the world.

Ultimately, this was the correlation I decided to look at for two main reasons:

1) Incomplete data wouldn't have as much of an impact on the p-values and correlation between indicators as it would for each individual country. While the countries with data will have far more weight in our International Correlation, I will always, at the very least, come to a p-value and slope that can allow us to make some conclusions (even if not 100% accurate)

2) It is simply just easier to do it this way. The way Ms.Feng's api works is that it takes in your data and makes a file where you can analyze further and reveal the p-values. If I had looked at the correlation for each individual country, I would've had to make a POST request 100+ times and make 100+ files. It would be much harder to keep track of and likely force me to resort to calculating the p-values myself instead of calling the API.

With this in mind, here are the International p-values that I came to: 

```python 
('Population', 'Gdp'): {'p_value': 3.124887702710133e-05, 'slope': -6.225753518546791e-06}
('Population', 'Life_Expectancy'): {'p_value': 0.0005415952365919185, 'slope': 3.206104367224094e-09}
('Population', 'Electricity'): {'p_value': 0.21117418758464002, 'slope': 3.801492607233462e-09}
('Population', 'Literacy'): {'p_value': 0.7240046782670069, 'slope': 1.264726337985555e-09}
('Gdp', 'Life_Expectancy'): {'p_value': 0.0, 'slope': 0.00036129896100911275}
('Gdp', 'Electricity'): {'p_value': 0.0, 'slope': 0.0004812734896363415}
('Gdp', 'Literacy'): {'p_value': 0.0, 'slope': 0.0004075645051586706}
('Life_Expectancy', 'Electricity'): {'p_value': 0.0, 'slope': 2.794025627977996}
('Life_Expectancy', 'Literacy'): {'p_value': 0.0, 'slope': 1.5141211956118987}
('Electricity', 'Literacy'): {'p_value': 0.0, 'slope': 0.4041856194561441}
```

The two values in the key represent the independent and dependent variables. With so much data, the p-values almost all suggest some correlation, be it sometimes very, very tiny. In some cases, even, the p-value was equal to zero, meaning the value was so ridiculously small that the program simply rounded to zero (likely 10+ orders of magnitude smaller than 1).

## Conclusion

Immediately, I think many of these values or correlations can be disregarded. The slope for population vs. literacy rates is so small that it isn't worth considering. Same for population and life expectancy or access to electricity.

The issue is that population grows so much quicker than the other, more stable variables, so it's very hard to determine any real relationship. Additionally, the values for access to electricity and and literacy rates are in percentages which majorly skew the data. Percentages can, at a maximum, go up by 100 points, while Population likely goes up by thousands each year.

The two values that I found the most interesting, or worth looking at, were the p-values and slopes for both life expectancy vs.access to electricity and life expectancy vs. literacy rates. The reasons why these datasets work and produce a clear correlation is because all three values are relatively stable with  small changes, and logically it is likely these variables would change alongside one another. Access to electricity vs. literacy rates likely has an insignificant slope due to incomplete data or simply just not be correlated in the real world.

The correlation between life expectancy and both literacy rates and access to electricity make sense in the real world. It can be assumed that life expectancy is higher in richer, more educated countries which would both boost the dependent variables.

In the future, I would pick indicators that have more similar change or manipulate the units so the slope makes more sense. It is likely population was correlated with some of the other indicators, but its extreme growth rate skewed the slope significantly.

I put all of the code in snippets throughout this post, but, in case your interested, here is the <a href="../assets/lab3.py" download>full python file</a>.


