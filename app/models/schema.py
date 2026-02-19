# Pydantic Schemas
# Output models (PharmaResponse, RiskAssessment)
from pydantic import BaseModel

class RiskAssessment(BaseModel):
    risk_label: str       # Safe, Adjust Dosage, Toxic, Ineffective
    confidence_score: float
    severity: str         # none, low, moderate, high, critical

class PharmaResponse(BaseModel):
    patient_id: str
    drug: str
    gene: str
    phenotype: str
    risk_assessment: RiskAssessment
    explanation: str