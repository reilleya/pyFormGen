"""This module contains tables of units and their long form names, their conversion rates with other units, and
functions for performing conversion."""

# The keys in this dictionary specify the units that all calculations are done in internally
unitLabels = {
    'm': 'Length',
    'm/s': 'Velocity',
    'N': 'Force',
    'Ns': 'Impulse',
    'Pa': 'Pressure',
    'kg': 'Mass',
    'kg/m^3': 'Density',
}

unitTable = [
    ('m', 'cm', 100),
    ('m', 'mm', 1000),
    ('m', 'in', 39.37),
    ('m', '64th in', 2519.68),
    ('m', 'ft', 3.28),

    ('m/s', 'cm/s', 100),
    ('m/s', 'mm/s', 1000),
    ('m/s', 'ft/s', 3.28),
    ('m/s', 'in/s', 39.37),

    ('N', 'lbf', 0.2248),

    ('Ns', 'lbfs', 0.2248),

    ('Pa', 'MPa', 1/1000000),
    ('Pa', 'psi', 1/6895),

    ('kg', 'g', 1000),
    ('kg', 'lb', 2.205),
    ('kg', 'oz', 2.205 * 16),

    ('kg/m^3', 'lb/in^3', 3.61273e-5),
    ('kg/m^3', 'g/cm^3', 0.001)
]

def getAllConversions(unit):
    """Returns a list of all units that the passed unit can be converted to."""
    allConversions = [unit]
    for conversion in unitTable:
        if conversion[0] == unit:
            allConversions.append(conversion[1])
        elif conversion[1] == unit:
            allConversions.append(conversion[0])
    return allConversions

def getConversion(originUnit, destUnit):
    """Returns the ratio to convert between the two units. If the conversion does not exist, an exception is raised."""
    if originUnit == destUnit:
        return 1
    for conversion in unitTable:
        if conversion[0] == originUnit and conversion[1] == destUnit:
            return conversion[2]
        if conversion[1] == originUnit and conversion[0] == destUnit:
            return 1/conversion[2]
    raise KeyError("Cannot find conversion from <" + originUnit + "> to <" + destUnit + ">")

def convert(quantity, originUnit, destUnit):
    """Returns the value of 'quantity' when it is converted from 'originUnit' to 'destUnit'."""
    return quantity * getConversion(originUnit, destUnit)

def convertAll(quantities, originUnit, destUnit):
    """Converts a list of values from 'originUnit' to 'destUnit'."""
    convRate = getConversion(originUnit, destUnit)
    return [q * convRate for q in quantities]

def convFormat(quantity, originUnit, destUnit, places=3):
    """Takes in a quantity in originUnit, converts it to destUnit and outputs a rounded and formatted string that
    includes the unit appended to the end."""
    num = round(convert(quantity, originUnit, destUnit), places)
    return str(num) + ' ' + destUnit
