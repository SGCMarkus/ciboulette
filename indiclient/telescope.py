# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with cameras via the INDI protocol, http://www.indilib.org.
"""

import time
import io

import logging
import logging.handlers

from astropy.io import fits
from astropy.table import Table

from .indiclient import indiclient
from ciboulette.indiclient.indimount import Telescope

log = logging.getLogger("")
log.setLevel(logging.INFO)

class telescopesimul(Telescope):
    """
    Wrap Mount, set driver to Simulator mount, and point to localhost by default.
    """
    def __init__(self, host='localhost', port=7624):
        super(telescopesimul, self).__init__(host, port, driver="Telescope Simulator")
        self.mount_name = "Telescope Simulator"
        self.process_events()
    
    @property
    def target_pier_side(self):
        return ["N/A"]

    @target_pier_side.setter
    def target_pier_side(self,string):
        pass

    @property
    def telescope_park_position(self):
        return ["N/A"]
    
class EQMod(Telescope):
    """
    Wrap Mount, set driver to EQMod mount, and point to localhost by default.
    """
    def __init__(self, host='localhost', port=7624):
        super(EQMod, self).__init__(host, port, driver="EQMod Mount")
        self.mount_name = "EQMod"
        self.process_events()
        """
        Set BAUD_RATE at 115200 : https://www.indilib.org/devices/telescopes/eqmod.html
        """
        self.baud_rate = '115200'
        
    @property    
    def baud_rate(self):
        """
        Return BAUD_RATE mode, return astropy table
        9600, 19200, 38400, 57600, 115200, 230400
        """        
        p = Table()
        p['9600'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "9600")]
        p['19200'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "19200")]
        p['38400'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "38400")]
        p['57600'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "57600")]
        p['115200'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "115200")]
        p['230400'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "230400")]
        return p

    @baud_rate.setter
    def baud_rate(self,label):
        """
        Set BAUD_RATE 
        """
        if label in ('9600','19200','38400','57600','115200','23040'):
            vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "DEVICE_BAUD_RATE", label)       
            if self.debug:
                vec.tell()               
            