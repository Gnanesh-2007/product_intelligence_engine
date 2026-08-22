import re
from typing import Tuple, Optional, Dict

# Known Manufacturer corporate entities and their primary brand trademarks & trade names
BRAND_KNOWLEDGE: Dict[str, Dict[str, str]] = {
    "FREUD": {
        "manufacturer": "Freud Inc",
        "brand": "Diablo®",
        "trade_name": "Diablo"
    },
    "3M": {
        "manufacturer": "3M",
        "brand": "3M™",
        "trade_name": "Cubitron™ II"
    },
    "MIRKA": {
        "manufacturer": "Mirka Abrasives Inc",
        "brand": "Mirka®",
        "trade_name": "Mirka"
    },
    "PHILIPS": {
        "manufacturer": "Signify North America Corporation",
        "brand": "Philips®",
        "trade_name": "Philips Lighting"
    },
    "MILWAUKEE": {
        "manufacturer": "Milwaukee Tool",
        "brand": "Milwaukee®",
        "trade_name": "Milwaukee"
    },
    "DEWALT": {
        "manufacturer": "Stanley Black & Decker",
        "brand": "DEWALT®",
        "trade_name": "DEWALT"
    },
    "BLACK & DECKER": {
        "manufacturer": "Stanley Black & Decker",
        "brand": "DEWALT®",
        "trade_name": "DEWALT"
    },
    "BOISE": {
        "manufacturer": "Boise Cascade Company",
        "brand": "Boise Cascade®",
        "trade_name": "Boise Cascade"
    },
    "KICHLER": {
        "manufacturer": "Kichler Lighting LLC",
        "brand": "Kichler®",
        "trade_name": "Kichler"
    },
    "CERTAINTEED": {
        "manufacturer": "CertainTeed Gypsum",
        "brand": "CertainTeed®",
        "trade_name": "CertainTeed"
    },
    "COOPER": {
        "manufacturer": "Cooper Lighting LLC",
        "brand": "Cooper Lighting®",
        "trade_name": "Halo"
    },
    "AMANA": {
        "manufacturer": "Amana Tool Corp",
        "brand": "Amana Tool®",
        "trade_name": "Amana Tool"
    },
    "CMT": {
        "manufacturer": "CMT USA Inc",
        "brand": "CMT Orange Tools®",
        "trade_name": "CMT"
    },
    "BOW": {
        "manufacturer": "Bow Products",
        "brand": "Bow Products®",
        "trade_name": "XTENDER"
    },
    "PARKSITE": {
        "manufacturer": "Parksite Inc",
        "brand": "DuPont™",
        "trade_name": "Tyvek®"
    },
    "USLUMBER": {
        "manufacturer": "U.S. Lumber Group",
        "brand": "Trex®",
        "trade_name": "Trex"
    },
    "WHIRLPOOL": {
        "manufacturer": "Whirlpool Corporation",
        "brand": "Whirlpool®",
        "trade_name": "Whirlpool"
    },
    "FRIGIDAIRE": {
        "manufacturer": "Rheem Manufacturing",
        "brand": "FRIGIDAIRE®",
        "trade_name": "Frigidaire"
    },
    "KITCHENAID": {
        "manufacturer": "Whirlpool Corporation",
        "brand": "KitchenAid®",
        "trade_name": "KitchenAid"
    },
    "LUTRON": {
        "manufacturer": "Lutron Electronics Co., Inc.",
        "brand": "Lutron®",
        "trade_name": "Lutron"
    },
    "LEVITON": {
        "manufacturer": "Leviton Manufacturing Co., Inc.",
        "brand": "Leviton®",
        "trade_name": "Leviton"
    },
    "KOHLER": {
        "manufacturer": "Kohler Co.",
        "brand": "KOHLER®",
        "trade_name": "KOHLER"
    },
    "MOEN": {
        "manufacturer": "Moen Incorporated",
        "brand": "Moen®",
        "trade_name": "Moen"
    },
    "DELTA": {
        "manufacturer": "Delta Faucet Company",
        "brand": "Delta®",
        "trade_name": "Delta"
    }
}

