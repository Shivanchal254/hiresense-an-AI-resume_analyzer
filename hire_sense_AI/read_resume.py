import pdfplumber
from docx import Document


def extract_text(file_path):
    text = ""

    try:
        # 📄 PDF
        if file_path.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

        # 📄 DOCX
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        # 📄 TXT
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

        else:
            return "Unsupported file format"

    except Exception as e:
        print("Error:", e)
        if not text.strip():
            return "No readable text found in resume"
    
    return text

#print(extract_text(file_path))


