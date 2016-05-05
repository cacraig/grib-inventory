from .NCEPModel import NCEPModel

class Nam(NCEPModel):

  def __init__(self):
    NCEPModel.__init__(self)
    self.lastForecastHour = "084"
    self.name = "nam"
    self.modelRegex = "nam.t..z.awip32...tm...grib2$"
    self.defaultTimes = ['000','003','006','009','012','015','018','021','024','027','030','033','036','039','042','045','048','051','054','057','060','063','066','069','072','075','078','081','084']
    self.modelTimes = []
    self.runTime  = ''
    self.modelAlias = "nam"
    return

  '''''
  Gets forecast hour from a filename, given a model.
  '''''
  def getForecastHour(self, fileName, noPrefix = False):
    forecastHour = ""
    prefix = "f"
    model = self.name

    if noPrefix:
      prefix = ""

    # for nam.t18z.awip3281.tm00.grib2 -> forecastHour = "081"
    forecastHour = prefix + "0" + fileName.split('.')[2][6:8]

    return forecastHour

  def getLastForecastHour(self):
    return self.lastForecastHour