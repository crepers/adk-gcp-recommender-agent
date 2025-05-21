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

"""Defines tools for brand search optimization agent"""

import logging 
import datetime
from google.cloud import bigquery
from google.adk.tools import ToolContext
from ..shared_libraries import constants

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) # 기본 로깅 레벨 설정

# Initialize the BigQuery client outside the function
try:
    bq_client = bigquery.Client()  # Initialize client once
    logger.info("BigQuery client initialized successfully.")
except Exception as e:
    logger.critical(f"CRITICAL: Error initializing BigQuery client: {e}", exc_info=True)
    client = None  # Set client to None if initialization fails

# def execute_bigquery_sql(tool_context: ToolContext) -> dict:
def execute_bigquery_sql(query: str) -> dict:
    """
    주어진 BigQuery SQL 쿼리 문자열을 실행하고 결과를 반환합니다.

    Args:
        query (str): 실행할 전체 BigQuery SQL 쿼리 문자열.

    Returns:
        dict: 실행 상태, 데이터 또는 오류 정보를 포함하는 딕셔너리.
              성공 시: {"executed_query": str, "status": "success", "data": list[dict]}
              실패 시: {"executed_query": str, "status": "error", "error_message": str, 
                       "error_details": {"type": str, "message": str, "raw_errors": list | None}}
    """
    if bq_client is None:
        logger.error("BigQuery client is not initialized. Cannot execute query.")
        return {
            "executed_query": query,
            "status": "error",
            "error_message": "BigQuery client is not initialized.",
            "error_details": {"type": "ClientInitializationError", "message": "Client is None", "raw_errors": None}
        }
    # query = tool_context.user_content.parts[0].text
    logger.info(f"Executing BigQuery query: {query[:500]}...")

    try:
        query_job = bq_client.query(query, location=constants.BIG_QUERY_LOCATION)
        results = query_job.result()

        processed_data = []
        for row in results:
            row_dict = {}
            for key, value in row.items():
                if isinstance(value, (datetime.datetime, datetime.date)):
                    row_dict[key] = value.isoformat()  # Convert datetime to ISO string
                else:
                    row_dict[key] = value
            processed_data.append(row_dict)
        
        data = processed_data # Assign processed data

        logger.info(f"Query executed successfully. Number of rows returned: {len(data)}")

        return {
            "executed_query": query,
            "status": "success",
            "data": data
        }

    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        raw_errors = None

        # Google Cloud 관련 예외는 좀 더 상세한 오류 정보를 포함할 수 있습니다.
        if hasattr(e, 'errors') and e.errors:
            # e.errors는 보통 리스트이며, 각 항목은 오류 세부사항을 담은 딕셔너리입니다.
            # 예: [{'reason': 'notFound', 'message': 'Not found: Table my-project:my_dataset.non_existent_table'}]
            raw_errors = list(e.errors) # 복사해서 저장
            if raw_errors and isinstance(raw_errors, list) and len(raw_errors) > 0 and 'message' in raw_errors[0]:
                error_message = raw_errors[0]['message'] # 첫 번째 오류 메시지를 주 메시지로 사용

        logger.error(
            f"BigQuery query execution failed. Query: [{query[:500]}...]. ErrorType: {error_type}, Message: {error_message}",
            exc_info=True # 스택 트레이스 로깅
        )

        return {
            "executed_query": query,
            "status": "error",
            "error_message": error_message, # 가장 대표적인 오류 메시지
            "error_details": {"type": error_type, "message": str(e), "raw_errors": raw_errors}
        }