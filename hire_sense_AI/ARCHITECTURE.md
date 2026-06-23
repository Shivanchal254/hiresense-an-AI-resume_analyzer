# 🏗️ System Architecture - Hire Sense

## Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT SIDE (Browser)                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐              ┌──────────────────┐    │
│  │  Upload Page 3   │              │  Results Page 4  │    │
│  │  (upload.html)   │              │ (results.html)   │    │
│  │                  │              │                  │    │
│  │ • Drag-drop      │              │ • NER Results    │    │
│  │ • File input     │──────────→ • Skills extracted │    │
│  │ • Validation     │              │ • Raw text       │    │
│  │ • Loading state  │              │ • Download       │    │
│  └──────────────────┘              │ • Print option   │    │
│           ↑                        └──────────────────┘    │
│           │                                  ↑              │
│           └──────────────────────────────────┘              │
│                     HTTP Requests                           │
└─────────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────────┐
│                    FLASK SERVER (app.py)                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Route Handlers                         │    │
│  │  • GET /         → Render upload.html             │    │
│  │  • POST /upload  → Process file & NER analysis    │    │
│  │  • POST /api/analyze → API endpoint               │    │
│  └────────────────────────────────────────────────────┘    │
│           ↓                                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │         File Processing Pipeline                   │    │
│  ├────────────────────────────────────────────────────┤    │
│  │ 1. Validate file (type, size)                      │    │
│  │ 2. Save uploaded file                              │    │
│  │ 3. Extract text (PDF/DOCX/TXT)                     │    │
│  │ 4. Perform NER analysis                            │    │
│  │ 5. Generate HTML highlighting                      │    │
│  │ 6. Extract skills                                  │    │
│  │ 7. Clean up temp files                             │    │
│  │ 8. Render results page                             │    │
│  └────────────────────────────────────────────────────┘    │
│           ↓                                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │    External Libraries & Models                     │    │
│  ├────────────────────────────────────────────────────┤    │
│  │ • pdfplumber → PDF text extraction                │    │
│  │ • python-docx → DOCX text extraction              │    │
│  │ • spaCy → NER model & entity extraction           │    │
│  │ • skill_extractor.py → Skill matching             │    │
│  └────────────────────────────────────────────────────┘    │
│           ↓                                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │    Data & Models Loaded at Startup                │    │
│  ├────────────────────────────────────────────────────┤    │
│  │ • nlp_ner → Loaded spaCy model                    │    │
│  │ • Skill patterns → From job pool CSV              │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
User Action
    ↓
┌───────────────────────────────┐
│ Select & Upload Resume File   │
│ (PDF/DOCX/TXT)               │
└───────────────┬───────────────┘
                ↓
        ┌──────────────┐
        │ File Received│
        └──────┬───────┘
               ↓
    ┌──────────────────────────┐
    │ VALIDATION              │
    │ • Check file type       │
    │ • Check file size       │
    │ • Verify not empty      │
    └──────┬───────────────────┘
           ↓
    INVALID ✗ → [ERROR PAGE]
           ↓
         VALID ✓
           ↓
    ┌──────────────────────────┐
    │ TEXT EXTRACTION         │
    │ • PDF → pdfplumber      │
    │ • DOCX → python-docx    │
    │ • TXT → read file       │
    └──────┬───────────────────┘
           ↓
    ┌──────────────────────────┐
    │ NER ANALYSIS            │
    │ Load spaCy model        │
    │ Process text            │
    │ Extract entities        │
    └──────┬───────────────────┘
           ↓
    ┌──────────────────────────┐
    │ SKILL EXTRACTION        │
    │ Match patterns          │
    │ Build skill list        │
    └──────┬───────────────────┘
           ↓
    ┌──────────────────────────┐
    │ HTML GENERATION         │
    │ Color-code entities     │
    │ Format results          │
    └──────┬───────────────────┘
           ↓
    ┌──────────────────────────┐
    │ RENDER RESULTS PAGE     │
    │ • Named Entities Tab    │
    │ • Extracted Skills Tab  │
    │ • Raw Text Tab          │
    └──────┬───────────────────┘
           ↓
    Display Results to User
```

## File Structure Overview

```
hire_sense/                          ← PROJECT ROOT
│
├── app.py ⭐                         ← MAIN FLASK APPLICATION
│   ├── Route handlers (/, /upload, /api/analyze)
│   ├── File validation & processing
│   ├── NER analysis integration
│   └── Error handling
│
├── read_resume.py
│   └── extract_text(filepath) → Handles PDF/DOCX/TXT extraction
│
├── models/
│   ├── ner_model.py
│   │   └── build_skill_ner() → Creates NER patterns
│   └── ner_model/              ← Trained spaCy model
│       ├── config.cfg
│       ├── meta.json
│       ├── tokenizer/
│       ├── entity_ruler/
│       │   └── patterns.jsonl ← Entity patterns
│       └── vocab/
│
├── algorithms/
│   ├── skill_extractor.py
│   │   └── extract_skills_from_resume() → Called by app.py
│   ├── job_matcher.py
│   └── ranking_engine.py
│
├── data/
│   └── master_job_pool.csv      ← Job database for skills
│
├── templates/ ⭐
│   ├── upload.html              ← PAGE 3: File upload interface
│   ├── results.html             ← PAGE 4: Results display
│   └── error.html               ← Error page
│
├── uploads/                      ← Temporary file storage
│
├── requirements.txt              ← Python dependencies
├── SETUP.md                      ← Quick start guide
├── README.md                     ← Full documentation
├── CONFIG.md                     ← Configuration guide
├── TESTING.md                    ← Testing procedures
├── INTEGRATION_SUMMARY.md        ← This integration overview
└── .env (optional)               ← Environment variables

