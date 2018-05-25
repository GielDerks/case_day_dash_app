from Wrapper import Wrapper
import pandas as pd
import csv
import pprint
import numpy as np

from unidecode import unidecode


def remove_non_ascii(text):
    return unidecode(str(text))

# initalize program and ask for information to start retrieve data from the API of overheid.io
#company = Wrapper('Bejo Zaden B.V.')  # Test gemeente Utrecht, #Test Triple - A rk finance

#companies = dict([(name, Wrapper(name).data) for name in ['AB WERKT DETACHERING B.V.']])

input_file = pd.read_excel('to_do_profile.xlsx')

# company_list = input_file['BEDRIJVEN']
#
# for x in company_list:
#     print (x)
lister = list(np.arange(982,1058,25))

for g in lister:
    w = g + 1



    start_from = str(w)

    start_from_name = 'ouput_' + start_from + '.csv'
    csv_file = open(start_from_name, 'w')

    data_writer = csv.writer(csv_file, delimiter=';')
    data_writer.writerow(['BEDRIJF_INPUT', 'VESTIGING', 'bagId', 'city', 'country', 'gpslat',
                   'gpslon', 'housenumber', 'houseNumberAddition','postalCode', 'rijksdriehoekX', 'rijksdriehoekY', 'rijksdriehoekZ',
                   'street', 'type', 'branchNumber', 'isMainSbi', 'sbiCode', 'sbiCodeDescription', 'employees',
                   'foundationDate', 'hasCommercialActivities', 'hasEntryInBusinessRegister', 'hasNonMailingIndication',
                   'isBranch', 'isLegalPerson', 'isMainBranch', 'kvkNumber', 'legalForm', 'registrationDate', 'rsin',
                   'businessName', 'currentStatutoryNames', 'currentTradeNames', 'shortBusinessName', 'fuzzy_match_score',
                   'matched_company_name', 'pass_fail', 'succesfull_profile'])

    csv_file4 = open('companies_large.csv', 'a')
    data_writer4 = csv.writer(csv_file, delimiter=';')


    count = int(start_from)

    for x in range(int(start_from), len(input_file)):

        try:


            if input_file['TO_DO'].iloc[x] == "NO":
                print(" SKIP")
                count+=1

                continue

            company = input_file['BEDRIJVEN'].iloc[x]
            company2 = company.replace(",", " ")
            print("MAIN INPUT ---> ", company)

            data_main = Wrapper(company).data


            data = data_main['data']
            print(data)

            if data == "Too many items":
                csv_file4.write(company + "\n")
                continue


            pass_fail = data_main['succesfull']


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
                        data_main['matched_company_name'],
                        pass_fail,
                        data[subcompanies]['succesfull_profile'],
                     ]

                print(row)

                row = [remove_non_ascii(x) for x in row]

                data_writer.writerow(row)

            if count == g + 25:
                break

            count += 1

        except:
            csv_file4.write(company + "\n")
            data_writer.writerow([company,
                        " ", '', '','', ' ', ' ', ' ', ' ',
                                  ' ', ' ', ' ', ' ', ' ',
                                  ' ', ' ',
                                  ' ', ' ', ' ', ' ', ' ', ' ',
                                  ' ',
                                  ' ', ' ', '',
                                  ' ',
                                  '', ' ', ' ', ' ', ' ', ' ',
                                  ' ',
                                  ' ', ' ', '', ' ',
                                  ' '])
            if count == g + 25:
                break

            count += 1
            pass

csv_file.close()
csv_file4.close()


csv = pd.read_csv(start_from_name, delimiter=';')

# csv.columns = ['BEDRIJF_INPUT', 'VESTIGING', 'bagId', 'city', 'country', 'gpslat',
#                'gpslon', 'housenumber', 'houseNumberAddition','postalCode', 'rijksdriehoekX', 'rijksdriehoekY', 'rijksdriehoekZ',
#                'street', 'type', 'branchNumber', 'isMainSbi', 'sbiCode', 'sbiCodeDescription', 'employees',
#                'foundationDate', 'hasCommercialActivities', 'hasEntryInBusinessRegister', 'hasNonMailingIndication',
#                'isBranch', 'isLegalPerson', 'isMainBranch', 'kvkNumber', 'legalForm', 'registrationDate', 'rsin',
#                'businessName', 'currentStatutoryNames', 'currentTradeNames', 'shortBusinessName', 'fuzzy_match_score',
#                'matched_company_name']

start_from_name = '/Users/gielderks/Downloads/Code/Final_excel/profilersinput/ouput_' + start_from + '_till_' + str(count) + '.csv'
csv.to_csv(start_from_name, index=False)


# pprint.pprint(companies)
