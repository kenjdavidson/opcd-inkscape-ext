
from argparse import ArgumentParser
import inkex 

class BaseOpcdExtension(inkex.EffectExtension):
    def add_arguments(self, pars: ArgumentParser) -> None:
        pars.add_argument(
            "--debug_mode", 
            type=inkex.Boolean, 
            help="Enable debug messages"
        )
        # The selected tab when `accept` button is clicked.  This could be used to run different functionality based on the 
        # current tab.  For now it doesn't do much.
        pars.add_argument(
            "--tab", 
            type=str, 
            dest="tab", 
            default="controls", 
            help=""
        )