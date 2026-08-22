from typing import Dict, Any, Tuple
from knowledge.brand_manufacturer import resolve_manufacturer_and_brand

class EntityResolver:
    """Resolves canonical Manufacturer, Brand with trademark symbols, Trade Name, and Part Numbers."""
    
    @staticmethod
    def resolve_entities(cleaned_record: Dict[str, Any]) -> Dict[str, Any]:
        raw_mfr = cleaned_record.get("Part_Manuf", "")
        raw_b_e1 = cleaned_record.get("E1_Brand", "")
        raw_b_unilog = cleaned_record.get("Unilog_Brand", "")
        raw_b_dib = cleaned_record.get("DIB_Brand", "")
        part_desc = cleaned_record.get("Part_Desc", "")
        mpn = cleaned_record.get("Mfg_Part_Num", "")
        
        mfr_name, brand_name, trade_name = resolve_manufacturer_and_brand(
            raw_mfr=raw_mfr,
            raw_brand_e1=raw_b_e1,
            raw_brand_unilog=raw_b_unilog,
            raw_brand_dib=raw_b_dib,
            part_desc=part_desc,
            mpn=mpn
        )
        
        return {
            "MANUFACTURER_NAME": mfr_name,
            "BRAND_NAME": brand_name,
            "TRADE_NAME": trade_name,
            "MANUFACTURER_PART_NUMBER": mpn,
            "ALTERNATE_PART_NUMBER": ""
        }

