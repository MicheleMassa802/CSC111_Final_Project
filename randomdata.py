"""CSC111 Winter 2021 Course Project: API Data Storage

Authors: Michele Massa, Nischal Nair, Nathan Zavys-Cox

Description: This module contains data obtained from the Skyscanner Flight Search API to be used
to fetch the data from the api since it takes certain country codes instead of country names.
countries_to_codes was first obtained as json data from the api's valid countries and codes
request then converted into a dict seen below. The other dict is used as saved api request data
to make sure we have the data and it works properly in the functions so there aren't http request
errors if the api goes down and it is used to speed up our program by storing the data instead of
fetching it.

This file is copyright (c) 2021 Michele Massa, Nischal Nair and Nathan Zavys-Cox."""

# Each country mapped to its code to be used in the api.
# This was data was returned from the api and converted into this dict.
COUNTRIES_TO_CODES = {'Puerto Rico': 'PR', 'Portugal': 'PT', 'Palau': 'PW', 'Paraguay': 'PY',
                      'Qatar': 'QA',
                      'Andorra': 'AD', 'United Arab Emirates': 'AE', 'Afghanistan': 'AF',
                      'Antigua and Barbuda': 'AG',
                      'Anguilla': 'AI', 'Albania': 'AL', 'Armenia': 'AM', 'Angola': 'AO',
                      'Antarctica': 'AQ',
                      'Argentina': 'AR', 'American Samoa': 'AS', 'Austria': 'AT', 'Reunion': 'RE',
                      'Australia': 'AU',
                      'Aruba': 'AW', 'Azerbaijan': 'AZ', 'Romania': 'RO',
                      'Bosnia and Herzegovina': 'BA',
                      'Barbados': 'BB', 'Serbia': 'RS', 'Bangladesh': 'BD', 'Belgium': 'BE',
                      'Russia': 'RU',
                      'Burkina Faso': 'BF', 'Bulgaria': 'BG', 'Rwanda': 'RW', 'Bahrain': 'BH',
                      'Burundi': 'BI',
                      'Benin': 'BJ', 'Saint Barthelemy': 'BL', 'Bermuda': 'BM', 'Brunei': 'BN',
                      'Bolivia': 'BO',
                      'Saudi Arabia': 'SA', 'Caribbean Netherlands': 'BQ', 'Solomon Islands': 'SB',
                      'Brazil': 'BR',
                      'Seychelles': 'SC', 'Bahamas': 'BS', 'Sudan': 'SD', 'Bhutan': 'BT',
                      'Sweden': 'SE',
                      'Singapore': 'SG', 'Botswana': 'BW', 'St. Helena': 'SH', 'Slovenia': 'SI',
                      'Belarus': 'BY',
                      'Belize': 'BZ', 'Slovakia': 'SK', 'Sierra Leone': 'SL', 'Senegal': 'SN',
                      'Somalia': 'SO',
                      'Canada': 'CA', 'Suriname': 'SR', 'Cocos (Keeling) Islands': 'CC',
                      'South Sudan': 'SS',
                      'DR Congo': 'CD', 'Sao Tome and Principe': 'ST',
                      'Central African Republic': 'CF',
                      'El Salvador': 'SV', 'Congo': 'CG', 'Switzerland': 'CH', 'St Maarten': 'SX',
                      'Ivory Coast': 'CI',
                      'Syria': 'SY', 'Swaziland': 'SZ', 'Cook Islands': 'CK', 'Chile': 'CL',
                      'Cameroon': 'CM',
                      'China': 'CN', 'Colombia': 'CO', 'Costa Rica': 'CR',
                      'Turks and Caicos Islands': 'TC',
                      'Chad': 'TD', 'Cuba': 'CU', 'Cape Verde': 'CV', 'Togo': 'TG', 'Curacao': 'CW',
                      'Thailand': 'TH',
                      'Christmas Island': 'CX', 'Cyprus': 'CY', 'Tajikistan': 'TJ',
                      'Czech Republic': 'CZ',
                      'East Timor': 'TL', 'Turkmenistan': 'TM', 'Tunisia': 'TN', 'Tonga': 'TO',
                      'Turkey': 'TR',
                      'Trinidad and Tobago': 'TT', 'Germany': 'DE', 'Tuvalu': 'TV', 'Taiwan': 'TW',
                      'Djibouti': 'DJ',
                      'Tanzania': 'TZ', 'Denmark': 'DK', 'Dominica': 'DM',
                      'Dominican Republic': 'DO', 'Ukraine': 'UA',
                      'Uganda': 'UG', 'Algeria': 'DZ', 'United Kingdom': 'UK', 'Ecuador': 'EC',
                      'United States': 'US', 'United States of America': 'US',
                      'UAE': 'AE',
                      'Estonia': 'EE', 'Egypt': 'EG', 'Uruguay': 'UY', 'Uzbekistan': 'UZ',
                      'Vatican City': 'VA',
                      'Eritrea': 'ER', 'Saint Vincent and the Grenadines': 'VC', 'Spain': 'ES',
                      'Ethiopia': 'ET',
                      'Venezuela': 'VE', 'British Virgin Islands': 'VG', 'US Virgin Islands': 'VI',
                      'Vietnam': 'VN',
                      'Vanuatu': 'VU', 'Finland': 'FI', 'Fiji': 'FJ', 'Falkland Islands': 'FK',
                      'Micronesia': 'FM',
                      'Faroe Islands': 'FO', 'France': 'FR', 'Wallis and Futuna Islands': 'WF',
                      'Gabon': 'GA',
                      'Samoa': 'WS', 'Grenada': 'GD', 'Georgia': 'GE', 'French Guiana': 'GF',
                      'Guernsey': 'GG',
                      'Ghana': 'GH', 'Gibraltar': 'GI', 'Greenland': 'GL', 'Gambia': 'GM',
                      'Guinea': 'GN',
                      'Guadeloupe': 'GP', 'Equatorial Guinea': 'GQ', 'Greece': 'GR',
                      'South Georgia & South Sandwich Islands': 'GS', 'Guatemala': 'GT',
                      'Guam': 'GU',
                      'Guinea-Bissau': 'GW', 'Guyana': 'GY', 'Hong Kong': 'HK', 'Honduras': 'HN',
                      'Croatia': 'HR',
                      'Haiti': 'HT', 'Yemen': 'YE', 'Hungary': 'HU', 'Indonesia': 'ID',
                      'Mayotte': 'YT', 'Ireland': 'IE',
                      'Israel': 'IL', 'India': 'IN', 'South Africa': 'ZA', 'Iraq': 'IQ',
                      'Iran': 'IR', 'Iceland': 'IS',
                      'Italy': 'IT', 'Zambia': 'ZM', 'Zimbabwe': 'ZW', 'Jamaica': 'JM',
                      'Jordan': 'JO', 'Japan': 'JP',
                      'Kenya': 'KE', 'Kyrgyzstan': 'KG', 'Cambodia': 'KH', 'Kiribati': 'KI',
                      'Comoros': 'KM',
                      'Saint Kitts and Nevis': 'KN', 'Kosovo': 'KO', 'North Korea': 'KP',
                      'South Korea': 'KR',
                      'Kuwait': 'KW', 'Cayman Islands': 'KY', 'Kazakhstan': 'KZ', 'Laos': 'LA',
                      'Lebanon': 'LB',
                      'Saint Lucia': 'LC', 'Liechtenstein': 'LI', 'Sri lanka': 'LK',
                      'Liberia': 'LR', 'Lesotho': 'LS',
                      'Lithuania': 'LT', 'Luxembourg': 'LU', 'Latvia': 'LV', 'Libya': 'LY',
                      'Morocco': 'MA',
                      'Monaco': 'MC', 'Moldova': 'MD', 'Montenegro': 'ME', 'Madagascar': 'MG',
                      'Marshall Islands': 'MH',
                      'Republic of Macedonia': 'MK', 'Mali': 'ML', 'Myanmar': 'MM',
                      'Mongolia': 'MN', 'Macau': 'MO',
                      'Northern Mariana Islands': 'MP', 'Martinique': 'MQ', 'Mauritania': 'MR',
                      'Montserrat': 'MS',
                      'Malta': 'MT', 'Mauritius': 'MU', 'Maldives': 'MV', 'Malawi': 'MW',
                      'Mexico': 'MX',
                      'Malaysia': 'MY', 'Mozambique': 'MZ', 'Namibia': 'NA', 'New Caledonia': 'NC',
                      'Niger': 'NE',
                      'Nigeria': 'NG', 'Nicaragua': 'NI', 'Netherlands': 'NL', 'Norway': 'NO',
                      'Nepal': 'NP',
                      'Nauru': 'NR', 'Niue': 'NU', 'New Zealand': 'NZ', 'Oman': 'OM',
                      'Panama': 'PA', 'Peru': 'PE',
                      'French Polynesia': 'PF', 'Papua New Guinea': 'PG', 'Philippines': 'PH',
                      'Pakistan': 'PK',
                      'Poland': 'PL', 'St. Pierre and Miquelon': 'PM'}

