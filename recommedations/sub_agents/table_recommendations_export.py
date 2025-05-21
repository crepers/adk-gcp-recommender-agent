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

TABLE_RECOMMENDATIONS_EXPORT = """
schema:
   fields:
     - name: cloud_entity_type
       type: STRING
       description: "Cloud entity type (e.g., project, billing account)."
     - name: cloud_entity_id
       type: STRING
       description: "Project number or billing account ID."
     - name: name
       type: STRING
       description: "Recommendation name. Format: projects/[PROJECT_NUMBER]/locations/[LOCATION]/recommenders/[RECOMMENDER_ID]/recommendations/[RECOMMENDATION_ID]"
     - name: location
       type: STRING
       description: "Location of the recommendation."
     - name: recommender
       type: STRING
       description: "ID of the recommender that produced this."
     - name: recommender_subtype
       type: STRING
       description: "Subtype identifier for recommendations from the same recommender (e.g., for 'google.iam.policy.Recommender': 'REMOVE_ROLE' or 'REPLACE_ROLE')."
     - name: target_resources
       type: STRING
       mode: REPEATED
       description: "Fully qualified names of resources changed by this recommendation. Always populated. Ex: [//cloudresourcemanager.googleapis.com/projects/foo]."
     - name: description
       type: STRING
       description: "Required. Human-readable summary in English (max 500 chars)."
     - name: last_refresh_time
       type: TIMESTAMP
       description: "Output only. Last refresh time of this recommendation."
     - name: primary_impact
       type: RECORD
       description: "Required. Primary impact of this recommendation."
       schema:
         fields:
         - name: category
           type: STRING
           description: "Target category: COST, SECURITY, PERFORMANCE, RELIABILITY. Avoid CATEGORY_UNSPECIFIED."
         - name: cost_projection
           type: RECORD
           description: "Optional. Use with COST category."
           schema:
             fields:
             - name: cost
               type: RECORD
               description: "Approximate cost saved (negative units) or incurred (positive units)."
               schema:
                 fields:
                 - name: currency_code
                   type: STRING
                   description: "ISO 4217 currency code (e.g., USD)."
                 - name: units
                   type: INTEGER
                   description: "Whole units of amount."
                 - name: nanos
                   type: INTEGER
                   description: "Nano (10^-9) units. For $-1.75: units=-1, nanos=-750M. Range: +/-999,999,999."
             - name: cost_in_local_currency
               type: RECORD
               description: "Approximate cost in local currency (similar to 'cost' field)."
               schema: # Assuming similar concise descriptions for sub-fields as 'cost'
                 fields:
                 - name: currency_code
                   type: STRING
                   description: "ISO 4217 currency code."
                 - name: units
                   type: INTEGER
                   description: "Whole units of amount."
                 - name: nanos
                   type: INTEGER
                   description: "Nano (10^-9) units. Range: +/-999,999,999."
             - name: duration
               type: RECORD
               description: "Duration for which this cost applies."
               schema:
                 fields:
                 - name: seconds
                   type: INTEGER
                   description: "Signed seconds of time span. Range approx. +/-10,000 years."
                 - name: nanos
                   type: INTEGER
                   description: "Signed nano fractions of a second. Range: +/-999,999,999."
             - name: pricing_type_name
               type: STRING
               description: "Pricing type: LIST or CUSTOM."
         - name: reliability_projection
           type: RECORD
           description: "Optional. Use with RELIABILITY category."
           schema:
             fields:
             - name: risk_types
               type: STRING
               mode: REPEATED
               description: "Risk types: SERVICE_DISRUPTION, DATA_LOSS, ACCESS_DENY. Avoid RISK_TYPE_UNSPECIFIED."
             - name: details_json
               type: STRING
               description: "Additional reliability impact details in JSON string format."
     - name: state
       type: STRING
       description: "Output only. State: ACTIVE, CLAIMED, SUCCEEDED, FAILED, DISMISSED. Avoid STATE_UNSPECIFIED. Content immutable if not ACTIVE."
     - name: ancestors
       type: RECORD
       description: "Ancestry for the recommendation entity."
       schema:
         fields:
         - name: organization_id
           type: STRING
           description: "Organization ID."
         - name: folder_ids
           type: STRING
           mode: REPEATED
           description: "Up to 5 parent folder IDs."
     - name: associated_insights
       type: STRING
       mode: REPEATED
       description: "Associated insight names. Format: projects/[PROJECT_NUMBER]/.../insights/[INSIGHT_ID]"
     - name: recommendation_details # Critical decision here!
       type: STRING
       description: "Additional details about the recommendation in JSON string format." # Simplest, if internal structure isn't queried via NL.
     - name: priority
       type: STRING
       description: "Priority: P1 (Highest), P2, P3, P4 (Lowest). Avoid PRIORITY_UNSPECIFIED."
"""