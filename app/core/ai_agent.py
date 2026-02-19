# AI Agent Module
# Med-Gemma 1.5 RAG implementation
import os
import google.generativeai as genai

# Load API key from environment
genai.configure(api_key="AIzaSyBtCua5J9WBU-fRJpg7rzMAoMdG0LXry-8")

async def generate_clinical_narrative(drug: str, gene: str, phenotype: str, risk_label: str) -> str:
    """Uses Med-Gemma 1.5 to explain the biological mechanism."""
    model = genai.GenerativeModel('gemini-2.5-flash')
 # Replace with specific Med-Gemma endpoint if available in your API tier
    
    prompt = (
        f"Act as an expert Clinical Pharmacogeneticist. "
        f"A patient is taking {drug}. Their genomic profile shows they are a '{phenotype}' for the {gene} gene. "
        f"The calculated risk level is '{risk_label}'. "
        f"Provide a short, 3-sentence clinical explanation of the biological mechanism causing this risk, "
        f"and what it means for the patient's treatment."
    )
    
    response = await model.generate_content_async(prompt)
    return response.text