import re

# Approved commercial abbreviations for Invoice descriptions (<= 40 chars, uppercase)
INVOICE_ABBREVIATIONS = {
    "STAINLESS STEEL": "SST",
    "STAINLESS": "SST",
    "STEEL": "STL",
    "DISHWASHER": "DISHWASHER",
    "PROFESSIONAL": "PRO",
    "LEG MOUNTING": "LEG",
    "BUILT-IN": "BLTLN",
    "BUILT IN": "BLTLN",
    "MOUNTING": "",
    "SERIES": "",
    "WASH CYCLE": "",
    "WASH CYCLES": "",
    "CYCLE": "",
    "CYCLES": "",
    "SANDING DISC": "SAND DISC",
    "SANDING BELT": "SAND BELT",
    "CUT-OFF DISC": "CUT-OFF",
    "CUT-OFF": "CUT-OFF",
    "ABRASIVE": "ABR",
    "DIAMETER": "DIA",
    "PACK": "PK",
    "PIECE": "PC",
    "PIECES": "PC",
    "INCHES": "IN",
    "INCH": "IN",
    "FEET": "FT",
    "FOOT": "FT",
    "VOLT": "V",
    "VOLTS": "V",
    "AMPERE": "A",
    "AMPERES": "A",
    "AMPS": "A",
    "AMP": "A",
    "DECIBEL": "DBA",
    "DECIBELS": "DBA",
    "WITH": "",
    "WITHOUT": "W/O",
    "CLEANBOOST": "",
    "DISPLAY ONLY": "",
    "-": " "
}

def abbreviate_for_invoice(text: str) -> str:
    """Converts raw text into standard uppercase invoice abbreviations under 40 chars."""
    result = text.upper()
    for full, abbr in INVOICE_ABBREVIATIONS.items():
        pattern = r'\b' + re.escape(full) + r'\b'
        result = re.sub(pattern, abbr, result)
        
    result = re.sub(r'[^A-Z0-9/\-\s]', '', result)
    result = re.sub(r'\s+', ' ', result).strip()
    
    # Truncate if exceeds 40 characters
    if len(result) > 40:
        words = result.split()
        truncated = ""
        for w in words:
            if len(f"{truncated} {w}".strip()) <= 40:
                truncated = f"{truncated} {w}".strip()
            else:
                break
        result = truncated or result[:40]
    return result

