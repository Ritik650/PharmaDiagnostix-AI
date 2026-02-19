import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the .env file
load_dotenv()

# 2. Get the single API key
# Emergency Hackathon Tip: If the .env file is being stubborn, 
# just replace the os.getenv(...) line with your actual key in quotes like:
# API_KEY = "AIzaSyYourRealKeyHere..."
API_KEY = os.getenv("GEMINI_API_KEY", "PASTE_YOUR_API_KEY_HERE")

# Configure the SDK once
genai.configure(api_key=API_KEY)

async def generate_clinical_narrative(drug: str, gene: str, phenotype: str, risk_label: str) -> str:
    """Uses Med-Gemma 1.5 to generate the clinical explanation using a single key."""
    
    prompt = (
        f"Act as an expert Clinical Pharmacogeneticist. "
        f"A patient is taking {drug}. Their genomic profile shows they are a '{phenotype}' for the {gene} gene. "
        f"The calculated risk level is '{risk_label}'. "
        f"Provide a short, 3-sentence clinical explanation of the biological mechanism causing this risk, "
        f"and what it means for the patient's treatment."
    )

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = await model.generate_content_async(prompt)
        return response.text
            
    except Exception as e:
        print(f"⚠️ AI Generation Error: {e}")
        return "Clinical Narrative Unavailable: Please refer to the calculated risk severity above and consult CPIC guidelines directly."
