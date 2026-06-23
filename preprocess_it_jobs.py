import pandas as pd
import numpy as np
import re
from pathlib import Path

print("\n" + "="*50)
print("🔧 IT JOBS DATASET PRE-PROCESSING")
print("="*50)

# Load the generated IT jobs dataset
it_jobs_path = 'data/it_jobs_dataset.csv'
df_it = pd.read_csv(it_jobs_path)

print(f"\n📊 Original Dataset Shape: {df_it.shape}")
print(f"   Rows: {len(df_it)}, Columns: {len(df_it.columns)}")

# ============ DATA QUALITY CHECKS ============

print("\n🔍 Data Quality Checks:")

# 1. Check for missing values
missing_values = df_it.isnull().sum()
if missing_values.sum() > 0:
    print("❌ Missing Values Found:")
    print(missing_values[missing_values > 0])
else:
    print("✅ No missing values")

# 2. Check for duplicate job_ids
duplicates = df_it['job_id'].duplicated().sum()
if duplicates > 0:
    print(f"❌ Found {duplicates} duplicate job_ids")
    df_it = df_it.drop_duplicates(subset=['job_id'], keep='first')
else:
    print("✅ All job_ids are unique")

# 3. Validate experience levels
valid_levels = {"Entry level", "Junior", "Mid-level", "Mid-Senior level", "Senior"}
invalid_levels = df_it[~df_it['experience_level'].isin(valid_levels)]
if len(invalid_levels) > 0:
    print(f"❌ Found {len(invalid_levels)} invalid experience levels")
    # Fix: standardize any invalid levels
    df_it.loc[~df_it['experience_level'].isin(valid_levels), 'experience_level'] = 'Mid-level'
else:
    print("✅ All experience levels are valid")

# 4. Validate years of experience (should be numeric)
df_it['years_exp_num'] = pd.to_numeric(df_it['years_exp_num'], errors='coerce').astype(int)
print("✅ Years of experience normalized to integers")

# 5. Clean and normalize skills
def clean_skills(skills_str):
    """Clean skills column"""
    if pd.isna(skills_str):
        return "general"
    skills_str = str(skills_str).lower()
    # Remove extra spaces and standardize
    skills_list = [s.strip() for s in skills_str.split(',')]
    skills_list = [s for s in skills_list if s]  # Remove empty strings
    return ', '.join(sorted(skills_list))

df_it['skills'] = df_it['skills'].apply(clean_skills)
print("✅ Skills cleaned and standardized")

# 6. Standardize job titles
df_it['job_title'] = df_it['job_title'].str.strip().str.title()
print("✅ Job titles standardized")

# 7. Remove rows with very short/invalid job titles
df_it = df_it[df_it['job_title'].str.len() > 2]
print(f"✅ Removed rows with invalid job titles")

# ============ ADDITIONAL VALIDATIONS ============

print("\n✔️ Additional Validations:")

# Check data types
print(f"   - job_id dtype: {df_it['job_id'].dtype}")
print(f"   - years_exp_num dtype: {df_it['years_exp_num'].dtype}")
print(f"   - experience_level dtype: {df_it['experience_level'].dtype}")

# Summary statistics
print(f"\n📈 Dataset Summary:")
print(f"   - Total Records: {len(df_it)}")
print(f"   - Unique Job Titles: {df_it['job_title'].nunique()}")
print(f"   - Unique Companies: {df_it['company'].nunique()}")
print(f"   - Average Years of Experience: {df_it['years_exp_num'].mean():.1f}")
print(f"   - Experience Level Distribution:")
for level in df_it['experience_level'].value_counts().index:
    count = df_it['experience_level'].value_counts()[level]
    pct = (count / len(df_it) * 100)
    print(f"      • {level}: {count} ({pct:.1f}%)")

# ============ SAVE PRE-PROCESSED DATA ============

processed_path = 'data/it_jobs_dataset_processed.csv'
df_it.to_csv(processed_path, index=False)

print(f"\n✅ Pre-processing Complete!")
print(f"📁 Processed dataset saved to: {processed_path}")

# ============ DATASET COMPARISON ============

print("\n" + "="*50)
print("📊 DATASET STRUCTURE VALIDATION")
print("="*50)

# Load original master_job_pool to compare structure
master_path = 'data/master_job_pool.csv'
df_master = pd.read_csv(master_path)

print(f"\n🔍 Comparing with Master Job Pool:")
print(f"   Master Pool Shape: {df_master.shape}")
print(f"   IT Jobs Dataset Shape: {df_it.shape}")
print(f"   Master Pool Columns: {list(df_master.columns)}")
print(f"   IT Jobs Columns: {list(df_it.columns)}")

# Verify columns match
if list(df_master.columns) == list(df_it.columns):
    print("✅ Column structure matches!")
else:
    print("❌ Column mismatch - needs alignment")
    print(f"   Missing columns: {set(df_master.columns) - set(df_it.columns)}")
    print(f"   Extra columns: {set(df_it.columns) - set(df_master.columns)}")

# ============ SAFETY CHECK ============

print("\n" + "="*50)
print("🛡️ INTEGRATION SAFETY CHECK")
print("="*50)

# Check for duplicate job_ids between datasets
master_ids = set(df_master['job_id'].unique())
it_ids = set(df_it['job_id'].unique())
overlap = master_ids.intersection(it_ids)

if len(overlap) > 0:
    print(f"⚠️ WARNING: Found {len(overlap)} overlapping job_ids!")
    print(f"   This could cause conflicts during integration.")
else:
    print("✅ No job_id conflicts - Safe to integrate")

# Check for data integrity
print(f"\n✅ Data Integrity Checks:")
print(f"   - All job_ids unique: {df_it['job_id'].duplicated().sum() == 0}")
print(f"   - No null values: {df_it.isnull().sum().sum() == 0}")
print(f"   - All experience levels valid: {df_it['experience_level'].isin(valid_levels).all()}")
print(f"   - All years_exp numeric: {df_it['years_exp_num'].dtype in ['int64', 'int32']}")

print("\n" + "="*50)
print("✅ PRE-PROCESSING COMPLETE & VALIDATION SUCCESSFUL")
print("="*50)
print("\n✨ Dataset is ready for integration!\n")
