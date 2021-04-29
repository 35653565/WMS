
import yahoo_fin.stock_info as yf
import pandas
ICR1 = [8,
        6.5,
        5.5,
        4.25,
        3,
        2.5,
        2.25,
        2,
        1.75,
        1.5,
        1.25,
        0.8,
        0.65,
        0.2,
        0]

ICR2 = [100000,
        8.499999,
        6.499999,
        5.499999,
        4.249999,
        2.999999,
        2.499999,
        2.249999,
        1.999999,
        1.749999,
        1.499999,
        1.249999,
        0.799999,
        0.649999,
        0.199999]
Rating = ['Aaa/AAA',
          'Aa2/AA',
          'A1/A+',
          'A2/A',
          'A3/A-',
          'Baa2/BBB',
          'Ba1/BB+',
          'Ba2/BB',
          'B1/B+',
          'B2/B',
          'B3/B-',
          'Caa/CCC',
          'Ca2/CC',
          'C2/C',
          'D2/D']
Spread = [0.63,
          0.78,
          0.98,
          1.08,
          1.22,
          1.56,
          2.00,
          2.40,
          3.51,
          4.21,
          5.15,
          8.20,
          8.64,
          11.34,
          15.12]
ICR_1 = [12.5,
        9.5,
        7.5,
        6,
        4.5,
        4,
        4,
        3,
        2.5,
        2,
        1.5,
        1.25,
        0.8,
        0.5,
        -100000]
ICR_2 = [100000,
        12.499999,
        9.499999,
        7.499999,
        5.999999,
        4.499999,
        4.499999,
        3.499999,
        2.999999,
        2.499999,
        1.999999,
        1.499999,
        1.249999,
        0.799999,
        0.499999]
ERP = 4.72

Rating_2 = ['Aaa/AAA',
            'Aa2/AA',
            'A1/A+',
            'A2/A',
            'A3/A-',
            'Baa2/BBB',
            'Ba1/BB+',
            'Ba2/BB',
            'B1/B+',
            'B2/B',
            'B3/B-',
            'Caa/CCC',
            'Ca2/CC',
            'C2/C',
            'D2/D']


Spread_2 = [0.63,
            0.78,
            0.98,
            1.08,
            1.22,
            1.56,
            2.00,
            2.40,
            3.51,
            4.21,
            5.15,
            8.20,
            8.64,
            11.34,
            15.12]
# list of Countries and their default rating based off risk of economic colapse
Countries = {'Abu Dhabi': 0.48,
             'Argentina': 11.62,
             'Australia': 0.00,
             'Austria': 0.38,
             'Bahamas': 2.91,
             'Bangladesh': 3.49,
             'Belgium': 0.59,
             'Bermuda': 0.82,
             'Bolivia': 5.33,
             'Brazil': 2.91,
             'Bulgaria': 1.55,
             'Cameroon': 5.33,
             'Canada': 0.00,
             'Cayman Islands': 0.59,
             'Chile': 0.68,
             'China': 0.68,
             'Colombia': 1.84,
             'Costa Rica': 5.33,
             'Croatia': 2.42,
             'Cuba': 8.72,
             'Czech Republic': 0.59,
             'Denmark': 0.00,
             'Dominican Republic': 3.49,
             'Ecuador': 9.68,
             'Egypt': 5.33,
             'Ethiopia': 5.33,
             'Finland': 0.38,
             'France':  0.48,
             'Germany': 0.00,
             'Greece':  3.49,
             'Hong Kong': 0.59,
             'Iceland': 0.82,
             'India': 2.13,
             'Iraq': 7.26,
             'Ireland': 0.82,
             'Israel': 0.68,
             'Italy': 2.13,
             'Jamaica': 5.33,
             'Japan': 0.68,
             'Korea': 0.48,
             'Luxembourg': 0.00,
             'Mexico': 1.55,
             'Netherlands': 0.00,
             'New Zealand': 0.00,
             'Norway': 0.00,
             'Peru': 1.16,
             'Poland': 0.82,
             'Portugal': 2.13,
             'Romania': 2.13,
             'Russia': 2.13,
             'Saudi Arabia': 0.68,
             'Serbia': 3.49,
             'Singapore': 0.00,
             'South Africa': 2.91,
             'Spain': 1.55,
             'Sweden': 0.00,
             'Switzerland': 0.00,
             'Ukraine': 6.30,
             'United Arab Emirates': 0.48,
             'United Kingdom': 0.59,
             'United States': 0.00}
Country_Risk_Premium = ['0.48%']
PerpetualGrowthRate = 0.025

def conv_mrktcap(marketcap):
    # if market cap is in trillions, follow these commands
    if 'T' in marketcap:
        # strip the T from the market cap, and put a 1 instead
        marketcap_stripped = marketcap.replace('T', "", 1)
        # Replace the T with 10^12 to convert to integers
        marketcap = float(marketcap_stripped) * (10 ** 12)
    # if market cap is in Billions, follow these commands
    elif 'B' in marketcap:
        # strip the M from the market cap, and put a 1 instead
        marketcap_stripped = marketcap.replace('B', "", 1)
        # Replace the B with 10^12 to convert to integers
        marketcap = float(marketcap_stripped) * (10 ** 9)
    # if market cap is in Millions, follow these commands
    elif 'M' in marketcap:
        marketcap_stripped = marketcap.replace('M', "", 1)
        # Replace the B with 10^12 to convert to integers
        marketcap = float(marketcap_stripped) * (10 ** 6)
    return marketcap

