

from pydantic import BaseModel
from commonPyLib.helpers.number import NumberHelper

class FincStatementBase(BaseModel):
    date: str 
    symbol: str
    reportedCurrency: str 
    cik: str
    fillingDate: str
    acceptedDate: str
    calendarYear: str
    period: str
    ###
    link: str | None = None
    finalLink: str | None = None

    @staticmethod
    def getUnwantedColumnsForContent() -> list[str]:
        return ["symbol", "reportedCurrency", "cik", "fillingDate", "acceptedDate", "calendarYear", "period", "link", "finalLink"]
    
    def getValue(self, key: str, default=None):
        return getattr(self, key, default)
    

class IncomeStatement(FincStatementBase):
    revenue: float
    costOfRevenue: float
    grossProfit: float
    researchAndDevelopmentExpenses: float
    generalAndAdministrativeExpenses: float
    sellingAndMarketingExpenses: float
    sellingGeneralAndAdministrativeExpenses: float
    otherExpenses: float
    operatingExpenses: float
    costAndExpenses: float
    interestIncome: float
    interestExpense: float
    depreciationAndAmortization: float
    ebitda: float
    operatingIncome: float
    totalOtherIncomeExpensesNet: float
    incomeBeforeTax: float
    incomeTaxExpense: float
    netIncome: float
    eps: float
    epsdiluted: float
    weightedAverageShsOut: float
    weightedAverageShsOutDil: float



class StructuredBalanceSheetAsset(BaseModel):
    cashAndCashEquivalents: float
    shortTermInvestments: float
    netReceivables: float
    inventory: float
    otherCurrentAssets: float
    propertyPlantEquipmentNet: float
    goodwill: float
    intangibleAssets: float
    longTermInvestments: float
    taxAssets: float
    otherNonCurrentAssets: float
    otherAssets: float

class StructuredBalanceSheetLiability(BaseModel):
    accountPayables: float
    shortTermDebt: float
    taxPayables: float
    deferredRevenue: float
    otherCurrentLiabilities: float
    longTermDebt: float
    deferredRevenueNonCurrent: float
    deferredTaxLiabilitiesNonCurrent: float
    otherNonCurrentLiabilities: float
    otherLiabilities: float
    capitalLeaseObligations: float

class StructuredBalanceSheetEquity(BaseModel):
    preferredStock: float
    commonStock: float
    retainedEarnings: float
    accumulatedOtherComprehensiveIncomeLoss: float
    othertotalStockholdersEquity: float
    minorityInterest: float


class StructureBalanceSheet(BaseModel):
    asset: StructuredBalanceSheetAsset
    liability: StructuredBalanceSheetLiability
    equity: StructuredBalanceSheetEquity


