# src/converter.py

"""Provide simple conversions for various unit types.

This module allows the user to make unit conversions.

Examples:
    >>> from unitconverter import converter
    >>> converter.convertLength(2, "m", "cm")
    200.0
    >>> converter.convertTime(3, "day", "hour")
    72
    >>> from unitconverter.converter import convertData
    >>> convertData(8, "bit", "byte")
    1.0

The module contains the following functions:

- `convertLength(value, input_unit, output_unit)` - Does length unit conversions.
- `convertWeight(value, input_unit, output_unit)` - Does wight unit conversions.
- `convertVolume(value, input_unit, output_unit)` - Does volume unit conversions.
- `convertEnergy(value, input_unit, output_unit)` - Does energy unit conversions.
- `convertPressure(value, input_unit, output_unit)` - Does pressure unit conversions.
- `convertData(value, input_unit, output_unit)` - Does data unit conversions.
- `convertTime(value, input_unit, output_unit)` - Does time conversions.
- `convertSpeed(value, input_unit, output_unit)` - Does speed unit conversions.
- `convertTemperature(value, input_unit, output_unit)` - Does temperature conversions.
"""

from typing import Union
def convertLength(value: Union[float, int], input_unit: Union[str, chr], output_unit: Union[str, chr]) -> float:

    """Convert various length units

    Examples:
        >>> convertLength(5, "km", "m")
        5000.0
        >>> convertLength(15.5, "cm", "mm")
        155.0
    Args:
        value: A number representing the value that needs conversion.
        input_unit: Text representing the input units name or abbreviation.
        output_unit: Text representing the name or abbreviation of the output unit.
    Returns:
        A number representing the converted value.
    """

    lengthAliases = {
        "angstrom" : "angstrom",
        "A" : "angstrom",
        "milimicron" : "milimicron",
        "mµ" : "milimicron",
        "micron" : "micron",
        "µ" : "micron",
        "milimeter" : "milimeter",
        "mm" : "milimeter",
        "centimeter" : "centimeter",
        "cm" : "centimeter",
        "meter" : "meter",
        "m" : "meter",
        "kilometer" : "kilometer",
        "km" : "kilometer",
        "foot" : "foot",
        "ft" : "foot",
        "mile" : "mile",
        "mi" : "mile",
        "yard" : "yard",
        "yd" : "yard",
        "inch" : "inch",
        "in" : "inch"}
    lengthUnitConversionFactors = {
        "angstrom" : 0.0000000001,
        "milimicron" : 0.000000001,
        "micron" : 0.000001,
        "milimeter" : 0.001,  
        "centimeter" : 0.01,  
        "meter" : 1.0,  
        "kilometer" : 1000.0,  
        "foot" : 0.3048,  
        "mile" : 1609.344,  
        "yard" : 0.9144,  
        "inch" : 0.0254
        }
    
    if input_unit in lengthAliases and output_unit in lengthAliases:
        return value * lengthUnitConversionFactors[lengthAliases[input_unit]] / lengthUnitConversionFactors[lengthAliases[output_unit]]
    else:
        raise ValueError("Invalid conversion units. Supported units are 'a' (angstrom), 'mµ' (milimicron), 'µ' (micron), 'mm' (milimeter), 'cm' (centimeter), 'm' (meter), 'km' (kilometer), 'ft' (foot), 'mi' (mile), 'yd' (yard), and 'in' (inch).")

