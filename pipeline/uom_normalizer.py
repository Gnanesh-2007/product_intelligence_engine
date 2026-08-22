from typing import List, Dict, Any
from knowledge.uom_standards import normalize_uom, format_number_uom
from knowledge.fraction_decimal import convert_string_decimals_to_fractions

class UOMNormalizer:
    """Normalizes unit symbols across all attributes, dimensions, and specifications."""
    
    @classmethod
    def normalize_attributes(cls, attributes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for attr in attributes:
            val = attr.get("value", "")
            uom = attr.get("uom", "")
            
            # Normalize UOM
            uom_norm = normalize_uom(uom) if uom else ""
            
            # Format value if it is a dimension or decimal
            if isinstance(val, str):
                val_formatted = convert_string_decimals_to_fractions(val)
            else:
                val_formatted = val
                
            normalized.append({
                "label": attr.get("label", ""),
                "value": val_formatted,
                "uom": uom_norm
            })
        return normalized

