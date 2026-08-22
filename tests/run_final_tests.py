import sys, pandas as pd
sys.path.insert(0, ".")
from tests.test_pipeline import (
    test_config_columns_count, test_uom_normalization, test_fraction_conversion,
    test_entity_resolution, test_preprocessor_placeholders,
    test_single_record_enrichment, test_batch_dataframe_enrichment
)
from pipeline.engine import ProductIntelligenceEngine
from config import EXPECTED_OUTPUT_COLUMNS

print("=== UNIT TESTS ===")
test_config_columns_count(); print(" [PASS] Column count = 252")
test_uom_normalization();    print(" [PASS] UOM normalization")
test_fraction_conversion();  print(" [PASS] Fraction conversion")
test_entity_resolution();    print(" [PASS] Entity / brand resolution")
test_preprocessor_placeholders(); print(" [PASS] Preprocessor placeholder scrubbing")
test_single_record_enrichment();  print(" [PASS] Single record enrichment")
test_batch_dataframe_enrichment(); print(" [PASS] Batch DataFrame enrichment")

print()
print("=== INTEGRATION: Primary 1,000-Item Feed ===")
engine = ProductIntelligenceEngine()
df1 = pd.read_csv("data/sample_input.csv")
out1, val1 = engine.enrich_dataframe(df1)
assert len(out1) == 1000
assert list(out1.columns) == EXPECTED_OUTPUT_COLUMNS
for idx, row in out1.head(10).iterrows():
    ld = str(row.get("LONG_DESC1", ""))
    assert ld and "," in ld, f"Sparse LONG_DESC1 at row {idx}: [{ld}]"
for idx, row in out1.iterrows():
    mob = str(row.get("MOBILE_DESC", ""))
    assert 60 <= len(mob) <= 80, f"MOBILE_DESC out of range ({len(mob)}) at row {idx}"
print(f" [PASS] 1000 rows | 252 cols | LONG_DESC1 non-sparse | MOBILE_DESC 60-80 (all)")

print()
print("=== INTEGRATION: Secondary Multi-Brand Catalog ===")
df2 = pd.read_csv("data/secondary_catalog.csv")
out2, val2 = engine.enrich_dataframe(df2)
assert len(out2) == 10
assert list(out2.columns) == EXPECTED_OUTPUT_COLUMNS
for idx, row in out2.iterrows():
    mob = str(row.get("MOBILE_DESC", ""))
    assert 60 <= len(mob) <= 80, f"MOBILE_DESC out of range ({len(mob)}) at row {idx}"
print(f" [PASS] 10 rows | 252 cols | MOBILE_DESC 60-80 (all)")

print()
print("=== SPOT-CHECK: Primary first 3 rows ===")
for _, row in out1.head(3).iterrows():
    inv = str(row.get("INVOICE_DESC",""))
    mob = str(row.get("MOBILE_DESC",""))
    ld  = str(row.get("LONG_DESC1",""))
    cp  = str(row.get("Classpath",""))
    un  = str(row.get("UNSPSC",""))
    brand = str(row.get("BRAND_NAME",""))
    print(f"  INV[{len(inv)}]: {inv}")
    print(f"  MOB[{len(mob)}]: {mob}")
    print(f"  LD1[{len(ld)}]: {ld[:130]}")
    print(f"  PATH: {cp}")
    print(f"  UNSPSC: {un if un else '(blank)'}")
    print(f"  BRAND: {brand}")
    print()

print("=== SPOT-CHECK: Secondary all 10 rows ===")
for _, row in out2.iterrows():
    inv = str(row.get("INVOICE_DESC",""))
    mob = str(row.get("MOBILE_DESC",""))
    cp  = str(row.get("Classpath",""))
    un  = str(row.get("UNSPSC",""))
    brand = str(row.get("BRAND_NAME",""))
    ld  = str(row.get("LONG_DESC1",""))
    print(f"  INV[{len(inv)}]: {inv}")
    print(f"  MOB[{len(mob)}]: {mob}")
    print(f"  LD1[{len(ld)}]: {ld[:100]}")
    print(f"  PATH: {cp}")
    print(f"  UNSPSC: {un if un else '(blank)'}")
    print(f"  BRAND: {brand}")
    print()

print("========================================================")
print(" ALL REGRESSION + INTEGRATION TESTS PASSED (100%)!")
print("========================================================")