class BalanceSheet(FincStatementBase):
    cashAndCashEquivalents: float
    shortTermInvestments: float
    cashAndShortTermInvestments: float
    netReceivables: float
    inventory: float
    otherCurrentAssets: float
    totalCurrentAssets: float
    propertyPlantEquipmentNet: float
    goodwill: float
    intangibleAssets: float
    goodwillAndIntangibleAssets: float
    longTermInvestments: float
    taxAssets: float
    otherNonCurrentAssets: float
    totalNonCurrentAssets: float
    otherAssets: float
    totalAssets: float
    accountPayables: float
    shortTermDebt: float
    taxPayables: float
    deferredRevenue: float
    otherCurrentLiabilities: float
    totalCurrentLiabilities: float
    longTermDebt: float
    deferredRevenueNonCurrent: float
    deferredTaxLiabilitiesNonCurrent: float
    otherNonCurrentLiabilities: float
    totalNonCurrentLiabilities: float
    otherLiabilities: float
    capitalLeaseObligations: float
    totalLiabilities: float
    preferredStock: float
    commonStock: float
    retainedEarnings: float
    accumulatedOtherComprehensiveIncomeLoss: float
    othertotalStockholdersEquity: float
    totalStockholdersEquity: float
    totalEquity: float
    totalLiabilitiesAndStockholdersEquity: float
    minorityInterest: float
    totalLiabilitiesAndTotalEquity: float
    totalInvestments: float
    totalDebt: float
    netDebt: float

    def calCurrentAssets(self) -> float:
        total = 0
        for item in [
            self.cashAndCashEquivalents,
            self.shortTermInvestments,
            self.netReceivables,
            self.inventory,
            self.otherCurrentAssets,
        ]:
            total += item
        return total
    
    def calCurrentLiabilities(self) -> float:
        total = 0
        for item in [
            self.accountPayables,
            self.shortTermDebt,
            self.taxPayables,
            self.deferredRevenue,
            self.otherCurrentLiabilities,
        ]:
            total += item
        return total
    
    def getTotalDebtValueForWacc(self) -> float:
        return self.shortTermDebt + self.longTermDebt + self.capitalLeaseObligations   


    def toStructuredBalanceSheet(self) -> StructureBalanceSheet:
        return StructureBalanceSheet(
            asset=StructuredBalanceSheetAsset(
                cashAndCashEquivalents=self.cashAndCashEquivalents,
                shortTermInvestments=self.shortTermInvestments,
                netReceivables=self.netReceivables,
                inventory=self.inventory,
                otherCurrentAssets=self.otherCurrentAssets,
                propertyPlantEquipmentNet=self.propertyPlantEquipmentNet,
                goodwill=self.goodwill,
                intangibleAssets=self.intangibleAssets,
                longTermInvestments=self.longTermInvestments,
                taxAssets=self.taxAssets,
                otherNonCurrentAssets=self.otherNonCurrentAssets,
                otherAssets=self.otherAssets
            ),
            liability=StructuredBalanceSheetLiability(
                accountPayables=self.accountPayables,
                shortTermDebt=self.shortTermDebt,
                taxPayables=self.taxPayables,
                deferredRevenue=self.deferredRevenue,
                otherCurrentLiabilities=self.otherCurrentLiabilities,
                longTermDebt=self.longTermDebt,
                deferredRevenueNonCurrent=self.deferredRevenueNonCurrent,
                deferredTaxLiabilitiesNonCurrent=self.deferredTaxLiabilitiesNonCurrent,
                otherNonCurrentLiabilities=self.otherNonCurrentLiabilities,
                otherLiabilities=self.otherLiabilities,
                capitalLeaseObligations=self.capitalLeaseObligations
            ),
            equity=StructuredBalanceSheetEquity(
                preferredStock=self.preferredStock,
                commonStock=self.commonStock,
                retainedEarnings=self.retainedEarnings,
                accumulatedOtherComprehensiveIncomeLoss=self.accumulatedOtherComprehensiveIncomeLoss,
                othertotalStockholdersEquity=self.othertotalStockholdersEquity,
                minorityInterest=self.minorityInterest
            )
        )


class CashFlowStatement(FincStatementBase):
    netIncome: float
    depreciationAndAmortization: float
    deferredIncomeTax: float
    stockBasedCompensation: float
    changeInWorkingCapital: float
    accountsReceivables: float
    inventory: float
    accountsPayables: float
    otherWorkingCapital: float
    otherNonCashItems: float
    netCashProvidedByOperatingActivities: float
    investmentsInPropertyPlantAndEquipment: float
    acquisitionsNet: float
    purchasesOfInvestments: float
    salesMaturitiesOfInvestments: float
    otherInvestingActivites: float
    netCashUsedForInvestingActivites: float
    debtRepayment: float
    commonStockIssued: float
    commonStockRepurchased: float
    dividendsPaid: float
    otherFinancingActivites: float
    netCashUsedProvidedByFinancingActivities: float
    effectOfForexChangesOnCash: float
    netChangeInCash: float
    cashAtEndOfPeriod: float
    cashAtBeginningOfPeriod: float
    operatingCashFlow: float
    capitalExpenditure: float
    freeCashFlow: float



class UnderlyingFincStatement(BaseModel):
    cashflows: list[CashFlowStatement] = []
    incomeStatements: list[IncomeStatement] = []
    balanceSheets: list[BalanceSheet] = []

    def __convertToContent(self, statements: list[IncomeStatement | CashFlowStatement | BalanceSheet]) -> str: 
        ###
        dataKeys = list(statements[0].model_fields.keys())
        unwantKeys = FincStatementBase.getUnwantedColumnsForContent()
        headers = [key for key in dataKeys if key not in unwantKeys]
        ###
        numberOfPeriods = len(statements)
        if numberOfPeriods < 1: return "No Information can be provided"
        content = ""
        for key in headers:
            if key == "date": continue
            content += f"{key}: "
            for i in range(numberOfPeriods):
                numberAsString = NumberHelper.convertNumberToReadableUnit(statements[i].getValue(key))
                content += f"${numberAsString} as of {statements[i].getValue('date')}"
                if i != numberOfPeriods - 1: content += ", "
                else: content += ". \n"
        return content
    
    def toText(self) -> str:
        content = ""
        if len(self.cashflows) > 0:
            content += "Cash Flows: \n"
            content += self.__convertToContent(self.cashflows)
        if len(self.incomeStatements) > 0:
            content += "Income Statements: \n"
            content += self.__convertToContent(self.incomeStatements)
        if len(self.balanceSheets) > 0:
            content += "Balance Sheets: \n"
            content += self.__convertToContent(self.balanceSheets)
        return content
