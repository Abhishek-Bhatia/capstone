from sentiment import Sentiment
from stock import StockPrice
from prediction import Prediction
import schedule
import time
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    

@app.route('/main_function',methods=['POST'])
def main_function():
    if list(request.form.values())[0] == 'AxisBank':
        pr = Prediction(['AxisBank',["#AxisBank","#axisbank","@axisBank","@RBI"]])
        pr.get_final_prediction()

        output = 'Rs. {}'.format(round(pr.get_final_prediction()[0],2))
    else:
        output = 'Not Available'

    return render_template('index.html', prediction_text='Forecasted value is {}'.format(output))




if __name__ == "__main__":
    app.run(debug=True)
