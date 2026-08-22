import re
from typing import Dict, Any
from config import PLACEHOLDER_STRINGS

class Preprocessor:
    """Cleans raw catalog records, strips placeholder strings, and extracts MPN."""
    
    @staticmethod
    def is_placeholder(val: Any) -> bool:
        if val is None:
            return True
        s = str(val).strip().lower()
        return s in PLACEHOLDER_STRINGS or s == ""

    @classmethod
    def clean_text(cls, val: Any) -> str:
        if cls.is_placeholder(val):
            return ""
        s = str(val).strip()
        # Collapse multiple spaces
        s = re.sub(r'\s+', ' ', s)
        return s

    @classmethod
    def preprocess_record(cls, record: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = {}
        
        # Map common aliases to standard keys
        cleaned["Mfg_Part_Num"] = cls.clean_text(
            record.get("Mfg_Part_Num") or record.get("MFG_PART_NUM") or record.get("MANUFACTURER_PART_NUMBER") or ""
        )
        cleaned["Part_Desc"] = cls.clean_text(
            record.get("Part_Desc") or record.get("PART_DESC") or record.get("Description") or ""
        )
        cleaned["E1_Brand"] = cls.clean_text(record.get("E1_Brand") or record.get("E1_BRAND") or "")
        cleaned["Unilog_Brand"] = cls.clean_text(record.get("Unilog_Brand") or record.get("UNILOG_BRAND") or "")
        cleaned["DIB_Brand"] = cls.clean_text(record.get("DIB_Brand") or record.get("DIB_BRAND") or "")
        cleaned["Part_Manuf"] = cls.clean_text(record.get("Part_Manuf") or record.get("PART_MANUF") or "")
        
        # Preserve original IDs if present
        cleaned["PART_NUMBER"] = record.get("PART_NUMBER") or record.get("Part_Number") or ""
        cleaned["SKU - MY_PART_NUMBER"] = record.get("SKU - MY_PART_NUMBER") or record.get("SKU") or ""
        cleaned["Dept"] = cls.clean_text(record.get("Dept") or "")
        cleaned["Class"] = cls.clean_text(record.get("Class") or "")
        cleaned["Fine"] = cls.clean_text(record.get("Fine") or "")
        
        # If Mfg_Part_Num is empty, attempt to extract leading alphanumeric code from Part_Desc
        if not cleaned["Mfg_Part_Num"] and cleaned["Part_Desc"]:
            match = re.match(r'^([A-Za-z0-9\-_/]+)\b', cleaned["Part_Desc"])
            if match:
                cleaned["Mfg_Part_Num"] = match.group(1)

        return cleaned

