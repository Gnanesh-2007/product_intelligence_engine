import unittest
import pandas as pd
from config import EXPECTED_OUTPUT_COLUMNS, CHAR_LIMITS
from knowledge.uom_standards import normalize_uom, format_number_uom
from knowledge.fraction_decimal import decimal_to_fraction, convert_string_decimals_to_fractions
from knowledge.brand_manufacturer import resolve_manufacturer_and_brand
from pipeline.preprocessor import Preprocessor
from pipeline.engine import ProductIntelligenceEngine

def test_config_columns_count():
    assert len(EXPECTED_OUTPUT_COLUMNS) == 252
    assert "MFR URL" in EXPECTED_OUTPUT_COLUMNS
    assert "ATTRIBUTE_LABEL 1" in EXPECTED_OUTPUT_COLUMNS
    assert "ATTRIBUTE_VALUE 50" in EXPECTED_OUTPUT_COLUMNS
    assert "Actual Image (Yes/No)" in EXPECTED_OUTPUT_COLUMNS

def test_uom_normalization():
    assert normalize_uom("inches") == "in"
    assert normalize_uom("in.") == "in"
    assert normalize_uom("volts") == "V"
    assert normalize_uom("amps") == "A"
    assert normalize_uom("dba") == "dBA"
    assert format_number_uom("24", "inches") == "24 in"

def test_fraction_conversion():
    assert decimal_to_fraction(50.25) == "50-1/4"
    assert decimal_to_fraction(0.5) == "1/2"
    assert decimal_to_fraction(24.0) == "24"
    assert convert_string_decimals_to_fractions("50.25 in") == "50-1/4 in"

def test_entity_resolution():
    mfr, brand, trade = resolve_manufacturer_and_brand(
        raw_mfr="Appliance Dealers Cooperative (APPDE)",
        raw_brand_e1="-- Unbranded --",
        raw_brand_unilog="-- No Unilog Brand --",
        raw_brand_dib="-- No DIB Brand --",
        part_desc="PDSH4816AF Dishwasher SS - Display Only",
        mpn="PDSH4816AF"
    )
    assert mfr == "Rheem Manufacturing"
    assert "FRIGIDAIRE" in brand
    assert brand.endswith("®")

def test_preprocessor_placeholders():
    record = {
        "Mfg_Part_Num": "PDSH4816AF",
        "Part_Desc": "PDSH4816AF Dishwasher SS",
        "E1_Brand": "-- Unbranded --",
        "Unilog_Brand": "-- No Unilog Brand --",
        "DIB_Brand": "None",
        "Part_Manuf": "Appliance Dealers Cooperative (APPDE)"
    }
    cleaned = Preprocessor.preprocess_record(record)
    assert cleaned["E1_Brand"] == ""
    assert cleaned["Unilog_Brand"] == ""
    assert cleaned["DIB_Brand"] == ""
    assert cleaned["Mfg_Part_Num"] == "PDSH4816AF"

def test_single_record_enrichment():
    engine = ProductIntelligenceEngine()
    raw_record = {
        "Mfg_Part_Num": "PDSH4816AF",
        "Part_Desc": "PDSH4816AF Dishwasher SS - Display Only",
        "E1_Brand": "-- Unbranded --",
        "Unilog_Brand": "-- No Unilog Brand --",
        "DIB_Brand": "-- No DIB Brand --",
        "Part_Manuf": "Appliance Dealers Cooperative (APPDE)"
    }
    enriched, val_res = engine.enrich_record(raw_record)
    
    # 252 columns exist
    assert len(enriched) == 252
    for col in EXPECTED_OUTPUT_COLUMNS:
        assert col in enriched
        
    # Check Invoice Desc <= 40 chars and uppercase
    inv = enriched["INVOICE_DESC"]
    assert len(inv) <= CHAR_LIMITS["INVOICE_DESC_MAX"]
    assert inv == inv.upper()
    
    # Check Mobile Desc
    mob = enriched["MOBILE_DESC"]
    assert len(mob) <= CHAR_LIMITS["MOBILE_DESC_MAX"]
    
    # Check Brand & Manufacturer
    assert "FRIGIDAIRE" in enriched["BRAND_NAME"]
    assert enriched["MANUFACTURER_NAME"] == "Rheem Manufacturing"
    assert enriched["Product Image"] == "FRIGIDAIRE_PDSH4816AF.jpg"
    assert enriched["Actual Image (Yes/No)"] == "Yes"

def test_batch_dataframe_enrichment():
    engine = ProductIntelligenceEngine()
    df_raw = pd.DataFrame([
        {
            "Mfg_Part_Num": "PDSH4816AF",
            "Part_Desc": "PDSH4816AF Dishwasher SS",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
            "Part_Manuf": "Appliance Dealers Cooperative (APPDE)"
        },
        {
            "Mfg_Part_Num": "WDTS7024RZ",
            "Part_Desc": "WDTS7024RZ Dishwasher SS",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
            "Part_Manuf": "Appliance Dealers Cooperative (APPDE)"
        },
        {
            "Mfg_Part_Num": "DCB518ASTS06G",
            "Part_Desc": "DCB518ASTS06G Diablo 1/2\"x18\" - Sanding Belt 6pc",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
            "Part_Manuf": "Freud Inc (2435)"
        }
    ])
    
    df_enriched, validations = engine.enrich_dataframe(df_raw)
    assert len(df_enriched) == 3
    assert len(df_enriched.columns) == 252
    assert list(df_enriched.columns) == EXPECTED_OUTPUT_COLUMNS

