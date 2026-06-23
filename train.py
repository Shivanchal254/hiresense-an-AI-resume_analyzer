import pandas as pd
import joblib
import os
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelEncoder
from spacy.lang.en import English

# 1. Create directory structure if it doesn't exist
if not os.path.exists('models'):
    os.makedirs('models')

def train_and_save():
    print("Reading training data...")
    df = pd.read_csv('data\cleaned_training_data.csv')
    
    # 2. Train Classifier
    print("Training Category Classifier...")
    le = LabelEncoder()
    df['Category_Encoded'] = le.fit_transform(df['Category'])
    
    tfidf = TfidfVectorizer(stop_words='english', max_features=3000)
    X = tfidf.fit_transform(df['cleaned_resume'])
    y = df['Category_Encoded']
    
    clf = OneVsRestClassifier(KNeighborsClassifier())
    clf.fit(X, y)
    
    # Save Classifier Assets
    joblib.dump(clf, 'models/resume_classifier.pkl')
    joblib.dump(tfidf, 'models/tfidf_vectorizer.pkl')
    joblib.dump(le, 'models/label_encoder.pkl')
    print("✅ Classifier and Vectorizer saved.")

    # 3. Create and Save NER Model (Skill Extractor)
    print("Building NER Skill Extractor...")
    jobs_df = pd.read_csv('data\master_job_pool.csv')
    all_skills = jobs_df['skills'].str.split(',').explode().str.strip().unique()
    all_skills = [s.lower() for s in all_skills if isinstance(s, str) and len(s) > 1]
    
    nlp = English()
    ruler = nlp.add_pipe("entity_ruler")
    patterns = [{"label": "SKILL", "pattern": [{"LOWER": s}]} for s in all_skills]
    ruler.add_patterns(patterns)
    
    # Save the SpaCy model folder
    nlp.to_disk("models/ner_model")
    print("✅ NER Model saved to models/ner_model")

if __name__ == "__main__":
    train_and_save()