running = True
while running:
    Business_Country = input('What Country is The Business From:')
    Revenue_stream = float(input('What Percentage of Total Revenue Comes From that Country? (1=100%, and if its a developed country write 1):'))
    WAM = int(input('What is the Weighted Average Maturity of Debt Found in 10k Report (if unsure write 5):'))
    print(int(input('Stock Based Compensation:')))
    Ticker = input("Insert Ticker:")
    quote = yf.get_quote_table(Ticker)
    # indexing market cap
    MarketCap = quote["Market Cap"]
    # print market cap
    beta = quote["Beta (5Y Monthly)"]
    print('Market Cap:', "{:,}".format(conv_mrktcap(MarketCap)), '$')
    print('Beta:', beta)
    stats = yf.get_stats_valuation(Ticker)
    Data = yf.get_data(Ticker)
    Balance_Sheet = yf.get_balance_sheet(Ticker)
    financials = yf.get_financials(Ticker)
    analyst = yf.get_analysts_info(Ticker)
    # import company's valuations as stats
    income = yf.get_income_statement(Ticker)
    Cash = yf.get_cash_flow(Ticker)

    # import comapny's income statement as income
    ebit = income.loc["ebit"]
    # indexing ebit in icnome statement
    ebit2020 = int(ebit["2020"])
    # indexing latest ebit in income statement
    print('Latest Calender Ebit:', "{:,}".format(ebit2020), "$")

    interestExpense = income.loc['interestExpense']
    # indexing interest expense in imcome statement
    interestExpense2020 = int(-interestExpense["2020"])
    # indexing latest interest expemse in income statement
    print('Latest Calendar Interest Expense:', "{:,}".format(interestExpense2020), '$')

    Total_Debt = income.loc['incomeBeforeTax']
    Total_Debt2020 = int(Total_Debt["2020"])
    Tax_Provision = income.loc["incomeTaxExpense"]
    Tax_Provision2020 = int(Tax_Provision["2020"])
    Tax_Rate = (Tax_Provision2020/Total_Debt2020) * 100
    print('Current Year Tax Rate:', '{:.4f}'.format(Tax_Rate), '%')

    #Calculating interest Coverage Ratio (ICR)
    icr = ebit2020 / interestExpense2020
    print("Interest Coverage Ratio:", '{:.4f}'.format(icr))
    # Equity Risk Premium
    Domestic_Business = Countries.get(Business_Country)
    print('Country Risk Premium Based Off Business\' Home Country:', (Revenue_stream * Domestic_Business))

    print('Equity Risk Premium:', ERP)

    # live pricing of United States 1O year Treasury Bond
    Tbond = yf.get_data('^TNX')
    Recent_Tbond = yf.get_live_price('^TNX')
    print("10 year Treasury bond:", "{:.4f}".format(Recent_Tbond), '%')

    # Cost of equity for that equity
    Cost_of_Equity = Recent_Tbond + beta * ERP
    print("Cost of Equity:", "{:.4f}".format(Cost_of_Equity), "%")

    stats2 = yf.get_stats(Ticker)
    OutstandingShares = conv_mrktcap(stats2.loc[9][1])
    print('Outstanding Shares:', "{:,}".format(OutstandingShares), 'Shares')
    LivePrice = yf.get_live_price(Ticker)
    MarketValueOfEquity = OutstandingShares * LivePrice
    print('Market Value of Equity', "{:,}".format(round(MarketValueOfEquity)), '$')
    TotalDebt = conv_mrktcap(stats2.loc[44][1])
    print('Total Debt:', "{:,}".format(TotalDebt), '$')

    if conv_mrktcap(MarketCap) > 5000000000:
        # Using for loop to iterate through the list to print out the necessary detail
        for i in range(0, len(ICR1)):
            # Checking if the ICR is in the boundary or not
            if (icr >= ICR1[i] and icr <= ICR2[i]):
                # Printing the results and breaking the loop
                print(f"Equity Rating is {Rating[i]} and Default Spread is {Spread[i]} %")

    elif conv_mrktcap(MarketCap) < 5000000000:
        # Using for loop to iterate through the list to print out the necessary detail
        for i in range(0, len(ICR_1)):
            # Checking if the ICR is in the boundary or not
            if (icr >= ICR_1[i] and icr <= ICR_2[i]):
                # Printing the results and breaking the loop
                print(f"Equity Rating is {Rating_2[i]} and Spread is {Spread_2[i]} %")

    AfterTaxCostofDebt = (((Recent_Tbond/100) + (i/100) + (Domestic_Business/100)) * (1 - (Tax_Rate/100)) *100)
    print('After Tax Cost of Debt:', "{:.2f}".format(AfterTaxCostofDebt), '%')
    CostofDebt = ((Recent_Tbond/100) + (i/100) + (Domestic_Business/100))
    C = interestExpense2020
    Kd = CostofDebt
    T = WAM
    FV = TotalDebt
    MarketValueOfDebt = (C*((1-(1/(1+Kd)**T))/Kd))+(FV/(1+Kd)**T)
    a = MarketValueOfEquity
    b = MarketValueOfDebt
    c = Cost_of_Equity/100
    d = AfterTaxCostofDebt/100
    CostofCapital = c*(a/(a+b)) + d*(b/(b+a))
    print('Cost of Capital (WACC):', "{:.2f}".format(CostofCapital *100), "%")
    print(financials)
    Depreciation_Amoritization = Cash.loc['depreciation']
