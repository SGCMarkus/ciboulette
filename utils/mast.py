"""
Mast class
File id google 12QY7fQLqnoySHFnEoLMWQbqYjHmaDpGn

Observation Type:
                        string: intentType
Mission:
                        string: obs_collection
Instrument: 
                        string: instrument_name
Detector: 
                        string: detector
Project: 
                        string: project
Filters: 
                        string: filters
Waveband: 
                        string: wavelength_region
Target Name: 
                        string: target_name
Target Classification: 
                        string: target_classification
Observation ID: 
                        string: obs_id
RA: 
                        float: s_ra
Dec: 
                        float: s_dec
Proposal ID: 
                        string: proposal_id
Principal Investigator: 
                        string: proposal_pi
Product Type: 
                        string: dataproduct_type
Calibration Level: 
                        int: calib_level
Start Time:
                        float: t_min              
End Time: 
                        float: t_max
Exposure Length: 
                        float: t_exptime
Min. Wavelength: 
                        float: em_min
Max. Wavelength: 
                        float: em_max
Observation Title: 
                        string: obs_title
Release Date: 
                        float: t_obs_release
Proposal Type: 
                        string:proposal_type
Sequence Number: 
                        int: sequence_number
Region: 
                        string: s_region
Focale: 
                        float: focal
Format: 
                        float: format
Seeing: 
                        float: seeing
Moon: 
                        float: moon
jpegURL: 
                        string: jpeg_url
url:
                        string: url

"""

import time
from astropy.table import Table, unique, vstack
from astropy import units as u
import os
import wget
from ciboulette.base import constant
from collections import Counter, OrderedDict


class Mast(object):
    
    def __init__(self, idgoogledrive='12QY7fQLqnoySHFnEoLMWQbqYjHmaDpGn', fileoutput='mast.csv'):
        self.idgoogledrive = idgoogledrive
        self.fileoutput = fileoutput
        self.observation = Table()
        self.header = Table()     
        self.available = False      
        
    @property
    def create(self):
        """
        Create MAST type file with fits archives file
        """
        return True
    
    @property
    def read(self):
        """
        Read MAST type file
        Ex:  wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=12QY7fQLqnoySHFnEoLMWQbqYjHmaDpGn' -O mast.csv        
        """
        if os.path.exists(self.fileoutput) :
            os.remove(self.fileoutput)
        url = 'https://docs.google.com/uc?export=download&id='+self.idgoogledrive
        filedownload = wget.download(url,out=self.fileoutput,bar=None)      
        # For MAST data_start=3
        self.observation = Table.read(self.fileoutput, format='ascii.csv',header_start=2,data_start=3)   
        if len(self.observation) > 0:
            self.header = Table.read('mast_header.csv', format='ascii.csv',header_start=2,data_start=3)   
            self.available = True
        else:
            self.available = False
        return self.available

    @property
    def idfiledrive(self):
        """
        Return ID google drive file
        """     
        return self.idgoogledrive    
    
    @idfiledrive.setter
    def idfiledrive(self,idgoogledrive):
        """
        Set ID google drive file
         idgoogledrive (str): ID google drive file.csv.       
        """     
        self.idgoogledrive = idgoogledrive                 

    @property
    def output(self):
        """
        Return fileoutput
        """     
        return self.fileoutput

    @output.setter
    def output(self,fileoutput):
        """
        Set table of exposures with google drive 
         fileoutput (str): file.csv output.
        """
        self.fileoutput = fileoutput

    def ha(self,observation):
        """
        Return RA of plan. Format: Hours H.HHHH
         plan (Table): plan of planning.
        """           
        if self.available:
            return float(observation['s_ra'])/15

    def ra(self,observation):
        """
        Return RA of plan. Format: Hours D.DDDD
         plan (Table): plan of planning.
        """           
        if self.available:
            return float(observation['s_ra'])

    def dec(self,observation):
        """
        Return DEC of plan. Format: Degrees D.DDDD
         plan (Table): plan of planning.
        """    
        if self.available:
            return float(observation['s_dec']) 

    def coordinates(self,observation):
        """
        Return coordinates RA,DEC
        """
        if self.available:
            return self.ra(observation), self.dec(observation)

    @property
    def observations(self):
        """
        Return observations table
        """
        if len(self.observation) > 0:
            return self.observation

    @property
    def projects(self):
        """
        Return projects table
        """
        if len(self.observation) > 0:
            words = unique(self.observation, keys='project')
            return words['project']

    @property
    def targets(self):
        """
        Return targets table
        """
        if len(self.observation) > 0:
            words = unique(self.observation, keys='target_name')
            return words['target_name']
        
    def query_project(self, projet_name = 'HII'):
        """
        Return observations projects in table
        """
        return self._query_all('project', projet_name)

    def query_target(self, target_name = 'M31'):
        """
        Return observations targets in table
        """
        return self._query_all('target_name', target_name)
        
    def _query_all(self, name = 'target_name', target = 'M31'):
        """
        Return observations find in table
        """
        if len(self.observation) > 0:
            observations = self.header
            unique_by_name = unique(self.observation, keys= name)
            if len(unique_by_name) > 0:
                matches = [match for match in unique_by_name[name] if target in match]
                if len(matches) > 0:
                    for targets in matches:
                        mask = self.observation[name] == targets
                        observations = vstack([self.observation[mask], observations])  
                
                    observations = observations[0:len(observations)-1]
                    return observations
                else:
                    return 'No target'
            else:
                return 'No name'
        else:
            return 'No observations'
