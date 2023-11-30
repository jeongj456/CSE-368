import csv
import matplotlib.pyplot as plt
import numpy as np


#Create dictionaries
ASPUS_dict = {} #{year: total average house price per year}
HPI_dict = {} #{year: house price index per year}
IR_dict = {} #{year: interest rate per year}
ADJUSTED_dict = {} #{year: calculated house price per year}
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
print("start")
print(f'ASPUS: {ASPUS_dict}' + "\n")
#print("\n")
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
print(f'House Price Index: {HPI_dict}' + "\n")
#print("\n")

#Store interest rate per year in our IR_dict
def interest_rates():
    with open("Interest_Rates.csv", "r") as file:
        reader = csv.reader(file)
        next(reader) #skip the header line
        for row in reader:
            IR_dict[row[0]]= float(row[1].strip())

interest_rates()
print(f'Interest Rates: {IR_dict}'+ "\n")


"""
From 1975 - 2022
-Take the average house price for every year, multiply it by the (1 + interest rate)
-Take the House Price Index, and since it is a percentage, divide it by 100 
to get it into decimal form, square the value
    -If it is greater than 0, (1 + HPI) * house price
    -If the HPI is a negative number, (1 - HPI) * house price


Since the average house price that we began with was just the cost of the house, we did the calculations to 
account for the additional costs of the interest rate, inflation year to year, and the gain/loss of the value of the property over time
"""

def calc_function():
    for year in ASPUS_dict:
        if int(year) > 1975 and int(year) < 2023:
            ASPUS_dict[year] = ASPUS_dict[year] * (1 + IR_dict[year])
            HPI = (HPI_dict[year]/100) ** 2
            if (HPI) > 0:
                ASPUS_dict[year] = ((1 + HPI) * ASPUS_dict[year])
            elif (HPI) < 0:
                ASPUS_dict[year] = ((1 - HPI) * ASPUS_dict[year])

calc_function()
for i in range(1975, 2023):
    ADJUSTED_dict[str(i)] = ASPUS_dict[str(i)]

print(f'Adjusted_dict: {ADJUSTED_dict}' + '\n')
y  =  list(x for x in ADJUSTED_dict.values()) #house prices
x  =  list(int(x) for x in ADJUSTED_dict.keys()) #years
print(f"Ajusted x: {x}" + "\n")
print(f"Ajusted y: {y}" + "\n")
print("****************************************END****************************************************")

#----------------------------------total line of best fit----------------------------------------------
#define data
x = np.array(x) #years
y = np.array(y) #house prices

#find line of best fit
a, b = np.polyfit(x, y, 1)
print(f'Linear Regression Model for True Average House Prices: y = {a}x + {b}')
#add points to plot
plt.scatter(x, y)

#add line of best fit to plot
plt.plot(x, a*x+b) 

#plot the individual data points
plt.plot(x,y)
plt.title("Linear Regression of House Prices in the U.S.")
plt.xlabel("Year")
plt.ylabel("Average House Price")
plt.xticks(rotation = 25)
plt.grid()
plt.show()
