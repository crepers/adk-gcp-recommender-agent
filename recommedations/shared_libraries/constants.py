# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines constants."""

import os
import dotenv

dotenv.load_dotenv()

AGENT_NAME = "recommender_data_analysis_agent"
DESCRIPTION = "A helpful assistant for analyze recommendation data exported from Google Cloud Recommender."
PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "EMPTY")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
MODEL = os.getenv("MODEL", "gemini-2.0-flash-001")
BIG_QUERY_PROJECT = os.getenv("BIG_QUERY_PROJECT", "EMPTY")
BIG_QUERY_LOCATION = os.getenv("BIG_QUERY_LOCATION", "us-central1")
BIG_QUERY_DATASET = os.getenv("BIG_QUERY_DATASET", "EMPTY")
DATASET_ID = os.getenv("DATASET_ID", "products_data_agent")
DISABLE_WEB_DRIVER = int(os.getenv("DISABLE_WEB_DRIVER", 0))
WHL_FILE_NAME = os.getenv("ADK_WHL_FILE", "")
STAGING_BUCKET = os.getenv("STAGING_BUCKET", "")
