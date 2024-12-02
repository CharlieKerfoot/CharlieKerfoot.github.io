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
            name = row['country']['value']
            if (row['country']['value'].find(',') != -1):
                name = row['country']['value'].split(',')[0]
            if key not in results:
                results[key] = CountryYear(
                    name, row['countryiso3code'], row['date'])
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
for country in countries:
   print(country)


API_KEY = "60aLDfoyewOG5tnPoRVKQjNUXTCYEFW9XQDyZi4jpny610UgkK0xZL13TOsNnWeN"


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
#for result in results:
#    print(f"{result}: {results[result]}")
