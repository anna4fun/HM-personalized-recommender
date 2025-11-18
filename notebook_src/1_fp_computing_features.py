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

# Connect to Hopswork Feature Store
project, fs = hopsworks_integration.get_feature_store()