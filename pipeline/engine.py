import pandas as pd
from typing import Dict, Any, List, Optional, Callable, Tuple
from config import EXPECTED_OUTPUT_COLUMNS
from pipeline.preprocessor import Preprocessor
from pipeline.entity_resolver import EntityResolver
from pipeline.classifier import TaxonomyClassifier
from pipeline.attribute_extractor import AttributeExtractor
from pipeline.uom_normalizer import UOMNormalizer
from pipeline.content_synthesizer import ContentSynthesizer
from pipeline.digital_assets import DigitalAssetResolver
from pipeline.validator import DataValidator

class ProductIntelligenceEngine:
    """Master AI & Rule-Powered Product Intelligence Pipeline Orchestrator."""
    
    def __init__(self):
        pass
        
    def enrich_record(self, raw_record: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        # Stage 1: Preprocessing & Placeholder Filtering
        cleaned = Preprocessor.preprocess_record(raw_record)
        
        # Stage 2: Entity Resolution
        entity_info = EntityResolver.resolve_entities(cleaned)
        
        # Stage 3: Taxonomy Classification
        tax_info = TaxonomyClassifier.classify(cleaned)
        
        # Stage 4: Attribute Extraction
        raw_attributes, spec_fields = AttributeExtractor.extract_attributes(cleaned, entity_info, tax_info)
        
        # Stage 5: UOM Normalization & Fraction Formatting
        norm_attributes = UOMNormalizer.normalize_attributes(raw_attributes)
        
        # Stage 6: Content Description Synthesizer
        content_info = ContentSynthesizer.synthesize_all(
            record=cleaned,
            entity_info=entity_info,
            tax_info=tax_info,
            attributes=norm_attributes,
            spec_fields=spec_fields
        )
        
        # Stage 7: Digital Asset Resolution
        asset_info = DigitalAssetResolver.resolve_assets(entity_info, cleaned)
        
        # Assemble 252-Column Dictionary
        row: Dict[str, Any] = {}
        for col in EXPECTED_OUTPUT_COLUMNS:
            row[col] = ""
            
        # Populate Base IDs & Cleansed Input Fields
        row["PART_NUMBER"] = cleaned.get("PART_NUMBER", "")
        row["SKU - MY_PART_NUMBER"] = cleaned.get("SKU - MY_PART_NUMBER", "")
        row["Mfg_Part_Num"] = cleaned.get("Mfg_Part_Num", "")
        row["Part_Desc"] = raw_record.get("Part_Desc", cleaned.get("Part_Desc", ""))
        row["E1_Brand"] = raw_record.get("E1_Brand", "")
        row["Unilog_Brand"] = raw_record.get("Unilog_Brand", "")
        row["DIB_Brand"] = raw_record.get("DIB_Brand", "")
        row["Part_Manuf"] = raw_record.get("Part_Manuf", "")
        
        # Entity fields
        row.update(entity_info)
        
        # Taxonomy fields
        row.update(tax_info)
        
        # Content descriptions & features
        row.update(content_info)
        
        # Specifications & Approvals
        row.update(spec_fields)
        
        # Digital assets
        row.update(asset_info)
        
        # Populate Attributes 1 to 50
        for idx, attr in enumerate(norm_attributes[:50], start=1):
            row[f"ATTRIBUTE_LABEL {idx}"] = attr.get("label", "")
            row[f"ATTRIBUTE_VALUE {idx}"] = attr.get("value", "")
            row[f"ATTRIBUTE_UOM {idx}"] = attr.get("uom", "")
            
        # Stage 8: Quality Validation & Traceability
        val_result = DataValidator.validate_record(row)
        
        return row, val_result

    def enrich_dataframe(
        self,
        df: pd.DataFrame,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> pd.DataFrame:
        """Enriches an entire pandas DataFrame and outputs exact 252-column schema."""
        enriched_rows = []
        validation_results = []
        total = len(df)
        
        for idx, (_, raw_series) in enumerate(df.iterrows()):
            raw_dict = raw_series.to_dict()
            enriched_row, val_res = self.enrich_record(raw_dict)
            enriched_rows.append(enriched_row)
            validation_results.append(val_res)
            
            if progress_callback:
                progress_callback(idx + 1, total)
                
        out_df = pd.DataFrame(enriched_rows, columns=EXPECTED_OUTPUT_COLUMNS)
        return out_df, validation_results

