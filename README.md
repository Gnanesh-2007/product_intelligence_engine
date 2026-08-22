# ? Industrial Product Intelligence Engine

> **AI-powered pipeline** that transforms fragmented industrial catalog data into structured, validated, commerce-ready product intelligence — across **252 standard columns**, with zero hallucination.

Built for the **UniHack AI Challenge** · Python · Streamlit · Rule-Based AI

---

## ?? What It Does

Industrial manufacturers manage product data spread across websites, catalogs, and PDFs. This engine automates the enrichment, classification, and validation of that data at scale.

```
Raw Catalog CSV/Excel  --?  8-Stage AI Pipeline  --?  252-Column Enriched Output
```

**Input:** Any industrial/distributor catalog (CSV or Excel)  
**Output:** 252-column Unilog-standard enriched file + confidence scores + audit trail

---

## ?? 8-Stage Pipeline

| Stage | Module | What It Does |
|---|---|---|
| 1 | Preprocessor | Strips placeholders, cleans delimiters, normalizes nulls |
| 2 | Entity Resolver | Maps brand strings ? canonical legal entities with ® / ™ |
| 3 | Taxonomy Classifier | Assigns Dept > Class > Fine > Classpath + UNSPSC (evidence-gated) |
| 4 | Attribute Extractor | Extracts up to 50 structured Label/Value/UOM triples from raw text |
| 5 | UOM Normalizer | Standardizes units + converts decimals to trade fractions (50.25 ? 50-1/4 in) |
| 6 | Content Synthesizer | Generates INVOICE_DESC (=40 CAPS), MOBILE_DESC (60-80 chars), LONG_DESC1, SHORT_DESC, RETAIL_DESC, MARKETING_DESCRIPTION |
| 7 | Digital Asset Mapper | Evidence-based image/spec-sheet filenames — never fabricated |
| 8 | Validator & Scorer | 252-column schema check, field rules, confidence score, human-review flag |

---

## ??? Zero-Hallucination Architecture

Every field is **evidence-gated**:
- Specs, dimensions, voltages ? only extracted from source text via regex
- UNSPSC ? only assigned when **=2 keyword signals** match (never guessed)
- Certifications, warranties, prices ? **left blank** if not in source
- Digital assets ? only generated when brand + MPN are both resolved
- Low-confidence records ? automatically flagged for **human-in-the-loop review**

---

## ?? Benchmark Results

| Metric | Result |
|---|---|
| Output Columns | **252 / 252 (100%)** |
| INVOICE_DESC = 40 chars + UPPERCASE | **100% compliant** |
| MOBILE_DESC 60–80 chars | **100% compliant** |
| UOM standardization | **100% compliant** |
| Avg Confidence (1,000-item feed) | **99.2%** |
| Throughput | **>3,000 items/sec** |
| Secondary multi-brand catalog | **100% confidence, 10/10 clean** |

---

## ?? Quickstart

### Prerequisites
```bash
pip install pandas openpyxl streamlit
```

### 1 — Streamlit Dashboard (recommended)
```bash
python -m streamlit run app/streamlit_app.py
```
Open **http://localhost:8501** — upload any catalog CSV/Excel and go.

### 2 — CLI
```bash
# Enrich a catalog ? Excel output
python cli.py data/sample_input.csv -o output/enriched.xlsx --format xlsx

# Enrich a catalog ? CSV output
python cli.py data/sample_input.csv -o output/enriched.csv --format csv
```

### 3 — Run Tests
```bash
python tests/run_final_tests.py
```

---

## ?? Project Structure

```
product_intelligence_engine/
+-- app/
¦   +-- streamlit_app.py        # Streamlit UI
+-- pipeline/
¦   +-- engine.py               # Master orchestrator
¦   +-- preprocessor.py         # Stage 1
¦   +-- entity_resolver.py      # Stage 2
¦   +-- classifier.py           # Stage 3
¦   +-- attribute_extractor.py  # Stage 4
¦   +-- uom_normalizer.py       # Stage 5
¦   +-- content_synthesizer.py  # Stage 6
¦   +-- digital_assets.py       # Stage 7
¦   +-- validator.py            # Stage 8
+-- knowledge/
¦   +-- brand_manufacturer.py   # Brand/manufacturer canonical database
¦   +-- taxonomy_rules.py       # Taxonomy rules + UNSPSC knowledge base
¦   +-- uom_standards.py        # Master UOM dictionary
+-- data/
¦   +-- sample_input.csv        # 1,000-item primary demo dataset
¦   +-- secondary_catalog.csv   # Multi-brand secondary demo dataset
+-- output/                     # Enriched outputs (gitignored)
+-- tests/
¦   +-- test_pipeline.py        # Unit tests
¦   +-- run_final_tests.py      # Full regression suite
+-- config.py                   # 252-column schema definition
+-- cli.py                      # CLI entry point
+-- run_app.bat                 # Windows one-click launcher
```

---

## ?? Demo Datasets

| Dataset | Items | Brands | Avg Confidence |
|---|---|---|---|
| Primary Industrial Feed | 1,000 | 3M, Diablo, Frigidaire, Whirlpool, Philips… | 99.2% |
| Multi-Brand Catalog | 10 | Schneider Electric, Parker, Fastenal, Makita, Eaton, ABB, Klein Tools, 3M | 100.0% |

---

## ??? Tech Stack

- **Python 3.9+** — core engine
- **Pandas** — data processing
- **Streamlit** — interactive web UI
- **OpenPyXL** — Excel I/O
- **Regex + Rule Engine** — zero-hallucination attribute extraction

---

*Built for the UniHack Industrial AI Challenge*
