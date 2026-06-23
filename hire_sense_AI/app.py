import os
import sys
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Add models and algorithms to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'models'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'algorithms'))
from connectivity import process_resume, extract_text
from models.ner_model import build_skill_ner
from algorithms.skill_extractor import extract_skills_from_resume
from algorithms.job_matcher import JobRecommender

# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)

# Config
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret-key")
app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER", "uploads")
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Global variables for cached models (loaded once on startup)
nlp_model = None
job_recommender = None

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_models():
    """Load NER model and Job Recommender on app startup"""
    global nlp_model, job_recommender
    try:
        print("[STARTUP] Loading NER model...")
        nlp_model = build_skill_ner('data/master_job_pool.csv')
        print("[SUCCESS] NER model loaded")
        
        print("[STARTUP] Loading Job Recommender...")
        job_recommender = JobRecommender('data/master_job_pool.csv')
        print("[SUCCESS] Job Recommender loaded")
    except Exception as e:
        print(f"[ERROR] Failed to load models: {str(e)}")
        raise

# Home route
@app.route('/')
def home():
    return jsonify({
        "message": "Resume Processing API is running 🚀",
        "endpoints": {
            "upload_and_process": "/upload-and-process (POST) - Upload file and get full processing",
            "health": "/health (GET) - Check API status"
        }
    })

# Health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "models_loaded": nlp_model is not None and job_recommender is not None
    })

# Combined endpoint: Upload → Extract → NER → Job Matching
@app.route('/upload-and-process', methods=['POST'])
def upload_and_process():
    """
    Upload a resume file and get complete processing in one request
    Flow: Upload → Extract Text → Run NER → Extract Skills → Get Job Recommendations
    """
    try:
        # Step 1: Validate file upload
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "Invalid file type. Allowed: PDF, DOCX, TXT"}), 400
        
        # Step 2: Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        filepath = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

        file.save(filepath)
        
        print(f"\n[PROCESSING] Starting resume processing for {unique_filename}")
        
        # Step 3: Extract text from file
        print("[STEP 1] Extracting text from resume...")
        resume_text = extract_text(filepath)
        
        if not resume_text:
            return jsonify({
                "success": False, 
                "error": "Failed to extract text from file"
            }), 400
        
        print(f"[SUCCESS] Extracted {len(resume_text)} characters")
        
        # Step 4: Extract skills using NER model
        print("[STEP 2] Extracting skills using NER model...")
        skills_found = extract_skills_from_resume(resume_text, nlp_model)
        print(f"[SUCCESS] Found {len(skills_found)} unique skills: {skills_found}")
        
        # Step 5: Get job recommendations
        print("[STEP 3] Getting job recommendations based on skills...")
        top_n = request.args.get('top_n', 5, type=int)
        recommendations = job_recommender.get_recommendations(resume_text, top_n=top_n)
        
        # Convert DataFrame to list of dicts
        job_matches = recommendations.to_dict('records')
        print(f"[SUCCESS] Found {len(job_matches)} job recommendations")
        
        # Step 6: Return complete response
       file_ext = os.path.splitext(filename)[1].replace('.', '').upper()
        
        response = {
            "success": True,
            "file_info": {
                "filename": unique_filename,
                "original_filename": secure_filename(file.filename),
                "file_path": filepath,
                "file_type": file_ext,
                "text_length": len(resume_text)
            },
            "skills_extraction": {
                "skills_found": skills_found,
                "skills_count": len(skills_found)
            },
            "job_recommendations": {
                "total_matches": len(job_matches),
                "jobs": job_matches
            }
        }
        
        print("[COMPLETE] Resume processing completed successfully\n")
        return jsonify(response), 200
        
    except Exception as e:
        print(f"[ERROR] Processing failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": "An internal error occurred while processing the resume."
        }), 500

# Legacy endpoints (kept for backward compatibility)
@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Legacy: Upload file only (without processing)
    For full processing, use /upload-and-process instead
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400
        
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        return jsonify({
            "success": True,
            "message": "File uploaded successfully",
            "filename": unique_filename,
            "path": filepath
        }), 200
        
    except Exception as e:
        print(f"[ERROR] Legacy upload failed: {str(e)}")
        return jsonify({"error": "An internal error occurred during file upload."}), 500

# Run app
if __name__ == '__main__':
    print("\n" + "="*60)
    print("Starting HireSense Resume Processing API")
    print("="*60)
    
    # Load models before starting the app
    load_models()
    
    print("="*60 + "\n")
    app.run(debug=False)