def convertWeight(value: Union[float, int], input_unit: Union[str, chr], output_unit: Union[str, chr]) -> float:

    """Convert various weight units

    Examples:
        >>> convertWeight(5, "g", "miligram")
        50.0
        >>> convertWeight(15.5, "decagram", "gram")
        155.0
    Args:
        value: A number representing the value that needs conversion.
        input_unit: Text representing the input units name or abbreviation.
        output_unit: Text representing the name or abbreviation of the output unit.
    Returns:
        A number representing the converted value.
    """

    weightAliases = {
        "miligram" : "miligram",
        "mg" : "miligram",
        "centigram" : "centigram",
        "cg" : "centigram",
        "decigram" : "decigram",
        "dg" : "decigram",
        "gram" : "gram",
        "g" : "gram",
        "kilogram" : "kilogram",
        "kg" : "kilogram",
        "decagram" : "decagram",
        "dag" : "decagram",
        "hectogram" : "hectogram",
        "hg" : "hectogram",
        "ounce" : "ounce",
        "oz." : "ounce",
        "pound" : "pound",
        "lb." : "pound",
        "stone" : "stone",
        "st." : "stone",
        "slug" : "slug",
        "short_ton" : "short_ton",
        "st" : "short_ton",
        "long_ton" : "long_ton",
        "lt" : "long_ton",
        "tonne" : "tonne",
        "T" : "tonne"}
    weightUnitConversionFactors = {
        "miligram" : 0.001,
        "centigram" : 0.01,
        "decigram" : 0.1,
        "gram" : 1.0,
        "decagram" : 10,    
        "hectagram" : 100.0,  
        "kilogram" : 1000.0,
        "ounce" : 28.34952,    
        "pound" : 453.592,
        "stone" : 6350.29,    
        "slug" : 14593.9,
        "short_ton" : 907185.0,
        "long_ton" : 1.016e+6,
        "tonne" : 1000000.0
    }
    if input_unit in weightAliases and output_unit in weightAliases:
        return value * weightUnitConversionFactors[weightAliases[input_unit]] / weightUnitConversionFactors[weightAliases[output_unit]]
    else:
        raise ValueError("Invalid conversion units. Supported units are 'mg' (miligram), 'cg' (centigram), 'dg' (decigram), 'g' (gram), 'dag' (decagram), 'hg' (hectagram), 'kg' (kilogram), 'ft' (ounce), 'mi' (pound), 'yd' (stone), 'slug' (slug), 'st' (short ton), 'lt' (long ton) and 'T' (tonne).")

def convertVolume(value: Union[float, int], input_unit: Union[str, chr], output_unit: Union[str, chr]) -> float:

    """Convert various volume units

    Examples:
        >>> convertVolume(5, "l", "mililiter")
        5000.0
        >>> convertVolume(15.5, "mililiter", "l")
        0.0155
    Args:
        value: A number representing the value that needs conversion.
        input_unit: Text representing the input units name or abbreviation.
        output_unit: Text representing the name or abbreviation of the output unit.
    Returns:
        A number representing the converted value.
    """

    volumeAliases = {
        "mililiter" : "mililiter",
        "ml" : "mililiter",
        "liter" : "liter",
        "L" : "liter",
        "cubic_meter" : "cubic_meter",
        "m3" : "cubic_meter",
        "cubic_inch" : "cubic_inch",
        "in3" : "cubic_inch",
        "cubic_foot" : "cubic_foot",
        "ft3" : "cubic_foot",
        "pint" : "pint",
        "pt" : "pint",
        "quart" : "quart",
        "qt" : "quart",
        "gallon" : "gallon",
        "gal" : "gallon",
        "barrel" : "barrel",
        "bbl" : "barrel"
        }
    volumeUnitConversionFactors = {
        "mililiter" : 1.0,
        "liter" : 1000.0,
        "cubic_meter" : 1000000.0,
        "cubic_inch" : 16.387064,
        "cubic_foot" : 28316.846592,    
        "pint" : 473.176473,  
        "quart" : 946.352946,
        "gallon" : 3785.411784,    
        "barrel" : 119240.471196
    }
    if input_unit in volumeAliases and output_unit in volumeAliases:
        return value * volumeUnitConversionFactors[volumeAliases[input_unit]] / volumeUnitConversionFactors[volumeAliases[output_unit]]
    else:
        raise ValueError("Invalid conversion units. Supported units are 'ml' (mililiter), 'L' (liter), 'm3' (cubic_meter), 'in3' (cubic_inch), 'ft3' (cubic_feet), 'pt' (pint), 'qt' (quart), 'gal' (gallon) and 'bbl' (barrel).")

