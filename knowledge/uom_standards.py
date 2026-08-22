import re
from typing import Optional

# Approved Unilog Unit-of-Measure mappings across measurement types
UOM_MAPPINGS = {
    # Length / Distance
    "in": "in", "inch": "in", "inches": "in", "in.": "in", '"': "in",
    "ft": "ft", "foot": "ft", "feet": "ft", "ft.": "ft", "'": "ft",
    "yd": "yd", "yard": "yd", "yards": "yd",
    "mm": "mm", "millimeter": "mm", "millimeters": "mm",
    "cm": "cm", "centimeter": "cm", "centimeters": "cm",
    "m": "m", "meter": "m", "meters": "m",
    
    # Electrical
    "v": "V", "volt": "V", "volts": "V", "vac": "V", "vdc": "VDC",
    "a": "A", "amp": "A", "amps": "A", "ampere": "A", "amperes": "A",
    "w": "W", "watt": "W", "watts": "W",
    "kw": "kW", "kilowatt": "kW",
    "kw-hr": "kW-hr", "kwh": "kW-hr", "kw hr": "kW-hr",
    "hz": "Hz", "hertz": "Hz",
    "ma": "mA", "milliamp": "mA", "milliamps": "mA",
    
    # Weight
    "lb": "lb", "lbs": "lb", "pound": "lb", "pounds": "lb",
    "oz": "oz", "ounce": "oz", "ounces": "oz",
    "kg": "kg", "kilogram": "kg", "kilograms": "kg",
    "g": "g", "gram": "g", "grams": "g",
    
    # Volume
    "gal": "gal", "gallon": "gal", "gallons": "gal",
    "qt": "qt", "quart": "qt", "quarts": "qt",
    "pt": "pt", "pint": "pt", "pints": "pt",
    "fl-oz": "fl-oz", "fl oz": "fl-oz", "fluid ounce": "fl-oz",
    "l": "L", "liter": "L", "liters": "L",
    "ml": "mL", "milliliter": "mL", "milliliters": "mL",
    
    # Sound
    "dba": "dBA", "db": "dBA", "decibel": "dBA", "decibels": "dBA",
    
    # Speed / Pressure / Flow
    "rpm": "rpm", "psi": "psi", "cfm": "cfm", "gpm": "gpm", "gph": "gph",
    
    # Time
    "hr": "hr", "hrs": "hr", "hour": "hr", "hours": "hr",
    "min": "min", "mins": "min", "minute": "min", "minutes": "min",
    "sec": "sec", "secs": "sec", "second": "sec", "seconds": "sec",
    "yr": "yr", "year": "yr", "years": "yr",
    
    # Packaging / Quantity
    "pc": "pc", "pcs": "pc", "piece": "pc", "pieces": "pc",
    "pk": "pk", "pack": "pk", "packs": "pk", "package": "pk", "pkg": "pk",
    "bx": "box", "box": "box", "boxes": "box",
    "cs": "case", "case": "case", "cases": "case",
    "rl": "roll", "roll": "roll", "rolls": "roll",
    "st": "set", "set": "set", "sets": "set",
    "pr": "pair", "pair": "pair", "pairs": "pair",
    "dz": "dz", "dozen": "dz",
    "ea": "ea", "each": "ea",
    "disc": "disc", "discs": "disc", "belt": "belt", "belts": "belt"
}

def normalize_uom(raw_uom: Optional[str]) -> Optional[str]:
    """Normalizes any raw unit string into Unilog standard abbreviation."""
    if not raw_uom:
        return None
    cleaned = str(raw_uom).strip().lower().rstrip(".")
    return UOM_MAPPINGS.get(cleaned, str(raw_uom).strip())

def format_number_uom(val: str, uom: Optional[str]) -> str:
    """Ensures exact single space between number and unit (e.g. '24 in', '120 V')."""
    if not uom:
        return str(val).strip()
    return f"{str(val).strip()} {normalize_uom(uom)}"

