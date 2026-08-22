from typing import Dict, Any, List
from config import CHAR_LIMITS, EXPECTED_OUTPUT_COLUMNS
from knowledge.uom_standards import UOM_MAPPINGS

class DataValidator:
    """Validates enriched product intelligence records against Unilog content rules and computes confidence."""
    
    @classmethod
    def validate_record(cls, enriched: Dict[str, Any]) -> Dict[str, Any]:
        issues: List[str] = []
        score = 100.0
        
        # 1. 252 Column Schema check
        missing_cols = [c for c in EXPECTED_OUTPUT_COLUMNS if c not in enriched]
        if missing_cols:
            issues.append(f"Missing {len(missing_cols)} schema columns")
            score -= 30.0
            
        # 2. Required Core Identity Fields
        mpn = enriched.get("MANUFACTURER_PART_NUMBER", "")
        if not mpn or mpn.lower() in {"none", "null", "nan", "-"}:
            issues.append("Missing Manufacturer Part Number (MPN)")
            score -= 30.0
            
        brand = enriched.get("BRAND_NAME", "")
        if not brand or brand.lower() in {"unbranded", "-- unbranded --", "none", "null", "nan", "-"}:
            issues.append("Missing canonical brand")
            score -= 20.0
        elif not (brand.endswith("®") or brand.endswith("™")):
            issues.append("Brand is missing registered trademark (®) or trademark (™) symbol")
            score -= 5.0
            
        # 3. Classpath & Product Name
        cp = enriched.get("Classpath", "")
        if not cp or ">" not in cp:
            issues.append("Taxonomy classpath is unclassified or missing")
            score -= 15.0
        elif cp.count(">") < 2:
            issues.append("Taxonomy classpath missing Dept>Class>Fine depth (only 1 level)")
            score -= 5.0

        prod_name = enriched.get("Product Name", "")
        if not prod_name or prod_name.lower() in {"none", "null", "nan", "-"}:
            issues.append("Product Name is missing")
            score -= 10.0

        # 4. Description Character Limit Checks
        inv = enriched.get("INVOICE_DESC", "")
        if not inv:
            issues.append("Invoice description is empty")
            score -= 20.0
        else:
            if len(inv) > CHAR_LIMITS["INVOICE_DESC_MAX"]:
                issues.append(f"Invoice description length {len(inv)} exceeds max {CHAR_LIMITS['INVOICE_DESC_MAX']}")
                score -= 15.0
            if inv != inv.upper():
                issues.append("Invoice description is not fully uppercase")
                score -= 5.0

        mob = enriched.get("MOBILE_DESC", "")
        if not mob:
            issues.append("Mobile description is empty")
            score -= 15.0
        else:
            if len(mob) < CHAR_LIMITS["MOBILE_DESC_MIN"]:
                issues.append(f"Mobile description length {len(mob)} is under min {CHAR_LIMITS['MOBILE_DESC_MIN']}")
                score -= 10.0
            elif len(mob) > CHAR_LIMITS["MOBILE_DESC_MAX"]:
                issues.append(f"Mobile description length {len(mob)} exceeds max {CHAR_LIMITS['MOBILE_DESC_MAX']}")
                score -= 10.0

        # 4b. LONG_DESC1 sparse sentinel check
        long1 = enriched.get("LONG_DESC1", "")
        if not long1 or long1.rstrip(".") == long1.split(",")[0].rstrip("."):
            # Only one comma-segment means no attributes were appended — purely a product name
            issues.append("LONG_DESC1 is sparse — no extracted attributes included")
            score -= 8.0
                
        # 5. Attributes completeness & Valid UOMs
        attr_count = 0
        invalid_uoms = 0
        for i in range(1, 51):
            lbl = enriched.get(f"ATTRIBUTE_LABEL {i}")
            val = enriched.get(f"ATTRIBUTE_VALUE {i}")
            uom = enriched.get(f"ATTRIBUTE_UOM {i}")
            if lbl or val:
                attr_count += 1
            if uom and str(uom).lower() not in UOM_MAPPINGS.values() and str(uom).lower() not in UOM_MAPPINGS:
                invalid_uoms += 1
                
        if attr_count == 0:
            issues.append("No structured attributes extracted")
            score -= 15.0
            
        if invalid_uoms > 0:
            issues.append(f"Found {invalid_uoms} non-standard UOM abbreviations")
            score -= 5.0
            
        confidence = max(0.0, min(100.0, score))
        needs_human_review = confidence < 75.0 or len(issues) > 0
        
        return {
            "confidence_score": round(confidence, 1),
            "is_valid": len(issues) == 0,
            "issues": issues,
            "attribute_count": attr_count,
            "needs_human_review": needs_human_review,
            "traceability": {
                "input_mpn": mpn,
                "resolved_brand": brand,
                "resolved_mfr": enriched.get("MANUFACTURER_NAME", ""),
                "classified_tax": cp,
                "synthesized_titles": bool(enriched.get("SHORT_DESC")),
                "assets_generated": bool(enriched.get("Product Image"))
            }
        }


