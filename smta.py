# flake8: noqa

import smta_ui
import smta_controller as c


import investiny


def main():
    ui = smta_ui.SmtaUI()
    c_search_by_name_controller = c.SearchByNameController()
    c_stock_data_request_controller = c.StockDataRequestController()
    c_stock_holdings_controller = c.StockHoldingsController()
    run_program = True
    while run_program:
        next_menu, user_input = ui.print_menu_and_display_request_options_to_user()
        if next_menu is False: return
        
        if ui.get_previous_menu_name() == 'Search by Name' and next_menu == 'Search by Name Results':
            search_by_name_results_menu = ui.get_menu_from_menu_tree(next_menu)
            if not search_by_name_results_menu.get_menu_dynamic_input():
                dynamic_input = c_search_by_name_controller.get_stock_name_match_from_user_input(user_input)
                if dynamic_input is False:
                    ui.backtrack_current_and_previous_menus()
                    continue
                search_by_name_results_menu.set_menu_dynamic_input(dynamic_input)
            success = search_by_name_results_menu.generate_dynamic_menu()
            if success is False and user_input == '#next':
                search_by_name_results_menu.reset_dynamic_menu()
                ui.backtrack_current_and_previous_menus()
                continue

        if ui.get_previous_menu_name() == 'Search by Name Results' and next_menu == 'Search by Name Results':
            search_by_name_results_menu = ui.get_menu_from_menu_tree(next_menu)
            if not search_by_name_results_menu.get_menu_dynamic_input():
                dynamic_input = c_search_by_name_controller.get_stock_name_match_from_user_input(user_input)
                if dynamic_input is False:
                    ui.backtrack_current_and_previous_menus()
                    continue
                search_by_name_results_menu.set_menu_dynamic_input(dynamic_input)
            success = search_by_name_results_menu.generate_dynamic_menu()
            if success is False and user_input == '#next':
                search_by_name_results_menu.reset_dynamic_menu()
                ui.backtrack_current_and_previous_menus()
                continue

        if ui.get_previous_menu_name() == 'Search by Name Results' and next_menu == 'Individual Stock View':
            individual_stock_view = ui.get_menu_from_menu_tree(next_menu)
            company_name = user_input
            stock_symbol = c_search_by_name_controller.get_stock_symbol_from_stock_name(company_name)
            dynamic_input = c_stock_data_request_controller.get_stock_information_for_individual_stock_view(stock_symbol)
            individual_stock_view.set_menu_dynamic_input(dynamic_input)
            success = individual_stock_view.generate_dynamic_menu()

        if ui.get_previous_menu_name() == 'Search by Symbol' and next_menu == 'Stock Symbol Confirmation':
            individual_stock_view = ui.get_menu_from_menu_tree(next_menu)
            stock_symbol = user_input
            dynamic_input = c_stock_data_request_controller.get_stock_information_for_search_by_symbol_confirmation(stock_symbol)
            print(dynamic_input)
            if dynamic_input is False:
                print('Error with stock symbol request.')
                ui.backtrack_current_and_previous_menus()
                continue
            individual_stock_view.set_menu_dynamic_input(dynamic_input)
            success = individual_stock_view.generate_dynamic_menu()
            if success is False:
                print('Error with displaying dynamic input')
                individual_stock_view.reset_dynamic_menu()
                ui.backtrack_current_and_previous_menus()
                continue

        if ui.get_previous_menu_name() == 'Stock Symbol Confirmation' and next_menu == 'Individual Stock View':
            individual_stock_view = ui.get_menu_from_menu_tree(next_menu)
            stock_symbol = user_input
            dynamic_input = c_stock_data_request_controller.get_stock_information_for_individual_stock_view(stock_symbol)
            individual_stock_view.set_menu_dynamic_input(dynamic_input)
            success = individual_stock_view.generate_dynamic_menu()

        if next_menu == 'Major Stock Indices':
            major_stock_indices = ui.get_menu_from_menu_tree(next_menu)
            dynamic_input = c_stock_data_request_controller.get_stock_information_for_major_stock_indices()
            major_stock_indices.set_menu_dynamic_input(dynamic_input)
            success = major_stock_indices.generate_dynamic_menu()

        if next_menu == 'Stock Holdings':
            stock_holdings = ui.get_menu_from_menu_tree(next_menu)
            dynamic_input = c_stock_holdings_controller.get_all_stock_data_performances_from_microservice()
            stock_holdings.set_menu_dynamic_input(dynamic_input)
            success = stock_holdings.generate_dynamic_menu()



if __name__ == '__main__':
    main()
