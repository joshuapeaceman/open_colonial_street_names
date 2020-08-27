class Street:
    def __init__(self, street_name):
        self.__street_name = street_name
        self.__city = ''
        self.__zip_code = ''
        self.__state = ''

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
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value