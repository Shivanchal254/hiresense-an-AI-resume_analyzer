import spacy

def extract_skills_from_resume(resume_text, nlp_model):
    """
    Uses the NER model to surgically pull out skills from a messy resume.
    """
    doc = nlp_model(resume_text)
    
    # Use a set to avoid duplicates (e.g., if 'Python' appears twice)
    extracted_skills = set()
    
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            extracted_skills.add(ent.text.lower())
            
    return list(extracted_skills)

# --- TEST ---
# test_resume = "Expert in Python and SQL. Familiar with PyTorch and Machine Learning."
# found = extract_skills_from_resume(test_resume, nlp_skill_extractor)
# print(f"Skills Found: {found}") 
# Output: ['python', 'sql', 'pytorch']