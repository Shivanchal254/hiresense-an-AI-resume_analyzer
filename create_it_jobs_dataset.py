import pandas as pd
import random
from itertools import combinations

# Comprehensive IT Jobs Dataset Generator
# This script creates a dataset with every major IT job category

IT_JOBS_DATA = {
    # Software Development Roles
    "Software Engineer": ["java", "python", "c#", "sql", "git"],
    "Senior Software Engineer": ["java", "python", "c++", "sql", "git", "microservices", "aws"],
    "Full Stack Developer": ["javascript", "html", "css", "node.js", "react", "sql", "mongodb"],
    "Frontend Developer": ["javascript", "react", "angular", "vue", "html", "css", "webpack"],
    "Backend Developer": ["java", "python", "node.js", "sql", "mongodb", "rest api", "microservices"],
    "Web Developer": ["html", "css", "javascript", "php", "sql", "wordpress"],
    "Mobile Developer": ["java", "swift", "kotlin", "react native", "flutter", "sql"],
    "iOS Developer": ["swift", "objective-c", "xcode", "cocoapods", "git"],
    "Android Developer": ["java", "kotlin", "android studio", "sqlite", "firebase"],
    "Game Developer": ["c#", "unity", "c++", "unreal engine", "graphics"],
    "Embedded Systems Engineer": ["c", "c++", "assembly", "microcontrollers", "embedded linux"],
    "DevOps Engineer": ["docker", "kubernetes", "jenkins", "ci/cd", "linux", "aws", "terraform"],
    "Cloud Engineer": ["aws", "azure", "gcp", "terraform", "docker", "kubernetes"],
    "Solutions Architect": ["system design", "aws", "azure", "microservices", "sql", "nosql"],
    
    # Data & Analytics
    "Data Scientist": ["python", "r", "sql", "machine learning", "tableau", "pandas", "scikit-learn"],
    "Data Engineer": ["python", "sql", "etl", "hadoop", "spark", "airflow", "kafka"],
    "Machine Learning Engineer": ["python", "tensorflow", "pytorch", "scikit-learn", "sql", "aws"],
    "Analytics Engineer": ["sql", "python", "dbt", "tableau", "looker", "analytics"],
    "Business Analyst": ["sql", "tableau", "excel", "analytics", "ui", "requirements analysis"],
    "Data Analyst": ["sql", "python", "excel", "tableau", "power bi", "statistics"],
    "AI Engineer": ["python", "tensorflow", "pytorch", "nlp", "deep learning", "ml ops"],
    "ML Ops Engineer": ["python", "docker", "kubernetes", "mlflow", "jenkins", "monitoring"],
    
    # Security
    "Security Engineer": ["network security", "encryption", "firewalls", "sql", "python"],
    "Cybersecurity Analyst": ["security", "network", "penetration testing", "firewall", "ids/ips"],
    "Application Security Engineer": ["secure coding", "owasp", "python", "java", "penetration testing"],
    "Security Architect": ["security design", "compliance", "network security", "encryption", "aws"],
    "Incident Response Specialist": ["forensics", "malware analysis", "network security", "python"],
    
    # Infrastructure & Operations
    "System Administrator": ["linux", "windows", "network", "sql", "security"],
    "Network Administrator": ["networking", "cisco", "routing", "firewall", "tcp/ip"],
    "Database Administrator": ["sql", "database design", "oracle", "mysql", "backup/recovery"],
    "Technical Support Engineer": ["troubleshooting", "networking", "windows", "linux", "customer service"],
    "Infrastructure Engineer": ["linux", "windows", "networking", "virtualization", "terraform"],
    "Site Reliability Engineer": ["linux", "python", "docker", "kubernetes", "monitoring", "aws"],
    
    # Testing & QA
    "QA Engineer": ["selenium", "testing", "automation", "sql", "performance testing"],
    "Test Automation Engineer": ["selenium", "python", "java", "junit", "jenkins", "ci/cd"],
    "Manual QA Engineer": ["testing", "bug tracking", "sql", "excel", "communication"],
    "Performance Test Engineer": ["jmeter", "loadrunner", "performance", "sql", "analysis"],
    "Security Test Engineer": ["penetration testing", "owasp", "security", "scripting", "networking"],
    
    # Management & Leadership
    "Technical Lead": ["leadership", "architecture", "java", "sql", "mentoring"],
    "Engineering Manager": ["management", "java", "sql", "leadership", "teamwork"],
    "Project Manager": ["project management", "agile", "scrum", "excel", "communication"],
    "Product Manager": ["product strategy", "analytics", "sql", "communication", "excel"],
    "Scrum Master": ["scrum", "agile", "leadership", "jira", "communication"],
    "Technical Program Manager": ["program management", "technical", "agile", "excel", "communication"],
    
    # Architecture & Design
    "Software Architect": ["system design", "microservices", "java", "sql", "aws"],
    "Enterprise Architect": ["enterprise design", "system architecture", "sql", "cloud", "networking"],
    "Solutions Architect": ["system design", "cloud", "aws", "microservices", "technical"],
    "API Architect": ["rest api", "graphql", "microservices", "system design", "java"],
    "Database Architect": ["sql", "nosql", "database design", "performance", "scaling"],
    
    # Specialized Roles
    "AI/ML Researcher": ["python", "pytorch", "tensorflow", "research", "deep learning", "statistics"],
    "NLP Engineer": ["python", "nlp", "spacy", "nltk", "transformers", "machine learning"],
    "Computer Vision Engineer": ["python", "opencv", "deep learning", "tensorflow", "image processing"],
    "Blockchain Developer": ["solidity", "ethereum", "cryptocurrency", "smart contracts", "web3"],
    "AR/VR Developer": ["unity", "unreal engine", "c#", "c++", "3d graphics"],
    "IoT Developer": ["embedded systems", "microcontrollers", "iot", "networking", "python"],
    
    # Support & Documentation
    "Technical Writer": ["documentation", "sql", "api", "communication", "technical knowledge"],
    "Developer Advocate": ["public speaking", "technical", "community", "documentation", "coding"],
    "Support Engineer": ["technical support", "troubleshooting", "communication", "linux", "networking"],
    "Technical Support Specialist": ["customer service", "troubleshooting", "networking", "windows"],
    
    # Additional IT Roles
    "IT Consultant": ["consulting", "system design", "java", "sql", "networking"],
    "Systems Engineer": ["system design", "linux", "windows", "networking", "automation"],
    "Automation Engineer": ["python", "scripting", "automation", "jenkins", "ci/cd"],
    "Release Manager": ["release management", "version control", "git", "jira", "deployment"],
    "Integration Engineer": ["api integration", "sql", "etl", "middleware", "python"],
    "Business Intelligence Developer": ["sql", "tableau", "power bi", "etl", "analytics"],
    "Data Warehouse Engineer": ["sql", "etl", "snowflake", "redshift", "analytics"],
    "Middleware Engineer": ["middleware", "java", "messaging", "networking", "enterprise"],
    "Quality Assurance Manager": ["qa management", "testing", "leadership", "sql", "automation"],
    "Compliance Officer": ["compliance", "security", "regulations", "documentation", "audit"],
}

