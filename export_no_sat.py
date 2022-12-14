#!/usr/bin/python

from argparse import ArgumentParser
import copy
import os
import subprocess
import tempfile
from base_opcd_extension import BaseOpcdExtension
import inkex
from logger import Logger

GSPRO_CONVERT = "GSProSVGConvert.exe"

class ExportNoSat(BaseOpcdExtension):
    """
    Export the no satellite version of your SVG.  If requested (on by default) the file will be run through the 
    conversion process.

    @see https://github.com/StefanTraistaru/batch-export/
    """

    def add_arguments(self, pars: ArgumentParser) -> None:
        super().add_arguments(pars)

        pars.add_argument(
            "--satellite_layer", 
            type=str, 
            default="Satellite", 
            help="Name of the satellite layer"
        )
        pars.add_argument(
            "--export_path", 
            type=str, 
            help="Export path for your terrain conversion files"
        )
        pars.add_argument(
            "--run_conversion", 
            type=inkex.Boolean, 
            help="Run conversion after export"
        )

    def effect(self):
        self.logger = Logger(self.options.debug_mode)
        self.no_sat_file_name = self.export_file_name()
        self.logger.debug("Exporting no satellite SVG file '{}'".format(self.no_sat_file_name))
        
        exported_file = self.export_file(self.remove_layer(), self.no_sat_file_name)

        if self.options.run_conversion:
            self.run_conversion(exported_file)

        self.logger.debug("Completed export of no sat!")

    def export_file_name(self):
        names = self.svg.name.split(".")
        return "{}_no_sat.{}".format(names[0], names[1])

    def remove_layer(self):
        """
        Remove the `Satellite` layer, or whichever label/name was provided in the options.
        """
        self.logger.debug("Attempting to remove '{}' layer".format(self.options.satellite_layer))
        document = copy.deepcopy(self.document)
        xpath = '//svg:g[@inkscape:label="{}"]'.format(self.options.satellite_layer)
        satellite_layers = document.xpath(xpath, namespaces=inkex.NSS)
        if satellite_layers:
            satellite_layer = satellite_layers[0]
            satellite_layer.getparent().remove(satellite_layer)
        else:
            self.logger.debug("'{}' layer was not found".format(self.options.satellite_layer))

        return document

    def export_file(self, document, file_name):
        """
        use `inkscape` to export that file do the appropriate location.  

        @see https://inkscape.org/doc/inkscape-man.html
        """
        temporary_file = self.write_temp_document(document)
        export_path = os.path.join(self.options.export_path, self.no_sat_file_name)
        command = [
            "inkscape",
            "--export-filename={}".format(export_path),
            temporary_file
        ]
        self.run_process(command)

        return export_path

    def write_temp_document(self, document):
        """
        Write the document to a temporary file.  I'm not entirely sure this is required (might be possible just to go straight to disk)
        but this allows the use of the `inkscape --export` from the file just incase something special happens.
        """
        with tempfile.NamedTemporaryFile(delete=False) as temporary_file:
            self.logger.debug("Creating temp file {}".format(temporary_file.name))
            document.write(temporary_file.name)
            return temporary_file.name

    def run_conversion(self, exported_file):
        """
        Run the conversion process.
        
        At this point it assumes the exe is in the output folder which follows the tutorials, so it should be ok.
        
        @see https://www.youtube.com/watch?v=1RxOddF5ICg&list=PLOHx7fwaLyc_IxIX7rIHY9Yk_OoMzJclO
        """
        command = [
            os.path.join(self.options.export_path, GSPRO_CONVERT),
            exported_file
        ]
        self.run_process(command)

    def run_process(self, command):
        try:
            self.logger.debug("Running command: {}".format(command))
            with subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as proc:
                proc.wait(timeout=300)
        except OSError as err:
            self.logger.debug('Error while exporting file {}.'.format(err))
            inkex.errormsg('Error while exporting file {}.'.format(command))
            exit()

if __name__ == '__main__':
    ExportNoSat().run()
