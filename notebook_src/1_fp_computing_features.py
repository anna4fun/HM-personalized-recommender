import warnings
from pprint import pprint

import polars as pl
import torch
from loguru import logger
from sentence_transformers import SentenceTransformer

warnings.filterwarnings("ignore")

from recsys import hopsworks_integration
from recsys.config import settings
from recsys.features.articles import (
    compute_features_articles,
    generate_embeddings_for_dataframe,
)
from recsys.features.customers import DatasetSampler, compute_features_customers
from recsys.features.interaction import generate_interaction_data
from recsys.features.ranking import compute_ranking_dataset
from recsys.features.transactions import compute_features_transactions
from recsys.hopsworks_integration import feature_store


# These are the default settings used across the lessons. You can always override them in the .env file that sits at the root of the repository:
pprint(dict(settings))
DatasetSampler.get_supported_sizes()  # Large: 50K, Medium 5K, Small 1K; use 1K

# Connect to Hopsworks Feature Store
project, fs = hopsworks_integration.get_feature_store() # Yay! It passed!

# Load the H&M dataset
# article ID: every individual cloth is named article, every article has a unique ID
# product code: parents/categories of article ID, article ID to product code are "many to one" relationship
from recsys.raw_data_sources import h_and_m as h_and_m_raw_data
articles_df = h_and_m_raw_data.extract_articles_df()
articles_df.shape # (105542, 25): 105k articles
articles_df.columns
articles_df.null_count()
# article feature engineering
articles_df = compute_features_articles(articles_df)

for i, desc in enumerate(articles_df["article_description"].head(n=3)):
    logger.info(f"Item {i+1}:\n{desc}")