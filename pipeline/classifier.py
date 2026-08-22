from typing import Dict, Any
from knowledge.taxonomy_rules import classify_product

class TaxonomyClassifier:
    """Classifies products into standard hierarchical categories and UNSPSC."""
    
    @staticmethod
    def classify(cleaned_record: Dict[str, Any]) -> Dict[str, Any]:
        part_desc = cleaned_record.get("Part_Desc", "")
        mpn = cleaned_record.get("Mfg_Part_Num", "")
        dept_raw = cleaned_record.get("Dept", "")
        class_raw = cleaned_record.get("Class", "")
        fine_raw = cleaned_record.get("Fine", "")
        
        dept, cls, fine, classpath, unspsc, prod_name = classify_product(
            part_desc=part_desc,
            mpn=mpn,
            dept_raw=dept_raw,
            class_raw=class_raw,
            fine_raw=fine_raw
        )
        
        return {
            "Dept": dept,
            "Class": cls,
            "Fine": fine,
            "Classpath": classpath,
            "UNSPSC": unspsc,
            "Product Name": prod_name
        }

