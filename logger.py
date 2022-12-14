
from inkex import utils

class Logger:
    """
    Standardize logging within the Inkscape extension package.
    """
    
    def __init__(self, debug: bool):
        self.debug_mode = debug

    def debug(self, what):
        if self.debug_mode:
            utils.debug(what)
