import xlrd
from PyQt5 import QtWidgets, QtCore
from xml.etree import ElementTree

from PyQt5.QtWidgets import QTreeWidgetItem

from src.model import Street
from src.gui import MainWindow


from src import BasePath
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




    def open_street_names_from_xlsx_file(self):
        wb = xlrd.open_workbook(BasePath.get_dresden_street_names_from_xlsx_dir())
        sheet = wb.sheet_by_index(0)

        for i in range(sheet.nrows):
            self.unique_streets.update({i: Street.Street(sheet.cell_value(i, 1),
                                                         sheet.cell_value(i, 2),
                                                         sheet.cell_value(i, 3))})

        self.load_street_names_into_table_widget()


    def load_street_names_into_table_widget(self):
        for idx in self.unique_streets:
            parent = QTreeWidgetItem(self._mainWindow.street_names)
            parent.setText(0, str(self.unique_streets[idx].street_name))
            parent.setText(1,  str(self.unique_streets[idx].stadtteil))
            parent.setText(2,  str(self.unique_streets[idx].zip_code))
            parent.setText(3,  str(self.unique_streets[idx].city))

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


