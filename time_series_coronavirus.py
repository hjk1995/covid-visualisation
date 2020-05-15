import numpy as np
import pandas as pd
import requests
import io


class CoronaVirusStats:

    def __init__(self):
        RECOVERED = 'Recovered'
        DEATH = 'Deaths'
        CONFIRMED = 'Confirmed'
        INFECTED = 'Infected'

        confirmed_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
        confirmed_data = pd.read_csv(confirmed_url)
        death_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
        death_data = pd.read_csv(death_url)
        recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
        recovered_data = pd.read_csv(recovered_url)

        LAST_COLUMN = confirmed_data.columns[-1]

        confirm_dataset = pd.DataFrame(confirmed_data,
                                       columns=['Province/State', 'Country/Region', 'Lat', 'Long', LAST_COLUMN]).rename(
            columns={LAST_COLUMN: CONFIRMED})
        death_dataset = pd.DataFrame(death_data,
                                     columns=['Province/State', 'Country/Region', 'Lat', 'Long', LAST_COLUMN]).rename(
            columns={LAST_COLUMN: DEATH})
        recover_dataset = pd.DataFrame(recovered_data,
                                       columns=['Province/State', 'Country/Region', 'Lat', 'Long', LAST_COLUMN]).rename(
            columns={LAST_COLUMN: RECOVERED})
        merged_dataset = confirm_dataset.merge(death_dataset,
                                               on=['Province/State', 'Country/Region', 'Lat', 'Long']).merge(
            recover_dataset, on=['Province/State', 'Country/Region', 'Lat', 'Long'])

        merged_dataset[INFECTED] = merged_dataset[CONFIRMED] - merged_dataset[DEATH] - merged_dataset[RECOVERED]
        merged_dataset['Country/Region'] = merged_dataset['Country/Region'].replace('Mainland China', 'China')
        merged_dataset[['Province/State']] = merged_dataset[['Province/State']].fillna('NA')
        merged_dataset[[CONFIRMED, DEATH, RECOVERED, INFECTED]] = merged_dataset[
            [CONFIRMED, DEATH, RECOVERED, INFECTED]].fillna(0)

        confirmed_data_latest = confirmed_data.groupby('Country/Region').sum().reset_index()
        confirmed_data_latest = confirmed_data_latest[confirmed_data_latest['Country/Region'] == 'US']
        confirmed_data_latest.head(100)

        dataset_copy = merged_dataset.groupby(['Country/Region'])[
            'Province/State', CONFIRMED, DEATH, RECOVERED, INFECTED].sum()
        self.stats = merged_dataset.groupby(['Country/Region'])[CONFIRMED, DEATH, RECOVERED, INFECTED].sum()
        self.stats = self.stats.sort_values(CONFIRMED, ascending=False)
        self.stats = self.stats.reset_index()

    def extractDataFromCountry(self, country):
        country_data = self.stats[self.stats['Country/Region'] == country]
        return country_data

covid = CoronaVirusStats()
df=covid.extractDataFromCountry('India')
print(df)
print(df['Confirmed'].iloc[0])