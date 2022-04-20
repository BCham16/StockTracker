# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 22:57:11 2021

@author: Brandon Chamberlain
"""
from datetime import datetime
from stock_class import Stock, DailyData
from account_class import Traditional, Robo
import matplotlib.pyplot as plt
import json
import csv


def add_stock(stock_list):
    userChoice = ""
    while userChoice != "0":
        print("Add Stock ---")
        tickerSymbol = input("Enter Ticker Symbol: ").upper()
        companyName = input("Enter Company Name: ").capitalize()
        numberOfShares = float(input("Enter Number of Shares: "))
        new_stock = Stock(tickerSymbol, companyName, numberOfShares)
        stock_list.append(new_stock)
        userChoice = (input("Press enter to add another stock or 0 to exit: "))
      

# Remove stock and all daily data
def delete_stock(stock_list):
    print("Delete Stock ----")
    print("Stock List: [", end="") #(do not start a new line at the end)
    for i in stock_list:
        print(i.symbol, end=" ") #(do not start a new line at the end)
    #output “]” (end the stock list)
    print("]")
    symbol = input("Enter Symbol to delete: ").upper() #(convert to upper case)
    found = False
    i = 0
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            stock_list.pop(i)
        i += 1
    if found == True:
        print("Deleted {}".format(stock.symbol))
    else:
        print("Error: Symbol not found.")
    _ = input("Press Enter to continue")
    
    
# List stocks being tracked
def list_stocks(stock_list):
    print("\nStock List ----")
    print("Symbol\t\t\tName\t\t\tShares")
    print("========================================")
    for i in stock_list:
        print(i.symbol," " * (14-len(str(i.symbol))),i.name," " * (14-len(str(i.name))),i.shares)
    print()
    _ = input("Press Enter to continue\n")
    
# Add Daily Stock Data
def add_stock_data(stock_list):
    print("Add Daily Stock Data ----")
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol," ",end="")
    print("]")
    symbol = input("Which stock do you want to use?: ").upper()
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            current_stock = stock
    if found == True:
        print("Ready to add data for: ",symbol)
        print("Enter Data Separated by Commas - Do Not use Spaces")
        print("Enter a Blank Line to Quit")
        print("Enter Date,Price,Volume")
        print("Example: 8/28/20,47.85,10550")
        data = input("Enter Date,Price,Volume: ")
        while data != "":
            date, price, volume = data.split(",")
            daily_data = DailyData(date,float(price),float(volume))
          
            current_stock.add_data(daily_data)
            data = input("Enter Date,Price,Volume: ")
        print("Date Entry Complete")
    else:
        print("Symbol Not Found ***")
    _ = input("Press Enter to Continue ***")

    
def investment_type(stock_list):
    print("Investment Account ---")
    balance = float(input("What is your initial balance: "))
    number = input("What is your account number: ")
    acct= input("Do you want a Traditional (t) or Robo (r) account: ")
    if acct.lower() == "r":
        years = float(input("How many years until retirement: "))
        robo_acct = Robo(balance, number, years)
        print("Your investment return is ",robo_acct.investment_return())
        print("\n\n")
    elif acct.lower() == "t":
        trad_acct = Traditional(balance, number)
        temp_list=[]
        print("Choose stocks from the list below: ")
        while True:
            print("Stock List: [",end="")
            for stock in stock_list:
                print(stock.symbol," ",end="")
            print("]")
            symbol = input("Which stock do you want to purchase, 0 to quit: ").upper()
            if symbol =="0":
                break
            shares = float(input("How many shares do you want to buy?: "))
            found = False
            for stock in stock_list:
              if stock.symbol == symbol:
                  found = True
                  current_stock = stock
            if found == True:
                current_stock.shares += shares 
                temp_list.append(current_stock)
                print("Bought ",shares,"of",symbol)
            else:
                print("Symbol Not Found ***")
        trad_acct.add_stock(temp_list)


# Function to create stock chart
def display_stock_chart(stock_list,symbol):
    # create a list called date
    date = []
    # create a list called price
    price = []
    # create a list called volume
    volume = []
    # set company to “”
    company = ""
    # for each stock in stock_list
    for stock in stock_list:
    #   if stock.symbol = symbol
     	if stock.symbol == symbol:
    # 		set company to stock.name
            company = stock.name
    # 		for each dailyData in stock.DataList
            for dailyData in stock.DataList:
                date.append(dailyData.date)
                price.append(dailyData.close)
                volume.append(dailyData.volume)
    # call plt.plot() passing date, price
    plt.plot(date, price)
    # call plt.xlabel() passing ‘Date’
    plt.xlabel(date)
    # call plt.ylabel() passing ‘Price’
    plt.ylabel(price)
    # call plt.title() passing company
    plt.title(company)
    # call plt.show()
    plt.show()
    


# Display Chart
def display_chart(stock_list):
    # output “Stock List: [“ (do not start a new line at the end)
    print('Stock List: [', end='')
    # for each stock in stock_list
    for stock in stock_list:
        # output stock.symbol + “ “ (do not start a new line at the end)
        print(stock.symbol + " ", end='')
    # output “]” (end the stock list)
    print("]")
    # input symbol (convert to upper case)
    symbol = input().upper()
    # set found to False
    found = False
    # for each stock in stock_list
    for stock in stock_list:
    # 	if stock.symbol = symbol then
        if stock.symbol == symbol:
    # 		set found to true
            found = True
    # current_stock = stock
            current_stock = stock
    # if found = True
    if found == True:
    # 	call display_stock_chart() and pass in stock_list, symbol
        display_stock_chart(stock_list, symbol)
    # else
    else:
    # 	output error message for symbol not found
        print('Symbol not found')
    # pause and prompt the user to press Enter to continue
    _ = input('Press Enter to continue')

  
    
#object encoder and decoder pasted here
def data_encoder(obj):
    data_dict = dict(date=obj.date, close = obj.close, volume = obj.volume)
    return data_dict

def obj_encoder(obj):
        dlist = []
        for o in obj.DataList:
            d = data_encoder(o)
            dlist.append(d)
        stock_dict = dict(symbol=obj.symbol, name = obj.name, shares = obj.shares, DataList = dlist)
        return stock_dict

def obj_decoder(obj):
        symbol = obj["symbol"]
        name = obj["name"]
        shares = obj["shares"]
        DL = obj["DataList"]
        objStock = Stock(symbol, name, shares)
        for o in DL:
            d = o['date']
            c = o['close']
            v = o['volume']
            dd = DailyData(d,c,v)
            objStock.add_data(dd)
        return objStock


def file_processing(stock_list):
#     set json_dict to {}
    json_dict = {}
# set choice to “”
    choice = ""
# while choice is not “E”
    while choice != "E":
        print("Please select an option:")
        print("(S)ave Data")
        print("(L)oad Data")
        print("Import (D)ata")
        print("(E)xit")
# prompt the user if they want to save data (S), load data (L), import data (D) or exit (E) set to upper() and save to choice
        choice = input("Enter Selection: ").upper()
        
# 	if choice is “S”
        if choice == 'S':
    # 		use a list comprehension to encode each stock
            json_list = [obj_encoder(stock) for stock in stock_list]
    #       Add the list to a python dictionary
            json_dict["Stock"]=json_list 
            try:
                with open("stock_data.json", "w") as f:
    #  				dump the json_dict to f 
                    json.dump(json_dict,f,indent=4)
    # 			output a suitable message stating the file was saved
                print('\nFile saved successfully: stock_data.json') 
            except IOError:
    # 			output a suitable message stating the file was not created
                print('Error saving file.') 
                raise SystemExit
                 
        
        elif choice == 'L': 
            try: 
                with open('stock_data.json', 'r') as f:
    # 				read in the file to str_file
                    str_file = f.read()   
    # 				replace all ‘ with “ in str_file
                    str_file = str_file.replace("\'", "\"")
    # 				use json.loads to load the str_file and save it to stock_obj 
                    stock_obj = json.loads(str_file)
                    for s in stock_obj['Stock']:
    # 					use the object decoder to decode s 
                        temp = obj_decoder(s)
    # 					append temp to the stock_list
                        stock_list.append(temp)
    # 			output a suitable message stating the file was loaded from stock_data.json
                print('\nData loaded from file stock_data.json successfully.') 
            except IOError:
    # 			output a suitable message stating the file was not created
                print('Error loading file.') 
                raise SystemExit
                   
        elif choice == 'D':
    # 		output a suitable message stating that historical data will be added
            print('\nAdd historical data to a stock in the stock list') 
            symbol = input('Enter stock ticker symbol: ').upper() 
    # 		input filename
            filename = input('Enter the file name: ') 
            import_stock_csv(stock_list, symbol, filename)
            display_report(stock_list, symbol)

                
# Get price and volume history from Yahoo! Finance using CSV import.
def import_stock_csv(stock_list,symbol,filename): #18:15
    for stock in stock_list:
            if stock.symbol == symbol:
                with open(filename, newline='') as stockdata:
                    datareader = csv.reader(stockdata,delimiter=',')
                    next(datareader)
                    for row in datareader:
                        daily_data = DailyData(str(row[0]),float(row[4]),float(row[6]))
                        stock.add_data(daily_data)

    
# Display Report for All Stocks
def display_report(stock_list, symbol):

    print("Stock Report ---")
    for stock in stock_list:
        if stock.symbol == symbol:
            print("Report for: ",stock.symbol,stock.name)
            print("Shares: ", stock.shares)
            count = 0
            price_total = 0.00
            volume_total = 0
            lowPrice = 999999.99
            highPrice = 0.00
            lowVolume = 999999999999
            highVolume = 0
           
            for daily_data in stock.DataList: 
                count = count + 1
                price_total = price_total + daily_data.close
                volume_total = volume_total + daily_data.volume
                if daily_data.close < lowPrice:
                    lowPrice = daily_data.close
                if daily_data.close > highPrice:
                    highPrice = daily_data.close
                if daily_data.volume < lowVolume:
                    lowVolume = daily_data.volume
                if daily_data.volume > highVolume:
                    highVolume = daily_data.volume

                priceChange = highPrice - lowPrice
                print(daily_data.date,daily_data.close,daily_data.volume)
            if count > 0:
                print("Summary ---",)
                print("Low Price:", "${:,.2f}".format(lowPrice))
                print("High Price:", "${:,.2f}".format(highPrice))
                print("Average Price:", "${:,.2f}".format(price_total/count))
                print("Low Volume:", lowVolume)
                print("High Volume:", highVolume)
                print("Average Volume:", "${:,.2f}".format(volume_total/count))
                print("Change in Price:", "${:,.2f}".format(priceChange))
                print("Profit/Loss","${:,.2f}".format(priceChange * stock.shares))
            else:
                print("*** No daily history.")
            print("\n\n\n")
    print("--- Report Complete ---")
    _ = input("Press Enter to Continue")    

    
def main_menu(stock_list):
    option = ""
    while True:
        print("Stock Analyzer ---")
        print("1 - Add Stock")
        print("2 - Delete Stock")
        print("3 - List stocks")
        print("4 - Add Daily Stock Data (Date, Price, Volume)")
        print("5 - Show Chart")
        print("6 - Investor Type")
        print("7 - Save/Load Data")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        if option =="0":
            print("Goodbye")
            break
        
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            delete_stock(stock_list)
        elif option == "3":
            list_stocks(stock_list)
        elif option == "4":
           add_stock_data(stock_list) 
        elif option == "5":
            display_chart(stock_list)
        elif option == "6":
            investment_type(stock_list)
        elif option == "7":
            file_processing(stock_list)
        else:
            
            print("Goodbye")

# Begin program
def main():
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()

