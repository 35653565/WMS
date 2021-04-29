
import yahoo_fin.stock_info as yf
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
ERP = 4.72
PerpetualGrowthRate = 0.025
WAM = 6
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

    AfterTaxCostofDebt = (((Recent_Tbond / 100) + (i / 100)) * (1 - (Tax_Rate / 100)) * 100)
    print('After Tax Cost of Debt:', "{:.2f}".format(AfterTaxCostofDebt), '%')
    CostofDebt = ((Recent_Tbond / 100) + (i / 100))
    C = interestExpense2020
    Kd = CostofDebt
    T = WAM
    FV = TotalDebt
    MarketValueOfDebt = (C * ((1 - (1 / (1 + Kd) ** T)) / Kd)) + (FV / (1 + Kd) ** T)
    a = MarketValueOfEquity
    b = MarketValueOfDebt
    c = Cost_of_Equity / 100
    d = AfterTaxCostofDebt / 100
    CostofCapital = c * (a / (a + b)) + d * (b / (b + a))
    print('Cost of Capital (WACC):', "{:.2f}".format(CostofCapital * 100), "%")
    print(financials)
    Depreciation_Amoritization = Cash.loc['depreciation']
    Depreciation_Amoritization2020 = int(Depreciation_Amoritization['2020'])
    PPE = Balance_Sheet.loc['propertyPlantEquipment']
    PPE2020 = int(PPE['2020'])
    IncomeTaxExpense = income.loc['incomeTaxExpense']
    IncomeTaxExpense2020 = int(interestExpense['2020'])




















































#'capx = Cash.loc["capitalExpenditures"]
#capx2020 = int(capx['2020'])
#capx2019 = int(capx['2019'])
#capx2018 = int(capx['2018'])
#capx2017 = int(capx['2017'])
#netcapx = capx2020 + capx2019 + capx2018 + capx2017
#Assets = Balance_Sheet.loc['totalCurrentAssets']
#Assets2020 = int(Assets['2020'])
#Liabilities = Balance_Sheet.loc['totalCurrentLiabilities']
#Liabilities2020 = int(Liabilities['2020'])
#Assets2019 = int(Assets['2019'])
#Liabilities2019 = int(Liabilities['2019'])
#WorkingCapital2020 = Assets2020 - Liabilities2020
#WorkingCapital2019 = Assets2019 - Liabilities2019
#ChngInWC = WorkingCapital2020 - WorkingCapital2019
#ReinvestmentRate = (((-netcapx) + ChngInWC) / (ebit2020 * (1 - (Tax_Rate / 100))))
#print('Reivestement Rate:', "{:.2f}".format(ReinvestmentRate),
      #'(Number Already Divided by 100 to Ease Future Calculations)')
#CapitalReturn = ((ebit2020 * (1 - (Tax_Rate / 100)) / WorkingCapital2020))
#OperatingIncome = CapitalReturn * ReinvestmentRate
#OperatingIncome2020 = income.loc['operatingIncome']
#OperatingIncome_2020 = int(OperatingIncome2020['2020'])
#Year1_Operatingincome = OperatingIncome_2020 * (1 + OperatingIncome)
#Year2_Operatingincome = Year1_Operatingincome * (1 + OperatingIncome)
#Year3_Operatingincome = Year2_Operatingincome * (1 + OperatingIncome)
#Year4_Operatingincome = Year3_Operatingincome * (1 + OperatingIncome)
#Year5_Operatingincome = Year4_Operatingincome * (1 + OperatingIncome)
#Reinvestement1 = Year1_Operatingincome * (1 - ReinvestmentRate)
#Reinvestement2 = Year2_Operatingincome * (1 - ReinvestmentRate)
#Reinvestement3 = Year3_Operatingincome * (1 - ReinvestmentRate)
#Reinvestement4 = Year4_Operatingincome * (1 - ReinvestmentRate)
#Reinvestement5 = Year5_Operatingincome * (1 - ReinvestmentRate)
#Year1FCFF = Year1_Operatingincome - Reinvestement1
#Year2FCFF = Year2_Operatingincome - Reinvestement2
#Year3FCFF = Year3_Operatingincome - Reinvestement3
#Year4FCFF = Year4_Operatingincome - Reinvestement4
#Year5FCFF = Year5_Operatingincome - Reinvestement5
#TerminalValue = ((Year5FCFF * (1 + PerpetualGrowthRate)) + (CostofCapital - PerpetualGrowthRate))
#DCF = ((Year1FCFF / (1 + (CostofCapital / 100)) + (Year2FCFF / (1 + (CostofCapital / 100))) + (
            #Year3FCFF / (1 + (CostofCapital / 100))) + (Year4FCFF / (1 + (CostofCapital / 100))) + (
                    #(Year5FCFF + TerminalValue) / (1 + (CostofCapital / 100))))
          #FairPrice = DCF / OutstandingShares
          #print('Fair Price', round(FairPrice), '$USD')
#MarginalSaftetyFairPrice = round(FairPrice) * 0.95
#if MarginalSaftetyFairPrice > LivePrice:
    #print('Great Price. Purchase Stock!!!')
#elif MarginalSaftetyFairPrice < LivePrice:
    #print('Stock Seems Overpriced. Do NOT Buy!!!')





