import numpy as np
import pandas as pd
class RankingEngine:
    def __init__(self, weights=None):
        # Default weights for the final score
        self.weights = weights or {
            'skills': 0.60,
            'experience': 0.25,
            'category': 0.15
        }

    def calculate_experience_score(self, user_exp, job_exp):
        """
        Calculates a score based on how close the user's exp is to the job's req.
        """
        # Perfect fit or slightly overqualified
        if user_exp >= job_exp and user_exp <= job_exp + 2:
            return 1.0
        # Underqualified (Linear penalty)
        elif user_exp < job_exp:
            return max(0, 1 - (job_exp - user_exp) * 0.2)
        # Significantly overqualified (Slight penalty)
        else:
            return 0.8 

    def rank_jobs(self, recommendations, user_category, user_exp):
        """
        Takes the initial matches and re-ranks them using hybrid logic.
        """
        final_results = []
        
        for _, row in recommendations.iterrows():
            # 1. Skill Score (already 0-100 from matcher)
            skill_score = row['match_score'] / 100
            
            # 2. Experience Score
            exp_score = self.calculate_experience_score(user_exp, row['years_exp_num'])
            
            # 3. Category Score (Binary check: is category in the job title?)
            category_score = 1.0 if user_category.lower() in row['job_title'].lower() else 0.5
            
            # Weighted Final Calculation
            final_score = (
                (skill_score * self.weights['skills']) +
                (exp_score * self.weights['experience']) +
                (category_score * self.weights['category'])
            ) * 100
            
            row['final_rank_score'] = round(final_score, 2)
            final_results.append(row)
            
        # Sort by the new hybrid score
        ranked_df = pd.DataFrame(final_results).sort_values(by='final_rank_score', ascending=False)
        return ranked_df
    