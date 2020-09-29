import traceback
from xml.etree import ElementTree

import jsonpickle
import xlrd
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTreeWidgetItem

from src import BasePath
from src.gui import MainWindow
from src.model import Street, ProblematicNames


class AppController:
    def __init__(self, app_version):
        self._app_version = app_version
        self.unique_streets = {}
        self.problematic_names = []
        self.statistics = {}

        self._mainWindow = None
        self.set_up_gui()

        """only needed for open street map data sets which are not very nice"""
        # self.read_street_names_from_osm_database()

        self.open_street_names_from_xlsx_file()

    def set_up_gui(self):
        self._mainWindow = MainWindow.MainWindow(self._app_version)
        self._mainWindow.show()

        self._mainWindow.search.clicked.connect(self.search_street_data_set_for_problematic_names)
        self._mainWindow.add.clicked.connect(self.add_name_to_problematic_list)

        self.load_categories_from_json_into_combo_box()
        self.load_problematic_names_from_json_into_treeWidget()

    def load_categories_from_json_into_combo_box(self):
        self._mainWindow.kategorie.clear()
        try:
            with open(BasePath.get_category_json_dir(), 'r') as file:
                data = file.read()
                jsonpickle.set_decoder_options('json', encoding='utf8')
                json_data = jsonpickle.decode(data)

                for item in json_data['categories']:
                    self._mainWindow.kategorie.addItem(item)
        except:
            traceback.print_exc()

    def load_problematic_names_from_json_into_treeWidget(self):

        self.problematic_names.clear()

        try:
            with open(BasePath.get_category_json_dir(), 'r') as file:
                data = file.read()
                jsonpickle.set_decoder_options('json', encoding='utf8')
                json_data = jsonpickle.decode(data)

                for item in json_data['problematic_names']:
                    name = str(item[0])
                    if 'Ã¶' in name:
                        print('stop')
                        name = name.replace('Ã¶', 'ö')
                    elif 'Ã¤' in name:
                        name = name.replace('Ã¤', 'ä')
                    elif 'Ã¼' in name:
                        name = name.replace('Ã¼', 'ü')
                    self.problematic_names.append(ProblematicNames.ProblematicNames(name,
                                                                                    str(item[1])))

                self.load_problematic_names_into_view()
        except:
            traceback.print_exc()

    def load_problematic_names_into_view(self):
        self._mainWindow.problematic_names.clear()
        for problematic_name in self.problematic_names:
            parent = QTreeWidgetItem(self._mainWindow.problematic_names)
            parent.setText(0, str(problematic_name.name))
            parent.setText(1, str(problematic_name.category))

        self._mainWindow.problematic_names.setHeaderLabels(
            ['Name', 'Kategorie'])

        self._mainWindow.problematic_names.setSortingEnabled(True)
        self._mainWindow.problematic_names.header().show()


    def search_street_data_set_for_problematic_names(self):
        self.statistics.clear()

        for street_object in self.problematic_names:
            for idx in self.unique_streets:
                prob_name = str(street_object.name).lower()
                street_name = str(self.unique_streets[idx].street_name).lower()
                if prob_name in street_name:
                    if street_name in self.statistics:
                        self.statistics[street_name] += 1
                    else:
                        self.statistics[street_name] = 1

                    print(street_name, self.unique_streets[idx].zip_code)

        self.load_statistics_into_result_view()

    def load_statistics_into_result_view(self):
        self._mainWindow. resultview.clear()

        for idx in self.statistics:

            parent = QTreeWidgetItem(self._mainWindow.resultview)
            parent.setText(0, str(idx))
            parent.setText(1, str(self.statistics[idx]))

        self._mainWindow.resultview.setHeaderLabels(
            ['Straßenname', 'Anzahl'])

        self._mainWindow.resultview.setSortingEnabled(True)
        self._mainWindow.resultview.header().show()

    def add_name_to_problematic_list(self):
        if self._mainWindow.name_begriff.text() != '' and self._mainWindow.kategorie.currentText() != '':
            self.problematic_names.append(ProblematicNames.ProblematicNames(self._mainWindow.name_begriff.text(), self._mainWindow.kategorie.currentText()))
            self.load_problematic_names_into_view()


    def open_street_names_from_xlsx_file(self):
        wb = xlrd.open_workbook(BasePath.get_dresden_street_names_from_xlsx_dir())
        sheet = wb.sheet_by_index(0)

        for i in range(sheet.nrows):
            self.unique_streets.update({i: Street.Street(sheet.cell_value(i, 1),
                                                         sheet.cell_value(i, 2),
                                                         sheet.cell_value(i, 3))})

        self.load_street_names_into_table_widget()

    def load_street_names_into_table_widget(self):
        self._mainWindow.street_names.clear()
        for idx in self.unique_streets:
            parent = QTreeWidgetItem(self._mainWindow.street_names)
            parent.setText(0, str(self.unique_streets[idx].street_name))
            parent.setText(1, str(self.unique_streets[idx].stadtteil))
            parent.setText(2, str(self.unique_streets[idx].zip_code))
            parent.setText(3, str(self.unique_streets[idx].city))

        self._mainWindow.street_names.setHeaderLabels(
            ['Straßenname', 'Stadtteil', 'Postleitzahl', 'Stadt'])

        self._mainWindow.street_names.setSortingEnabled(True)
        self._mainWindow.street_names.header().show()

    def open_osm_files_and_return_file_dir(self):
        dialog = QtWidgets.QFileDialog(None)
        dialog.setWindowTitle('Open OSM File')
        dialog.setNameFilter('OSM files (*.osm *.xml)')
        dialog.setDirectory(QtCore.QDir.currentPath())
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])
            return file_full_path

    def read_street_names_from_osm_database(self):
        cnt = 0
        for _, element in ElementTree.iterparse(self.open_osm_files_and_return_file_dir()):
            if element.tag == 'way':
                for c in element:
                    if 'k' in c.attrib:
                        if c.attrib['k'] == 'name':
                            if c.attrib['v'] != '':
                                self.streets.update({cnt: []})
                                self.streets[cnt].append(c.attrib['v'])

                                # street = Street.Street(c.attrib['v'])
                                for x in element:
                                    if 'k' in x.attrib:
                                        if c.attrib['k'] == 'addr:city':
                                            self.streets[cnt].append(x.attrib['v'])
                                        if x.attrib['k'] == 'postal_code' or x.attrib['k'] == 'addr:postcode':
                                            self.streets[cnt].append(x.attrib['v'])
                                cnt += 1

        for _ in self.streets:
            self.unique_streets.update({self.streets[_][0]: ''})

        pass

        # for idx, data in enumerate(self.unique_streets):
        #     for idx2, data2 in enumerate(self.streets):
        #         if data == self.streets[idx2][0]:
        #             if len(self.streets[idx2]) > 1:
        #                 pass
