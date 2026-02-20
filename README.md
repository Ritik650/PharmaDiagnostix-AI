# 🧬 PharmaDiagnostix AI

### **Precision Pharmacogenomics & AI Clinical Decision Support**

**PharmaDiagnostix AI** is a clinical-grade decision support tool designed to prevent adverse drug reactions (ADRs) by analyzing a patient's genomic profile. By cross-referencing raw VCF (Variant Call Format) data with CPIC guidelines, the platform provides real-time, personalized medication risk assessments.

---

## 🚀 Key Features

* **Traffic Light Risk System:** Instant visual classification of drug safety (Green: Safe, Yellow: Adjust Dosage, Red: Toxic/Ineffective).
* **Med-Gemma AI Integration:** Generates human-readable clinical narratives explaining the biological mechanism of genetic risks.
* **Hybrid Genomic Engine:** Combines the strict **PharmCAT (Java)** clinical engine with a custom **Python Rescue Parser** for handling sparse hackathon datasets.
* **Enterprise EHR Interface:** A professional clinician portal with patient demographics, history, and genomic telemetry.
* **Automated Clinical Reports:** One-click generation of downloadable `.txt` reports for patient records.

---

## 🛠️ Technology Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Interactive Clinician Dashboard)
* **AI Engine:** Med-Gemma 1.5 clinical logic
* **Bioinformatics:** * **PharmCAT (Java):** Official CPIC guideline engine.
* **Python:** Custom VCF line-by-line parser for diplotype calculation.


* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (High-performance asynchronous API)

---

## ⚙️ Architecture: The Hybrid Rescue Pipeline

To ensure 100% accuracy during live demos, PharmaDiagnostix uses a dual-engine approach:

1. **Primary Engine (PharmCAT):** Executes the official Java-based pipeline to match full-genome data against the PharmGKB database.
2. **Rescue Parser (Python):** If the input VCF is sparse (common in hackathons), our custom Python logic scans for specific `rsID` genotypes and calculates the **Star Allele Diplotype** (e.g., `*1/*2`) manually.


Team Members:-
---
Koustav Karmakar
Manish
Ritik Yadav


## 💻 Local Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ritik650/PharmaDiagnostix-AI.git
cd PharmaDiagnostix-AI

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Run the Application

```bash
streamlit run frontend.py

```

---

## 🧪 Testing with Sample Data

You can test the system using the provided clinical sample files in the `data/uploads/` directory:

* **TC_P1_PATIENT_001_Normal.vcf:** Test with `CLOPIDOGREL` to see a **Safe** result (`*1/*1`).
* **Modified Toxic Sample:** Change the `CYP2C19` genotype to `1/1` to trigger the **Toxic** alert (`*2/*2`).

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Developed with ❤️ in the Rift Hackathon 2026.**
*Prescribe with Precision.*

---

[Deployment Link](https://pharmadiagnostix-ai.streamlit.app/)
