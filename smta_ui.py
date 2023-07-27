# flake8: noqa

import os

class Menu():
    def __init__(self, menu_name, previous_menu, menu_display):
        self.menu_name = menu_name
        self.menu_display = menu_display
        self.menu_default_display = menu_display
        self.previous_menu_name = previous_menu
        self.menu_choices = dict()
        self.menu_with_dynamic_selection = False
        self.menu_with_enumerated_values = False
        self.menu_dynamic_input = []
        self.menu_dynamic_length = 10
        self.menu_dynamic_input_start = 0
        self.menu_dynamic_input_stop = 0

    def get_menu_name(self):
        return self.menu_name

    def get_menu_display(self):
        return self.menu_display

    def set_menu_display(self, menu_display):
        self.menu_display = menu_display

    def get_menu_default_display(self):
        return self.menu_default_display

    def get_previous_menu_name(self):
        return self.previous_menu_name

    def get_menu_choices(self):
        return self.menu_choices

    def get_menu_choice(self, menu_choice):
        return self.menu_choices[menu_choice]
    
    def add_menu_choice(self, selection_request, menu_choice):
        self.menu_choices[selection_request] = menu_choice

    def is_menu_with_dynamic_selection(self):
        return self.menu_with_dynamic_selection

    def set_menu_dynamic_selection(self):
        self.menu_with_dynamic_selection = True

    def is_menu_with_enumerated_values(self):
        return self.menu_with_enumerated_values

    def set_menu_enumerated_values(self):
        self.menu_with_enumerated_values = True

    def get_menu_dynamic_input(self):
        return self.menu_dynamic_input

    def set_menu_dynamic_input(self, dynamic_input):
        self.menu_dynamic_input = dynamic_input

    def get_menu_dynamic_length(self):
        return self.menu_dynamic_length

    def get_menu_dynamic_input_start(self):
        return self.menu_dynamic_input_start

    def set_menu_dynamic_input_start(self, start):
        self.menu_dynamic_input_start = start

    def get_menu_dynamic_input_stop(self):
        return self.menu_dynamic_input_stop

    def set_menu_dynamic_input_stop(self, stop):
        self.menu_dynamic_input_stop = stop

    def reset_menu_dynamic_input_start_stop(self):
        self.set_menu_dynamic_input_start(0)
        self.set_menu_dynamic_input_stop(0)

    def reset_dynamic_menu(self):
        self.reset_menu_dynamic_input_start_stop()
        self.set_menu_dynamic_input(list())

    def generate_dynamic_input_location(self):
        dynamic_input_list_len = len(self.get_menu_dynamic_input())  
        start = self.get_menu_dynamic_input_start()
        stop = self.get_menu_dynamic_input_stop()
        
        # Dynamic input list is empty; generate error message.
        if start == dynamic_input_list_len:
            print('Error with dynamic input. Length is 0')
            start = None
            stop = None
        # Stop generating dynamic input when reaching the end of dynamic input list.
        elif stop == dynamic_input_list_len:
            start = None
            stop = None
        # Generate dynamic input; increment start and stop.
        elif stop < dynamic_input_list_len:
            start = stop
            stop = stop + self.get_menu_dynamic_length() if stop + self.get_menu_dynamic_length() <= dynamic_input_list_len else dynamic_input_list_len
        
        if start is not None:
            self.set_menu_dynamic_input_start(start)
            self.set_menu_dynamic_input_stop(stop)
        return start, stop

    def generate_dynamic_menu(self):
        menu_display = self.get_menu_default_display()
        dynamic_input_list = self.get_menu_dynamic_input()
        new_menu_display = list()
        for index in range(menu_display.index('placeholder')):
            new_menu_display.append(menu_display[index])

        start, stop = self.generate_dynamic_input_location()
        if start is not None:
            for index in range(start, stop):
                if self.is_menu_with_enumerated_values() is True:
                    new_menu_display.append(f"{index+1}: " + '\n'.join(dynamic_input_list[index]))
                else:
                    new_menu_display.append('\n'.join(dynamic_input_list[index]))
                new_menu_display.append('\n')
            
            for index in range(menu_display.index('placeholder')+1, len(menu_display)):
                new_menu_display.append(menu_display[index])

            self.set_menu_display(new_menu_display)
        else:
            return False


