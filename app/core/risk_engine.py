TARGET_MAP = {
    "CODEINE": "CYP2D6",
    "CLOPIDOGREL": "CYP2C19",
    "WARFARIN": "CYP2C9",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}

def calculate_risk(drug: str, phenotype: str) -> dict:
    """Translates PharmCAT phenotypes into Hackathon severity scores."""
    drug = drug.upper()
    phenotype_lower = phenotype.lower()

    # Safety-First check for invalid/missing data
    if "indeterminate" in phenotype_lower:
        return {"label": "Unknown", "severity": "moderate"}

    # Default safe baseline for Normal Metabolizers
    risk_data = {"label": "Safe", "severity": "none"}

    if "poor" in phenotype_lower or "decreased" in phenotype_lower:
        risk_data = {"label": "Toxic/Ineffective", "severity": "high"}
    elif "intermediate" in phenotype_lower:
        risk_data = {"label": "Adjust Dosage", "severity": "moderate"}
    elif "ultra-rapid" in phenotype_lower and drug == "CODEINE":
        risk_data = {"label": "Toxic", "severity": "critical"}

    return risk_data