```

## Component Interactions

```
┌────────────────────────┐
│   Browser (User)       │
└────────────┬───────────┘
             │
    HTML/CSS/JavaScript ← Tailwind CSS CDN
             │
     ┌───────▼───────┐
     │  upload.html  │ ← Form submission
     └───────┬───────┘
             │
        POST /upload
    FormData {file}
             │
     ┌───────▼──────────────┐
     │   Flask app.py       │
     │   (/upload route)    │
     └───────┬──────────────┘
             │
    ┌────────▼─────────────────────────┐
    │ 1. VALIDATE FILE                 │
    │    werkzeug.utils.secure_filename│
    └────────┬─────────────────────────┘
             │
    ┌────────▼─────────────────────────┐
    │ 2. EXTRACT TEXT                  │
    │    read_resume.extract_text()    │
    │    ├─ pdfplumber (PDF)          │
    │    ├─ python-docx (DOCX)        │
    │    └─ open() (TXT)              │
    └────────┬─────────────────────────┘
             │
    ┌────────▼─────────────────────────┐
    │ 3. PERFORM NER ANALYSIS          │
    │    perform_ner_analysis()        │
    │    ├─ spacy.load(nlp_ner)       │
    │    ├─ doc = nlp_ner(text)       │
    │    └─ Generate HTML highlighting │
    └────────┬─────────────────────────┘
             │
    ┌────────▼─────────────────────────┐
    │ 4. EXTRACT SKILLS                │
    │    skill_extractor.py            │
    │    extract_skills_from_resume()  │
    └────────┬─────────────────────────┘
             │
    ┌────────▼─────────────────────────┐
    │ 5. RENDER RESULTS PAGE           │
    │    render_template(              │
    │      'results.html',             │
    │      filename=...,               │
    │      ner_result=...,             │
    │      skills=...                  │
    │    )                             │
    └────────┬─────────────────────────┘
             │
        HTML Response
             │
     ┌───────▼──────────┐
     │  results.html    │ ← Three tabs:
     │                  │   - Named Entities
     │                  │   - Extracted Skills
     │                  │   - Raw Text
     └──────────────────┘
```

## Entity Highlighting Pipeline

```
Raw Text
   ↓
┌─────────────────────────────┐
│ spaCy NER Processing        │
│ doc = nlp(text)             │
│ for ent in doc.ents:        │
│   type = ent.label_         │
│   start = ent.start_char    │
│   end = ent.end_char        │
│   text = ent.text           │
└──────────┬──────────────────┘
           ↓
    Entity Data:
    type: "SKILL"
    text: "Python"
           ↓
┌─────────────────────────────┐
│ Color Mapping               │
│ SKILL → #ddd2d2            │
│ ORG → #c1ecff              │
│ PERSON → #ffebee           │
│ DATE → #fff4c6             │
│ GPE → #e8f5e9              │
│ PRODUCT → #f3e5f5          │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│ HTML Generation             │
│ <mark style="               │
│ background-color: #ddd2d2;  │
│ padding: 2px 6px;           │
│ margin: 0 2px;">            │
│ Python⭐                    │
│ <span>SKILL</span>          │
│ </mark>                     │
└──────────┬──────────────────┘
           ↓
Display in Browser with
Highlighting & Labels
```

## Session Lifecycle

```
1. STARTUP
   ├─ Load spaCy NER model
   ├─ Initialize Flask app
   └─ Ready for requests

2. USER REQUEST: GET /
   ├─ Return upload.html
   └─ Display upload form

3. USER ACTION: Upload file
   └─ POST /upload

4. FILE PROCESSING
   ├─ Validate file
   ├─ Extract text
   ├─ Analyze with NER
   ├─ Extract skills
   ├─ Generate HTML
   ├─ Clean up temp files
   └─ Return results.html

5. USER ACTION: Navigate tabs
   └─ JavaScript changes display
      (no server round-trip needed)

6. USER ACTION: Download/Print
   ├─ Download: JavaScript triggers file download
   └─ Print: Browser print dialog

7. USER ACTION: Upload another resume
   └─ Return to step 2
```

## Error Handling Flow

```
                    Error Occurs
                        ↓
                ┌────────┴────────┐
                ↓                  ↓
          Invalid File       Processing Error
                ↓                  ↓
        ┌─────────────────┐  ┌──────────────────┐
        │ Type mismatch?  │  │ Text empty?      │
        │ File too large? │  │ NER failed?      │
        │ Not readable?   │  │ Extraction error?│
        └─────┬───────────┘  └────┬─────────────┘
              ↓                    ↓
        render_template('error.html', error=msg)
              ↓
        Display error page with:
        • Error message
        • File name
        • Troubleshooting tips
        • Navigation options
```

## Performance Characteristics

```
Operation            │ Time      │ Notes
───────────────────────────────────────────────
App Startup          │ 2-3 sec   │ Loading spaCy model
File Upload          │ < 1 sec   │ Network dependent
Text Extraction      │ 1-2 sec   │ PDF slower than TXT
NER Analysis         │ 1-3 sec   │ Text length dependent
Skill Extraction     │ < 500ms   │ Pattern matching
HTML Generation      │ < 100ms   │ Markup building
Page Rendering       │ < 1 sec   │ Browser rendering
───────────────────────────────────────────────
Total (avg)          │ 2-5 sec   │ For average resume
```

---

This architecture is designed to be:
- ✅ Modular (easy to extend)
- ✅ Scalable (can handle multiple requests)
- ✅ Maintainable (clear separation of concerns)
- ✅ Secure (input validation, file handling)
- ✅ Performant (models loaded once)
- ✅ User-friendly (responsive UI with feedback)