class SmtaUI():
    def __init__(self):
        self.current_menu_name = 'Main Menu'
        self.previous_menu_name = 'Main Menu'
        self.invalid_inputs = dict()
        self.menu_tree = dict()
        self.populate_invalid_inputs()
        self.build_main_menu()
        self.build_search_stocks_search_node_menu()
        self.build_search_by_symbol_menu()
        self.build_stock_symbol_confirmation_menu()
        self.build_search_by_name_menu()
        self.build_search_by_name_results_menu()
        self.build_individual_stock_view_menu()
        self.build_stock_holdings_menu()
        self.build_major_stock_indices_menu()
        self.build_application_tutorial_menu()

    def get_current_menu_name(self):
        return self.current_menu_name

    def set_current_menu_name(self, current_menu_name):
        self.current_menu_name = current_menu_name

    def get_previous_menu_name(self):
        return self.previous_menu_name

    def set_previous_menu_name(self, previous_menu_name):
        self.previous_menu_name = previous_menu_name

    def backtrack_current_and_previous_menus(self):
        next_menu = self.get_menu_from_menu_tree(self.get_current_menu_name())
        current_menu = self.get_menu_from_menu_tree(next_menu.get_previous_menu_name())
        previous_menu = self.get_menu_from_menu_tree(current_menu.get_previous_menu_name())
        self.set_current_menu_name(current_menu.get_menu_name())
        self.set_previous_menu_name(previous_menu.get_menu_name())

    def get_menu_tree(self):
        return self.menu_tree

    def add_menu_to_menu_tree(self, menu_name: str, menu: Menu) -> bool:
        if menu_name in self.menu_tree:
            return False
        else:
            self.menu_tree[menu_name] = menu
            return True

    def get_menu_from_menu_tree(self, menu_name: str) -> Menu:
        return self.menu_tree[menu_name]

    def get_invalid_inputs(self):
        return self.invalid_inputs

    def populate_invalid_inputs(self):
        self.invalid_inputs[''] = None

    def build_main_menu(self):
        menu_display = [
            'Main Menu\n',
            '\n',
            'Select a menu item:\n',
            '1 Search Stocks (For ease of use, select Search by Symbol on next screen and enter stock symbol, if searching for a specific company)\n',
            '2 Stock Holdings (Your personal stock holdings)\n',
            '3 Major Stock Indices\n',
            '4 Application Tutorial\n']
        menu = Menu('Main Menu', 'Main Menu', menu_display)
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
        menu = Menu('Search Mode', 'Main Menu', menu_display)
        menu.add_menu_choice('1', 'Search by Symbol')
        menu.add_menu_choice('2', 'Search by Name')
        menu.add_menu_choice('3', 'Main Menu')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_search_by_symbol_menu(self):
        menu_display = [
            'Search Stocks:Search Mode:Search by Symbol\n',
            '\n',
            'Stock symbol can include any variation of letters ranging from one value up to seven. A new request for input will be presented when an invalid input has been made.\n'
            'Input Stock Symbol, "#back" to go back to Search Mode screen, or "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Search by Symbol', 'Search Mode', menu_display)
        menu.add_menu_choice('#back', menu.get_previous_menu_name())
        menu.add_menu_choice('#main', 'Main Menu')
        menu.add_menu_choice('@#$%^&*!dynamic screen@#$%^&*!', 'Stock Symbol Confirmation')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_stock_symbol_confirmation_menu(self):
        menu_display = [
            'Search Stocks:Search Mode:Search by Symbol:Stock Symbol Confirmation\n',
            '\n',
            'Is the following information correct?\n',
            'placeholder',
            '\n',
            'For confirmation, input 1 for "yes" or 2 for "no". You can also input "#back" to go back to Search by Symbol screen or "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Stock Symbol Confirmation', 'Search by Symbol', menu_display)
        menu.add_menu_choice('#back', menu.get_previous_menu_name())
        menu.add_menu_choice('2', 'Search by Symbol')
        menu.add_menu_choice('#main', 'Main Menu')
        menu.add_menu_choice('@#$%^&*!dynamic screen@#$%^&*!', 'Individual Stock View')
        menu.set_menu_dynamic_selection()
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_search_by_name_menu(self):
        menu_display = [
            'Search Stocks:Search Mode:Search by Name\n',
            '\n',
            'Stock names can include any variation of letters with spaces ranging from 1 to 10 characters. First value must be an alpha character. A new request for input will be presented when an invalid input has been made.\n',
            'Input Stock Name, "#back" to go back to Search Mode screen, or "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Search by Name', 'Search Mode', menu_display)
        menu.add_menu_choice('#back', menu.get_previous_menu_name())
        menu.add_menu_choice('#main', 'Main Menu')
        menu.add_menu_choice('@#$%^&*!dynamic screen@#$%^&*!', 'Search by Name Results')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_search_by_name_results_menu(self):
        menu_display = [
            'Search Stocks:Search Mode:Search by Name:Search by Name Results\n',
            '\n',
            'placeholder',
            '\n',
            'Input corresponding number for the company you wish to request. Input "#next" to view more company names (if there are remaining companies), "#back" to go back to Search by Name screen, or "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Search by Name Results', 'Search by Name', menu_display)
        menu.add_menu_choice('#back', menu.get_previous_menu_name())
        menu.add_menu_choice('#main', 'Main Menu')
        menu.add_menu_choice('#next', 'Search by Name Results')
        menu.add_menu_choice('@#$%^&*!dynamic screen@#$%^&*!', 'Individual Stock View')
        menu.set_menu_dynamic_selection()
        menu.set_menu_enumerated_values()
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_individual_stock_view_menu(self):
        menu_display = [
            'Individual Stock View\n',
            '\n',
            'placeholder',
            '\n',
            'Input "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Individual Stock View', 'Main Menu', menu_display)
        menu.add_menu_choice('#main', 'Main Menu')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_stock_holdings_menu(self):
        menu_display = [
            'Stock Holdings\n',
            '\n',
            'placeholder',
            '\n',
            'Input "#main" to go back to the Main Menu screen or "#refresh" to refresh current stock prices and performances (while during standard open market hours): \n']
        menu = Menu('Stock Holdings', 'Main Menu', menu_display)
        menu.add_menu_choice('#main', 'Main Menu')
        menu.add_menu_choice('#refresh', 'Stock Holdings')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def build_major_stock_indices_menu(self):
        menu_display = [
            'Major Stock Indices\n',
            '\n',
            'placeholder',
            '\n',
            'Input "#main" to go back to the Main Menu screen: \n']
        menu = Menu('Major Stock Indices', 'Main Menu', menu_display)
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
        menu = Menu('Application Tutorial', 'Main Menu', menu_display)
        menu.add_menu_choice('#main', 'Main Menu')
        self.add_menu_to_menu_tree(menu.get_menu_name(), menu)

    def acquire_user_selected_menu(self):
        user_input = ''
        next_menu = None
        current_menu = self.get_menu_from_menu_tree(self.get_current_menu_name())
        valid_input = user_input in current_menu.get_menu_choices()
        while not valid_input:
            user_input = input('Input request: ')
            if user_input == 'exit': return False, None ##### Temporary exit command
            valid_input = user_input in current_menu.get_menu_choices()
            dynamic_screen = '@#$%^&*!dynamic screen@#$%^&*!' in current_menu.get_menu_choices()
            if valid_input:
                next_menu = current_menu.get_menu_choice(user_input)
                if user_input in ['#back', '#main']:
                    current_menu.reset_dynamic_menu()
            elif not valid_input:
                if dynamic_screen and current_menu.is_menu_with_dynamic_selection() is False:
                    if user_input not in self.get_invalid_inputs() and user_input.isdigit() is False:
                        next_menu = current_menu.get_menu_choice('@#$%^&*!dynamic screen@#$%^&*!')
                        break
                elif dynamic_screen and current_menu.is_menu_with_dynamic_selection() is True:
                    if user_input.isdigit() \
                            and int(user_input) > 0 \
                            and int(user_input) <= len(current_menu.get_menu_dynamic_input()):
                        next_menu = current_menu.get_menu_choice('@#$%^&*!dynamic screen@#$%^&*!')
                        user_input = current_menu.get_menu_dynamic_input()[int(user_input)-1][0]
                        current_menu.reset_dynamic_menu()
                        break
                print('Incorrect request entered. Please try again.\n')
                user_input = ''
        return next_menu, user_input

    def print_menu_and_display_request_options_to_user(self):
        print(self)
        next_menu, user_input = self.acquire_user_selected_menu()
        if next_menu is False: return False, None ##### Temporary exit command
        self.set_previous_menu_name(self.get_current_menu_name())
        self.set_current_menu_name(next_menu)
        return next_menu, user_input
    
    def __str__(self):
        menu = ''.join((self.get_menu_from_menu_tree(self.get_current_menu_name())).get_menu_display())
        os.system('clear')
        print()
        return menu

            
if __name__ == '__main__':
    ui = SmtaUI()
    ui.print_menu_and_display_request_options_to_user()
