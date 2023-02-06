import pandas
import tabula
import re

class Analyzer:
    def __init__(self,file_path:str) -> None:
        """_summary_

        Args:
            file_path (str): _description_
        """
        self.file=file_path
    @staticmethod
    def getPaymentMethod(inputString:str)->str:
        if len(re.findall("^\d{6}",inputString.strip()))>0:
            return "Cheque"
        elif len(re.findall("UPI",inputString.strip()))>0:
            return "UPI"
        elif len(re.findall("^NEFT",inputString.strip()))>0:
            return "NEFT"
        elif len(re.findall("^IMPS",inputString.strip()))>0:
            return "IMPS"
        elif len(re.findall("^ID|^nfs/|^cashnet/",inputString.strip()))>0:
            return "ATM"
        elif len(re.findall("^SMS|^ANNUAL|Keeping|RENEWAL",inputString.strip()))>0:
            return "SMS Charge"
        elif len(re.findall("^ANNUAL",inputString.strip()))>0:
            return "Some ANNUAL Charge"
        elif len(re.findall("^ACH-",inputString.strip()))>0:
            return "Automated Clearing Payment"
        elif len(re.findall("POS/",inputString.strip()))>0:
            return "Payment done at retail store"
        elif len(re.findall("[\.\/+\:\-\_]",inputString.strip()))==0:
            return "Unknown Type Payment"
        else:
            return "Other"
    @staticmethod
    def getRecipientName(inputString:str)->str:
        if len(re.findall("^\d{6}",inputString.strip()))>0:
            return inputString.strip()[7:].strip()
        elif len(re.findall("UPI",inputString.strip()))>0:
            return re.split("[/@]",inputString.strip())[-1].strip()
        elif len(re.findall("^NEFT",inputString.strip()))>0:
            return inputString.strip().split("-")[-1].strip()
        elif len(re.findall("^ACH-",inputString.strip()))>0:
            return inputString.split('-')[1].strip()
        elif len(re.findall("^IMPS",inputString.strip()))>0:
            return inputString.strip().split("/")[2].strip()
        elif len(re.findall("^SMS|^ANNUAL|Keeping|RENEWAL",inputString.strip()))>0:
            return "IDBI Bank"
        elif len(re.findall("^ID|^nfs/|^cashnet/",inputString.strip()))>0:
            return "Self"
        elif len(re.findall("POS/",inputString.strip()))>0:
            return inputString.strip().split("POS/")[-1].strip()
        elif len(re.findall("[\.\/+\:\-\_]",inputString.strip()))==0:
            return inputString.strip()
        else:
            return "Other"
    def convertToTable(self)->pandas.DataFrame:
        data=tabula.read_pdf(self.file,pages="all")
        final_table=pandas.concat(data)
        final_table['Amount']=final_table['Amount'].apply(lambda x:float(x.replace(",","")))
        final_table['Date']=pandas.to_datetime(final_table['Date'],dayfirst=True)
        final_table=final_table.reset_index(drop=True)
        final_table.sort_values(by="Date")
        self.Statement=final_table
        self.Statement=self.Statement.sort_index(ascending=False)
        Cumulative_Balance=0
        Cumulative_Balances=[]
        types=list(self.Statement['Type'])
        Amounts=list(self.Statement['Amount'])
        for index in range(len(Amounts)):
            if types[index].strip()=="Dr":
                Cumulative_Balance-=round(Amounts[index],2)
            elif types[index].strip()=="Cr":
                Cumulative_Balance+=round(Amounts[index],2)
            Cumulative_Balances.append(Cumulative_Balance)
        self.Statement['Cumulative_Balance']=Cumulative_Balances
        self.Statement['Payment_Mode']=self.Statement['Description'].apply(Analyzer.getPaymentMethod)
        self.Statement['Recipient_Name']=self.Statement['Description'].apply(Analyzer.getRecipientName)
        return self.Statement
    def getCreditTable(self)->pandas.DataFrame:
        return self.Statement[self.Statement['Type']=="Cr"].sort_values(by='Date',ascending=False).reset_index(drop=True)
    def getDebitTable(self)->pandas.DataFrame:
        return self.Statement[self.Statement['Type']=="Dr"].sort_values(by="Date",ascending=False).reset_index(drop=True)
    def getCreditPaymentTypes(self):
        return self.Statement[self.Statement['Type']=="Cr"]['Payment_Mode'].value_counts()
    def getDebitPaymentTypes(self):
        return self.Statement[self.Statement['Type']=="Dr"]['Payment_Mode'].value_counts().sort_values(ascending=False)
    def getCreditPaymentRecipient(self):
        return self.Statement[self.Statement['Type']=="Cr"]['Recipient_Name'].value_counts()
    def getDebitPaymentRecipient(self):
        return self.Statement[self.Statement['Type']=="Dr"]['Recipient_Name'].value_counts()
    def getNumberOfRecords(self):
        return len(self.Statement)
    def getFirstDate(self):
        return str(self.Statement.sort_values(by="Date",ascending=True).reset_index(drop=True)["Date"][0])[:10]
    def getLastDate(self):
        return str(self.Statement.sort_values(by="Date",ascending=False).reset_index(drop=True)["Date"][0])[:10]
    def getCumulativeDifference(self):
        return self.Statement.sort_values(by="Date",ascending=False).reset_index(drop=True)["Cumulative_Balance"][0]