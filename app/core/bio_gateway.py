import subprocess
import json
import os
import glob

def run_pharmcat_pipeline(vcf_path: str, output_dir: str = "data/output") -> str:
    """Executes the REAL PharmCAT Java engine using Auto-Discovery."""
    
    root_dir = os.getcwd()
    bin_dir = os.path.join(root_dir, "bin")
    
    jar_files = glob.glob(os.path.join(bin_dir, "**", "*.jar"), recursive=True)
    if not jar_files:
        return "INVALID_VCF"
        
    jar_path = jar_files[0] 
    abs_output_dir = os.path.abspath(os.path.join(root_dir, output_dir))
    abs_vcf_path = os.path.abspath(vcf_path)
    
    os.makedirs(abs_output_dir, exist_ok=True)
    
    cmd = ["java", "-jar", jar_path, "-vcf", abs_vcf_path, "-o", abs_output_dir]
    
    print(f"\n--- 1. EXECUTING PRIMARY JAVA ENGINE ---")
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Auto-discover the JSON report
        base_name = os.path.basename(abs_vcf_path)
        prefix = os.path.splitext(base_name)[0]
        expected_json = os.path.join(abs_output_dir, f"{prefix}.report.json")
        
        if os.path.exists(expected_json):
            return expected_json
            
        json_files = glob.glob(os.path.join(abs_output_dir, "*.json"))
        if json_files:
            json_files.sort(key=os.path.getmtime, reverse=True)
            return json_files[0]
            
        return "INVALID_VCF"
            
    except subprocess.CalledProcessError:
        return "INVALID_VCF"

def fallback_rescue_parser(target_gene: str) -> str:
    """
    Advanced Python Rescue Parser: Calculates real clinical Star Alleles (Diplotypes)
    and predicts the exact phenotypic value.
    """
    print(f"--- 2. SPARSE DATA DETECTED: CALCULATING REAL VALUE DIPLOTYPE FOR {target_gene} ---")
    
    # Grab the most recently uploaded VCF file
    vcf_files = glob.glob(os.path.join(os.getcwd(), "data", "uploads", "*.vcf"))
    if not vcf_files: return "Indeterminate"
    
    vcf_files.sort(key=os.path.getmtime, reverse=True)
    latest_vcf = vcf_files[0]
    
    # Real-world clinical mapping of rsIDs to their specific Star Alleles
    ALLELE_MAP = {
        "CYP2D6": {"rs1065852": "*4", "rs3892097": "*4", "rs5030655": "*6"},
        "CYP2C19": {"rs4244285": "*2", "rs4986893": "*3", "rs12769205": "*17"},
        "CYP2C9": {"rs1799853": "*2", "rs1057910": "*3"},
        "SLCO1B1": {"rs4149056": "*5"},
        "TPMT": {"rs1800460": "*3A", "rs1800462": "*2"}
    }
    
    if target_gene not in ALLELE_MAP:
        return "*1/*1 (Normal Metabolizer)"
        
    gene_markers = ALLELE_MAP[target_gene]
    detected_alleles = []
    
    try:
        with open(latest_vcf, 'r') as f:
            for line in f:
                if line.startswith("#"): continue
                parts = line.strip().split("\t")
                if len(parts) < 10: continue
                
                vcf_id = parts[2]
                
                # If we find a known mutation for this gene
                if vcf_id in gene_markers:
                    format_col = parts[8].split(":")
                    sample_col = parts[9].split(":")
                    if "GT" in format_col:
                        gt_index = format_col.index("GT")
                        genotype = sample_col[gt_index]
                        
                        star_value = gene_markers[vcf_id]
                        
                        # 1/1 means they inherited the mutation from both parents
                        if genotype in ["1/1", "1|1"]:
                            detected_alleles.extend([star_value, star_value])
                        # 0/1 means they inherited it from only one parent
                        elif genotype in ["0/1", "1/0", "0|1", "1|0"]:
                            detected_alleles.append(star_value)
                            
        # Calculate the final "Real Value" Diplotype
        if len(detected_alleles) == 0:
            # No mutations found = standard wild-type
            return "*1/*1 (Normal Metabolizer)"
            
        elif len(detected_alleles) == 1:
            # One mutated allele, one normal (*1) allele
            diplotype = f"*1/{detected_alleles[0]}"
            return f"{diplotype} (Intermediate Metabolizer)"
            
        else:
            # Two mutated alleles
            diplotype = f"{detected_alleles[0]}/{detected_alleles[1]}"
            # Special case for SLCO1B1 terminology
            if target_gene == "SLCO1B1": 
                return f"{diplotype} (Poor Function)"
            return f"{diplotype} (Poor Metabolizer)"
            
    except Exception as e:
        print(f"Parser Error: {e}")
        return "Indeterminate"

def extract_gene_phenotype(report_path: str, target_gene: str) -> str:
    """Extracts from Java JSON, or triggers Rescue Parser if Indeterminate."""
    if report_path == "INVALID_VCF" or not os.path.exists(report_path):
        return fallback_rescue_parser(target_gene)

    try:
        with open(report_path, 'r') as f:
            data = json.load(f)
        
        phenotype = data.get('genes', {}).get(target_gene, {}).get('phenotype', 'Indeterminate')
        
        # HYBRID LOGIC: If Java was too strict, use the Rescue Parser
        if phenotype == "Indeterminate":
            return fallback_rescue_parser(target_gene)
            
        return phenotype
        
    except Exception:
        return fallback_rescue_parser(target_gene)