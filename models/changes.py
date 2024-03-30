class BackgroundChange:
    def __init__(self, previous_color, new_color):
        self.__previous_color = previous_color
        self.__new_color = new_color

    def get_previous_color(self):
        return self.__previous_color

    def get_new_color(self):
        return self.__new_color


class TextAreaChange:
    def __init__(self):
        pass
