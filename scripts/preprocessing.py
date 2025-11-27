
"""
Data Preprocessing Script
Task 1: Data Preprocessing

This script cleans and preprocesses the scraped reviews data.

- Handles missing values
- Normalizes dates
- Cleans text data
- Removes duplicate rows
- Filters out reviews written in Amharic (non-English)
"""

import sys
import os
import re
import pandas as pd
import numpy as np
from datetime import datetime
from config import DATA_PATHS

# Add parent directory to path to allow importing modules from there
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def contains_amharic(text):
    """Detect if text contains any Amharic characters."""
    pattern = re.compile(r'[\u1200-\u137F]')
    return bool(pattern.search(str(text)))  # ensure text is string

class ReviewPreprocessor:
    """Preprocessor class for review data"""

    def __init__(self, input_path=None, output_path=None):
        self.input_path = input_path or DATA_PATHS['raw_reviews']
        self.output_path = output_path or DATA_PATHS['processed_reviews']
        self.df = None
        self.stats = {}

    def load_data(self):
        print("Loading raw data...")
        try:
            self.df = pd.read_csv(self.input_path)
            print(f"Loaded {len(self.df)} reviews")
            self.stats['original_count'] = len(self.df)
            return True
        except FileNotFoundError:
            print(f"ERROR: File not found: {self.input_path}")
            return False
        except Exception as e:
            print(f"ERROR: Failed to load data: {str(e)}")
            return False

    def check_missing_data(self):
        print("\n[1/7] Checking for missing data...")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        print("\nMissing values:")
        for col in missing.index:
            if missing[col] > 0:
                print(f"  {col}: {missing[col]} ({missing_pct[col]:.2f}%)")
        self.stats['missing_before'] = missing.to_dict()

        critical_cols = ['review_text', 'rating', 'bank_name']
        missing_critical = self.df[critical_cols].isnull().sum()
        if missing_critical.sum() > 0:
            print("\nWARNING: Missing values in critical columns:")
            print(missing_critical[missing_critical > 0])

    def handle_missing_values(self):
        print("\n[2/7] Handling missing values...")
        critical_cols = ['review_text', 'rating', 'bank_name']
        before_count = len(self.df)
        self.df = self.df.dropna(subset=critical_cols)
        removed = before_count - len(self.df)
        if removed > 0:
            print(f"Removed {removed} rows with missing critical values")

        # Fill optional columns with defaults
        if 'user_name' in self.df.columns:
            self.df['user_name'] = self.df['user_name'].fillna('Anonymous')
        if 'thumbs_up' in self.df.columns:
            self.df['thumbs_up'] = self.df['thumbs_up'].fillna(0)
        if 'reply_content' in self.df.columns:
            self.df['reply_content'] = self.df['reply_content'].fillna('')

        self.stats['rows_removed_missing'] = removed
        self.stats['count_after_missing'] = len(self.df)

    def normalize_dates(self):
        print("\n[3/7] Normalizing dates...")
        try:
            self.df['review_date'] = pd.to_datetime(self.df['review_date'])
            self.df['review_date'] = self.df['review_date'].dt.date
            self.df['review_year'] = pd.to_datetime(self.df['review_date']).dt.year
            self.df['review_month'] = pd.to_datetime(self.df['review_date']).dt.month
            print(f"Date range: {self.df['review_date'].min()} to {self.df['review_date'].max()}")
        except Exception as e:
            print(f"WARNING: Error normalizing dates: {str(e)}")

    def clean_text(self):
        print("\n[4/7] Cleaning text...")

        def clean_review_text(text):
            if pd.isna(text) or text == '':
                return ''
            text = str(text)
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            return text


        self.df['review_text'] = self.df['review_text'].apply(clean_review_text)

        before_count = len(self.df)
        self.df = self.df[self.df['review_text'].str.len() > 0]
        removed = before_count - len(self.df)
        if removed > 0:
            print(f"Removed {removed} reviews with empty text")

        # Create text_length column here! This is critical for downstream steps.
        self.df['text_length'] = self.df['review_text'].str.len()

        self.stats['empty_reviews_removed'] = removed
        self.stats['count_after_cleaning'] = len(self.df)

    def remove_duplicates(self):
        print("\n[5/7] Removing duplicate reviews...")
        before_count = len(self.df)
        # Drop exact duplicate rows - customize subset if needed
        self.df = self.df.drop_duplicates()
        removed = before_count - len(self.df)
        if removed > 0:
            print(f"Removed {removed} duplicate reviews")
        else:
            print("No duplicate reviews found")
        self.stats['duplicates_removed'] = removed

    def filter_non_english_reviews(self):
        print("\n[6/7] Filtering out Amharic (non-English) reviews...")
        before_count = len(self.df)
        self.df = self.df[~self.df['review_text'].apply(contains_amharic)]
        removed = before_count - len(self.df)
        if removed > 0:
            print(f"Removed {removed} reviews containing Amharic characters")
        else:
            print("No Amharic reviews found")
        self.stats['amharic_reviews_removed'] = removed

    def validate_ratings(self):
        print("\n[7/7] Validating ratings...")
        invalid = self.df[(self.df['rating'] < 1) | (self.df['rating'] > 5)]
        if len(invalid) > 0:
            print(f"WARNING: Found {len(invalid)} reviews with invalid ratings")
            self.df = self.df[(self.df['rating'] >= 1) & (self.df['rating'] <= 5)]
        else:
            print("All ratings are valid (1-5)")
        self.stats['invalid_ratings_removed'] = len(invalid)

    def prepare_final_output(self):
        print("\nPreparing final output...")

        output_columns = [
            'review_id',
            'review_text',
            'rating',
            'review_date',
            'review_year',
            'review_month',
            'bank_code',
            'bank_name',
            'user_name',
            'thumbs_up',
            'text_length',
            'source'
        ]

        # Only include columns that exist, especially text_length
        output_columns = [col for col in output_columns if col in self.df.columns]
        self.df = self.df[output_columns]

        # Sort by bank_code ascending and review_date descending
        self.df = self.df.sort_values(['bank_code', 'review_date'], ascending=[True, False])
        self.df = self.df.reset_index(drop=True)

        print(f"Final dataset: {len(self.df)} reviews")

    def save_data(self):
        print("\nSaving processed data...")
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            self.df.to_csv(self.output_path, index=False)
            print(f"Data saved to: {self.output_path}")
            self.stats['final_count'] = len(self.df)
            return True
        except Exception as e:
            print(f"ERROR: Failed to save data: {str(e)}")
            return False

    def generate_report(self):
        print("\n" + "=" * 60)
        print("PREPROCESSING REPORT")
        print("=" * 60)

        print(f"\nOriginal records: {self.stats.get('original_count', 0)}")
        print(f"Records with missing critical data: {self.stats.get('rows_removed_missing', 0)}")
        print(f"Empty reviews removed: {self.stats.get('empty_reviews_removed', 0)}")
        print(f"Duplicate reviews removed: {self.stats.get('duplicates_removed', 0)}")
        print(f"Amharic reviews removed: {self.stats.get('amharic_reviews_removed', 0)}")
        print(f"Invalid ratings removed: {self.stats.get('invalid_ratings_removed', 0)}")
        print(f"Final records: {self.stats.get('final_count', 0)}")

        if self.stats.get('original_count', 0) > 0:
            retention_rate = (self.stats.get('final_count', 0) / self.stats.get('original_count', 1)) * 100
            error_rate = 100 - retention_rate
            print(f"\nData retention rate: {retention_rate:.2f}%")
            print(f"Data error rate: {error_rate:.2f}%")

            if error_rate < 5:
                print("✓ Data quality: EXCELLENT (<5% errors)")
            elif error_rate < 10:
                print("✓ Data quality: GOOD (<10% errors)")
            else:
                print("⚠️ Data quality: NEEDS ATTENTION (>10% errors)")

        if self.df is not None:
            print("\nReviews per bank:")
            bank_counts = self.df['bank_name'].value_counts()
            for bank, count in bank_counts.items():
                print(f"  {bank}: {count}")

            print("\nRating distribution:")
            rating_counts = self.df['rating'].value_counts().sort_index(ascending=False)
            for rating, count in rating_counts.items():
                pct = (count / len(self.df)) * 100
                print(f"  {'⭐️' * int(rating)}: {count} ({pct:.1f}%)")

            print(f"\nDate range: {self.df['review_date'].min()} to {self.df['review_date'].max()}")

            print(f"\nText statistics:")
            print(f"  Average length: {self.df['text_length'].mean():.0f} characters")
            print(f"  Median length: {self.df['text_length'].median():.0f} characters")
            print(f"  Min length: {self.df['text_length'].min()}")
            print(f"  Max length: {self.df['text_length'].max()}")

    def process(self):
        print("=" * 60)
        print("STARTING DATA PREPROCESSING")
        print("=" * 60)

        if not self.load_data():
            return False

        self.check_missing_data()
        self.handle_missing_values()
        self.normalize_dates()
        self.clean_text()                # text_length created here
        self.remove_duplicates()         # remove duplicate rows here
        self.filter_non_english_reviews()
        self.validate_ratings()
        self.prepare_final_output()      # accesses text_length, so must come after clean_text
        if self.save_data():
            self.generate_report()
            return True

        return False


def main():
    preprocessor = ReviewPreprocessor()
    success = preprocessor.process()
    if success:
        print("\n✓ Preprocessing completed successfully!")
        return preprocessor.df
    else:
        print("\n✗ Preprocessing failed!")
        return None


if __name__ == "__main__":
    processed_df = main()