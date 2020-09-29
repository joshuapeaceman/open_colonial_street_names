import os
import sys


def get_file_dir():
    application_path = getattr(sys, '_MEIPASS', None)
    if not application_path:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return str(application_path)




def xgv_configs_path():
    return os.path.join('xgv', 'configs')


def get_mainWindow_ui_file_path():
    return os.path.join(get_file_dir(), 'gui', 'mainWindow.ui')

def get_dresden_street_names_from_xlsx_dir():
    return os.path.join(get_file_dir(), 'data_and_configs', 'dresden.xlsx')

def get_category_json_dir():
    return os.path.join(get_file_dir(), 'data_and_configs', 'categories_and_problematic_names.json')