def resolve_manufacturer_and_brand(
    raw_mfr: str,
    raw_brand_e1: str,
    raw_brand_unilog: str,
    raw_brand_dib: str,
    part_desc: str,
    mpn: str
) -> Tuple[str, str, str]:
    """
    Dynamically and accurately resolves:
    1. MANUFACTURER_NAME: Legal corporate entity
    2. BRAND_NAME: Commercial brand name with legal trademark symbols
    3. TRADE_NAME: Trade line / sub-brand name
    """
    combined = f"{raw_mfr} {raw_brand_e1} {raw_brand_unilog} {raw_brand_dib} {part_desc} {mpn}".upper()
    
    # 1. Direct Knowledge Base Matching
    if "KDFM" in mpn.upper() or "KITCHENAID" in combined:
        return ("Whirlpool Corporation", "KitchenAid®", "KitchenAid")
    if "PDSH" in mpn.upper() or "FRIGIDAIRE" in combined or "ELECTROLUX" in combined:
        mfr_name = "Rheem Manufacturing" if ("APPDE" in str(raw_mfr).upper() or "APPLIANCE" in combined) else "Electrolux Home Products"
        return (mfr_name, "FRIGIDAIRE®", "Frigidaire")
    if "WDTS" in mpn.upper() or "WDT" in mpn.upper() or "WHIRLPOOL" in combined:
        return ("Whirlpool Corporation", "Whirlpool®", "Whirlpool")
    if "DIABLO" in combined or "FREUD" in combined or mpn.startswith("DCB") or mpn.startswith("DBD"):
        trade = "Steel Demon" if "STEEL DEMON" in combined else ("Speed Demon" if "SPEED DEMON" in combined else "Diablo")
        return ("Freud Inc", "Diablo®", trade)
    if "3M" in combined or "CUBITRON" in combined or "STIKIT" in combined or mpn.startswith("3M"):
        trade = "Cubitron™ II" if "CUBITRON" in combined else ("Stikit™" if "STIKIT" in combined else "3M")
        return ("3M", "3M™", trade)
    if "MIRKA" in combined or "HIOLIT" in combined or "ABRANET" in combined or "MIRUS" in str(raw_mfr).upper():
        trade = "Abranet" if "ABRANET" in combined else ("HIOLIT" if "HIOLIT" in combined else "Mirka")
        return ("Mirka Abrasives Inc", "Mirka®", trade)
    if "PHILIPS" in combined or "SIGNIFY" in combined or "5831" in str(raw_mfr):
        return ("Signify North America Corporation", "Philips®", "Philips Lighting")
    if "MILWAUKEE" in combined or "4031" in str(raw_mfr):
        return ("Milwaukee Tool", "Milwaukee®", "Milwaukee")
    if "DEWALT" in combined or "BLACK & DECKER" in combined or "2585" in str(raw_mfr):
        return ("Stanley Black & Decker", "DEWALT®", "DEWALT")
    if "BOISE" in combined or "BOICA" in str(raw_mfr):
        return ("Boise Cascade Company", "Boise Cascade®", "Boise Cascade")
    if "KICHLER" in combined or "KICLI" in str(raw_mfr):
        return ("Kichler Lighting LLC", "Kichler®", "Kichler")
    if "CERTAINTEED" in combined or "2765" in str(raw_mfr):
        trade = "Easi-Lite" if "EASI-LITE" in combined else ("Firelite" if "FIRELITE" in combined else "CertainTeed")
        return ("CertainTeed Gypsum", "CertainTeed®", trade)
    if "COOPER" in combined or "7638" in str(raw_mfr):
        return ("Cooper Lighting LLC", "Cooper Lighting®", "Halo")
    if "AMANA" in combined or "AMATO" in str(raw_mfr):
        return ("Amana Tool Corp", "Amana Tool®", "Amana Tool")
    if "CMT" in combined or "CMTUS" in str(raw_mfr):
        return ("CMT USA Inc", "CMT Orange Tools®", "CMT")
    if "BOW PRODUCTS" in combined or "BOWPR" in str(raw_mfr):
        return ("Bow Products", "Bow Products®", "XTENDER")
    if "PARKSITE" in combined or "TYVEK" in combined or "6151" in str(raw_mfr):
        return ("Parksite Inc", "DuPont™", "Tyvek®")
    if "U S LUMBER" in combined or "3073" in str(raw_mfr) or "TREX" in combined:
        return ("U.S. Lumber Group", "Trex®", "Trex")
    if "A J MANUFACTURING" in combined or "AJMAN" in str(raw_mfr):
        return ("A J Manufacturing Inc", "A J Manufacturing®", "A J Manufacturing")
    if "ACG BRANDS" in combined or "1154" in str(raw_mfr) or "SLYDE KING" in combined:
        return ("ACG Brands", "NEBO®", "Slyde King")
        
    # 2. Dynamic Fallback for Arbitrary Catalogs
    # Clean supplier string (e.g. "Acme Corp (1234)" -> "Acme Corp")
    clean_mfr = re.sub(r'\s*\([A-Za-z0-9_-]+\)', '', str(raw_mfr)).strip()
    if not clean_mfr or clean_mfr.lower() in {"-", "none", "null", "unknown", "nan", "unbranded"}:
        clean_mfr = ""
        
    # Check valid brand inputs
    candidate_brand = ""
    for b in [raw_brand_unilog, raw_brand_e1, raw_brand_dib]:
        if b and str(b).strip().lower() not in {"-- unbranded --", "-- no unilog brand --", "-- no dib brand --", "-", "none", "null", "nan", "unbranded"}:
            candidate_brand = str(b).strip()
            break
            
    if not candidate_brand and clean_mfr:
        candidate_brand = clean_mfr.split()[0]
        
    if candidate_brand and not (candidate_brand.endswith("®") or candidate_brand.endswith("™")):
        candidate_brand = f"{candidate_brand}®"
        
    trade_name = candidate_brand.rstrip("®™") if candidate_brand else ""
    return (clean_mfr, candidate_brand, trade_name)


