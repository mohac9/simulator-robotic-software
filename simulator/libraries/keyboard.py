import robot_components.boards as boards


def get_name():
    return "Keypad"


def get_methods():
    """
    Returns the methods of the library as a dict, whose
    key is the naming in Arduino and whose value is the
    corresponding method.
    Returns:
        A dict with the methods
    """
    methods = {}
    methods["getKey"] = ("char", "get_key", [], -1)
    return methods


def get_not_implemented():
    return []


class Keypad:

    def __init__(self, board=None, keymap=None, pin_rows=None,
                 pin_columns=None, size_rows=None, size_columns=None):
        """
        Constructor for Keypad class
        """
        self.board = board
        self.keymap = keymap
        self.pin_rows = pin_rows
        self.pin_columns = pin_columns
        self.size_rows = size_rows
        self.size_columns = size_columns

    def set_board(self, board: boards.Board):
        """
        Sets the board that the robot is using
        """
        self.board = board

    def get_key(self):
        pass

    def make_keymap(self):
        pass

