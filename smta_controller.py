# flake8: noqa

import csv
import yfinance as yf
import zmq

class SearchByNameController():

    def __init__(self) -> None:
        self.stocks_hash = dict()
        with open('stocks_list.csv') as csv_file:
            stocks_list = csv.reader(csv_file)
            for stock in stocks_list:
                stock_symbol = stock[0]
                stock_name = stock[1]
                if stock_name[0].lower() not in self.stocks_hash:
                    self.stocks_hash[stock_name[0].lower()] = dict()
                self.stocks_hash[stock_name[0].lower()][stock_name.lower()] = stock_symbol

    def get_stock_names_for_alphabetical_entry(self, alphabetical_entry):
        return self.stocks_hash[alphabetical_entry]

    def get_stock_name_match_from_user_input(self, search_value):
        user_input = search_value.lower()
        # Requires input to start with at least one alpha character.
        if not (user_input.isalnum() and user_input[0].isalpha()):
            return False
        else:
            alpha_list = sorted(self.get_stock_names_for_alphabetical_entry(user_input[0]).keys())
            selection_list = [[selection] for selection in alpha_list if selection.startswith(user_input)]
            return selection_list if selection_list else False

    def get_stock_symbol_from_stock_name(self, stock_name):
        return self.get_stock_names_for_alphabetical_entry(stock_name[0])[stock_name]
    
class StockDataRequestController():

    def __init__(self) -> None:
        pass
    
    def get_stock_information_for_search_by_symbol_confirmation(self, stock_symbol):
        
        for attempt in range(5):
            try:
                ticker = yf.Ticker(stock_symbol.upper())
                company_name = ticker.info['longName']
                symbol = ticker.info['symbol']
                return [[symbol, company_name]]
            except:
                continue
        return False

    def get_stock_information_for_individual_stock_view(self, stock_symbol):
        
        for attempt in range(5):
            try:
                ticker = yf.Ticker(stock_symbol.upper())
                company_name = ticker.info['longName']
                symbol = ticker.info['symbol']
                current_price = str(ticker.info['currentPrice'])
                return [[company_name, symbol, current_price]]
            except:
                continue
        return False
    
    def get_stock_information_for_major_stock_indices(self):
        dynamic_data = list()
        major_indices = ['^GSPC', '^DJI', '^IXIC']
        for major_index in major_indices:
            for attempt in range(5):
                try:
                    ticker = yf.Ticker(major_index)
                    company_name = ticker.info['longName']
                    symbol = ticker.info['symbol']
                    current_price = str(ticker.info['open'])
                    dynamic_data.append([company_name, symbol, current_price])
                    dynamic_data.append([''])
                    break
                except:
                    continue
        return dynamic_data if dynamic_data else False


class StockHoldingsController():

    def __init__(self) -> None:
        self.database = {'AAPL': {'single_share_purchase_price': 185.340,
                                  'total_amount_initially_invested': 1250.000},
                         'MSFT': {'single_share_purchase_price': 288.680,
                                  'total_amount_initially_invested': 10000.000},
                         'PLTR': {'single_share_purchase_price': 21.25,
                                  'total_amount_initially_invested': 634.000}}
        self.stock_request_tool = StockDataRequestController()

    def get_stock_holdings_database_keys(self):
        return list(self.database.keys())

    def get_stock_holding_values(self, stock_symbol):
        return self.database[stock_symbol]
    
    def get_stock_request_tool(self):
        return self.stock_request_tool
    
    def get_all_stock_data_performances_from_microservice(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        protocol = 'tcp'
        interface = 'localhost'
        port = '5555'
        socket.connect(f"{protocol}://{interface}:{port}")

        dynamic_data = list()

        for stock_symbol in self.get_stock_holdings_database_keys():
            dynamic_input = list()
            stock_holdings_data = self.get_stock_holding_values(stock_symbol)
            single_share_purchase_price = stock_holdings_data['single_share_purchase_price']
            total_amount_initially_invested = stock_holdings_data['total_amount_initially_invested']
            total_shares = int(total_amount_initially_invested) / int(single_share_purchase_price)
            
            stock_curent_data = self.get_stock_request_tool().get_stock_information_for_individual_stock_view(stock_symbol)
            if stock_curent_data is False: return False
            company_name = stock_curent_data[0][0]
            single_share_current_price = float(stock_curent_data[0][2])

            microservice_request = (single_share_purchase_price, single_share_current_price, total_amount_initially_invested)
            socket.send_pyobj(microservice_request)
            
            per_share_gain_or_loss, percentage_gain_or_loss, investment_profit_or_loss = socket.recv_pyobj()[0]

            # company_name, stock_symbol
            # single_share_purchase_price, single_share_current_price, total_amount_initially_invested, total_shares
            # per_share_gain_or_loss, percentage_gain_or_loss, investment_profit_or_loss

            dynamic_input.append('----------------------------------------------------------------------')
            dynamic_input.append(f'Company Name:               {company_name}')
            dynamic_input.append(f'Stock Symbol:               {stock_symbol}')
            dynamic_input.append(f'Shares:                     {total_shares:0.2f}')
            dynamic_input.append(f'Purchase Price:             ${single_share_purchase_price:.2f}')
            dynamic_input.append(f'Total Invested:             ${total_amount_initially_invested:.2f}')
            dynamic_input.append('')
            dynamic_input.append(f'Current Share Price:        ${single_share_current_price:.2f}')
            dynamic_input.append(f'Per Share Gain or Loss:     ${per_share_gain_or_loss:.2f}')
            dynamic_input.append(f'Performance:                {percentage_gain_or_loss:.2f}%')
            dynamic_input.append(f'Investment Profit or Loss:  ${investment_profit_or_loss:.2f}')
            dynamic_data.append(dynamic_input)
        dynamic_data.append(['----------------------------------------------------------------------'])
        return dynamic_data


if __name__ == '__main__':
    stocks = StockHoldingsController()
    stocks.get_all_stock_data_performances_from_microservice()