def convertEnergy(value: Union[float, int], input_unit: Union[str, chr], output_unit: Union[str, chr]) -> float:

    """Convert various energy units

    Examples:
        >>> convertEnergy(5000, "kcal", "thm")
        0.19842
        >>> convertEnergy(15.5, "calorie", "J")
        64852.0
    Args:
        value: A number representing the value that needs conversion.
        input_unit: Text representing the input units name or abbreviation.
        output_unit: Text representing the name or abbreviation of the output unit.
    Returns:
        A number representing the converted value.
    """

    energyAliases = {
        "Btu" : "Btu",
        "therm" : "therm",
        "thm" : "therm",
        "calorie" : "calorie",
        "cal" : "calorie",
        "kilocalorie" : "kilocalorie",
        "kcal" : "kilocalorie",
        "teracalorie" : "teracalorie",
        "tcal" : "teracalorie",
        "megajoule" : "megajoule",
        "MJ" : "megajoule",
        "joule" : "joule",
        "J" : "joule",
        "gigajoule" : "gigajoule",
        "GJ" : "gigajoule",
        "terajoule" : "terajoule",
        "TJ" : "terajoule",
        "watthour" : "watthour",
        "Wh" : "watthour",
        "kilowatthour" : "kilowatthour",
        "kWh" : "kilowatthour",
        "megawatthour" : "megawatthour",
        "MWh" : "megawatthour",
        "gigawatthour" : "gigawatthour",
        "GWh" : "gigawatthour",
        "terawatthour" : "terawatthour",
        "TWh" : "terawatthour"
        }
    energyUnitConversionFactors = {
        "Btu" : 1055.06,
        "therm" : 1.055e+8,
        "calorie" : 4.184,
        "kilocalorie" : 4184,    
        "thermie" : 4185800,  
        "teracalorie" : 4.184e+12,
        "megajoule" : 1000000,    
        "joule" : 1.0,
        "gigajoule" : 1e+9,    
        "terajoule" : 1e+12,
        "watthour" : 3600,
        "kilowatthour" : 3.6e+6,
        "megawatthour" : 3.6e+9,
        "gigawatthour" : 3.6e+12,
        "terawatthour" : 3.6e+15
    }
    if input_unit in energyAliases and output_unit in energyAliases:
        return value * energyUnitConversionFactors[energyAliases[input_unit]] / energyUnitConversionFactors[energyAliases[output_unit]]
    else:
        raise ValueError("Invalid conversion units.")
    
def convertPressure(value: Union[float, int], input_unit: Union[str, chr], output_unit: Union[str, chr]) -> float:

    """Convert various pressure units

    Examples:
        >>> convertPressure(5000, "atn", "psi")
        73479.5
        >>> convertPressure(15.5, "bar", "pascal")
        1550000.0
    Args:
        value: A number representing the value that needs conversion.
        input_unit: Text representing the input units name or abbreviation.
        output_unit: Text representing the name or abbreviation of the output unit.
    Returns:
        A number representing the converted value.
    """

    pressureAliases = {
        "pounds_per_square_inch" : "pounds_per_square_inch",
        "psi" : "pounds_per_square_inch",
        "atmosphere" : "atmosphere",
        "atn" : "atmosphere",
        "torr" : "torr",
        "bar" : "bar",
        "milibar" : "milibar",
        "mbar" : "milibar",
        "mb" : "milibar",
        "pascal" : "pascal",
        "Pa" : "pascal",
        "kilopascal" : "kilopascal",
        "kPa" : "kilopascal",
        "megapascal" : "megapascal",
        "MPa" : "megapascal",
        "gigapascal" : "gigapascal",
        "GPa" : "gigapascal"
        }
    pressureUnitConversionFactors = {
        "pounds_per_square_inch" : 1.0,
        "atmosphere" : 14.6959,
        "torr" : 0.0193368,
        "bar" : 14.5038,    
        "milibar" : 0.0145038,  
        "pascal" : 0.000145038,
        "kilopascal" : 0.145038,    
        "megapascal" : 145.038,
        "gigapascal" : 145038
    }
    if input_unit in pressureAliases and output_unit in pressureAliases:
        return value * pressureUnitConversionFactors[pressureAliases[input_unit]] / pressureUnitConversionFactors[pressureAliases[output_unit]]
    else:
        raise ValueError("Invalid conversion units.")
    
