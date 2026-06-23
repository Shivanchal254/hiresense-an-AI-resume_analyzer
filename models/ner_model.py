import spacy
from spacy.lang.en import English
import pandas as pd

def build_skill_ner(job_pool_path):
    # 1. Load your master jobs to get the "Source of Truth" for skills
    df = pd.read_csv(job_pool_path)
    
    # 2. Extract and clean the unique skills list
    all_skills = df['skills'].str.split(',').explode().str.strip().unique()
    all_skills = [s.lower() for s in all_skills if isinstance(s, str) and len(s) > 1]
    
    # 3. Initialize a Blank English model
    nlp = English()
    
    # 4. Create an EntityRuler (The Rule-Based Engine)
    ruler = nlp.add_pipe("entity_ruler")
    
    # 5. Create patterns for every skill in your database
    patterns = []
    for skill in all_skills:
        patterns.append({"label": "SKILL", "pattern": [{"LOWER": skill}]})
    
    ruler.add_patterns(patterns)
    
    # 6. Save the model to your project folder
    # nlp.to_disk("models/ner_model/skill_recognizer")
    return nlp

# Usage:
# nlp_skill_extractor = build_skill_ner('data/master_job_pool.csv')