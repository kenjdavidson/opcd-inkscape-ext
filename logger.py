
from inkex import utils

class Logger:
    def __init__(self, debug: bool):
        self.debug_mode = debug

    def debug(self, what):
        if self.debug_mode:
            utils.debug(what)
