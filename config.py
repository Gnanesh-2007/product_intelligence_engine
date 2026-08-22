from typing import List, Set

# Master list of all 252 static output columns in exact order
EXPECTED_OUTPUT_COLUMNS: List[str] = [
    "MFR URL",
    "Ref URL 1",
    "Ref URL 2",
    "Ref URL 3",
    "Ref URL 4",
    "Ref URL 5",
    "PART_NUMBER",
    "Dept",
    "Class",
    "Fine",
    "SKU - MY_PART_NUMBER",
    "Mfg_Part_Num",
    "Part_Desc",
    "E1_Brand",
    "Unilog_Brand",
    "DIB_Brand",
    "Part_Manuf",
    "MANUFACTURER_NAME",
    "BRAND_NAME",
    "TRADE_NAME",
    "MANUFACTURER_PART_NUMBER",
    "ALTERNATE_PART_NUMBER",
    "Classpath",
    "MOBILE_DESC",
    "INVOICE_DESC",
    "SHORT_DESC",
    "LONG_DESC1",
    "RETAIL_DESC",
    "MARKETING_DESCRIPTION",
]

for i in range(1, 21):
    EXPECTED_OUTPUT_COLUMNS.append(f"ITEM_FEATURES_{i}")

EXPECTED_OUTPUT_COLUMNS.extend([
    "With",
    "Standard/Approvals",
    "Prop 65",
    "Application",
    "Includes",
    "Product Name",
])

for i in range(1, 51):
    EXPECTED_OUTPUT_COLUMNS.extend([
        f"ATTRIBUTE_LABEL {i}",
        f"ATTRIBUTE_VALUE {i}",
        f"ATTRIBUTE_UOM {i}"
    ])

EXPECTED_OUTPUT_COLUMNS.extend([
    "UPC",
    "EAN",
    "GTIN",
    "UNSPSC",
    "Warranty",
    "List Price",
    "Selling Qty",
    "Selling UOM",
    "Standard Packaging Information",
    "LENGTH",
    "LENGTH_UOM",
    "HEIGHT",
    "HEIGHT_UOM",
    "WIDTH",
    "WIDTH_UOM",
    "WEIGHT",
    "WEIGHT_UOM",
    "VOLUME",
    "VOLUME_UOM",
    "Product Image",
    "Alternate Image 1",
    "Alternate Image 2",
    "Alternate Image 3",
    "Alternate Image 4",
    "SDS",
    "SDS_1",
    "Warranty Information",
    "Catalog",
    "Specification Sheet",
    "Instruction/Installation Manual",
    "Service Manual",
    "Owners/User Manual",
    "Line Drawing",
    "MTR",
    "RoHS",
    "Full Engineering Drawing",
    "Energy Star Guide",
    "Technical Bulletin",
    "Submittal",
    "Compatibility Chart",
    "Size Chart",
    "Product Label/Insert",
    "Video Link",
    "Video Link 1",
    "Country Of Origin",
    "Discontinued",
    "Actual Image (Yes/No)"
])

assert len(EXPECTED_OUTPUT_COLUMNS) == 252, f"Expected 252 columns, got {len(EXPECTED_OUTPUT_COLUMNS)}"

PLACEHOLDER_STRINGS: Set[str] = {
    "-- unbranded --",
    "-- no unilog brand --",
    "-- no dib brand --",
    "-- unbranded--",
    "--no unilog brand--",
    "--no dib brand--",
    "unbranded",
    "none",
    "null",
    "n/a",
    "na",
    "-",
    "--",
    "unknown",
    "display only",
    "display-only",
    "nan"
}

CHAR_LIMITS = {
    "INVOICE_DESC_MAX": 40,
    "MOBILE_DESC_MIN": 60,
    "MOBILE_DESC_MAX": 80,
    "SHORT_DESC_MAX": 255,
    "RETAIL_DESC_MAX": 255,
}

