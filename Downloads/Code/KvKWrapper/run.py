from Wrapper import Wrapper
import pandas as pd
import csv
import pprint

# initalize program and ask for information to start retrieve data from the API of overheid.io
#company = Wrapper('Bejo Zaden B.V.')  # Test gemeente Utrecht, #Test Triple - A rk finance

#companies = dict([(name, Wrapper(name).data) for name in ['AB WERKT DETACHERING B.V.']])

input_file = pd.read_excel('workfile2016_clean.xlsx')

# company_list = input_file['BEDRIJVEN']
#
# for x in company_list:
#     print (x)

start_from = str(0)

start_from_name = 'ouput_' + start_from + '.csv'
csv_file = open(start_from_name, 'w')

data_writer = csv.writer(csv_file, delimiter=';')
count = int(start_from)

for x in range(int(start_from), len(input_file)):

    company = input_file['BEDRIJVEN'].iloc[x]

    print("MAIN INPUT ---> ", company)

    data_main = Wrapper(company).data

    data = data_main['data']

    for subcompanies in data:
        print("SUB INPUT ---> ", subcompanies)

        row = [company,
                subcompanies,
                data[subcompanies]['addresses'][0].get('bagId'),
                data[subcompanies]['addresses'][0].get('city'),
                data[subcompanies]['addresses'][0].get('country'),
                data[subcompanies]['addresses'][0].get('gpsLatitude'),
                data[subcompanies]['addresses'][0].get('gpsLongitude'),
                data[subcompanies]['addresses'][0].get('houseNumber'),
                data[subcompanies]['addresses'][0].get('houseNumberAddition'),
                data[subcompanies]['addresses'][0].get('postalCode'),
                data[subcompanies]['addresses'][0].get('rijksdriehoekX'),
                data[subcompanies]['addresses'][0].get('rijksdriehoekY'),
                data[subcompanies]['addresses'][0].get('rijksdriehoekZ'),
                data[subcompanies]['addresses'][0].get('street'),
                data[subcompanies]['addresses'][0].get('type'),
                data[subcompanies]['branchNumber'],
                data[subcompanies]['businessActivities'][0]['isMainSbi'],
                data[subcompanies]['businessActivities'][0]['sbiCode'],
                data[subcompanies]['businessActivities'][0]['sbiCodeDescription'],
                data[subcompanies]['employees'],
                data[subcompanies]['foundationDate'],
                data[subcompanies]['hasCommercialActivities'],
                data[subcompanies]['hasEntryInBusinessRegister'],
                data[subcompanies]['hasNonMailingIndication'],
                data[subcompanies]['isBranch'],
                data[subcompanies]['isLegalPerson'],
                data[subcompanies]['isMainBranch'],
                data[subcompanies]['kvkNumber'],
                data[subcompanies]['legalForm'],
                data[subcompanies]['registrationDate'],
                data[subcompanies]['rsin'],
                data[subcompanies]['tradeNames']['businessName'],
                data[subcompanies]['tradeNames']['currentStatutoryNames'],
                data[subcompanies]['tradeNames']['currentTradeNames'],
                data[subcompanies]['tradeNames']['shortBusinessName'],
                data_main['fuzzy_match_score'],
                data_main['matched_company_name']
             ]
        print(row)
        data_writer.writerow(row)
    if count == 10:
        break
    count += 1

csv_file.close()

csv= pd.read_csv(start_from_name, header=None, delimiter=';')
csv.columns = ['BEDRIJF_INPUT', 'VESTIGING', 'bagId', 'city', 'country', 'gpslat',
               'gpslon', 'housenumber', 'houseNumberAddition','postalCode', 'rijksdriehoekX', 'rijksdriehoekY', 'rijksdriehoekZ',
               'street', 'type', 'branchNumber', 'isMainSbi', 'sbiCode', 'sbiCodeDescription', 'employees',
               'foundationDate', 'hasCommercialActivities', 'hasEntryInBusinessRegister', 'hasNonMailingIndication',
               'isBranch', 'isLegalPerson', 'isMainBranch', 'kvkNumber', 'legalForm', 'registrationDate', 'rsin',
               'businessName', 'currentStatutoryNames', 'currentTradeNames', 'shortBusinessName', 'fuzzy_match_score',
               'matched_company_name']
start_from_name = 'ouput_' + start_from + '_till_' + str(count) + '.xlsx'
csv.to_excel(start_from_name, index=False)


# pprint.pprint(companies)
