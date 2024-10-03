import pandas as pd
import numpy as np

translation_dict = {
    'Россия': 'russian federation',
    'Армения': 'Armenia',
    'Португалия': 'Portugal',
    'Испания': 'Spain',
    'Молдова': 'Moldova',
    'Франция': 'France',
    'Германия': 'Germany',
    'Вьетнам': 'Vietnam',
    'Грузия': 'Georgia',
    'Азербайджан': 'Azerbaijan',
    'Чили': 'Chile',
    'Беларусь': 'Belarus',
    'Бельгия': 'Belgium',
    'США': 'United States',
    'Италия': 'Italy',
    'Южная Африка': 'South Africa',
    'Сербия': 'Serbia',
    'Турция': 'Turkey',
    'Греция': 'Greece',
    'Индия': 'India',
    'Израиль': 'Israel',
    'Латвия': 'Latvia',
    'Великобритания': 'United Kingdom',
    'Венгрия': 'Hungary',
    'Китай': 'China',
    'Болгария': 'Bulgaria',
    'Новая Зеландия': 'New Zealand',
    'Узбекистан': 'Uzbekistan',
    'Таиланд': 'Thailand',
    'Япония': 'Japan',
    'Украина': 'Ukraine',
    'Мексика': 'Mexico',
    'Марокко': 'Morocco',
    'Исландия': 'Iceland',
    'Индонезия': 'Indonesia',
    'Кения': 'Kenya',
    'Иран': 'Iran',
    'Нидерланды': 'Netherlands',
    'Австрия': 'Austria',
    'Польша': 'Poland',
    'Швейцария': 'Switzerland',
    'Швеция': 'Sweden',
    'Малайзия': 'Malaysia',
    'Абхазия': 'Abkhazia',
    'Шри-Ланка': 'Sri Lanka',
    'Аргентина': 'Argentina',
    'Австралия': 'Australia',
    'Сингапур': 'Singapore',
    'Бразилия': 'Brazil',
    'Маврикий': 'Mauritius',
    'Литва': 'Lithuania',
    'Киргизия': 'Kyrgyzstan',
    'Казахстан': 'Kazakhstan',
    'Хорватия': 'Croatia',
    'Пакистан': 'Pakistan',
    'Российская Федерация': 'Russian Federation',
    'Уругвай': 'Uruguay',
    'Египет': 'Egypt',
    'Южная Осетия': 'South Ossetia',
    'Корея': 'Korea',
    'Шотландия': 'Scotland',
    'Шотландия, Великобритания': 'Scotland',
    'Ирландия': 'Ireland',
    'Словакия': 'Slovakia',
    'Саудовская Аравия': 'Saudi Arabia',
    'Перу': 'Peru',
    'Эквадор': 'Ecuador',
    'Коста-Рика': 'Costa Rica',
    'Колумбия': 'Colombia',
    'Филиппины': 'Philippines',
    'Таджикистан': 'Tajikistan',
    'Тунис': 'Tunisia',
    'Доминикана': 'Dominica',
    'Доминиканская республика': 'Dominican Republic',
    'Барбадос': 'Barbados',
    'Финляндия': 'Finland',
    'Словения': 'Slovenia',
    'Чехия': 'Czech Republic',
    'Молдавия': 'Moldova',
    'Канада': 'Canada',
    'Дания': 'Denmark',
    'Республика Сербия': 'Serbia',
    'ОАЭ': 'UNITED ARAB EMIRATES',
    'Камерун': 'Cameroon',
    'Эстония': 'Estonia',
    'Гватемала': 'Guatemala'
}

for k in translation_dict.keys():
    translation_dict[k] = translation_dict[k].lower()

gdp_df = pd.read_csv('data/gdp.csv')

gdp_df['country'] = gdp_df['country'].str.lower()
gdp_dict = dict(zip(gdp_df['country'], gdp_df['gdp']))

gdp_df['gdp'] = gdp_df['gdp'].replace('no data', np.nan)
gdp_df['gdp'] = pd.to_numeric(gdp_df['gdp'])

def translate_country_name(country_name):
    return translation_dict.get(country_name, 'no data')
    
def get_country_gdp_per_capita(country):
    translated_country = translate_country_name(country)
    if country == 'Импорт' or country == 'Unknown':
        return gdp_df['gdp'].mean()
    return gdp_dict.get(translated_country)