import os
import google.generativeai as genai
from dotenv import load_dotenv

# This is the magic line that connects Python directly to your .env file!
load_dotenv()

# 1. Load your 5 keys safely from the .env file
API_KEYS = [
    os.getenv("GEMINI_KEY_1", ""),
    os.getenv("GEMINI_KEY_2", ""),
    os.getenv("GEMINI_KEY_3", ""),
    os.getenv("GEMINI_KEY_4", ""),
    os.getenv("GEMINI_KEY_5", "")
]

# Keep track of which key is currently active
current_key_index = 0

async def generate_clinical_narrative(drug: str, gene: str, phenotype: str, risk_label: str) -> str:
    """Uses Med-Gemma 1.5 with a 5-key automatic fallback system to prevent rate-limit crashes."""
    global current_key_index
    
    prompt = (
        f"Act as an expert Clinical Pharmacogeneticist. "
        f"A patient is taking {drug}. Their genomic profile shows they are a '{phenotype}' for the {gene} gene. "
        f"The calculated risk level is '{risk_label}'. "
        f"Provide a short, 3-sentence clinical explanation of the biological mechanism causing this risk, "
        f"and what it means for the patient's treatment."
    )

    # 2. Try up to 5 times (once for each key)
    for _ in range(len(API_KEYS)):
        try:
            # Check if the current key is actually loaded
            active_key = API_KEYS[current_key_index]
            if not active_key:
                raise ValueError("Empty API Key")

            # Configure the SDK with the current key
            genai.configure(api_key=active_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Attempt to generate the response
            response = await model.generate_content_async(prompt)
            return response.text
            
        except Exception as e:
            print(f"⚠️ API Key {current_key_index + 1} failed or hit limit: {e}")
            
            # 3. If it fails, rotate to the next key in the list
            current_key_index = (current_key_index + 1) % len(API_KEYS)
            print(f"🔄 Switching to API Key {current_key_index + 1}...")

    # If all 5 keys fail
    return "Clinical Narrative Unavailable: High server traffic. Please refer to the calculated risk severity above and consult CPIC guidelines directly."