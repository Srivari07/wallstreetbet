import pandas as pd
from pathlib import Path
import datetime as dt
from dotenv import dotenv_values
import asyncio
from alpha_vantage.async_support.timeseries import TimeSeries
import nest_asyncio
nest_asyncio.apply()


class FinanceAnalysis:

    def analyze(self):
        # Load data from file, generate data by running the `ticker_counts.py` script
        data_directory = Path('./Data')
        input_path = data_directory / f'{dt.date.today()}_df_tickets.csv'

        df_tick = pd.read_csv(input_path).sort_values(
            by=['Mentions', 'Ticker'], ascending=False)

        symbols = [tick for tick in df_tick["Ticker"].head(5)]

        config=dotenv_values(".env")
        API_KEY = config["API_KEY"]

        async def get_data(symbol):
            ts = TimeSeries(key=API_KEY)
            data, _ = await ts.get_quote_endpoint(symbol)
            await ts.close()
            return data

        loop = asyncio.get_event_loop()
        tasks = [get_data(symbol) for symbol in symbols]
        group1 = asyncio.gather(*tasks)
        results = loop.run_until_complete(group1)
        df = pd.DataFrame(results)
        df.rename(columns={'01. symbol': "Ticker", '02. open': "Open", '03. high': "High", '04. low': "Low", '05. price': "Price", '06. volume': "Volume", '07. latest trading day': "LatestTradingDay", '08. previous close': "PreviousClose",
        '09. change': "Change", '10. change percent': "ChangePercent"}, inplace=True)

        # Save to file to load into alpha analysis script
        output_path = data_directory / f'{dt.date.today()}_df_financial.csv'
        df.to_csv(output_path, index=False, float_format='%.4f')
        print(df.head())


def main():
    analyzer = FinanceAnalysis()
    analyzer.analyze()


if __name__ == '__main__':
    main()
