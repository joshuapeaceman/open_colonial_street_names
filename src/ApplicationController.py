from PyQt5 import QtWidgets, QtCore
from xml.etree import ElementTree
from src.model import Street

class AppController:
    def __init__(self):
        self.unique_streets = {}
        self.streets = {}
        self.colonial_problems = []
        self.statistics = {}

        self._mainWindow = None
        self.set_up_gui()
        self.read_street_names_from_osm_database()

    def set_up_gui(self):
        pass

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


