from typing import Dict, Tuple

# Multi-industry hierarchical taxonomy knowledge base:
# (Keywords, (Dept, Class, Fine, Classpath, UNSPSC, Product_Name))
TAXONOMY_RULES = [
    # Appliances
    (
        ["dishwasher", "dish washer", "built-in dishwasher"],
        ("Appliances", "Large Appliances", "Dishwashers",
         "Appliances & Consumer Electronics>Kitchen Appliances>Built-In Dishwashers",
         "47121600", "Dishwasher")
    ),
    (
        ["refrigerator", "fridge", "freezer"],
        ("Appliances", "Large Appliances", "Refrigerators",
         "Appliances & Consumer Electronics>Kitchen Appliances>Refrigerators",
         "52141501", "Refrigerator")
    ),
    (
        ["range", "cooktop", "oven", "microwave"],
        ("Appliances", "Large Appliances", "Cooking Appliances",
         "Appliances & Consumer Electronics>Kitchen Appliances>Ovens & Ranges",
         "52141510", "Range")
    ),
    # Abrasives & Belts
    (
        ["sanding belt", "abrasive belt", "sand belt"],
        ("Tools & Equipment", "Power Tool Accessories", "Abrasives",
         "Abrasives & Polishing>Abrasive Belts>Sanding Belts",
         "31191500", "Sanding Belt")
    ),
    (
        ["stikit", "cubitron", "sanding disc", "film disc", "abranet", "hiolit", "hookit", "disc/box", "sanding pad"],
        ("Tools & Equipment", "Power Tool Accessories", "Abrasives",
         "Abrasives & Polishing>Abrasive Discs & Belts>Sanding Discs",
         "31191500", "Sanding Disc")
    ),
    (
        ["cut-off disc", "metal cut-off", "steel demon", "speed demon", "cut-off wheel", "grinding disc"],
        ("Tools & Equipment", "Power Tool Accessories", "Saw Blades",
         "Tools & Equipment>Power Tool Accessories>Blades>Cut-Off Wheels",
         "27112800", "Cut-Off Disc")
    ),
    (
        ["saw blade", "circular blade", "dado", "planer blade", "miter blade"],
        ("Tools & Equipment", "Power Tool Accessories", "Saw Blades",
         "Tools & Equipment>Power Tool Accessories>Blades>Saw Blades",
         "27112802", "Saw Blade")
    ),
    (
        ["countersink", "drill bit", "drill stop", "step drill", "carbide bit"],
        ("Tools & Equipment", "Power Tool Accessories", "Drill Bits",
         "Tools & Equipment>Power Tool Accessories>Drill Bits>Countersinks",
         "27112801", "Countersink Drill Bit")
    ),
    # Power Tools
    (
        ["grease gun", "cordless grease gun"],
        ("Tools & Equipment", "Power Tools", "Cordless Tools",
         "Tools & Equipment>Power Tools>Cordless Tools>Grease Guns",
         "27112700", "Grease Gun")
    ),
    (
        ["impact driver", "drill driver", "cordless drill", "impact wrench"],
        ("Tools & Equipment", "Power Tools", "Cordless Tools",
         "Tools & Equipment>Power Tools>Cordless Tools>Drills & Drivers",
         "27112703", "Cordless Drill")
    ),
    # Lighting & Electrical
    (
        ["down light", "recessed downlight", "recessed light", "downlight"],
        ("Lighting & Electrical", "Lighting Fixtures", "Recessed Downlights",
         "Lighting & Electrical>Lighting Fixtures>Recessed Downlights",
         "39111500", "Recessed Downlight")
    ),
    (
        ["motion lt", "motion light", "security light", "flood light"],
        ("Lighting & Electrical", "Lighting Fixtures", "Outdoor Lighting",
         "Lighting & Electrical>Lighting Fixtures>Motion Sensor Lights",
         "39111600", "Motion Sensor Light")
    ),
    (
        ["flash light", "flashlt", "flashlight", "slyde king"],
        ("Lighting & Electrical", "Lighting Fixtures", "Flashlights",
         "Lighting & Electrical>Lighting Fixtures>Flashlights & Portable Lights",
         "39111610", "Flashlight")
    ),
    (
        ["led bulb", "led lamp", "a19", "par38", "br30", "bulb", "lamp"],
        ("Lighting & Electrical", "Lamps & Bulbs", "LED Lamps",
         "Lighting & Electrical>Lamps & Bulbs>LED Bulbs",
         "39101628", "LED Lamp")
    ),
    (
        ["elect tape", "electrical tape", "vinyl tape"],
        ("Hardware & Fasteners", "Adhesives & Tapes", "Electrical Tape",
         "Hardware & Fasteners>Adhesives & Tapes>Electrical Tape",
         "31201502", "Electrical Tape")
    ),
    # Building Materials
    (
        ["drywall", "gypsum", "easi-lite", "firelite", "sheetrock"],
        ("Building Materials", "Drywall & Plaster", "Gypsum Boards",
         "Building Materials>Drywall & Plaster>Gypsum Boards",
         "30103600", "Drywall Board")
    ),
    (
        ["rail kit", "baluster", "deck rail", "handrail", "classic horiz"],
        ("Building Materials", "Decking & Railing", "Railing Kits",
         "Building Materials>Decking & Railing>Railing Kits",
         "30103601", "Railing Kit")
    ),
    (
        ["attic access door", "access door", "access panel"],
        ("Building Materials", "Doors & Windows", "Access Doors",
         "Building Materials>Doors & Windows>Access Doors",
         "30171500", "Access Door")
    ),
    (
        ["lumber", "beam", "engineered wood", "decking", "timber"],
        ("Building Materials", "Lumber & Composites", "Engineered Wood",
         "Building Materials>Lumber & Composites>Engineered Wood",
         "30103600", "Engineered Wood")
    ),
    (
        ["fence", "xtender fence", "featherboard"],
        ("Tools & Equipment", "Woodworking Accessories", "Fences",
         "Tools & Equipment>Woodworking Accessories>Table Fences",
         "27112800", "Extender Fence")
    ),
    (
        ["tire pressure", "inflator gauge", "pressure gauge"],
        ("Tools & Equipment", "Measuring & Layout Tools", "Pressure Gauges",
         "Tools & Equipment>Measuring & Layout Tools>Pressure Gauges",
         "41112400", "Tire Pressure Gauge")
    ),
    # Plumbing
    (
        ["cplg", "coupling", "fitting", "elbow", "tee", "adapter", "valve", "nipple"],
        ("Plumbing & Pumps", "Pipes, Valves & Fittings", "Fittings",
         "Plumbing & Pumps>Pipes, Valves & Fittings>Fittings",
         "40142315", "Pipe Fitting")
    ),
    (
        ["faucet", "sink faucet", "kitchen faucet", "lavatory faucet"],
        ("Plumbing & Pumps", "Faucets & Fixtures", "Sink Faucets",
         "Plumbing & Pumps>Faucets & Fixtures>Sink Faucets",
         "30181702", "Sink Faucet")
    )
]

