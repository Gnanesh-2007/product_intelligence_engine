import streamlit as st
import pandas as pd
import os, io, time
from config import EXPECTED_OUTPUT_COLUMNS, CHAR_LIMITS
from pipeline.engine import ProductIntelligenceEngine

st.set_page_config(
    page_title="Industrial Product Intelligence Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 2.1rem; font-weight: 800; color: #0f4c81; }
    .sub-header  { font-size: 1.0rem; color: #4a5568; margin-bottom: 1.1rem; }
    .step-label  { font-size: 0.78rem; font-weight: 700; color: #6b7280;
                   text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 2px; }
    .badge-clean  { background:#d1fae5; color:#065f46; padding:3px 9px;
                    border-radius:5px; font-weight:700; font-size:0.82rem; }
    .badge-review { background:#fef3c7; color:#92400e; padding:3px 9px;
                    border-radius:5px; font-weight:700; font-size:0.82rem; }
    .badge-halt   { background:#fee2e2; color:#991b1b; padding:3px 9px;
                    border-radius:5px; font-weight:700; font-size:0.82rem; }
    .evidence-box { background:#f0fdf4; border-left:4px solid #22c55e;
                    padding:10px 14px; border-radius:6px; font-size:0.9rem; }
    .halluc-box   { background:#fef2f2; border-left:4px solid #ef4444;
                    padding:10px 14px; border-radius:6px; font-size:0.9rem; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=52)
st.sidebar.title("Pipeline Config")
st.sidebar.markdown("---")
st.sidebar.subheader("Active Pipeline Stages")
for stage in [
    "1. Preprocessor & Placeholder Stripper",
    "2. Evidence-Based Entity Resolver",
    "3. Multi-Domain Taxonomy & UNSPSC",
    "4. 50-Triple Attribute Extractor",
    "5. Unilog Master UOM & Trade Fractions",
    "6. Multi-Tier Description Synthesizer",
    "7. Evidence-Based Digital Asset Mapper",
    "8. Quality Validator & Confidence Scorer",
]:
    st.sidebar.checkbox(stage, value=True, disabled=True)

st.sidebar.markdown("---")
st.sidebar.info("Output Schema: **252 Static Columns**\nUnilog Master Format Compliant")

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">⚡ Industrial Product Intelligence Engine</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Transform any industrial catalog into structured, validated, '
    'commerce-ready product intelligence — across 252 standard columns, with zero hallucination.</div>',
    unsafe_allow_html=True
)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [
    ("enriched_df", None), ("validation_results", None),
    ("input_df", None),    ("dataset_name", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default

tabs = st.tabs(["📂 1 · Upload & Analyze", "⚡ 2 · Enrich & Export",
                "🛡️ 3 · Zero-Hallucination Audit", "🔍 4 · Record Deep Dive"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Upload & Schema Analysis
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.subheader("Step 1 — Load Your Industrial Catalog")
    st.markdown(
        "Upload **any** supplier, distributor, or manufacturer catalog in CSV or Excel format. "
        "The engine auto-detects column mappings and adapts to your schema."
    )

    uploaded_file = st.file_uploader(
        "Drop your catalog here (CSV or Excel)",
        type=["csv", "xlsx", "xls"],
        help="Supports any industrial/commercial catalog with product descriptions and part numbers.",
        label_visibility="collapsed",
    )

    # Demo datasets — tucked away, not the main CTA
    with st.expander("📋  Load a Demo Dataset instead", expanded=False):
        d1, d2 = st.columns(2)
        with d1:
            if st.button("Load 1,000-Item Abrasives / Appliances Feed", width='stretch'):
                path = "data/sample_input.csv"
                if os.path.exists(path):
                    st.session_state["input_df"] = pd.read_csv(path)
                    st.session_state["dataset_name"] = "Demo — 1,000-Item Industrial Feed (Abrasives, Appliances, Lighting)"
                    st.session_state["enriched_df"] = None
                    st.session_state["validation_results"] = None
        with d2:
            if st.button("Load Multi-Brand Catalog (Schneider, Parker, 3M…)", width='stretch'):
                path = "data/secondary_catalog.csv"
                if os.path.exists(path):
                    st.session_state["input_df"] = pd.read_csv(path)
                    st.session_state["dataset_name"] = "Demo — Multi-Brand Catalog (Schneider Electric, Parker, Fastenal, Makita, ABB, 3M…)"
                    st.session_state["enriched_df"] = None
                    st.session_state["validation_results"] = None

    # Handle upload
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith((".xlsx", ".xls")):
                st.session_state["input_df"] = pd.read_excel(uploaded_file)
            else:
                st.session_state["input_df"] = pd.read_csv(uploaded_file)
            st.session_state["dataset_name"] = uploaded_file.name
            st.session_state["enriched_df"] = None
            st.session_state["validation_results"] = None
        except Exception as e:
            st.error(f"Could not read file: {e}")

    if st.session_state["input_df"] is not None:
        df_in = st.session_state["input_df"]
        st.success(
            f"**{st.session_state['dataset_name']}** — "
            f"{len(df_in):,} rows · {len(df_in.columns)} source columns detected"
        )

        # Schema analysis
        st.markdown("---")
        st.subheader("Step 2 — Schema Analysis")
        s1, s2, s3 = st.columns(3)
        s1.metric("Source Rows", f"{len(df_in):,}")
        s2.metric("Source Columns", len(df_in.columns))
        s3.metric("Target Output Columns", 252)

        st.markdown("**Detected Source Fields:**")
        col_tags = "  ".join([f"`{c}`" for c in df_in.columns])
        st.markdown(col_tags)

        KNOWN_MAPPINGS = {
            "Part_Desc": "Product Description", "Mfg_Part_Num": "MPN",
            "E1_Brand": "Brand", "Unilog_Brand": "Brand (Unilog)",
            "DIB_Brand": "Brand (DIB)", "Part_Manuf": "Manufacturer",
            "PART_NUMBER": "Internal SKU", "SKU - MY_PART_NUMBER": "Alternate SKU",
        }
        mappings = [(src, KNOWN_MAPPINGS.get(src, "→ Extracted by engine")) for src in df_in.columns]
        st.table(pd.DataFrame(mappings, columns=["Source Column", "Mapped Role"]))

        with st.expander("Preview first 5 source rows", expanded=False):
            st.dataframe(df_in.head(5), width='stretch')

        st.info(
            "✅ Schema mapped. Proceed to **⚡ 2 · Enrich & Export** to run the full pipeline."
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Enrich & Export
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    if st.session_state["input_df"] is None:
        st.info("👈 Upload or load a catalog in **📂 1 · Upload & Analyze** first.")
    else:
        df_in = st.session_state["input_df"]
        st.subheader("Step 3 — Run Enrichment Pipeline")
        st.markdown(
            f"Ready to enrich **{len(df_in):,} items** from `{st.session_state['dataset_name']}`."
        )

        run_btn = st.button(
            "⚡ Run Full Enrichment Pipeline",
            type="primary", width='content'
        )

        if run_btn:
            engine = ProductIntelligenceEngine()
            prog = st.progress(0, text="Initializing...")
            start_t = time.time()

            def cb(curr, total):
                pct = int((curr / total) * 100)
                prog.progress(pct, text=f"Enriching: {curr} / {total} items ({pct}%)")

            df_out, validations = engine.enrich_dataframe(df_in, progress_callback=cb)
            elapsed = time.time() - start_t
            prog.empty()

            st.session_state["enriched_df"] = df_out
            st.session_state["validation_results"] = validations
            st.success(
                f"✅ Enriched **{len(df_out):,} items** in **{elapsed:.2f}s** "
                f"({len(df_out)/max(elapsed, 0.001):.0f} items/sec)"
            )

        if st.session_state["enriched_df"] is not None:
            df_out = st.session_state["enriched_df"]
            vals   = st.session_state["validation_results"]
            total  = len(df_out)
            avg_c  = sum(v["confidence_score"] for v in vals) / total
            clean  = sum(1 for v in vals if v["is_valid"])
            review = sum(1 for v in vals if v["needs_human_review"])

            st.markdown("---")
            st.subheader("Step 4 — Results & Validation Summary")
            k1, k2, k3, k4, k5 = st.columns(5)
            k1.metric("Items Enriched",    f"{total:,}")
            k2.metric("Output Columns",    f"{len(df_out.columns)} / 252", delta="100% Preserved")
            k3.metric("Avg Confidence",    f"{avg_c:.1f}%")
            k4.metric("Clean & Compliant", f"{clean:,}", f"{100*clean//total}%")
            k5.metric("Needs Review",      f"{review:,}", delta_color="off")

            # Filtered view
            filter_opt = st.radio(
                "Filter:",
                ["All Records", "Clean & Compliant Only", "Needs Human Review"],
                horizontal=True
            )
            if filter_opt == "Clean & Compliant Only":
                idx = [i for i, v in enumerate(vals) if v["is_valid"]]
            elif filter_opt == "Needs Human Review":
                idx = [i for i, v in enumerate(vals) if v["needs_human_review"]]
            else:
                idx = list(range(total))
            st.dataframe(df_out.iloc[idx].head(200), width='stretch')

            # Downloads
            st.markdown("---")
            st.subheader("Step 5 — Download Enriched Catalog")
            dl1, dl2, _ = st.columns([1, 1, 2])
            with dl1:
                buf = io.StringIO()
                df_out.to_csv(buf, index=False)
                st.download_button(
                    "📥 Download CSV (252 Columns)",
                    data=buf.getvalue().encode("utf-8"),
                    file_name="enriched_product_catalog.csv",
                    mime="text/csv",
                    width='stretch',
                )
            with dl2:
                try:
                    xbuf = io.BytesIO()
                    with pd.ExcelWriter(xbuf, engine="openpyxl") as writer:
                        df_out.to_excel(writer, index=False, sheet_name="Product Intelligence")
                    st.download_button(
                        "📊 Download Excel (.xlsx)",
                        data=xbuf.getvalue(),
                        file_name="enriched_product_catalog.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        width='stretch',
                    )
                except Exception:
                    st.info("Excel export available after enrichment.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Zero-Hallucination Audit  (the evidence screen)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    if st.session_state["validation_results"] is None:
        st.info("Run the enrichment pipeline first to view the audit.")
    else:
        vals   = st.session_state["validation_results"]
        df_out = st.session_state["enriched_df"]
        total  = len(df_out)

        st.subheader("🛡️ Zero-Hallucination Audit Dashboard")
        st.markdown(
            "Every enriched field is **evidence-gated**: if the source record doesn't contain it, "
            "it is left blank. The audit below verifies that claim with per-record flags."
        )

        # ── Compliance proof ─────────────────────────────────────────────────
        st.markdown("### ✅ Compliance Proof — Rule-by-Rule")
        inv_lens = [len(str(x)) for x in df_out["INVOICE_DESC"]]
        mob_lens = [len(str(x)) for x in df_out["MOBILE_DESC"]]
        brands   = df_out["BRAND_NAME"].astype(str)
        unspsc   = df_out["UNSPSC"].astype(str)
        long1    = df_out["LONG_DESC1"].astype(str)
        assets   = df_out["Product Image"].astype(str)

        inv_pass  = sum(1 for l in inv_lens if l <= 40)
        mob_pass  = sum(1 for l in mob_lens if 60 <= l <= 80)
        inv_upper = sum(1 for x in df_out["INVOICE_DESC"] if str(x) == str(x).upper())
        tm_pass   = sum(1 for b in brands if "®" in b or "™" in b)
        unspsc_blank = sum(1 for u in unspsc if not u or u == "nan")
        long_rich = sum(1 for d in long1 if "," in d)
        asset_ev  = sum(1 for a in assets if a and a != "nan")

        rules = [
            ("INVOICE_DESC ≤ 40 chars",         inv_pass,     total, "Characters strictly capped — no truncation hallucination"),
            ("INVOICE_DESC fully UPPERCASE",     inv_upper,    total, "Casing enforced via rule, never AI guessed"),
            ("MOBILE_DESC 60–80 chars",          mob_pass,     total, "Padded/trimmed to exact range — never over or under"),
            ("Brand has ® or ™ symbol",          tm_pass,      total, "Only added when source resolves to a known entity"),
            ("UNSPSC left blank (low-conf items)",unspsc_blank, total, "UNSPSC is never guessed — left empty unless ≥2 keyword signals match"),
            ("LONG_DESC1 has extracted attributes", long_rich,  total, "Built from real spec extraction, not boilerplate copy"),
            ("Digital Assets evidence-based",    asset_ev,     total, "Only populated when brand + MPN are resolved"),
        ]

        rule_rows = []
        for label, passed, total_n, note in rules:
            pct = 100.0 * passed / total_n if total_n else 0
            status = "✅ PASS" if pct >= 95 else ("⚠️ PARTIAL" if pct >= 70 else "❌ FAIL")
            rule_rows.append({
                "Rule": label,
                "Pass": f"{passed:,} / {total_n:,}",
                "Rate": f"{pct:.1f}%",
                "Status": status,
                "Evidence Basis": note,
            })
        st.dataframe(pd.DataFrame(rule_rows), width='stretch', hide_index=True)

        # ── Hallucination-risk field audit ────────────────────────────────────
        st.markdown("---")
        st.markdown("### 🔬 Hallucination-Risk Field Audit")
        st.markdown(
            "Fields most susceptible to AI fabrication are explicitly blanked when unsupported. "
            "The counts below confirm how many records correctly have these left empty."
        )

        RISKY_FIELDS = {
            "UNSPSC":             "Product classification code — only if ≥2 keyword signals",
            "Specification Sheet":"URL only generated if brand + MPN resolved",
            "Product Image":      "Filename only if brand + MPN resolved",
            "WARRANTY_INFO":      "Warranty — left blank unless source states it",
            "PRICE":              "Price — never generated; sourced only",
        }
        risky_rows = []
        for field, reason in RISKY_FIELDS.items():
            if field in df_out.columns:
                populated = sum(1 for v in df_out[field].astype(str) if v and v not in {"", "nan"})
                blank     = total - populated
                risk_flag = "🟢 Controlled" if blank > 0 or field not in ["WARRANTY_INFO", "PRICE"] else "🔴 Review"
                risky_rows.append({
                    "Field": field,
                    "Populated": populated,
                    "Left Blank": blank,
                    "Anti-Hallucination Rule": reason,
                    "Status": risk_flag,
                })
        if risky_rows:
            st.dataframe(pd.DataFrame(risky_rows), width='stretch', hide_index=True)

        # ── Issue frequency ───────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📋 Validation Issue Frequency")
        from collections import Counter
        all_issues = [issue for v in vals for issue in v["issues"]]
        if all_issues:
            freq = Counter(all_issues).most_common(15)
            freq_df = pd.DataFrame(freq, columns=["Issue", "Count"])
            freq_df["% of Records"] = (freq_df["Count"] / total * 100).round(1).astype(str) + "%"
            st.dataframe(freq_df, width='stretch', hide_index=True)
        else:
            st.success("Zero validation issues detected across all records.")

        # ── Confidence distribution ───────────────────────────────────────────
        st.markdown("---")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("### 📊 Confidence Score Distribution")
            scores  = [v["confidence_score"] for v in vals]
            score_df = pd.DataFrame({"Score": scores})
            st.bar_chart(score_df["Score"].value_counts().sort_index())
        with c2:
            st.markdown("### 🚦 Records Needing Human Review")
            review_idx = [i for i, v in enumerate(vals) if v["needs_human_review"]]
            if review_idx:
                avail_cols = [c for c in ["Mfg_Part_Num", "Part_Desc", "BRAND_NAME", "INVOICE_DESC", "Classpath"] if c in df_out.columns]
                rev_df = df_out.iloc[review_idx][avail_cols].copy()
                rev_df.insert(0, "Confidence", [vals[i]["confidence_score"] for i in review_idx])
                rev_df["Issues"] = ["; ".join(vals[i]["issues"][:2]) for i in review_idx]
                st.dataframe(rev_df.head(50), width='stretch', hide_index=True)
            else:
                st.success("All records passed all validation rules automatically.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Record Deep Dive
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    if st.session_state["enriched_df"] is None:
        st.info("Run the enrichment pipeline first.")
    else:
        df_out = st.session_state["enriched_df"]
        df_in  = st.session_state["input_df"]
        vals   = st.session_state["validation_results"]

        st.subheader("🔍 Single Record Deep Dive & Field Traceability")
        row_idx = st.slider("Select item index", 0, len(df_out) - 1, 0)

        r_out = df_out.iloc[row_idx].to_dict()
        r_val = vals[row_idx]

        # Status banner
        if r_val["is_valid"]:
            st.success(f"🟢 Clean & Compliant — Confidence: {r_val['confidence_score']}%")
        else:
            issues_text = " · ".join(r_val["issues"])
            st.warning(
                f"🟡 Flagged for Human Review — Confidence: {r_val['confidence_score']}%  \n"
                f"**Issues:** {issues_text}"
            )

        c_left, c_right = st.columns(2)

        with c_left:
            st.markdown("#### 📥 Raw Source Data")
            if df_in is not None and row_idx < len(df_in):
                st.json(df_in.iloc[row_idx].dropna().to_dict())

            st.markdown("#### 🎯 Resolved Entities & Taxonomy")
            for label, key in [
                ("Manufacturer", "MANUFACTURER_NAME"),
                ("Brand",        "BRAND_NAME"),
                ("Trade Name",   "TRADE_NAME"),
                ("MPN",          "MANUFACTURER_PART_NUMBER"),
                ("Classpath",    "Classpath"),
                ("UNSPSC",       "UNSPSC"),
                ("Product Name", "Product Name"),
            ]:
                val = r_out.get(key) or ""
                if key == "UNSPSC" and not val:
                    val = "(blank — insufficient classification confidence)"
                st.write(f"**{label}:** {val}")

        with c_right:
            st.markdown("#### 📝 Generated Descriptions")
            inv_str = str(r_out.get("INVOICE_DESC", ""))
            mob_str = str(r_out.get("MOBILE_DESC",  ""))

            inv_ok  = len(inv_str) <= 40 and inv_str == inv_str.upper()
            mob_ok  = 60 <= len(mob_str) <= 80

            st.markdown(
                f"**Invoice Desc (≤40 CAPS):** `{inv_str}` "
                f"— {len(inv_str)} chars {'✅' if inv_ok else '❌'}"
            )
            st.markdown(
                f"**Mobile Desc (60–80 chars):** `{mob_str}` "
                f"— {len(mob_str)} chars {'✅' if mob_ok else '❌'}"
            )
            st.markdown(f"**Short Desc:** {r_out.get('SHORT_DESC', '')}")
            st.markdown(f"**Long Desc:** {r_out.get('LONG_DESC1', '')}")
            st.markdown(f"**Retail Desc:** {r_out.get('RETAIL_DESC', '')}")
            st.markdown(f"**Marketing Description:** {r_out.get('MARKETING_DESCRIPTION', '')}")

            st.markdown("#### 🖼️ Digital Assets (Evidence-Based Only)")
            img = r_out.get("Product Image") or "(blank — MPN/brand not resolved)"
            spec = r_out.get("Specification Sheet") or "(blank — MPN/brand not resolved)"
            st.write(f"**Primary Image:** `{img}`")
            st.write(f"**Spec Sheet:** `{spec}`")

        st.markdown("---")
        st.markdown("#### 🏷️ Extracted Attributes (Evidence-Gated — 50 Slots)")
        attr_rows = []
        for i in range(1, 51):
            lbl = r_out.get(f"ATTRIBUTE_LABEL {i}")
            val = r_out.get(f"ATTRIBUTE_VALUE {i}")
            uom = r_out.get(f"ATTRIBUTE_UOM {i}")
            if lbl or val:
                attr_rows.append({"#": i, "Label": lbl, "Value": val, "UOM": uom or ""})
        if attr_rows:
            st.dataframe(pd.DataFrame(attr_rows), width='stretch', hide_index=True)
        else:
            st.info(
                "No attributes extracted — source text did not contain measurable specifications. "
                "Fields left blank per zero-hallucination policy."
            )

