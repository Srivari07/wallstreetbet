
import pandas as pd
from datetime import datetime
import os.path

from flask import Flask, jsonify, request
from flask_cors import CORS

from ticketCounter import main as updateRedditMentions
from alphaVintageAnalysis import main as updateFinancialData



app = Flask(__name__)
cors = CORS(app)


def dataExists():
	data_directory = "./Data"
	date_created = datetime.today().strftime('%Y-%m-%d')
	mentions_filename = f"{data_directory}/{date_created}_df_tickets.csv"
	financial_filename = f"{data_directory}/{date_created}_df_financial.csv"

	if not os.path.exists(mentions_filename):
		updateRedditMentions()

	if not os.path.exists(financial_filename):
		updateFinancialData()

@app.route("/", methods=['GET'])
def home():
	msg ="Welcome to home page go to /data"
	return msg

@app.route('/data', methods=['GET'])
def getData() -> str:
	# Make sure we have today's data (as the server may run for multiple days)
	dataExists()

	# Read the dataframes
	data_directory = "./Data"
	date_created = datetime.today().strftime('%Y-%m-%d')
	mentions_filename = f"{data_directory}/{date_created}_df_tickets.csv"
	financial_filename = f"{data_directory}/{date_created}_df_financial.csv"
	mentions_df = pd.read_csv(f"{mentions_filename}")
	financial_df = pd.read_csv(f"{financial_filename}")

	# Join the dataframes
	combined_df = financial_df.join(mentions_df.set_index('Ticker'), on='Ticker')
	combined_df.sort_values(by=["Mentions"], inplace=True, ascending=False)

	return jsonify(data=combined_df.where(pd.notnull(combined_df), None).to_dict(orient="records"))
