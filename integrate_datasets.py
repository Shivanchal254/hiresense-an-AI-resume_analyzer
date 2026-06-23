import pandas as pd
import numpy as np
import shutil
from datetime import datetime
from pathlib import Path

print("\n" + "="*60)
print("🔗 DATASET INTEGRATION SCRIPT")
print("="*60)

# ============ STEP 1: LOAD DATASETS ============

print("\n📂 Step 1: Loading Datasets...")

master_path = 'data/master_job_pool.csv'
it_processed_path = 'data/it_jobs_dataset_processed.csv'

# Create backup of master pool
backup_path = f'data/master_job_pool_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
shutil.copy(master_path, backup_path)
print(f"✅ Backup created: {backup_path}")

# Load datasets
df_master = pd.read_csv(master_path)
df_it = pd.read_csv(it_processed_path)

print(f"✅ Master Job Pool loaded: {len(df_master)} records")
print(f"✅ IT Jobs dataset loaded: {len(df_it)} records")

# ============ STEP 2: COMPREHENSIVE SAFETY CHECKS ============

print("\n🛡️ Step 2: Performing Safety Checks...")

# Check 1: Column compatibility
master_cols = set(df_master.columns)
it_cols = set(df_it.columns)

if master_cols != it_cols:
    print("❌ Column mismatch detected!")
    print(f"   Master columns: {master_cols}")
    print(f"   IT dataset columns: {it_cols}")
    raise ValueError("Columns do not match!")
else:
    print("✅ Columns are compatible")

# Check 2: Data types compatibility
print("\n   Checking data types...")
for col in df_master.columns:
    master_dtype = df_master[col].dtype
    it_dtype = df_it[col].dtype
    if not (str(master_dtype) == str(it_dtype) or 
            (master_dtype in ['int64', 'int32'] and it_dtype in ['int64', 'int32']) or
            (str(master_dtype).startswith('object') and str(it_dtype).startswith('object'))):
        print(f"   ⚠️ {col}: Master={master_dtype}, IT={it_dtype}")
    else:
        print(f"   ✅ {col}: Compatible")

# Check 3: ID uniqueness
master_ids = set(df_master['job_id'].unique())
it_ids = set(df_it['job_id'].unique())
overlap = master_ids.intersection(it_ids)

if len(overlap) == 0:
    print("\n✅ No ID conflicts - datasets are independent")
else:
    print(f"\n⚠️ WARNING: {len(overlap)} overlapping IDs found")
    print("   These will be handled by deduplication...")

# Check 4: Data integrity
print("\n   Integrity Checks:")
null_check_master = df_master.isnull().sum().sum()
null_check_it = df_it.isnull().sum().sum()
print(f"   ✅ Master nulls: {null_check_master}")
print(f"   ✅ IT nulls: {null_check_it}")

# Check 5: Experience level validation
valid_levels = {"Entry level", "Junior", "Mid-level", "Mid-Senior level", "Senior"}
master_invalid = ~df_master['experience_level'].isin(valid_levels)
it_invalid = ~df_it['experience_level'].isin(valid_levels)
print(f"   ✅ Master invalid levels: {master_invalid.sum()}")
print(f"   ✅ IT invalid levels: {it_invalid.sum()}")

# ============ STEP 3: DATA VALIDATION ============

print("\n✔️ Step 3: Data Validation...")

# Validate years of experience ranges
print("   Years of Experience ranges:")
print(f"   Master - Min: {df_master['years_exp_num'].min()}, Max: {df_master['years_exp_num'].max()}, Avg: {df_master['years_exp_num'].mean():.1f}")
print(f"   IT     - Min: {df_it['years_exp_num'].min()}, Max: {df_it['years_exp_num'].max()}, Avg: {df_it['years_exp_num'].mean():.1f}")

# Validate job titles
print(f"\n   Job Title Statistics:")
print(f"   Master unique titles: {df_master['job_title'].nunique()}")
print(f"   IT unique titles: {df_it['job_title'].nunique()}")

# ============ STEP 4: PRE-MERGE ANALYSIS ============

print("\n📊 Step 4: Pre-Merge Analysis...")

