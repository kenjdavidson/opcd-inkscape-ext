#!/usr/bin/python

from argparse import ArgumentParser
from base_opcd_extension import BaseOpcdExtension
import inkex
from logger import Logger
from spline_type import SplineType

class ShowSplinesOfType(BaseOpcdExtension):
    """
    Update visibility settings of paths so that only those of the selected type are 
    showing.
    """

    def add_arguments(self, pars: ArgumentParser) -> None:
        super().add_arguments(pars)

        pars.add_argument(
            "--spline_type",
            type=str,
            default="TEE",
            help="Type of spline to show (the rest will be hidden)"
        )
        pars.add_argument(
            "--show_all",
            type=inkex.Boolean,
            default=False,
            help="Show all spline types"
        )
        pars.add_argument(
            "--show_unknown",
            type=inkex.Boolean,
            default=False,
            help="Show splines which don't match OPCD colours"
        )

    def effect(self):
        self.logger = Logger(self.options.debug_mode)
        self.logger.debug("Showing all {}(s) (hiding all others)".format(self.options.spline_type))
        paths = self.document.xpath('//svg:path', namespaces=inkex.NSS)

        self.logger.debug("Found {} paths".format(len(paths)))
    
        if self.options.show_unknown:
            self.show_unknown(paths)
        elif self.options.show_all:
            self.show_all(paths)
        else:
            self.display_paths(paths, SplineType[self.options.spline_type])

    def display_paths(self, paths, spline_type):
        count = 0

        for path in paths:
            if path.style['fill'].upper() == spline_type.value.upper() :
                path.style  ['display'] = 'inline'
                count += 1
            else:
                path.style['display'] = 'none'

        self.logger.debug("Found {} paths of type {}".format(count, spline_type.name))

    def show_all(self, paths):
        for path in paths:
            path.style['display'] = 'inline'

    def show_unknown(self, paths):
        count = 0
        all_splines = set([spline.value for spline in SplineType])
        self.logger.debug("Found {} unknown Spline types".format(count))

        for path in paths:
            if path.style['fill'].upper() in all_splines:
                path.style['display'] = 'none'
            else:
                path.style['display'] = 'inline'
                count += 1

        self.logger.debug("Found {} unknown splines".format(count))

if __name__ == '__main__':
    ShowSplinesOfType().run()
