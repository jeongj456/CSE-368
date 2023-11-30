import csv
# import matplotlib.pyplot as plt
# import numpy as np
# from sklearn import datasets, linear_model
# from sklearn.metrics import mean_squared_error, r2_score


#Create dictionaries
ASPUS_dict = {} #{year: total average house price per year}
HPI_dict = {} #{year: house price index per year}
IR_dict = {} #{year: interest rate per year}

#Average all 4 data points in the ASPUS for each year - calculate the total average per year
def find_total_average_house_price():
    with open("ASPUS.csv", "r") as file:
        reader = csv.reader(file)
        next(reader) #skip the header line
        count = 0
        for row in reader:
            year = row[0].split("/")[2]
            if year not in ASPUS_dict.keys():
                ASPUS_dict[year]=int(row[1])
                count += 1
            else:
                ASPUS_dict[year] = ASPUS_dict[year]+int(row[1])
                count += 1
                if count == 4:
                    ASPUS_dict[year] = (ASPUS_dict[year]/4)
                    count = 0
        #This is due to 2023 only having 3 data points whereas all other years have 4
        ASPUS_dict[year] = (ASPUS_dict[year]/3)

#Test if we calculate average house price correctly
find_total_average_house_price()
print(f'ASPUS: {ASPUS_dict}' + '\n')
#1963 -> 19375
#1964 -> 20300
#2023 -> 507233.33

#Store house price index per year in our HPI_dict
def house_index():
    with open("House_Index.csv", "r") as file:
        reader = csv.reader(file)
        next(reader) #skip the header line
        for row in reader:
            HPI_dict[row[0]]=float(row[1].strip())

house_index()
print(f'House Price Index: {HPI_dict}' + '\n')

#Store interest rate per year in our IR_dict
def interest_rates():
    with open("Interest_Rates.csv", "r") as file:
        reader = csv.reader(file)
        next(reader) #skip the header line
        for row in reader:
            IR_dict[row[0]]= float(row[1].strip())

interest_rates()
print(f'Interest Rates: {IR_dict}')


"""
From 1975 - 2022
Take the average house price for every year, multiply it by the (1 + interest rate)
Take the House Price Index, and since it is a percentage, divide it by 100 to get it into decimal form and if it is greater than zero, (1 + HPI) * house price
If the HPI is a negative number, (1 - HPI) * house price
"""