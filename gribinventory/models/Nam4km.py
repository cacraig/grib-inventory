from .NCEPModel import NCEPModel

class Nam4km(NCEPModel):

  def __init__(self):
    NCEPModel.__init__(self)
    self.lastForecastHour = "060"
    self.name = "nam4km"
    self.runTime = ''
    self.modelRegex = 'nam.t..z.(conus\w+).hiresf...tm...grib2$'
    self.defaultTimes = ['000','001','002','003','004','005','006','007','008','009','010','011','012','013','014','015','016','017','018','019','020','021','022','023','024','025', \
                '026','027','028','029','030','031','032','033','034','035','036','039','042','045','048','051','054','057','060']
    self.modelTimes = []
    self.modelAlias = "nam"
    self.gribVars = ["PRMSL:mean sea level", "PRES:surface", "TMP:2 m above ground", "DPT:2 m above ground", "RH:2 m above ground", \
               "UGRD:10 m above ground","VGRD:10 m above ground", "APCP:surface","ACPCP:surface","WEASD:surface", \
               "PWAT:entire atmosphere (considered as a single layer)", \
               "CAPE:180-0 mb above ground", "CIN:180-0 mb above ground", \
               "TMP:surface", "REFC:entire atmosphere (considered as a single layer)", \
               "TMP:850 mb", "TMP:500 mb", "TMP:30-0 mb above ground", \
               "MAXUW:10 m above ground","MAXVW:10 m above ground", \
               "HLCY:3000-0 m above ground", "HLCY:1000-0 m above ground"]
               # ,"RH:850 mb","DPT:850 mb", "CSNOW:surface","CICEP:surface","CFRZR:surface", "CRAIN:surface"
    return

  '''''
  Gets forecast hour from a filename, given a model.
  '''''
  def getForecastHour(self, fileName, noPrefix = False):
    forecastHour = ""
    prefix = "f"

    if noPrefix:
      prefix = ""

    # for nam.t06z.blahblah.hiresf07.blah -> forecastHour = "007"
    forecastHour = prefix + "0" + fileName.split('.')[3][6:8]

    return forecastHour

  def getLastForecastHour(self):
    return self.lastForecastHour