COMPANIES = [
    "Google", "Microsoft", "Amazon", "Apple", "Meta",
    "Netflix", "Tesla", "IBM", "Oracle", "Salesforce",
    "Adobe", "Cisco", "VMware", "Slack", "Stripe",
    "Zoom", "Dropbox", "Airbnb", "Uber", "Twitter",
    "LinkedIn", "Spotify", "GitHub", "Figma", "Notion",
    "TikTok", "Snapchat", "Discord", "Roblox", "Square",
    "Palantir", "Databricks", "Canva", "Miro", "HashiCorp",
    "JetBrains", "MongoDB", "Elastic", "CockroachDB", "Kafka",
    "DataStax", "Confluent", "Okta", "Auth0", "Twilio",
    "SendGrid", "Stripe", "Square", "Toast", "Shopify",
    "Intel", "NVIDIA", "AMD", "Qualcomm", "Broadcom",
    "Accenture", "Deloitte", "McKinsey", "PwC", "EY",
    "Infosys", "TCS", "Wipro", "HCL", "Tech Mahindra",
    "Cognizant", "Capgemini", "IBM", "Atos", "NTT Data"
]

EXPERIENCE_LEVELS = ["Entry level", "Junior", "Mid-level", "Mid-Senior level", "Senior"]

def assign_experience_level(job_title):
    """Assign experience level based on job title"""
    if "Senior" in job_title or "Manager" in job_title or "Lead" in job_title or "Architect" in job_title:
        return random.choice(["Mid-Senior level", "Senior"])
    elif "Junior" in job_title or "Associate" in job_title:
        return random.choice(["Entry level", "Junior"])
    else:
        return random.choice(["Junior", "Mid-level", "Mid-Senior level"])

def assign_years_of_experience(experience_level):
    """Assign years of experience based on level"""
    experience_ranges = {
        "Entry level": random.randint(0, 1),
        "Junior": random.randint(2, 4),
        "Mid-level": random.randint(5, 8),
        "Mid-Senior level": random.randint(9, 13),
        "Senior": random.randint(14, 20)
    }
    return experience_ranges.get(experience_level, 5)

# Generate Dataset
dataset = []
job_id_counter = 1

for job_title, skills in IT_JOBS_DATA.items():
    for i in range(3):  # Create 3 entries per job title (different companies)
        experience_level = assign_experience_level(job_title)
        years_exp = assign_years_of_experience(experience_level)
        company = random.choice(COMPANIES)
        
        # Create skill variations
        num_skills = random.randint(4, len(skills))
        selected_skills = random.sample(skills, min(num_skills, len(skills)))
        skills_str = ", ".join(selected_skills)
        
        dataset.append({
            "job_id": f"IT-{job_id_counter}",
            "job_title": job_title,
            "skills": skills_str,
            "years_exp_num": years_exp,
            "experience_level": experience_level,
            "company": company,
            "mandatory_qualification": "Any"
        })
        job_id_counter += 1

# Create DataFrame
df = pd.DataFrame(dataset)

# Save to CSV
output_path = 'data/it_jobs_dataset.csv'
df.to_csv(output_path, index=False)

print(f"✅ IT Jobs Dataset Created Successfully!")
print(f"📊 Dataset Statistics:")
print(f"   - Total Jobs: {len(df)}")
print(f"   - Unique Job Titles: {df['job_title'].nunique()}")
print(f"   - Companies: {df['company'].nunique()}")
print(f"\n📁 Saved to: {output_path}")
print(f"\n🔍 Dataset Preview:")
print(df.head(10).to_string())
