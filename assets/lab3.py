import requests


class CountryYear:
    def __init__(self, name, country_iso3, year):
        self.name = name
        self.country_iso3 = country_iso3
        self.year = year
        self.indicators = {}

    def __str__(self):
        indicators_str = ', '.join(f"{value}" for value in self.indicators.values())
        return f"{self.name}, {self.country_iso3}, {self.year}, {indicators_str}"

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


def create_country_data(indicators):
    results = {}
    for indicator_name, indicator_id in indicators.items():
        process_indicator(indicator_name, indicator_id, results)
    return list(results.values())

INDICATORS = {
        "Population": "SP.POP.TOTL",
        "Gdp": "NY.GDP.PCAP.CD",
        "Life_Expectancy": "SP.DYN.LE00.IN",
        "Electricity": "EG.ELC.ACCS.ZS",
        "Literacy": "SE.ADT.1524.LT.ZS",
    }


print(f"Name, Iso3, Year, {list(INDICATORS)[0]}, {list(INDICATORS)[1]}, {list(INDICATORS)[2]}, {list(INDICATORS)[3]}, {list(INDICATORS)[4]}")
countries = create_country_data(INDICATORS)
# for country in countries:
#     print(country)