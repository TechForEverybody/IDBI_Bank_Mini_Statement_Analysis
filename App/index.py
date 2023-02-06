from flask import Flask,render_template,redirect,request,jsonify
from Analyzer import Analyzer

import hashlib

App=Flask(__name__)


file_name="a"
encrypted_filename=""
data={}

@App.route("/")
def index():
    return render_template("index.html"),200

@App.route("/analytics")
def analytics():
    print(request.remote_addr)
    global file_name,encrypted_filename,data
    if file_name:
        try:
            print(file_name)
            analyzer=Analyzer("./Files/"+encrypted_filename)
            data=analyzer.convertToTable()
            credit_table=analyzer.getCreditTable()
            credit_type=analyzer.getCreditPaymentTypes()
            credit_sender=analyzer.getCreditPaymentRecipient()

            debit_table=analyzer.getDebitTable()
            debit_receiver=analyzer.getDebitPaymentRecipient()
            debit_type=analyzer.getDebitPaymentTypes()


            return render_template(
                "analytics.html",
                file_name=file_name,
                number_of_records=analyzer.getNumberOfRecords(),
                first_date=analyzer.getFirstDate(),
                last_date=analyzer.getLastDate(),
                balance_difference=analyzer.getCumulativeDifference(),
                credit_table=credit_table,
                credit_sender=credit_sender,
                credit_type=credit_type,
                debit_table=debit_table,
                debit_receiver=debit_receiver,
                debit_type=debit_type,
                ip_address=request.remote_addr,
            ),200
        except Exception as e:
            print(e)
            return redirect("/error")
    return redirect("/")

@App.route('/upload_file', methods=['GET', 'POST'])
def uploadFile():
    global file_name,encrypted_filename
    if request.method == 'POST':
        f = request.files['file']
        print(f)
        file_name=f.filename
        encrypted_filename=hashlib.md5(request.remote_addr.lower().encode("utf-8")).hexdigest()+"pdf"
        f.save("./Files/"+encrypted_filename)
        
    return redirect("/analytics")

@App.route("/get_transactions",methods=['GET', 'POST'])
def getTransactions():
    global data
    if request.method == 'POST':
        return data.to_json()
    return ""

@App.route("/error")
def error():
    return render_template("error.html")

@App.errorhandler(404)
def Error(error):
    return redirect("/error"), 404





if __name__=="__main__":
    App.run(debug=True)