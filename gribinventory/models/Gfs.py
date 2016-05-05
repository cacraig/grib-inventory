from .NCEPModel import NCEPModel
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
    
class Gfs(NCEPModel):

  def __init__(self):
    NCEPModel.__init__(self)
    self.lastForecastHour = "384"
    self.name = "gfs"
    self.modelRegex = 'gfs.t..z.pgrb2.0p25.f\d{0,3}$'
    self.defaultTimes = ['000','003','006','009','012','015','018','021','024','027','030','033','036','039','042','045','048','051','054','057','060','063','066','069','072','075','078', \
            '081','084','087','090','093','096','099','102','105','108','111','114','117','120','126','132','138','144', \
            '150','156','162','168','174','180','186','192','198','204','210','216','222', \
            '228','234','240','252','264','276', \
            '288','300','312','324','336','348','360','372','384']
    self.modelTimes = []
    self.modelAlias = "gfs"
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
    print modelDataUrl
    content = urllib2.urlopen(modelDataUrl).read()

    self.latestRunDir = latestRunDir

    print modelDataUrl

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

    self.runTime = latestRunDir.split('/')[0].split('.')[1]
    runFileList = self.filterFiles(runFileList)

    print "Length of currently updated files: " + str(len(runFileList))

    return (latestRunDir[:-1],runFileList)

  def getDataUrl(self):
    return self.highResDataHttp + self.modelAlias + "/prod/" + self.latestRunDir

  '''''
  Filter GFS model file list:
  000-120 Hour (3 hour increment)
  120-240 Hour (6 hour increment)
  240-384 Hour (12 hour increment)

  Reduces number of files, Data + Memory usage, and Processing time.
  Additional timesteps aren't really necessary anyways. After 240th hour
  shit hits the fan in terms of chaos and inaccuracy.

  Expected Filtered file count: 73
  '''''
  def filterFiles(self, fileList):
    fileListCopy = []
    for idx, fileName in enumerate(fileList):
      forecastHour = int(fileName.split('.')[4][1:4])

      if forecastHour <= 120:
        fileListCopy.append(fileName)

      elif forecastHour > 120 and forecastHour <=240 and (forecastHour % 6) == 0:
        # Remove file from list.
        fileListCopy.append(fileName)

      elif forecastHour > 240 and (forecastHour % 12) == 0:
        # Remove file from list.
        fileListCopy.append(fileName)

    return fileListCopy

  '''''
  Gets forecast hour from a filename, given a model.
  '''''
  def getForecastHour(self, fileName, noPrefix = False):
    forecastHour = ""
    prefix = "f"

    if noPrefix:
      prefix = ""

    # for gfs.t18z.pgrb2full.0p50.f006 -> forecastHour = "006"
    forecastHour = prefix + fileName.split('.')[4][1:4]

    return forecastHour
    
  def getLastForecastHour(self):
    return self.lastForecastHour