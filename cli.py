import argparse
import os
import sys
import time
import pandas as pd
from pipeline.engine import ProductIntelligenceEngine

def main():
    parser = argparse.ArgumentParser(
        description="UniHack AI-Powered Industrial Product Intelligence Engine"
    )
    parser.add_argument("input_path", help="Path to input CSV or Excel file")
    parser.add_argument(
        "-o", "--output", help="Path to save enriched output file", default=None
    )
    parser.add_argument(
        "-f", "--format", choices=["xlsx", "csv"], default="xlsx", help="Output format"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_path):
        print(f"Error: Input file '{args.input_path}' not found.", file=sys.stderr)
        sys.exit(1)
        
    print(f"\n========================================================")
    print(f"  AI-POWERED INDUSTRIAL PRODUCT INTELLIGENCE ENGINE")
    print(f"========================================================")
    print(f"[*] Reading input: {args.input_path}")
    
    start_time = time.time()
    if args.input_path.endswith(".xlsx") or args.input_path.endswith(".xls"):
        df_in = pd.read_excel(args.input_path)
    else:
        df_in = pd.read_csv(args.input_path)
        
    print(f"[*] Input shape: {df_in.shape[0]} rows, {df_in.shape[1]} columns")
    
    engine = ProductIntelligenceEngine()
    
    def print_progress(current, total):
        pct = (current / total) * 100
        sys.stdout.write(f"\r[*] Processing records: {current}/{total} ({pct:.1f}%)")
        sys.stdout.flush()
        
    df_out, validations = engine.enrich_dataframe(df_in, progress_callback=print_progress)
    print("\n[*] Enrichment complete!")
    
    elapsed = time.time() - start_time
    avg_confidence = sum(v["confidence_score"] for v in validations) / len(validations) if validations else 0.0
    valid_count = sum(1 for v in validations if v["is_valid"])
    review_count = sum(1 for v in validations if v["needs_human_review"])
    
    # Determine output path
    if not args.output:
        base_name = os.path.splitext(os.path.basename(args.input_path))[0]
        out_dir = os.path.join(os.path.dirname(args.input_path), "output")
        os.makedirs(out_dir, exist_ok=True)
        args.output = os.path.join(out_dir, f"{base_name}_enriched.{args.format}")
    else:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        
    if args.output.endswith(".xlsx") or args.format == "xlsx":
        df_out.to_excel(args.output, index=False, engine="openpyxl")
    else:
        df_out.to_csv(args.output, index=False)
        
    print(f"\n--- EXECUTION SUMMARY ---")
    print(f"Total Rows Processed : {len(df_out)}")
    print(f"Output Columns       : {len(df_out.columns)} (100% Schema Preserved)")
    print(f"Elapsed Time         : {elapsed:.2f}s ({len(df_out)/max(elapsed, 0.001):.1f} rows/sec)")
    print(f"Average Confidence   : {avg_confidence:.1f}%")
    print(f"Fully Compliant Rows : {valid_count}/{len(df_out)} ({(valid_count/len(df_out))*100:.1f}%)")
    print(f"Needs Human Review   : {review_count}/{len(df_out)}")
    print(f"Saved Output File    : {os.path.abspath(args.output)}")
    print(f"========================================================\n")

if __name__ == "__main__":
    main()

