from . units import unitLabels, getAllConversions, convert, convertAll, convFormat
from .properties import PropertyCollection, EnumProperty

class UnitPreferences(PropertyCollection):
    def __init__(self, propDict = None):
        super().__init__()
        for unit in unitLabels:
            self.props[unit] = EnumProperty(unitLabels[unit], getAllConversions(unit))
        if propDict is not None:
            self.setProperties(propDict)

    def convert(self, quantity, originUnit):
        return convert(quantity, originUnit, self.getProperty(originUnit))

    def convertAll(self, quantities, originUnit):
        return convertAll(quantities, originUnit, self.getProperty(originUnit))

    def convFormat(self, quantity, originUnit, places=3):
        return convFormat(quantity, originUnit, self.getProperty(originUnit), places)

    def getUnit(self, fromUnit):
        if fromUnit in self.props:
            return self.getProperty(fromUnit)
        return fromUnit
