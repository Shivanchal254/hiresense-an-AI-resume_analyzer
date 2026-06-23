# 🎯 HireSense Project - Complete Theory & Architecture Documentation

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack & Libraries](#technology-stack--libraries)
4. [Project Structure & Modules](#project-structure--modules)
5. [Data Flow & Processing Pipeline](#data-flow--processing-pipeline)
6. [Detailed Module Explanations](#detailed-module-explanations)
7. [How Everything Works Together](#how-everything-works-together)

---

## 🌟 Project Overview

**HireSense** is an AI-powered resume analysis and job recommendation system that:
- Takes a user's resume (PDF, DOCX, or TXT format)
- Extracts text and analyzes it using NLP (Natural Language Processing)
- Identifies skills, experience level, and professional category
- Matches the resume against a job pool database
- Recommends the top job positions that best fit the user's profile

**Key Goals:**
- Automate the job matching process
- Extract meaningful skills from resumes
- Classify resumes into professional categories
- Rank job recommendations based on multiple criteria (skills match, experience level, category)

---

## 🏗️ System Architecture

### High-Level Architecture Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE (Web Frontend)            │
│  (HTML Templates: upload_resume.html, results.html)          │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP Request (POST /upload)
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              FLASK WEB SERVER (app.py, main.py)              │
│  Route Handlers & Request Processing                         │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│File Extract  │ │  NER Model   │ │Job Matching  │
│(connectivity)│ │(ner_model.py)│ │(job_matcher) │
└──────────────┘ └──────────────┘ └──────────────┘
        │            │            │
        └────────────┼────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              ALGORITHMS & PROCESSING LAYER                   │
│  • skill_extractor.py → Extract skills from text            │
│  • ranking_engine.py → Rank job matches                     │
│  • job_matcher.py → Find best job matches                   │
└─────────────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              DATA LAYER                                      │
│  • master_job_pool.csv → Job database                       │
│  • cleaned_training_data.csv → Training data                │
│  • Pre-trained Models → Classifier, Vectorizer, NER         │
└─────────────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              RESULTS RENDERED BACK TO USER                   │
│  JSON Response with extracted skills & recommended jobs     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Technology Stack & Libraries

### Core Dependencies & Their Purpose

#### **1. Flask (v3.1.3)**
- **Purpose:** Web framework for building the HTTP server and REST API
- **Used For:**
  - Creating route handlers (`/upload`, `/health`, etc.)
  - Rendering HTML templates
  - Managing HTTP requests and responses
  - Session management
- **Why:** Lightweight, fast, and perfect for REST APIs

---

#### **2. Flask-CORS (v6.0.2)**
- **Purpose:** Enable Cross-Origin Resource Sharing
- **Used For:**
  - Allowing requests from different domains
  - Enabling communication between frontend and backend
- **Why:** Prevents browser CORS (Cross-Origin) errors

---

#### **3. pdfplumber (v0.11.0)**
- **Purpose:** Extract text and tables from PDF files
- **Used For:**
  - Reading resume PDFs
  - Converting PDF content to plain text
  - Preserving formatting and structure
- **Code Location:** `read_resume.py` → `extract_text()` function
- **Why:** More accurate than other PDF libraries for resume extraction

---

#### **4. python-docx (v1.0.1)**
- **Purpose:** Read and manipulate DOCX (Microsoft Word) files
- **Used For:**
  - Extracting text from .docx resume files
  - Reading paragraphs from Word documents
- **Code Location:** `read_resume.py` → `extract_text()` function
- **Why:** Official library for working with Word documents in Python

---

#### **5. spaCy (v3.8.0)** ⭐ MOST IMPORTANT
- **Purpose:** Industrial-strength NLP (Natural Language Processing) library
- **Used For:**
  - Building the Named Entity Recognition (NER) model
  - Recognizing and extracting skills from resume text
  - Language processing and tokenization
- **Core Component:** Custom NER Model built using spaCy's EntityRuler
- **Why:** Fast, accurate, and production-ready for NLP tasks

---

#### **6. pandas (v2.0.3)**
- **Purpose:** Data manipulation and analysis library
- **Used For:**
  - Loading CSV files (job pool, training data)
  - Creating and manipulating DataFrames
  - Filtering and sorting job recommendations
  - Handling tabular data efficiently
- **Key Files:** Used in job_matcher.py, ranking_engine.py, ner_model.py

---

#### **7. scikit-learn (v1.3.2)**
- **Purpose:** Machine Learning library for Python
- **Used For:**
  - **TfidfVectorizer:** Convert text to numerical vectors
  - **cosine_similarity:** Calculate similarity between resumes and jobs
  - **KNeighborsClassifier:** Classify resumes into professional categories
  - **LabelEncoder:** Encode categorical labels
  - **OneVsRestClassifier:** Multi-class classification wrapper
- **Key Files:** job_matcher.py, train.py, ranking_engine.py

---

#### **8. Werkzeug (v3.0.1)**
- **Purpose:** WSGI utility library (foundation for Flask)
- **Used For:**
  - `secure_filename()` for safe file name handling
  - File upload security
  - Password hashing utilities
- **Why:** Essential for secure file handling in web apps

---

#### **9. Jinja2 (v3.1.4)**
- **Purpose:** Template engine for HTML rendering
- **Used For:**
  - Rendering HTML templates with dynamic content
  - Passing Python variables to HTML files
  - Conditional rendering (if/else in templates)
- **Example:** `templates/base.html`, `upload_resume.html`, `results.html`

---

#### **10. python-dotenv**
- **Purpose:** Load environment variables from .env file
- **Used For:**
  - Storing sensitive data (API keys, database credentials)
  - Configuration management
  - Keeping secrets out of source code
- **Usage:** `load_dotenv()` in app.py

---

#### **11. Flask-SQLAlchemy (v3.1.1)**
- **Purpose:** ORM (Object-Relational Mapping) for database interactions
- **Used For:**
  - Defining database models (User model in app.py)
  - User registration and login authentication
  - Storing user data in SQLite database
- **Database:** SQLite (`users.db`)

---

### Summary Table: Libraries & Their Role

| Library | Version | Primary Use | Location |
|---------|---------|-------------|----------|
| Flask | 3.1.3 | Web Framework | app.py, main.py |
| pdfplumber | 0.11.0 | PDF Text Extraction | read_resume.py |
| python-docx | 1.0.1 | DOCX Text Extraction | read_resume.py |
| spaCy | 3.8.0 | NER Model & NLP | ner_model.py, skill_extractor.py |
| pandas | 2.0.3 | Data Manipulation | job_matcher.py, ranking_engine.py |
| scikit-learn | 1.3.2 | ML Algorithms | train.py, job_matcher.py |
| Werkzeug | 3.0.1 | Security & Utilities | app.py |
| Jinja2 | 3.1.4 | HTML Templating | templates/ |
| Flask-SQLAlchemy | 3.1.1 | Database ORM | app.py |

---

## 📂 Project Structure & Modules

### Directory Layout
```
Hiresense_New/
├── app.py                          # Main Flask app with user authentication
├── train.py                        # Training script for ML models
├── hire_sense_AI/
│   ├── app.py                      # Flask routes for resume processing
│   ├── main.py                     # Main recommendation engine pipeline
│   ├── read_resume.py              # Resume text extraction
│   ├── connectivity.py             # Resume processing pipeline
│   ├── ARCHITECTURE.md             # Architecture documentation
│   ├── requirements.txt            # Python dependencies
│   └── data/
│       ├── master_job_pool.csv     # Job database
│       └── cleaned_training_data.csv # Training dataset
│
├── algorithms/
│   ├── skill_extractor.py          # Extract skills from text using NER
│   ├── job_matcher.py              # Match resume to jobs using TF-IDF
│   └── ranking_engine.py           # Rank jobs by multiple criteria
│
├── models/
│   ├── ner_model.py                # Build custom NER model
│   └── ner_model/                  # Saved spaCy NER model
│       ├── config.cfg
│       ├── meta.json
│       ├── tokenizer
│       ├── entity_ruler/
│       └── vocab/
│
├── templates/                      # HTML Templates (Jinja2)
│   ├── base.html                   # Base template (header, footer)
│   ├── index.html                  # Home page
│   ├── upload_resume.html          # Resume upload page
│   ├── results.html                # Job recommendations page
│   ├── login.html                  # Login page
│   └── signup.html                 # Signup page
│
├── static/                         # Static files
│   ├── style.css                   # Global CSS
│   ├── login_style.css             # Login page CSS
│   ├── signup_style.css            # Signup page CSS
│   └── icons/                      # Icon images
│
├── data/
│   ├── master_job_pool.csv         # Job database
│   └── cleaned_training_data.csv   # Training data for classifier
│
└── uploads/                        # Uploaded resume files (temporary)
```

---

## 🔄 Data Flow & Processing Pipeline

### Step-by-Step Resume Processing Flow

```
1. USER UPLOADS RESUME
   ↓
2. FILE VALIDATION
   - Check file type (PDF/DOCX/TXT)
   - Check file size (max 5MB)
   - Verify file is not empty
   ↓
3. TEXT EXTRACTION
   - If PDF → Use pdfplumber to extract text
   - If DOCX → Use python-docx to extract text
   - If TXT → Read directly
   ↓
4. NER MODEL ANALYSIS
   - Load custom spaCy NER model
   - Process text with entity ruler
   - Extract SKILL entities
   ↓
5. SKILL EXTRACTION
   - Use NER model to identify skills
   - Return list of unique skills found
   ↓
6. JOB MATCHING
   - Convert resume text to TF-IDF vector
   - Compare against all jobs in database
   - Calculate cosine similarity scores
   - Get top 5-10 matching jobs
   ↓
7. RANKING & REFINEMENT
   - Apply ranking engine
   - Combine skill score + experience score + category score
   - Apply weighted formula
   - Final ranked job list
   ↓
8. RESPONSE TO USER
   - Return JSON with:
     * Extracted skills
     * Number of skills found
     * Top job recommendations
     * Match scores for each job
```

---

## 🔍 Detailed Module Explanations

### 1. **read_resume.py** - File Type Handler
**Location:** `hire_sense_AI/read_resume.py`

**Purpose:** Extract text from different file formats

**Key Function:** `extract_text(file_path)`
```
Input:  file_path (string) - path to resume file (PDF/DOCX/TXT)
Output: resume_text (string) - extracted plain text

Logic:
- Check file extension
- If PDF: Use pdfplumber.open() to read each page
- If DOCX: Use Document() from python-docx
- If TXT: Use file.read()
- Return concatenated text
```

**Libraries Used:**
- pdfplumber
- python-docx

---

### 2. **connectivity.py** - Resume Processing Pipeline
**Location:** `hire_sense_AI/connectivity.py`

**Purpose:** Orchestrate the entire resume processing workflow

**Key Functions:**
1. `extract_text(file_path)` - Same as read_resume.py
2. `process_resume(file_path, job_pool_path)` - Main processing function

**Workflow:**
```
process_resume():
  1. Extract text from file
  2. Build NER model from job pool
  3. Extract skills using NER
  4. Return results dictionary
```

**Output Dictionary:**
```python
{
    "success": True/False,
    "file_type": "PDF/DOCX/TXT",
    "text_length": 5000,
    "resume_text": "Actual text...",
    "skills_found": ["python", "java", "sql"],
    "skills_count": 3
}
```

---

### 3. **ner_model.py** - Custom NER Model Builder
**Location:** `models/ner_model.py`

**Purpose:** Build a custom Named Entity Recognition model for skill extraction

**Key Function:** `build_skill_ner(job_pool_path)`

**How it Works:**
```
1. Load master_job_pool.csv
2. Extract all unique skills from 'skills' column
3. Clean and lowercase skills
4. Create spaCy English model (blank)
5. Add EntityRuler pipeline
6. Create patterns for each skill:
   {
       "label": "SKILL",
       "pattern": [{"LOWER": "python"}]
   }
7. Add all patterns to ruler
8. Return trained nlp model
```

**Why This Approach?**
- Rule-based: Fast, no training needed
- Exact matching from known job pool
- Guaranteed to find skills that exist in database
- No false positives

---

### 4. **skill_extractor.py** - Skill Recognition
**Location:** `algorithms/skill_extractor.py`

**Purpose:** Use NER model to extract skills from resume text

**Key Function:** `extract_skills_from_resume(resume_text, nlp_model)`

**Logic:**
```python
1. Run nlp_model on resume text (spaCy processing)
2. Extract all entities with label == "SKILL"
3. Convert to lowercase
4. Add to set (avoid duplicates)
5. Return list of unique skills
```

**Example:**
```
Input: "I have 5 years experience in Python and SQL"
Output: ["python", "sql"]
```

---

### 5. **job_matcher.py** - Job Recommendation Engine
**Location:** `algorithms/job_matcher.py`

**Purpose:** Match resume against job database using TF-IDF + Cosine Similarity

**Key Class:** `JobRecommender`

**Algorithm:**
```
1. Load job pool CSV
2. Create TfidfVectorizer (converts text to numbers)
3. Fit vectorizer on all job skills
4. For user resume:
   a. Clean text (lowercase, remove special chars)
   b. Transform to TF-IDF vector
   c. Calculate cosine_similarity with all jobs
   d. Get top N matches
   e. Add match_score (0-100%)
5. Return DataFrame of top jobs
```

**TF-IDF Explanation:**
- TF: Term Frequency (how often a word appears)
- IDF: Inverse Document Frequency (how unique the word is)
- Combined score: More important words get higher weight

**Cosine Similarity:**
- Measures angle between two vectors (0 to 1)
- 1.0 = Perfect match, 0.0 = No match

**Output Example:**
```
job_title          company    skills    years_exp  match_score
Software Engineer  Tech Corp  java,sql  3          85.5
Web Developer      StartUp    html,css  2          72.3
```

---

### 6. **ranking_engine.py** - Multi-Criteria Ranking
**Location:** `algorithms/ranking_engine.py`

**Purpose:** Rank job recommendations using multiple factors

**Key Class:** `RankingEngine`

**Ranking Factors:**
```
1. Skills Match Score (60% weight)
   - From job_matcher TF-IDF calculation
   
2. Experience Score (25% weight)
   - Perfect fit: user_exp >= job_exp and ≤ job_exp + 2
     → Score: 1.0
   - Underqualified: user_exp < job_exp
     → Score: max(0, 1 - (gap * 0.2))
   - Overqualified: user_exp > job_exp + 2
     → Score: 0.8
   
3. Category Score (15% weight)
   - If job category matches user category: 1.0
   - Otherwise: 0.5
```

**Final Formula:**
```
final_score = (skill_score × 0.60) + (exp_score × 0.25) + (cat_score × 0.15)
final_score *= 100  (convert to 0-100 scale)
```

**Example Calculation:**
```
Skill Score: 0.85 × 0.60 = 0.51
Exp Score:   1.0  × 0.25 = 0.25
Cat Score:   1.0  × 0.15 = 0.15
─────────────────────────────
Final Score: 0.91 × 100 = 91%
```

---

### 7. **main.py** - Full Pipeline Orchestrator
**Location:** `hire_sense_AI/main.py`

**Purpose:** Run complete recommendation pipeline from resume to job matches

**Key Function:** `run_pipeline(resume_text)`

**Pipeline Steps:**
```
1. Load all required models:
   - resume_classifier (KNN classifier)
   - tfidf_vectorizer (TF-IDF model)
   - label_encoder (category labels)
   - nlp_ner (spaCy NER model)
   - job_recommender (job matcher)

2. Classify Resume Category:
   - Transform resume to TF-IDF features
   - Predict professional category
   
3. Extract Skills:
   - Run NER model on resume text
   - Get list of skills
   
4. Match Jobs:
   - Get initial 10 job matches
   
5. Rank Jobs:
   - Apply ranking engine
   - Get final ranked list

6. Return Results:
   {
       "category": "Software Engineer",
       "skills": ["python", "java"],
       "jobs": [job1, job2, job3, ...]
   }
```

---

### 8. **train.py** - Model Training Script
**Location:** `train.py`

**Purpose:** Train and save all ML models

**Training Process:**
```
1. Load Training Data:
   - cleaned_training_data.csv (resumes with categories)
   
2. Train Category Classifier:
   - Encode categories using LabelEncoder
   - Vectorize resumes using TfidfVectorizer
   - Train OneVsRestClassifier(KNeighborsClassifier)
   - Save: resume_classifier.pkl, tfidf_vectorizer.pkl, label_encoder.pkl

3. Build NER Model:
   - Load job pool
   - Extract all unique skills
   - Create spaCy EntityRuler with skill patterns
   - Save to: models/ner_model/ (spaCy format)
```

**Models Generated:**
- `models/resume_classifier.pkl` - Category classifier
- `models/tfidf_vectorizer.pkl` - TF-IDF vectorizer
- `models/label_encoder.pkl` - Category encoder
- `models/ner_model/` - spaCy NER model directory

---

### 9. **app.py** - Main Flask Web Application
**Location:** `app.py` (root level)

**Purpose:** Main Flask application with user authentication and routes

**Key Components:**

1. **Database Model:**
```python
class User(db.Model):
    id - Primary key
    fullname - User's full name
    username - Unique username
    email - Unique email
    password - Hashed password (using werkzeug)
```

2. **Routes:**
   - `GET /` - Home page
   - `POST /signup` - User registration
   - `POST /login` - User authentication
   - `GET /logout` - Clear session
   - `POST /upload` - Resume upload and processing

3. **Key Functions:**
   - `allowed_file(filename)` - Validate file extensions
   - File upload handling with validation
   - Integration with NER pipeline

---

### 10. **hire_sense_AI/app.py** - Resume Processing API
**Location:** `hire_sense_AI/app.py`

**Purpose:** REST API for resume processing

**Models Loaded on Startup:**
- `nlp_model` - Custom NER model
- `job_recommender` - Job matcher

**Routes:**
1. `GET /` - API status
2. `GET /health` - Health check
3. `POST /upload-and-process` - Upload and process resume

**Processing Flow:**
```
POST /upload-and-process
├── Validate file
├── Extract text
├── Run NER for skills
├── Match against jobs
└── Return JSON response
```

---

### 11. **HTML Templates** - User Interface

#### **base.html** - Base Template
- Navigation bar with logo and links
- Footer with contact info
- Jinja2 blocks for extending templates

#### **upload_resume.html** - Resume Upload Page
- Drag-and-drop file upload area
- File type validation (PDF/DOCX/TXT)
- JavaScript for drag-drop functionality
- Visual feedback for selected file

#### **results.html** - Job Recommendations Page
- Display extracted skills
- Show resume text
- List job recommendations with:
  - Job title
  - Company name
  - Required skills
  - Match score percentage
  - Years of experience required

#### **login.html & signup.html** - Authentication Pages
- User registration form
- Login form
- Password hashing using werkzeug

---

## 🚀 How Everything Works Together

### Complete User Journey

```
1. USER STARTS
   ↓
2. OPENS WEBSITE (/)
   → Renders index.html (home page)
   
3. UPLOADS RESUME
   → POST to /upload endpoint
   → File saved to uploads/ folder
   
4. FILE PROCESSING CHAIN
   ├─ read_resume.py extracts text (PDF/DOCX/TXT)
   │
   ├─ ner_model.py runs spaCy NER model
   │  (identifies SKILL entities)
   │
   ├─ skill_extractor.py extracts unique skills
   │
   ├─ job_matcher.py finds matching jobs
   │  (TF-IDF + cosine similarity)
   │
   └─ ranking_engine.py ranks jobs
      (skills × 0.60 + exp × 0.25 + category × 0.15)
   
5. RESULTS RETURNED
   → JSON response with:
     * Extracted skills
     * Top 5-10 job recommendations
     * Match scores for each job
   
6. FRONTEND RENDERS RESULTS
   → Shows skills extracted
   → Shows job recommendations
   → User can download/print results
```

---

### Key Algorithms Summary

#### Algorithm 1: Skill Extraction (NER)
**Input:** Resume text
**Process:**
1. Create blank spaCy model
2. Add EntityRuler with skill patterns
3. Run model on text
4. Extract SKILL entities
**Output:** List of skills

---

#### Algorithm 2: Job Matching (TF-IDF)
**Input:** Resume text
**Process:**
1. Vectorize resume using TfidfVectorizer
2. Compare against all job vectors
3. Calculate cosine similarity scores
4. Sort by score
**Output:** Top N jobs with similarity scores

---

#### Algorithm 3: Job Ranking (Hybrid Scoring)
**Input:** Job matches + user profile
**Process:**
1. Calculate skill match score (0-1)
2. Calculate experience fit score (0-1)
3. Calculate category match score (0-1)
4. Combine with weights:
   - Skills: 60%
   - Experience: 25%
   - Category: 15%
**Output:** Final ranked score (0-100)

---

### Data Sources

#### 1. **master_job_pool.csv**
- Job database with columns:
  - job_id: Unique identifier
  - job_title: Position name
  - skills: Required skills (comma-separated)
  - years_exp_num: Years of experience required
  - experience_level: Entry/Mid/Senior
  - company: Company name

#### 2. **cleaned_training_data.csv**
- Training dataset for category classifier
- Contains sample resumes with their categories

#### 3. **ner_model/** (spaCy model directory)
- Pre-trained NER model with skill patterns
- Contains:
  - config.cfg: Model configuration
  - meta.json: Model metadata
  - tokenizer: Text tokenization rules
  - entity_ruler: Skill patterns
  - vocab: Vocabulary data

---

### Technology Interaction Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML/CSS/JS)                   │
├─────────────────────────────────────────────────────────────┤
│  • upload_resume.html - Upload UI                           │
│  • results.html - Display results                           │
│  • Handles form submission & display                        │
└────────────┬──────────────────────────────────────────────┘
             │
             ↓ HTTP POST
┌─────────────────────────────────────────────────────────────┐
│              FLASK APP (app.py)                              │
├─────────────────────────────────────────────────────────────┤
│  • Route handlers                                           │
│  • Authentication (Flask-SQLAlchemy)                        │
│  • File upload management (Werkzeug)                        │
└────────────┬──────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│        FILE EXTRACTION (read_resume.py)                     │
├─────────────────────────────────────────────────────────────┤
│  • pdfplumber → PDF extraction                              │
│  • python-docx → DOCX extraction                            │
│  • File I/O → TXT extraction                                │
└────────────┬──────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│         NER PROCESSING (ner_model.py + spaCy)               │
├─────────────────────────────────────────────────────────────┤
│  • Load skill patterns from job pool                        │
│  • Run EntityRuler on resume text                           │
│  • Extract SKILL entities                                   │
└────────────┬──────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│       SKILL EXTRACTION (skill_extractor.py)                 │
├─────────────────────────────────────────────────────────────┤
│  • Get unique skills from NER output                        │
│  • Remove duplicates & normalize                            │
└────────────┬──────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│  JOB MATCHING (job_matcher.py + scikit-learn)               │
├─────────────────────────────────────────────────────────────┤
│  • TfidfVectorizer → Convert text to vectors                │
│  • cosine_similarity → Calculate match scores               │
│  • Return top N jobs                                        │
└────────────┬──────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│     JOB RANKING (ranking_engine.py)                         │
├─────────────────────────────────────────────────────────────┤
│  • Combine: Skills (60%) + Experience (25%) + Category (15%)│
│  • Final ranked scores                                      │
└────────────┬──────────────────────────────────────────────┘
             │
             ↓ JSON Response
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND DISPLAY                        │
├─────────────────────────────────────────────────────────────┤
│  • Show extracted skills                                    │
│  • Show recommended jobs with scores                        │
│  • Allow download/print                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Processing Example

**Scenario:** User uploads resume for "Python Developer"

```
┌─ INPUT RESUME TEXT ──────────────────────────────────────┐
│ "5 years Python developer with expertise in Django,      │
│  SQL, and AWS. Strong in REST APIs and microservices."   │
└──────────────────────────────────────────────────────────┘

↓ STEP 1: NER Skill Extraction (spaCy EntityRuler)
  Output: ["python", "django", "sql", "aws", "rest", "api"]

↓ STEP 2: Job Matching (TF-IDF + Cosine Similarity)
  Compare against master_job_pool.csv
  Top 3 matches:
  1. "Senior Python Developer" - match: 92%
  2. "Full Stack Developer" - match: 78%
  3. "Data Engineer" - match: 65%

↓ STEP 3: Ranking Engine
  For "Senior Python Developer" (requires 5 years):
  - Skill Score: 0.92 × 0.60 = 0.552
  - Exp Score: 1.0 × 0.25 = 0.250 (perfect match: 5 years)
  - Category: 1.0 × 0.15 = 0.150 (Python Developer match)
  - Final: (0.552 + 0.250 + 0.150) × 100 = 95.2%

┌─ OUTPUT JSON ────────────────────────────────────────────┐
│ {                                                         │
│   "skills_found": ["python", "django", "sql", "aws"],   │
│   "skills_count": 4,                                      │
│   "recommendations": [                                    │
│     {                                                     │
│       "job_title": "Senior Python Developer",            │
│       "company": "Tech Corp",                            │
│       "skills": "python, django, sql, aws",             │
│       "final_rank_score": 95.2                           │
│     },                                                    │
│     ...                                                   │
│   ]                                                       │
│ }                                                         │
└──────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Concepts & Terminology

| Term | Definition |
|------|-----------|
| **NER** | Named Entity Recognition - identifying and classifying named entities (in this case, SKILL entities) |
| **TF-IDF** | Term Frequency-Inverse Document Frequency - algorithm for converting text to numerical vectors |
| **Cosine Similarity** | Measure of similarity between two vectors (0-1 scale) |
| **EntityRuler** | spaCy component that matches patterns and assigns entity labels |
| **Vectorization** | Converting text to numerical representation that ML algorithms can process |
| **Classifier** | ML model that predicts categories (here: professional category) |
| **Ranking** | Process of ordering items by score/relevance |
| **Hybrid Scoring** | Combining multiple scoring factors with weights |

---

## 🔐 Security Features

1. **File Upload Security:**
   - File type validation (PDF/DOCX/TXT only)
   - File size limit (5MB)
   - `secure_filename()` from Werkzeug

2. **Password Security:**
   - Passwords hashed using werkzeug
   - Not stored in plain text

3. **Session Management:**
   - Flask session for user authentication
   - Secret key for session encryption

---

## 📈 Performance Considerations

1. **Model Loading:**
   - Models loaded once at startup (cached)
   - Avoid reloading on every request

2. **Vectorization:**
   - TF-IDF vectorizer pre-fitted on job skills
   - Only transform incoming resume

3. **Similarity Calculation:**
   - Cosine similarity is fast (linear algebra)
   - Scales well with larger job pools

---

## 🎓 Summary

**HireSense** is an intelligent job matching system that combines:
- **Text Processing:** Extract content from multiple file formats
- **NLP:** Use spaCy for skill recognition
- **Machine Learning:** TF-IDF matching and ranking
- **Web Framework:** Flask for REST API
- **Database:** SQLite for user management

The system intelligently matches resumes to jobs using a hybrid approach that considers skills, experience level, and professional category. All libraries work together seamlessly to provide accurate job recommendations to users.

---

**Last Updated:** April 28, 2026
**Project:** HireSense - AI-Powered Resume Analysis & Job Matching System
