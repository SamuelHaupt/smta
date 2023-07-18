# flake8: noqa

import os

class Menu():
    def __init__(self, menu_name, menu_display):
        self.menu_name = menu_name
        self.menu_display = menu_display
        self.menu_choices = dict()
        self.parents_menu = dict()
        self.children_menu = dict()

    def get_menu_name(self):
        return self.menu_name

    def get_menu_display(self):
        return self.menu_display
    
    def add_menu_choice(self, selection_request, menu_choice):
        self.menu_choices[selection_request] = menu_choice
    
    def get_menu_choices(self):
        return self.menu_choices

    def add_parent_menu(self, parent_menu):
        self.parents_menu[parent_menu] = None

    def is_parent_menu(self, parent_menu):
        return parent_menu in self.parent_menu
    
    def add_child_menu(self, child_menu):
        self.children_menu[child_menu] = None
    
    def is_child_menu(self, child_menu):
        return child_menu is self.children_menu


class Smta_Ui():
    def __init__(self):
        self.current_menu = 'Main Menu'
        self.previous_menu = 'Main Menu'
        self.invalid_inputs = dict()
        self.menu_tree = dict()
        self.populate_invalid_inputs()
        self.build_main_menu()
        self.build_search_stocks_search_node_menu()
        self.build_search_by_symbol_menu()
        self.build_stock_symbol_confirmation_menu()
        self.build_search_by_name_menu()
        self.build_individual_stock_view_menu()
        self.build_stock_holdings_menu()
        self.build_major_stock_indices_menu()
        self.build_application_tutorial_menu()

    def add_menu_to_menu_tree(self, menu_name: str, menu: Menu) -> None:
        if menu_name in self.menu_tree:
            return False
        else:
            self.menu_tree[menu_name] = menu
            return True

    def populate_invalid_inputs(self):
        self.invalid_inputs[''] = None

    def build_main_menu(self):
        menu_display = [
            'Main Menu\n',
            '\n',
            'Select a menu item:\n',
            '1 Search Stocks (For ease of use, select Search by Symbol on next screen and enter stock symbol, if searching for a specific company)\n',
            '2 Stock Holdings (Your person stock holdings)\n',
            '3 Major Stock Indices\n',
            '4 Application Tutorial\n']
        menu = Menu('Main Menu', menu_display)
        menu.add_menu_choice('1', 'Search Mode')
        menu.add_menu_choice('2', 'Stock Holdings')
        menu.add_menu_choice('3', 'Major Stock Indices')
        menu.add_menu_choice('4', 'Application Tutorial')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_search_stocks_search_node_menu(self):
        menu_display = [
            'Search Stocks:Search Mode\n',
            '\n',
            'Select search mode:\n',
            '1 Search by Symbol (Will provide exact company based on matched stock symbol)\n',
            '2 Search by Name (The advanced feature will provide a list of partially matched company names and may take longer to find a specific company)\n',
            '3 Go to Main Menu\n']
        menu = Menu('Search Mode', menu_display)
        menu.add_parent_menu('Main Menu')
        menu.add_menu_choice('1', 'Search by Symbol')
        menu.add_menu_choice('2', 'Search by Name')
        menu.add_menu_choice('3', 'Main Menu')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_search_by_symbol_menu(self):
        menu_display = [
            'Search Stocks:Search Mode:Search by Symbol\n',
            '\n',
            'Stock symbol can include any variation of letters ranging from one value up to seven.\n'
            'Input Stock Symbol, "#back" to go back to Search Mode screen, or "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Search by Symbol', menu_display)
        menu.add_parent_menu('Search Mode')
        menu.add_menu_choice('#back', 'Search Mode')
        menu.add_menu_choice('#main', 'Main Menu')
        menu.add_menu_choice('@#$%^&*!variable screen@#$%^&*!', 'Stock Symbol Confirmation')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_stock_symbol_confirmation_menu(self):
        menu_display = [
            'Search Stocks:Search Mode:Search by Symbol:Stock Symbol Confirmation\n',
            '\n',
            'Is Apple Inc. with stock symbol: AAPL correct? Input "yes" or "no"  to indicate confirmation, "#back" to go back to Search by Symbol screen, or "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Stock Symbol Confirmation', menu_display)
        menu.add_parent_menu('Search by Symbol')
        menu.add_menu_choice('yes', 'Individual Stock View')
        menu.add_menu_choice('no', 'Search by Symbol')
        menu.add_menu_choice('#back', 'Search by Symbol')
        menu.add_menu_choice('#main', 'Main Menu')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_search_by_name_menu(self):
        menu_display = [
            'Search Stocks:Search Mode:Search by Name\n',
            '\n',
            'Stock names can include any variation of letters ranging from 1 to 255 characters.\n'
            'Input Stock Name, "#back" to go back to Search Mode screen, or "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Search by Name', menu_display)
        menu.add_parent_menu('Search Mode')
        menu.add_menu_choice('#back', 'Search Mode')
        menu.add_menu_choice('#main', 'Main Menu')
        menu.add_menu_choice('@#$%^&*!variable screen@#$%^&*!', 'Search Mode')  #Implement: Search by Name Results
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_individual_stock_view_menu(self):
        menu_display = [
            'Individual Stock View\n',
            '\n',
            'Apple Inc.\n',
            'AAPL\n',
            '$193.999\n',
            '\n',
            '\n',
            'Input "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Individual Stock View', menu_display)
        menu.add_parent_menu('Main Menu')
        menu.add_menu_choice('#main', 'Main Menu')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_stock_holdings_menu(self):
        menu_display = [
            'Stock Holdings\n',
            '\n',
            '[company name]\n',
            '[stock symbol]\n',
            '[stock price]\n',
            '\n',
            '[company name]\n',
            '[stock symbol]\n',
            '[stock price]\n',
            '\n',
            '[company name]\n',
            '[stock symbol]\n',
            '[stock price]\n',
            '\n',
            '\n',
            'Input "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Stock Holdings', menu_display)
        menu.add_parent_menu('Main Menu')
        menu.add_menu_choice('#main', 'Main Menu')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_major_stock_indices_menu(self):
        menu_display = [
            'Major Stock Indices\n',
            '\n',
            'Nasdaq Composite\n',
            '.IXIC\n',
            '$14,244.955\n',
            '\n',
            '\n',
            'Input "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Major Stock Indices', menu_display)
        menu.add_parent_menu('Main Menu')
        menu.add_menu_choice('#main', 'Main Menu')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_application_tutorial_menu(self):
        menu_display = [
            'Application Tutorial\n',
            '\n',
            "Search Stocks provides you with two options, either to search by stock symobl or company name. The stock symbol has to be exact, otherwise it will require you to re-input a stock symbol. The search by company name gives you partial matches of a company name. It provides a greater amount of flexibility when you don't know the stock symbol and can get you in the vicinity of a company whose name you don't fully know.\n",
            '\n',
            'Stock Holdings provides you an overview of all stock positions held by you. You can then view each stock individually by selecting a company from your holdings.\n',
            '\n',
            'Major Stock Indices provide you a list of indices and their prices: the Dow Jones Industrial Average, S&P500, and Nasdaq Composite.\n',
            '\n',
            '\n',
            'Input "#main" to go back to the Main Menu:\n']
        menu = Menu('Application Tutorial', menu_display)
        menu.add_parent_menu('Main Menu')
        menu.add_menu_choice('#main', 'Main Menu')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def acquire_user_selected_menu(self):
        user_input = ''
        while user_input not in (self.menu_tree[self.current_menu]).get_menu_choices():
            user_input = input('Input request: ')
            if user_input == 'exit': return False ##### Temporary exit command
            valid_input = user_input in (self.menu_tree[self.current_menu]).get_menu_choices()
            variable_screen = '@#$%^&*!variable screen@#$%^&*!' in (self.menu_tree[self.current_menu]).get_menu_choices()
            if not valid_input:
                if variable_screen and user_input not in self.invalid_inputs:
                    return (self.menu_tree[self.current_menu]).get_menu_choices()['@#$%^&*!variable screen@#$%^&*!']
                print('Incorrect request entered. Please try again.\n')
                user_input = ''
        menu = (self.menu_tree[self.current_menu]).get_menu_choices()[user_input]
        return menu

    def print_menu_and_display_request_options_to_user(self):
        print(self)
        menu = self.acquire_user_selected_menu()
        if menu is False: return False ##### Temporary exit command
        self.previous_menu = self.current_menu
        self.current_menu = menu
        return True
    
    def __str__(self):
        menu = ''.join((self.menu_tree[self.current_menu]).get_menu_display())
        os.system('clear')
        print()
        return menu

            
if __name__ == '__main__':
    ui = Smta_Ui()
    ui.print_menu_and_display_request_options_to_user()
