import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Streamlit Cloud Secret or local .env
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def generate_clinical_narrative(drug: str, gene: str, phenotype: str, risk_label: str) -> str:
    """Uses the new SDK without async to prevent cloud crashes."""
    prompt = (
        f"Act as an expert Clinical Pharmacogeneticist. "
        f"A patient is taking {drug}. Their genomic profile shows they are a '{phenotype}' for the {gene} gene. "
        f"The calculated risk level is '{risk_label}'. "
        f"Provide a short, 3-sentence clinical explanation of the biological mechanism causing this risk, "
        f"and what it means for the patient's treatment."
    )
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Clinical Narrative Unavailable: {str(e)}"
