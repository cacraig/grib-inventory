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


class NonNCEPModel:
  '''''
  Base Class for all Non-NCEP models.
  '''''
  def __init__(self):

    self.modelUrls = ''

    self.isNCEPSource = False
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

  def getName(self):
    return self.name

  def getAlias(self):
    if self.modelAliases != "":
      return self.modelAlias
    else:
      return self.name

  def getForecastHourInt(self, filename, noPrefix = False):
    fhour = self.getForecastHour(filename, noPrefix)
    return int(fhour[1:])

  def getForecastHour(self, fileName, noPrefix = False):
    return ""

  def getLastForecastHour(self):
    return "000"

  def getRun(self):
    return

  def getName(self):
    return self.name