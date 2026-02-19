# PharmaDiagnostix-AI Main Application

import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.models.schema import PharmaResponse, RiskAssessment
from app.core.risk_engine import TARGET_MAP, calculate_risk
from app.core.bio_gateway import run_pharmcat_pipeline, extract_gene_phenotype
from app.core.ai_agent import generate_clinical_narrative
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="PharmaDiagnostix AI Backend")

@app.post("/analyze", response_model=PharmaResponse)
async def analyze_vcf(
    patient_id: str = Form(...),
    drug: str = Form(...),
    vcf_file: UploadFile = File(...)
):
    drug = drug.upper()
    if drug not in TARGET_MAP:
        raise HTTPException(status_code=400, detail=f"Drug {drug} not supported. Use one of {list(TARGET_MAP.keys())}")

    target_gene = TARGET_MAP[drug]
    
    # 1. Save uploaded VCF temporarily
    temp_vcf_path = f"data/uploads/{vcf_file.filename}"
    os.makedirs("data/uploads", exist_ok=True)
    with open(temp_vcf_path, "wb") as f:
        f.write(await vcf_file.read())

    # 2. Run Bio-Engine (PharmCAT)
    report_path = run_pharmcat_pipeline(temp_vcf_path)
    phenotype = extract_gene_phenotype(report_path, target_gene)

    # 3. Apply Original Risk Logic
    risk_data = calculate_risk(drug, phenotype)

    # 4. Generate AI Explanation
    explanation = await generate_clinical_narrative(drug, target_gene, phenotype, risk_data["label"])

    # Cleanup temporary VCF
    if os.path.exists(temp_vcf_path):
        os.remove(temp_vcf_path)

    # 5. Return Hackathon JSON Schema
    return PharmaResponse(
        patient_id=patient_id,
        drug=drug,
        gene=target_gene,
        phenotype=phenotype,
        risk_assessment=RiskAssessment(
            risk_label=risk_data["label"],
            confidence_score=0.99,
            severity=risk_data["severity"]
        ),
        explanation=explanation
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)