def _clean_field(val: str) -> bool:
    """Returns True if field has a real, non-placeholder value."""
    return bool(val and str(val).strip() not in {"", "nan", "-", "N/A", "n/a"})


def classify_product(part_desc: str, mpn: str, dept_raw: str = "", class_raw: str = "", fine_raw: str = "") -> Tuple[str, str, str, str, str, str]:
    """
    Classifies a product into Dept, Class, Fine, Classpath, UNSPSC, and Product Name.

    UNSPSC assignment requires ≥2 keyword signals (strict anti-hallucination guard).
    Classpath is always derived dynamically from the resolved dept/class/fine values.
    """
    combined = f"{part_desc} {mpn} {dept_raw} {class_raw} {fine_raw}".lower()

    best_match = None
    best_score = 0

    for keywords, (dept, cls, fine, classpath, unspsc, prod_name) in TAXONOMY_RULES:
        hit_count = sum(1 for kw in keywords if kw in combined)
        if hit_count > best_score:
            best_score = hit_count
            best_match = (dept, cls, fine, classpath, unspsc, prod_name)

    if best_match and best_score >= 1:
        dept, cls, fine, classpath, unspsc, prod_name = best_match
        resolved_dept  = dept_raw  if _clean_field(dept_raw)  else dept
        resolved_cls   = class_raw if _clean_field(class_raw) else cls
        resolved_fine  = fine_raw  if _clean_field(fine_raw)  else fine
        # Dynamic classpath from resolved values
        resolved_path  = f"{resolved_dept}>{resolved_cls}>{resolved_fine}"
        # Only assign UNSPSC when ≥2 keyword hits (high-confidence match)
        resolved_unspsc = unspsc if best_score >= 2 else ""
        return (resolved_dept, resolved_cls, resolved_fine, resolved_path, resolved_unspsc, prod_name)

    # Fallback: derive values from raw input fields if present; leave UNSPSC blank
    resolved_dept  = dept_raw  if _clean_field(dept_raw)  else "Industrial Supplies"
    resolved_cls   = class_raw if _clean_field(class_raw) else "General Maintenance"
    resolved_fine  = fine_raw  if _clean_field(fine_raw)  else "Hardware"
    resolved_path  = f"{resolved_dept}>{resolved_cls}>{resolved_fine}"

    # Build a meaningful fallback product name from the description (skip generic 1-char tokens)
    words = [w for w in part_desc.split() if len(w) > 2] if part_desc else []
    fallback_name = " ".join(words[:3]).title() if words else "Industrial Product"

    return (resolved_dept, resolved_cls, resolved_fine, resolved_path, "", fallback_name)