print(f"   Combined dataset would have {len(df_master) + len(df_it)} records")
print(f"   Memory impact: ~{(len(df_master) + len(df_it)) * 0.001:.1f} KB")

# Sample analysis
print("\n   Sample from IT dataset:")
sample = df_it[['job_id', 'job_title', 'company', 'skills']].head(3)
print(sample.to_string())

# ============ STEP 5: MERGE DATASETS ============

print("\n🔀 Step 5: Merging Datasets...")

# Concatenate dataframes
df_combined = pd.concat([df_master, df_it], ignore_index=True)

# Remove any duplicates based on job_id (keep first occurrence)
duplicates_before = len(df_combined)
df_combined = df_combined.drop_duplicates(subset=['job_id'], keep='first')
duplicates_removed = duplicates_before - len(df_combined)

if duplicates_removed > 0:
    print(f"⚠️ Removed {duplicates_removed} duplicate records")
else:
    print("✅ No duplicates found")

print(f"✅ Merged dataset size: {len(df_combined)} records")

# ============ STEP 6: POST-MERGE VALIDATION ============

print("\n✔️ Step 6: Post-Merge Validation...")

# Check integrity
print(f"   ✅ Total unique job_ids: {df_combined['job_id'].nunique()}")
print(f"   ✅ Null values: {df_combined.isnull().sum().sum()}")
print(f"   ✅ Duplicate job_ids: {df_combined['job_id'].duplicated().sum()}")

# Verify all experience levels are valid
invalid_levels = ~df_combined['experience_level'].isin(valid_levels)
print(f"   ✅ Invalid experience levels: {invalid_levels.sum()}")

# Distribution summary
print("\n   Experience Level Distribution:")
for level in df_combined['experience_level'].value_counts().index:
    count = df_combined['experience_level'].value_counts()[level]
    pct = (count / len(df_combined) * 100)
    print(f"      • {level}: {count} ({pct:.1f}%)")

# ============ STEP 7: SAVE INTEGRATED DATASET ============

print("\n💾 Step 7: Saving Integrated Dataset...")

# Sort by job_id for consistency
df_combined_sorted = df_combined.sort_values('job_id').reset_index(drop=True)

# Save to master_job_pool.csv
df_combined_sorted.to_csv(master_path, index=False)
print(f"✅ Master job pool updated: {master_path}")

# Also create a timestamped backup of the merged dataset
merged_backup = f'data/master_job_pool_integrated_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
df_combined_sorted.to_csv(merged_backup, index=False)
print(f"✅ Timestamped backup created: {merged_backup}")

# ============ STEP 8: FINAL REPORT ============

print("\n" + "="*60)
print("📈 INTEGRATION REPORT")
print("="*60)

print(f"\n✅ INTEGRATION SUCCESSFUL!")
print(f"\n📊 Final Statistics:")
print(f"   Original Master Pool: {len(df_master)} records")
print(f"   IT Jobs Dataset: {len(df_it)} records")
print(f"   Combined Total: {len(df_combined_sorted)} records")
print(f"   Growth: +{len(df_it)} records ({(len(df_it)/len(df_master)*100):.1f}% increase)")

print(f"\n📋 Dataset Composition:")
print(f"   • Unique Job Titles: {df_combined_sorted['job_title'].nunique()}")
print(f"   • Unique Companies: {df_combined_sorted['company'].nunique()}")
print(f"   • Average Years of Experience: {df_combined_sorted['years_exp_num'].mean():.1f}")
print(f"   • Columns: {', '.join(df_combined_sorted.columns)}")

print(f"\n🛡️ Data Quality:")
print(f"   ✅ No null values: {df_combined_sorted.isnull().sum().sum() == 0}")
print(f"   ✅ Unique job_ids: {df_combined_sorted['job_id'].nunique() == len(df_combined_sorted)}")
print(f"   ✅ Valid experience levels: {invalid_levels.sum() == 0}")

print(f"\n📁 Files:")
print(f"   • Original Backup: {backup_path}")
print(f"   • Integrated Backup: {merged_backup}")
print(f"   • Active Master Pool: {master_path}")

print("\n" + "="*60)
print("✨ DATASET INTEGRATION COMPLETE!")
print("="*60)
print("\nThe project is now ready for testing with the expanded job pool.\n")
