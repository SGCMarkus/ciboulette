"""Ciboulette class

"""

import time
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time
from astropy.table import Table
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u
from astropy import wcs
from astropy.utils.data import get_pkg_data_filename
from alpaca import Telescope, Camera, FilterWheel
from ciboulette.base import constent
from ciboulette.sector import sector as Sct
from ciboulette.utils import exposure as Exp
from ciboulette.utils import planning as Pln
from astropy import wcs


class Ciboulette(object):
        
    def __init__(self):
        self.data = []
        self.api_version = constent.API_version
        self.server = '192.168.1.18'
        self.port = 11111
        self.device = 0
        self.focale = 85.0
        self.diameter = 60
        self.latitude = 49.5961
        self.longitude = 359.65
        self.elevation = 100
        self.instrument = 'Atik 383L+'
        self.naxis1 = 3326
        self.naxis2 = 2504
        self.binXY = 1
        self.pixelXY = 5.4
        self.filter_name = 'L'
        self.telescope_name = 'CIBOULETTE-A'
        self.observer_name = 'CAM1'
        self.dataset = 'dataset'
        self.archive_table = 'dataset/archives'
        self.ra = 0.0 # hours
        self.dec = 90.0 # degrees
        self.object_name = 'INIT'

    @property
    def table(self):
        """
        Return table of ciboulette values
        """
    
        api = [self.api_version]                                # Astropy API
        server = [self.server + ':' + str(self.port)]           # Server IP:port
        device = [self.device]                                  # Device for alpaca
        focale = [self.focale]                                  # Focal millimeter
        diameter = [self.focale]                                # Diameter millimeter
        latitude = [self.latitude]                              # Site latitude degrees
        longitude = [self.longitude]                            # Site longitude degrees
        elevation = [self.elevation]                            # Site elevation meter
        instrument = [self.instrument]                          # Instrument name
        naxis1 = [self.naxis1]                                  # Size naxis1
        naxis2 = [self.naxis2]                                  # Size naxis2
        binXY = [self.binXY]                                    # Binning
        pixelXY = [self.pixelXY]                                # Pixel size X and Y
        filter_name = [self.filter_name]                        # Filter name
        telescope_name = [self.telescope_name]                  # Telescope name
        observer_name = [self.observer_name]                    # Observer name
        dataset = [self.dataset]                                # Dataset repository
        archive_table = [self.archive_table]                    # Archives repository
        ra = [self.ra]                                          # Hours
        dec = [self.dec]                                        # Degrees
        object_name = [self.object_name]                        # Object name
        
        return Table([api,server,device,focale,diameter,latitude,longitude,elevation,instrument,naxis1,naxis2,
                      binXY,pixelXY,filter_name,telescope_name,observer_name,dataset,archive_table,ra,dec,object_name], 
                      names=['API','SERVER','DEVICE','FOCAL','DIAM','SITE_LAT','SITE_LONG','SITE_ELEV','INSTRUME','NAXIS1','NAXIS2',
                         'BINXY','PIXELXY','FILTER','NAME','OBSERVER','DATASET','ARCHIVES','RA','DEC','OBJECT'])  

    @property
    def serverport(self):
        """
        Return Server:port configuration
        """
        return self.server + ':' + str(self.port)

    @serverport.setter
    def serverport(self,serverdict):
        """
        Set server and port
         serverdict:
         {
            "SVR": string - Server 
            "PORT": int - Port
          }
        """  
        self.server = str(serverdict['SVR'])
        self.port = int(serverdict['PORT'])
                
    @property
    def atik383L(self):
        """
        Set Atik383L+ configuration
        """
        self.instrument = 'Atik 383L+'
        self.naxis1 = 3326
        self.naxis2 = 2504
        self.pixelXY = 5.4
    
    @property
    def atiktitan(self):
        """
        Set Atik Titan configuration
        """
        self.instrument = 'Atik Titan'
        self.naxis1 = 659
        self.naxis2 = 494
        self.pixelXY = 7.4       
    
    @property
    def asi120(self):
        """
        Set ASI 120 configuration
        """
        self.instrument = 'ASI 120'
        self.naxis1 = 1280
        self.naxis2 = 960
        self.pixelXY = 3.75       

    @property
    def samyang85_1_4(self):
        """
        Set Samyang 85mm F1.4 configuration
        """
        self.focale = 85
        self.diameter = 60

    @property
    def canon200_2_8(self):
        """
        Set Canon 200mm F2.8 configuration
        """
        self.focale = 200
        self.diameter = 71

    @property
    def sigma120_400(self):
        """
        Set Sigma 120-400 configuration 120mm
        """
        self.focale = 120
        self.diameter = 71

    @sigma120_400.setter
    def sigma120_400(self,f):
        """
        Set Sigma 120-400 configuration
        """
        if f >= 120 and f <= 400:
            self.focale = f
            self.diameter = 71
    
    @property
    def filtername(self):
        """
        Return filter name
        """
        return self.filter_name
    
    @filtername.setter
    def filtername(self,string):
        """
        Set filter name
        """
        self.filter_name = string
    
    def filterwheel(self,filterwheel):
        """
        Set filter of filterweel
         filterwheel (Filterwheel): Filterwheel object (Alpaca or Indilib).
         filter_name (str): Filter name.           
        """       
        filter_number = 0  
        filter_names = filterwheel.names()
        if self.filter_name in filter_names:
            filter_number = filter_names.index(self.filter_name)
            filterwheel.position(filter_number)

    @property
    def coordinates(self):
        """
        Return RA and DEC to hours and degrees
        """
        return self.ra,self.dec
    
    @coordinates.setter
    def coordinates(self,coordinatesdict):
        """
        Set RA and DEC
         coordinatesdict:
         {
            "RA": float - Right ascencion
            "DEC": float - Declination
          }
        """  
        if 'RA' in coordinatesdict:
            ra = float(coordinatesdict['RA'])
            if ra >= 0 and ra < 24:
                self.ra = ra
        if 'DEC' in coordinatesdict:
            dec = float(coordinatesdict['DEC'])
            if dec >= -90 and dec <= 90:
                self.dec = dec    

    @property
    def site(self):
        """
        Return site latitude, site longitude and site elevation 
        """
        return self.latitude,self.longitude,self.elevation
    
    @site.setter
    def site(self,sitedict):
        """
        Set latitude, longitude and elevation
         coordinatesdict:
         {
            "LAT": float - Latitude
            "LONG": float - Longitude
            "ELEV": float - Elevation
          }
        """  
        if 'LAT' in sitedict:
            latitude = float(sitedict['LAT'])
            if latitude >= -90 and latitude <= 90:
                self.latitude = latitude
        if 'LONG' in sitedict:
            longitude = float(sitedict['LONG'])
            if longitude >= 0 and longitude <= 360:
                self.longitude = longitude    
        if 'ELEV' in sitedict:
            elevation = float(sitedict['ELEV'])
            if elevation >= 0 and elevation <= 8000:
                self.elevation = elevation    

    def slewtocoordinates(self,telescope):
        """
        Slew RA and DEC to telescope 
         telescope (Telescope): Telescope object (Alpaca or Indilib).
         ra (float): Hours.
         dec (float): Degrees           
        """
        telescope.slewtocoordinates(self.ra,self.dec)

    @property
    def projections(self):
        """
        Displays the archived sectors, RA and DEC on an aitoff projection      
        """
        sct = Sct.Sector()
        sector_arch = sct.readarchives(self.archive_table)
        # Read archive table
        value_quadran_ra = []
        value_quadran_dec = []   
        for line in sector_arch:        
            # RA and DEC in degrees
            value_RA_quadran = float(line['RA'])*u.deg
            value_DEC_quadran = float(line['DEC'])*u.deg
            # ICRS configuration
            c = SkyCoord(value_RA_quadran, value_DEC_quadran, frame='icrs')
            # RA and DEC in radian
            value_quadran_ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            value_quadran_dec.append(c.dec.radian)
            
        value_ra_graph = []
        value_dec_graph = []
        value_color_graph = []
        title =''    
        # RA and DEC in degrees
        ra=float(self.ra)*15*u.deg
        dec=float(self.dec)*u.deg
        # ICRS configuration
        c = SkyCoord(ra, dec, frame='icrs', unit=(u.deg, u.deg))
        # RA and DEC in radian
        value_ra = -c.ra.wrap_at(180 * u.deg).radian
        value_dec= c.dec.radian
        title = self.telescope_name + ' | ' + self.observer_name + ' | ' + self.filter_name + '\n'
        # Display configuration
        fig = plt.figure(figsize=(7,7))
        # Configuration de la projecion cartographique du titre et grille 
        ax = fig.add_subplot(111,projection='aitoff')
        plt.grid(True,axis='both',linestyle='--')
        # Projection drawing
        if len(sector_arch) > 0:
            plt.plot(value_quadran_ra, value_quadran_dec, 's', color='green', markersize=5, alpha=0.2)   
        plt.plot(value_ra, value_dec, 's', color='red', markersize=5, alpha=0.4)
        # Modification of labels in hours
        ax.set_xticklabels(['10h','08h','06h','04h','02h','0h','22h','20h','18h','16h','14h'],alpha=0.4)
        ax.set_title(title, fontsize = 12)
        # Display
        plt.show()
        
    @property    
    def starmap(self):
        """
        Displays the stars map with maximal magnitude 12
        """

        RA_deg = self.ra*15
        DEC_deg = self.dec
      
        # Element for CRPIX
        crpix1 = int(self.naxis1)/2
        crpix2 = int(self.naxis2)/2

        # Element for CDELT
        cdelt1 = (206*int(self.pixelXY)*int(self.binXY)/self.focale)/3600
        cdelt2 = (206*int(self.pixelXY)*int(self.binXY)/self.focale)/3600

        # Header WCS
        w = wcs.WCS(naxis=2)
        w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
        # CRVAL 
        w.wcs.crval = [RA_deg, DEC_deg] 
        # CRPIX Vecteur à 2 éléments donnant les coordonnées X et Y du pixel de référence 
        # (def = NAXIS / 2) dans la convention FITS (le premier pixel est 1,1)
        w.wcs.crpix = [crpix1, crpix2]
        # CDELT Vecteur à 2 éléments donnant l'incrément physique au pixel de référence
        w.wcs.cdelt = [-cdelt1, cdelt2]   
    
        sct = Sct.Sector()
        field_RA = cdelt1*self.naxis1
        field_DEC= cdelt2*self.naxis2
        #field_RA = 1.5
        #field_DEC= 1.5
        mag = 12
        catalog = 'GSC2.3'
        data_field = sct.regionincatalog(RA_deg, DEC_deg,field_RA,field_DEC,mag,catalog,'_RAJ2000', '_DEJ2000', 'Vmag')
    
        title = 'VizieR-' + catalog + ' | ' + 'F'+str(self.focale) + ' | ' +  self.instrument
    
        fig = plt.figure(figsize=(20,16))
        ax = fig.add_subplot(111, projection=w)
        ax.grid(b = True, linestyle = '--', color = 'black', alpha = 0.40)
        ax.scatter(data_field['RA'], data_field['DEC'], transform=ax.get_transform('icrs'), s=data_field['MARKER'],edgecolor='black', facecolor='black')
        fig.suptitle(title, y = 0.92, fontsize = 12)
        plt.xlabel('RA')
        plt.ylabel('Dec')
        # Display
        plt.show()
        
    def exposure(self,exposure,ccd,telescope,filterwheel):
        """
        Get CCD, telescope and filterwheel and write fits file 
         exposure (Exposure): Exposure object.
         ccd (Camera): CCD alpaca object.
         telescope (Telescope): Telescope alpaca object.
         filterwheel (Filterwheel): Filterwheel alpaca object.
            
        """

        # Shoot
        exptime = exposure.gettime()
        frameid = exposure.getnumber()
        ccd.startexposure(exptime,True)

        while not ccd.imageready():
            time.sleep(1)
         
        date_obs = ccd.lastexposurestarttime()
        self.binXY = ccd.binx()
        self.pixelXY = ccd.pixelsizex()
        self.naxis1 = ccd.cameraxsize()
        self.naxis2 = ccd.cameraysize()   
        ccd_temperature = 0 #ccd.ccdtemperature()

        # Translate picture
        data_ccd = ccd.imagearray()
        data_new = np.rot90(data_ccd)
        data_int16 = data_new.astype(np.int16) 
        #data_real = np.fliplr(data_int16) # inversion verticale  
     
        self.ra = telescope.rightascension()
        self.dec = telescope.declination()
        RA_deg = 15 * self.ra
        DEC_deg = self.dec
        site_lat = float(telescope.sitelatitude())
        site_long = float(telescope.sitelongitude())
   
        filter_names = filterwheel.names()
        self.filter_name = filter_names[filterwheel.position()]
    
        # Create fits
        hdu = fits.PrimaryHDU(data=data_int16)
        file_name = self.dataset+'/'+self.observer_name+'_'+self.object_name+'_'+str(frameid)+'.fits'
        fits.writeto(file_name, hdu.data, hdu.header, overwrite=True) 
        
        # Modification fits header
        #fits_file = get_pkg_data_filename(file_name)
        fits_file = file_name
            
        fits.setval(fits_file, 'PIXSIZE1', value=self.pixelXY, comment='[um] Pixel Size X, binned', savecomment=True)
        fits.setval(fits_file, 'PIXSIZE2', value=self.pixelXY, comment='[um] Pixel Size Y, binned', savecomment=True)
        fits.setval(fits_file, 'XBINNING', value=self.binXY, comment='Binning factor X', savecomment=True)
        fits.setval(fits_file, 'YBINNING', value=self.binXY, comment='Binning factor Y', savecomment=True)
        fits.setval(fits_file, 'EXPTIME', value=exptime, comment='[s] Total Exposure Time', savecomment=True)
        fits.setval(fits_file, 'OBJECT', value=self.object_name, comment='Observed object name', savecomment=True)
        fits.setval(fits_file, 'OBSERVER', value=self.observer_name, comment='Observed name', savecomment=True)
        fits.setval(fits_file, 'TELESCOP', value=self.telescope_name, comment='Telescope name', savecomment=True)
        fits.setval(fits_file, 'INSTRUME', value=self.instrument, comment='Instrument used for acquisition', savecomment=True)                         
        fits.setval(fits_file, 'ROWORDER', value='TOP-DOWN', comment='Order of the rows in image array', savecomment=True)                 
        fits.setval(fits_file, 'CCD-TEMP', value=ccd_temperature, comment='CCD temperature (Celsius)', savecomment=True) 
        fits.setval(fits_file, 'FRAME', value='Light', comment='Frame Type', savecomment=True)                                   
        fits.setval(fits_file, 'IMAGETYP', value='Light', comment='Image Type', savecomment=True)                                  
        fits.setval(fits_file, 'FILTER', value=self.filter_name, comment='Filter info', savecomment=True)     
        fits.setval(fits_file, 'SITELAT', value=site_lat, comment='Observatory latitude', savecomment=True) 
        fits.setval(fits_file, 'SITELONG', value=site_long, comment='Observatory longitude', savecomment=True) 
        fits.setval(fits_file, 'SWCREATE', value=self.driver_name, comment='Driver create', savecomment=True) 
        fits.setval(fits_file, 'FOCALLEN', value=self.focale, comment='[mm] Telescope focal length', savecomment=True) 
        fits.setval(fits_file, 'FRAMEX', value=0, comment='Frame start x', savecomment=True)
        fits.setval(fits_file, 'FRAMEY', value=0, comment='Frame start y', savecomment=True)                                                                   
        fits.setval(fits_file, 'FRAMEHGT', value=self.naxis1, comment='Frame height', savecomment=True)        
        fits.setval(fits_file, 'FRAMEWDH', value=self.naxis2, comment='Frame width', savecomment=True)
        fits.setval(fits_file, 'DATE-OBS', value=date_obs, comment='UTC start date of observation', savecomment=True)
        fits.setval(fits_file, 'RADESYSA', value='ICRS', comment='Equatorial coordinate system', savecomment=True)
        fits.setval(fits_file, 'FRAMEID', value=frameid, comment='Frame ID', savecomment=True)
        fits.setval(fits_file, 'EQUINOX', value=2000.0, comment='Equinox date', savecomment=True)
        fits.setval(fits_file, 'DATATYPE', value='Intensity', comment='Type of data', savecomment=True)
        fits.setval(fits_file, 'MJD-OBS', value=0.0, comment='MJD of start of obseration', savecomment=True)
        fits.setval(fits_file, 'JD-OBS', value=0.0, comment='JD of start of obseration', savecomment=True)

        hdu = fits.open(fits_file)[0]
        header = hdu.header

        # Modification telescope name header
        header['TELESCOP'] = self.telescope_name

        # Modification JD and MJD header
        date_obs = header['DATE-OBS']
        time_obs = Time(header['DATE-OBS'])
        header['JD-OBS'] = time_obs.jd
        header['MJD-OBS'] = time_obs.mjd

        # Elements for CRPIX
        crpix1 = int(header['NAXIS1'])/2
        crpix2 = int(header['NAXIS2'])/2

        # Element for CDELT
        cdelt1 = (206*int(header['PIXSIZE1'])*int(header['XBINNING'])/self.focale)/3600
        cdelt2 = (206*int(header['PIXSIZE2'])*int(header['YBINNING'])/self.focale)/3600

        # Header WCS
        w = wcs.WCS(naxis=2)
        w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
        # CRVAL position
        w.wcs.crval = [RA_deg, DEC_deg] 
        # CRPIX Vecteur à 2 éléments donnant les coordonnées X et Y du pixel de référence 
        # (def = NAXIS / 2) dans la convention FITS (le premier pixel est 1,1)
        w.wcs.crpix = [crpix1, crpix2]
        # CDELT Vecteur à 2 éléments donnant l'incrément physique au pixel de référence
        w.wcs.cdelt = [-cdelt1, cdelt2] 

        # Now, write out the WCS object as a FITS header
        hdu.header = header + w.to_header()

        # Header and data
        hdr = hdu.header
        data = hdu.data
   
        # Sauvegarde
        fits.writeto(file_name, data, hdr, overwrite=True)
        
        return frameid