def convertData(value: Union[float, int], input_unit: Union[str, chr], output_unit: Union[str, chr]) -> float:

    """Convert various data units

    Examples:
        >>> convertData(5000, "Mb", "Gb")
        5.0
        >>> convertData(1, "byte", "bit")
        8.0
    Args:
        value: A number representing the value that needs conversion.
        input_unit: Text representing the input units name or abbreviation.
        output_unit: Text representing the name or abbreviation of the output unit.
    Returns:
        A number representing the converted value.
    """

    dataAliases = {
        "bit" : "bit",
        "b" : "bit",
        "byte" : "byte",
        "B" : "byte",
        "kilobyte" : "kilobyte",
        "KB" : "kilobyte",
        "kilobit" : "kilobit",
        "Kb" : "kilobit",
        "megabyte" : "megabyte",
        "MB" : "megabyte",
        "megabit" : "megabit",
        "Mb" : "megabit",
        "gigabyte" : "gigabyte",
        "GB" : "gigabyte",
        "gigabit" : "gigabit",
        "Gb" : "gigabit",
        "terabyte" : "terabyte",
        "TB" : "terabyte",
        "terabit" : "terabit",
        "Tb" : "terabit",
        "petabyte" : "petabyte",
        "PB" : "petabyte",
        "petabit" : "petabit",
        "Pb" : "petabit"
        }
    dataUnitConversionFactors = {
        "bit" : 0.125,
        "byte" : 1,
        "kilobyte" : 1000,
        "kilobit" : 125,
        "megabyte" : 1000000,
        "megabit" : 125000,    
        "gigabyte" : 1e+9,
        "gigabit" : 1.25e+8,  
        "terabyte" : 1e+12,
        "terabit" : 1.25e+11,
        "petabyte" : 1e+15,
        "petabit" : 1.25e+14
    }
    if input_unit in dataAliases and output_unit in dataAliases:
        return value * dataUnitConversionFactors[dataAliases[input_unit]] / dataUnitConversionFactors[dataAliases[output_unit]]
    else:
        raise ValueError("Invalid conversion units.")
    
def convertTime(value: int, input_unit: Union[str, chr], output_unit: Union[str, chr]) -> int:

    """Convert time units

    Examples:
        >>> convertTime(1, "hr", "minute")
        60
        >>> convertTime(24, "hour", "day")
        1
    Args:
        value: A number representing the value that needs conversion.
        input_unit: Text representing the input units name or abbreviation.
        output_unit: Text representing the name or abbreviation of the output unit.
    Returns:
        A number representing the converted value.
    """

    timeAliases = {
        "second" : "second",
        "s" : "second",
        "minute" : "minute",
        "min" : "minute",
        "hour" : "hour",
        "hr" : "hour",
        "day" : "day",
        "d" : "day"
        }
    timeConversionFactors = {
        "second": {
            "second": 1,
            "minute": 1 / 60,
            "hour": 1 / 3600,
            "day": 1 / 86400
        },
        "minute": {
            "second": 60,
            "minute": 1,
            "hour": 1 / 60,
            "day": 1 / 1440
        },
        "hour": {
            "second": 3600,
            "minute": 60,
            "hour": 1,
            "day": 1 / 24
        },
        "day": {
            "second": 86400,
            "minute": 1440,
            "hour": 24,
            "day": 1
        }
    }

    if input_unit in timeAliases and output_unit in timeAliases:
        conversion_factor = timeConversionFactors[timeAliases[input_unit]][timeAliases[output_unit]]
        return value * conversion_factor
    else:
        raise ValueError("Invalid conversion units. Supported units are 's' (seconds), 'min' (minutes), 'hr' (hours), and 'day' (days).")

