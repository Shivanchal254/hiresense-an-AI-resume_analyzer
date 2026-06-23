
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_resume_text(text):
    """Simple cleaner for input resumes"""
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s,]', '', text) 
    return text

class JobRecommender:
    def __init__(self, job_df):
        # FIX: Check if we were passed a path or a DataFrame
        if isinstance(job_df, str):
            self.df = pd.read_csv(job_df)
        else:
            self.df = job_df
            
        self.vectorizer = TfidfVectorizer(stop_words='english')
        # Ensure 'skills' column exists and has no NaN values
        self.df['skills'] = self.df['skills'].fillna('')
        self.job_vectors = self.vectorizer.fit_transform(self.df['skills'])

    def get_recommendations(self, user_resume, top_n=5):
        # 1. Vectorize the input
        cleaned_resume = clean_resume_text(user_resume)
        resume_vector = self.vectorizer.transform([cleaned_resume])
        
        # 2. Mathematical Comparison
        similarity_scores = cosine_similarity(resume_vector, self.job_vectors).flatten()
        
        # 3. Sorting and Ranking
        top_indices = similarity_scores.argsort()[-top_n:][::-1]
        
        # 4. Preparing Results
        recommendations = self.df.iloc[top_indices].copy()
        recommendations['match_score'] = (similarity_scores[top_indices] * 100).round(2)
        
        return recommendations[['job_title', 'company', 'skills', 'years_exp_num', 'match_score']]