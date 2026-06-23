import pdfplumber
from docx import Document
import sys
import os

# Add models and algorithms to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'models'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'algorithms'))

from models.ner_model import build_skill_ner
from algorithms.skill_extractor import extract_skills_from_resume


def extract_text(file_path):
    """
    Extract text from a resume file.
    """
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            return ' '.join([page.extract_text() for page in pdf.pages])
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        return ' '.join([paragraph.text for paragraph in doc.paragraphs])
    else:
        return "Unsupported file format"


def process_resume(file_path, job_pool_path='data/master_job_pool.csv'):
   
    try:
        # Step 1: Extract text from resume (file type checking happens here)
        print("[STEP 1] Extracting text from resume...")
        resume_text = extract_text(file_path)
        
        if not resume_text or resume_text == "Unsupported file format":
            print("[ERROR] Failed to extract text from resume")
            return {"success": False, "error": "Unsupported file format or empty text"}
        
        print(f"[SUCCESS] Extracted {len(resume_text)} characters from resume")
        
        # Step 2: Build/Load NER model for skill recognition
        print("[STEP 2] Building NER model for skill extraction...")
        nlp_model = build_skill_ner(job_pool_path)
        print("[SUCCESS] NER model built successfully")
        
        # Step 3: Extract skills from the resume using the model
        print("[STEP 3] Extracting skills from resume using NER model...")
        skills = extract_skills_from_resume(resume_text, nlp_model)
        print(f"[SUCCESS] Found {len(skills)} unique skills")
        
        return {
            "success": True,
            "file_type": file_path.split('.')[-1].upper(),
            "text_length": len(resume_text),
            "resume_text": resume_text,
            "skills_found": skills,
            "skills_count": len(skills)
        }
    
    except Exception as e:
        print(f"[ERROR] Error processing resume: {str(e)}")
        return {"success": False, "error": str(e)}
