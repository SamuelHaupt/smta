# flake8: noqa

import smta_ui
import smta_controller as controller


import investiny


def main():
    ui = smta_ui.Smta_Ui()
    run_program = True
    while run_program:
        if ui is False: return
        run_program = ui.print_menu_and_display_request_options_to_user()



if __name__ == '__main__':
    main()