def convertSpeed(value: Union[float, int], input_unit: Union[str, chr], output_unit: Union[str, chr]) -> float:

    """Convert various speed units

    Examples:
        >>> convertSpeed(1, "km/s", "m/s")
        1000.0
        >>> convertSpeed(1, "m/s", "cm/s")
        0.01
    Args:
        value: A number representing the value that needs conversion.
        input_unit: Text representing the input units name or abbreviation.
        output_unit: Text representing the name or abbreviation of the output unit.
    Returns:
        A number representing the converted value.
    """

    speedUnitConversionFactors = {
        "m/s" : 1.0,
        "km/h" : 0.277778,
        "km/s" : 1000.0,
        "cm/s" : 0.01,
        "mph" : 0.44704,    
        "ft/s" : 0.3048,  
        "yd/s" : 0.9144,
        "mi/s" : 1609.34,    
        "knots" : 0.514444,   
        "c" : 2.998e+8
    }
    if input_unit in speedUnitConversionFactors and output_unit in speedUnitConversionFactors:
        return value * speedUnitConversionFactors[input_unit] / speedUnitConversionFactors[output_unit]
    else:
        raise ValueError("Invalid conversion units. Supported units are 'm/s' (meter per second), 'km/h' (kilometer per hour), 'km/s' (kilometer per second), 'cm/s' (centimeter per second), 'mph' (mile per hour), 'ft/s' (foot per second), 'yd/s' (yard per second), 'mi/s' (mile per second), 'knots' (knots), and 'c' (light speed).")

def convertTemperature(value: Union[float, int], input_unit: Union[str, chr], output_unit: Union[str, chr]) -> float:

    """Convert temperatures

    Examples:
        >>> convertTemperature(1, "C", "fahrenheit")
        33.8
        >>> convertTemperature(1, "kelvin", "celsius")
        -272.15
    Args:
        value: A number representing the value that needs conversion.
        input_unit: Text representing the input units name or abbreviation.
        output_unit: Text representing the name or abbreviation of the output unit.
    Returns:
        A number representing the converted value.
    """

    if (input_unit == "C" or input_unit == "celsius") and (output_unit == "C" or output_unit == "celsius"):
        return value
    if (input_unit == "F" or input_unit == "fahrenheit") and (output_unit == "F" or output_unit == "fahrenheit"):
        return value
    if (input_unit == "K" or input_unit == "kelvin") and (output_unit == "K" or output_unit == "kelvin"):
        return value
    if (input_unit == "C" or input_unit == "celsius") and (output_unit == "F" or output_unit == "fahrenheit"):
        return (value * 9 / 5) + 32
    elif (input_unit == "F" or input_unit == "fahrenheit") and (output_unit == "C" or output_unit == "celsius"):
        return 5 / 9 * (value - 32)
    elif (input_unit == "C" or input_unit == "celsius") and (output_unit == "K" or output_unit == "kelvin"):
        return value - 273.15
    elif (input_unit == "K" or input_unit == "kelvin") and (output_unit == "C" or output_unit == "celsius"):
        return value + 273.15
    elif (input_unit == "F" or input_unit == "fahrenheit") and (output_unit == "K" or output_unit == "kelvin"):
        return 9 / 5 * (value - 273.15) + 32
    elif (input_unit == "K" or input_unit == "kelvin") and (output_unit == "F" or output_unit == "fahrenheit"):
        return 5 / 9 * (value - 32) + 273.15
    else:
        raise ValueError("Invalid conversion units. Supported units are 'C' (Celsius), 'F' (Fahrenheit) and 'K' (Kelvin).")
    