import pandas as pd
import joblib
import spacy
import re
from algorithms.ranking_engine import RankingEngine
from algorithms.skill_extractor import extract_skills_from_resume
from algorithms.job_matcher import JobRecommender


# --- CONFIGURATION ---
DATA_PATH = 'data/master_job_pool.csv'
TRAINING_DATA_PATH = 'hire_sense_AI/data/cleaned_training_data.csv'
MODEL_PATH = 'models/resume_classifier.pkl'
VECTORIZER_PATH = 'models/tfidf_vectorizer.pkl'
NER_MODEL_PATH = 'models/ner_model'

def run_pipeline(resume_text):
    print("\n" + "="*30)
    print("🚀 STARTING RECOMMENDATION ENGINE")
    print("="*30)

    try:
        # 1. Load Assets
        print("📦 Loading models and datasets...")
        classifier = joblib.load(MODEL_PATH)
        tfidf_vec = joblib.load(VECTORIZER_PATH)
        # Assuming you've saved the LabelEncoder too
        label_enc = joblib.load('models/label_encoder.pkl') 
        
        # Load the custom NER model we built
        nlp_ner = spacy.load(NER_MODEL_PATH)
        
        # Initialize the Matcher with the Job Pool
        matcher = JobRecommender(DATA_PATH)

        # 2. Step 1: Classification (Identify the Field)
        print("🔍 Analyzing professional category...")
        # Simple cleaning for classification
        cleaned_text = resume_text.lower()
        features = tfidf_vec.transform([cleaned_text])
        category_id = classifier.predict(features)[0]
        category_name = label_enc.inverse_transform([category_id])[0]
        print(f"✅ Detected Category: {category_name}")

        # 3. Step 2: NER Skill Extraction
        print("✂️ Extracting specific technical skills...")
        extracted_skills = extract_skills_from_resume(resume_text, nlp_ner)
        print(f"✅ Skills Found: {', '.join(extracted_skills) if extracted_skills else 'None detected'}")

        # 4. Step 3: Matching & Ranking
        print("🎯 Finding best job matches...")
        recommendations = matcher.get_recommendations(resume_text, top_n=5)

        # 5. Output Results
        print("\n" + "-"*30)
        print(f"TOP 5 RECOMMENDATIONS FOR {category_name.upper()}")
        print("-"*30)
        print(recommendations[['job_title', 'company', 'match_score']].to_string(index=False))
        # Inside run_pipeline function:

        # ... (Previous Classification and NER steps) ...

        # 1. Get initial 10 matches based on skills
        initial_matches = matcher.get_recommendations(resume_text, top_n=10)

        # 2. Pass through Ranking Engine for precision
        # Assume we extracted '3' as user_exp via NER or manual input
        ranker = RankingEngine()
        final_ranked_jobs = ranker.rank_jobs(
            initial_matches, 
            user_category=category_name, 
            user_exp=3 
        )
        final_ranked_jobs = final_ranked_jobs.drop_duplicates(subset=["job_title", "company"])

        print(final_ranked_jobs[['job_title', 'company', 'final_rank_score']].head(5))
        return {
            "category": category_name,
            "skills": extracted_skills,
            "jobs": final_ranked_jobs.to_dict("records")
}
    except Exception as e:
        print(f"❌ Pipeline Error: {e}")
        return None

if __name__ == "__main__":
    # Example raw resume input (This would come from a PDF parser or UI in the future)
    sample_resume = """
    Experienced Java Developer with a strong background in Spring Boot, 
    Hibernate, and MySQL. Proficient in building RESTful APIs and 
    microservices architecture. Familiar with AWS and Docker.
    """
    
    run_pipeline(sample_resume)
    # main.py snippet

