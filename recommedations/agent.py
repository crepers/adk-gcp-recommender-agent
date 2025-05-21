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

"""Recommender Data Analysis Agent"""

from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool

from .shared_libraries import constants
from .tools import bq_connector
from . import prompt
from .sub_agents import result_formatter_prompt, recommender_query_gen_prompt


query_target_table_agent = Agent(
    model=constants.MODEL,
    name="query_target_table_agent",
    description="Identifies the single most relevant BigQuery table (recommendations_export or insights_export) to query based on the user's request.",
    instruction=recommender_query_gen_prompt.QUERY_TARGET_TABLE_PROMPT,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

recommendations_sql_generator_agent = Agent(
    model=constants.MODEL,
    name="recommendations_sql_generator_agent",
    description="BigQuery SQL query **specifically for the 'recommendations_export' table**.",
    instruction=recommender_query_gen_prompt.RECOMMENDATIONS_SQL_GENERATOR_PROMPT_TEMPLATE,
    disallow_transfer_to_parent=False,
    disallow_transfer_to_peers=True,
)

insights_sql_generator_agent = Agent(
    model=constants.MODEL,
    name="insights_sql_generator_agent",
    description="BigQuery SQL query **specifically for the 'insights_export' table**.",
    instruction=recommender_query_gen_prompt.INSIGHTS_SQL_GENERATOR_PROMPT_TEMPLATE,
    disallow_transfer_to_parent=False,
    disallow_transfer_to_peers=True,
)

result_formatter_agent = Agent(
    model=constants.MODEL,
    name="result_formatter_agent",
    description="A helpful agent to find keywords",
    instruction=result_formatter_prompt.RESULT_FORMATTER_AGENT_PROMPT,
    tools=[
        bq_connector.execute_bigquery_sql,
    ],
    disallow_transfer_to_parent=False,
    disallow_transfer_to_peers=True,
)

root_agent = Agent(
    model=constants.MODEL,
    name="recommender_data_analysis_agent",
    description="Orchestrates the generation of BigQuery SQL queries by first identifying the target table and then generating the SQL and then execute the query for that table.",
    instruction=prompt.ROOT_PROMPT,
    tools=[
        AgentTool(query_target_table_agent),
        AgentTool(recommendations_sql_generator_agent),
        AgentTool(insights_sql_generator_agent),
        bq_connector.execute_bigquery_sql,
        AgentTool(result_formatter_agent),
    ],
    disallow_transfer_to_parent=False,
    disallow_transfer_to_peers=False,
)