class Street:
    def __init__(self, street_name, stadtteil, zip_code):
        self.__street_name = street_name
        self.__city = 'Dresden'
        self.__zip_code = zip_code
        self.__stadtteil = stadtteil

    @property
    def street_name(self):
        return self.__street_name

    @street_name.setter
    def street_name(self, value):
        self.__street_name = value

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, value):
        self.__city = value

    @property
    def zip_code(self):
        return self.__zip_code

    @zip_code.setter
    def zip_code(self, value):
        self.__zip_code = value

    @property
    def stadtteil(self):
        return self.__stadtteil

    @stadtteil.setter
    def stadtteil(self, value):
        self.__stadtteil = value