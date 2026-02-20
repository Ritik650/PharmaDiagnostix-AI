import os
from google import genai
from dotenv import load_dotenv

# Connect to .env
load_dotenv()

# Get the single API key
API_KEY = os.getenv("GEMINI_API_KEY", "PASTE_YOUR_API_KEY_HERE")

# Initialize the NEW SDK client (Synchronous)
client = genai.Client(api_key=API_KEY)

def generate_clinical_narrative(drug: str, gene: str, phenotype: str, risk_label: str) -> str:
    """Uses the new google-genai SDK for stable Streamlit deployment."""
    
    prompt = (
        f"Act as an expert Clinical Pharmacogeneticist. "
        f"A patient is taking {drug}. Their genomic profile shows they are a '{phenotype}' for the {gene} gene. "
        f"The calculated risk level is '{risk_label}'. "
        f"Provide a short, 3-sentence clinical explanation of the biological mechanism causing this risk, "
        f"and what it means for the patient's treatment."
    )

    try:
        # Standard synchronous call - prevents the cloud threading crash
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
            
    except Exception as e:
        print(f"⚠️ AI Generation Error: {e}")
        return "Clinical Narrative Unavailable: Please refer to the calculated risk severity above."