# Saved data from the api calls to speed up creating the graph.
EDGE_DATA_FROM_API = {('Canada', 'United Kingdom'): 243,
                      ('Canada', 'United States of America'): 113, ('Canada', 'Brazil'): 432,
                      ('United States of America', 'Japan'): 308,
                      ('United States of America', 'United Kingdom'): 226,
                      ('United States of America', 'France'): 172,
                      ('United States of America', 'Nigeria'): 445,
                      ('United States of America', 'Brazil'): 150,
                      ('United States of America', 'Argentina'): 315, ('Argentina', 'Brazil'): 192,
                      ('Argentina', 'South Africa'): 892, ('Brazil', 'Nigeria'): 921,
                      ('Brazil', 'France'): 218, ('Brazil', 'South Africa'): 276,
                      ('United Kingdom', 'Russia'): 37, ('United Kingdom', 'Hong Kong'): 448,
                      ('United Kingdom', 'India'): 211, ('United Kingdom', 'Germany'): 16,
                      ('United Kingdom', 'UAE'): 73, ('United Kingdom', 'France'): 16,
                      ('France', 'Germany'): 30, ('France', 'Italy'): 16, ('Italy', 'Nigeria'): 440,
                      ('Italy', 'Egypt'): 33, ('Italy', 'Germany'): 17, ('Germany', 'Russia'): 72,
                      ('Russia', 'UAE'): 173, ('Russia', 'India'): 228, ('Russia', 'Japan'): 243,
                      ('Russia', 'China'): 269, ('Egypt', 'UAE'): 32, ('Egypt', 'Kenya'): 265,
                      ('Nigeria', 'Kenya'): 539, ('Nigeria', 'South Africa'): 510,
                      ('Kenya', 'UAE'): 257, ('Kenya', 'South Africa'): 392,
                      ('South Africa', 'India'): 133, ('UAE', 'India'): 37,
                      ('India', 'Singapore'): 125, ('India', 'Hong Kong'): 236,
                      ('India', 'Australia'): 322, ('China', 'Japan'): 242,
                      ('China', 'Singapore'): 156, ('China', 'Hong Kong'): 153,
                      ('Hong Kong', 'Australia'): 366, ('Hong Kong', 'Japan'): 75,
                      ('Hong Kong', 'Singapore'): 130, ('Singapore', 'Japan'): 162,
                      ('Singapore', 'Australia'): 102, ('Australia', 'Japan'): 290}


def get_countries_to_codes() -> dict:
    """ Returns a mapping of countries to their code to be used in the make request function.
    """
    return COUNTRIES_TO_CODES


def get_saved_prices() -> dict:
    """ Returns the saved api data for the edges
    """
    return EDGE_DATA_FROM_API


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E9999', 'E9998', 'R0913'],
        'extra-imports': [],
        'max-nested-blocks': 5
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()
