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

TABLE_INSIGHTS_EXPORT = """
schema:
  - fields:
      - name: cloud_entity_type
        type: STRING
        description: "Cloud entity type (e.g., project, billing account)."
      - name: cloud_entity_id
        type: STRING
        description: "Project number or billing account ID."
      - name: name
        type: STRING
        description: "Insight name. Format: projects/[PROJECT_NUMBER]/locations/[LOCATION]/insightTypes/[INSIGHT_TYPE_ID]/insights/[INSIGHT_ID]"
      - name: location
        type: STRING
        description: "Location of the insight."
      - name: insight_type
        type: STRING
        description: "ID of the InsightType that produced this insight (e.g., google.iam.policy.Insight)."
      - name: insight_subtype
        type: STRING
        description: "Subtype identifier for insights from the same insight_type (e.g., for 'google.iam.security.SecurityHealthAnalyticsInsight': 'SERVICE_ACCOUNT_KEY_UNUSED')."
      - name: target_resources
        type: STRING
        mode: REPEATED
        description: "Fully qualified names of resources this insight pertains to. Always populated. Ex: [//cloudresourcemanager.googleapis.com/projects/foo]."
      - name: description
        type: STRING
        description: "Required. Human-readable summary in English (max 500 chars)."
      - name: last_refresh_time
        type: TIMESTAMP
        description: "Output only. Last refresh time of this insight."
      - name: category
        type: STRING
        description: "Insight category: COST, SECURITY, PERFORMANCE, MANAGEABILITY, RELIABILITY. Avoid CATEGORY_UNSPECIFIED."
      - name: state
        type: STRING
        description: "Output only. Insight state: ACTIVE, CLAIMED, SUCCEEDED, FAILED, DISMISSED. Avoid STATE_UNSPECIFIED."
      - name: ancestors
        type: RECORD
        description: "Ancestry for the insight entity."
        schema:
          fields:
          - name: organization_id
            type: STRING
            description: "Organization ID."
          - name: folder_ids
            type: STRING
            mode: REPEATED
            description: "Up to 5 parent folder IDs."
      - name: associated_recommendations
        type: STRING
        mode: REPEATED
        description: "Associated recommendation names. Format: projects/[PROJECT_NUMBER]/locations/[LOCATION]/recommenders/[RECOMMENDER_ID]/recommendations/[RECOMMENDATION_ID]"
      - name: insight_details # Assuming JSON string content
        type: STRING
        description: "Additional details about the insight in JSON string format (may include 'content' like custom fields, 'observation_period', 'state_metadata')."
      - name: severity
        type: STRING
        description: "Insight severity: CRITICAL, HIGH, MEDIUM, LOW. Avoid SEVERITY_UNSPECIFIED."
"""