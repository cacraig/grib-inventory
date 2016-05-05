import time
from bs4 import BeautifulSoup
import sys
if (sys.version_info > (3, 0)):
  # Python 3 code in this block
  import urllib.request as urllib2
else:
  # Python 2 code in this block
  import urllib2
import datetime, re, os


class NCEPModel:
  '''''
  Base Class for all NCEP models.
  '''''
  def __init__(self):
    self.name = ""
    self.modelRegex = ""

    self.gribVars = ["PRMSL:mean sea level", "ABSV:250 mb", "ABSV:500 mb", "ABSV:850 mb","ABSV:700 mb", \
                   "PRES:surface","HGT:surface","TMP:2 m above ground","DPT:2 m above ground","RH:2 m above ground", \
                   "UGRD:10 m above ground","VGRD:10 m above ground", "APCP:surface","ACPCP:surface","WEASD:surface", \
                   "PWAT:entire atmosphere (considered as a single layer)", \
                   "CAPE:180-0 mb above ground", "CIN:180-0 mb above ground", "TMP:850 mb", \
                   "TMP:750 mb","TMP:surface", "REFC:entire atmosphere (considered as a single layer)", "HGT:500 mb", "HGT:850 mb","HGT:700 mb", \
                   "HGT:1000 mb","TMP:500 mb","TMP:700 mb","RH:700 mb","DPT:700 mb","TMP:850 mb","RH:850 mb","DPT:850 mb", \
                   "RH:1000 mb","UGRD:500 mb","VGRD:500 mb","UGRD:850 mb","VGRD:850 mb","UGRD:1000 mb","VGRD:1000 mb", \
                   "UGRD:700 mb","VGRD:700 mb", "UGRD:250 mb","VGRD:250 mb","MAXUW:10 m above ground","MAXVW:10 m above ground", "HGT:250 mb", \
                   "HLCY:3000-0 m above ground", "HLCY:1000-0 m above ground"]
                   # "CSNOW:surface","CICEP:surface","CFRZR:surface","CRAIN:surface",

    # Default times.
    self.modelTimes = []

    # Define domain/resolution to obtain.
    self.modelTypes = {'ecmwf': '', 'gfs': '211', 'nam':'212', 'ruc': '236', 'ukmet': '','nam12km':'218','nam4km':''}

    # HTTP DATA SOURCES.
    # Link List base Url.
    self.baseDataHttp = "http://motherlode.ucar.edu/repository/entry/show/RAMADDA/Data/IDD+Data/decoded/gempak/model/"

    # Data GET base URL 
    self.getDataHttp = "http://motherlode.ucar.edu/repository/entry/get/RAMADDA/Data/IDD+Data/decoded/gempak/model/"

    self.highResDataHttp = "http://www.ftp.ncep.noaa.gov/data/nccf/com/"

    # Dict to store model => runTime
    self.runTime = ''

    self.modelGems = {}

    self.modelAliases = ""
    self.isNCEPSource = True

    return
  
  '''''
  This method gets all conusnest High-Resolution model paths. These model paths are an array
  of download paths for grib2 data (one for each time stamp).

  @param list html   - List containing HTML content
  @param String type - String containing model type. 
  @return list
  '''''
  def getFiles(self, html, type, alias = None):
    soup = BeautifulSoup(html)

    modelType = alias

    urlRegex = '(' + modelType + '.*)[^/]*$'
    hrefList = soup.find_all('a', text=re.compile(urlRegex))

    dirList = [i.get('href') for i in hrefList if i.get('href')]

    # Assure that we have the latest run Date.
    latestRun = 0
    for dir in dirList:
      date = dir.split('.')[1][:-1]
      model = dir.split('.')[0]
      if model == modelType and int(date) > int(latestRun):
        latestRunDir = dir

    modelDataUrl = self.highResDataHttp + modelType + "/prod/" + latestRunDir

    content = urllib2.urlopen(modelDataUrl).read()

    self.latestRunDir = latestRunDir


    soup = BeautifulSoup(content, 'html.parser')

    urlRegex = self.modelRegex

    hrefList = soup.find_all('a', text=re.compile(urlRegex))
    fileList = [i.get('href') for i in hrefList]

    # for each href, grab latest Run hour.
    latestHour = "00"
    runFileList = []

    # Loop through file list. Build a list of files with latest run only.
    for file in fileList:
      runHour = file.split('.')[1][1:3]
      if int(runHour) > int(latestHour):
        latestHour = runHour
        runFileList = []
        runFileList.append(file)
      else:
        runFileList.append(file)

    # Associate the current runTime with the model... nam4km => YYYYMMDDZZ
    if modelType is not type:
      # Use full name, and not alias.
      modelType = type


    self.runTime = latestRunDir.split('/')[0].split('.')[1] + latestHour

    return (latestRunDir[:-1],runFileList)

  def getDataUrl(self):
    return self.highResDataHttp + self.modelAlias + "/prod/" + self.latestRunDir


  '''''
  This method gets the url for the latest model run of the model type requested.
  Returns a dictionary keyed on url (Url to get file), and file (The file name).

  Get model data for NAM 4km, HRRR, WRF ARW, GFS .5 degree... etc.
  These must be downloaded as subsets of .grib2 files (due to their massive size)
  We must specify certain paramaters/levels to grab, rather than pulling the entire model run's data.
  '''''
  def getRun(self):

    runDict = {}

    model = self.name
    alias = self.getAlias()

    contentListUrl = self.highResDataHttp + alias + "/prod/"
    contentList = urllib2.urlopen(contentListUrl).read()

    filesList = self.getFiles(contentList, model, alias)
    
    
    latestRun = filesList[0]
    files = filesList[1]

    # Set file download paths, along with desired vars/levels.
    gribDir = latestRun

    for file in files:
      runDict[file] = file

    dataDict = {}

    # A list of all Download urls.
    dataDict['files'] = runDict

    dataDict = {self.name: dataDict}

    return dataDict
  
  '''''
  Filters file list according to rules.
  This is just a template. Default this does nothing. May be overidden.
  '''''
  def filterFiles(self, fileList):
    return

  '''''
  Gets the previous forecast hour  for a given model, and forecast hour.
  '''''
  def getPreviousTime(self, model, currentHour):
    if currentHour == '000':
      return '000'
    defaultHours = self.getDefaultHours()
    defaultHours.sort() #assert ascending order
    for (idx,hour) in enumerate(defaultHours):
      if currentHour == hour:
        return defaultHours[idx-1]

    return '000'

  '''''
  Intialze all of our models hour stamp data to defaults.
  '''''
  def setDefaultHours(self):
    # Default times.
    self.modelTimes = self.defaultTimes
    return

    '''''
  Intialze all of our models hour stamp data to defaults.
  '''''
  def getDefaultHours(self):
    # Default times.
    return self.defaultTimes

  '''''
  Intialze all of our models hour stamp data to defaults.
  '''''
  def getDefaultHours(self):
    # Default times.
    modelTimes = self.defaultTimes
    
    return modelTimes

  def getForecastHourInt(self, filename, noPrefix = False):
    fhour = self.getForecastHour(filename, noPrefix)
    return int(fhour[1:])

  def getName(self):
    return self.name

  def getAlias(self):
    return self.modelAlias

  def getForecastHour(self, fileName, noPrefix = False):
    return ""

  def getLastForecastHour(self):
    return "000"

  


  