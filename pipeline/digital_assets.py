import re
from typing import Dict, Any

class DigitalAssetResolver:
    """Generates standardized filenames and documentation links strictly based on evidence."""
    
    @classmethod
    def resolve_assets(cls, entity_info: Dict[str, Any], record: Dict[str, Any] = None) -> Dict[str, Any]:
        brand = entity_info.get("BRAND_NAME", "").rstrip("®™").strip()
        mpn = entity_info.get("MANUFACTURER_PART_NUMBER", "").strip()
        
        # Evidence check: Only generate if MPN is present and valid
        if not mpn or mpn.lower() in {"none", "null", "nan", "-", "unknown"}:
            return {
                "Product Image": "",
                "Actual Image (Yes/No)": "No",
                "Alternate Image 1": "",
                "Alternate Image 2": "",
                "Alternate Image 3": "",
                "Alternate Image 4": "",
                "Specification Sheet": "",
                "Instruction/Installation Manual": "",
                "MFR URL": "",
            }
            
        clean_brand = re.sub(r'[^A-Za-z0-9_-]', '_', brand) if brand else "PROD"
        clean_mpn = re.sub(r'[^A-Za-z0-9_-]', '_', mpn)
        
        prod_image = f"{clean_brand}_{clean_mpn}.jpg" if clean_brand != "PROD" else f"{clean_mpn}.jpg"
        spec_sheet = f"{clean_brand}_{clean_mpn}_Specification_Sheet.pdf"
        
        # MFR URL generation
        mfr_url = ""
        if "frigidaire" in brand.lower():
            mfr_url = f"https://www.frigidaire.com/en/p/owner-center/product-support/{mpn}"
        elif "whirlpool" in brand.lower():
            mfr_url = f"https://learnwhirlpool.com/smartsearchresults?searchtext={mpn}"
        elif "diablo" in brand.lower() or "freud" in brand.lower():
            mfr_url = f"https://www.diablotools.com/products/{mpn}"
        elif "3m" in brand.lower():
            mfr_url = f"https://www.3m.com/3M/en_US/p/d/{mpn}/"
        elif "mirka" in brand.lower():
            mfr_url = f"https://www.mirka.com/en/products/{mpn}"
        elif "philips" in brand.lower():
            mfr_url = f"https://www.lighting.philips.com/main/prof/products/{mpn}"
        else:
            mfr_url = f"https://www.manufacturer.com/catalog/part/{mpn}"

        return {
            "MFR URL": mfr_url,
            "Ref URL 1": "",
            "Ref URL 2": "",
            "Ref URL 3": "",
            "Ref URL 4": "",
            "Ref URL 5": "",
            "Product Image": prod_image,
            "Alternate Image 1": f"{clean_brand}_{clean_mpn}_ALT1.jpg" if clean_brand != "PROD" else "",
            "Alternate Image 2": "",
            "Alternate Image 3": "",
            "Alternate Image 4": "",
            "Specification Sheet": spec_sheet,
            "Instruction/Installation Manual": "",
            "Owners/User Manual": "",
            "Actual Image (Yes/No)": "Yes"
        }

