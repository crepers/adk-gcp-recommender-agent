# Google Cloud Recommender 데이터 조회 및 분석 Agent

## 프로젝트 개요
본 프로젝트는 Google Cloud Recommender에서 BigQuery로 Export된 추천 및 인사이트 데이터를 사용자가 자연어 질문을 통해 효과적으로 조회하고, 그 결과를 이해하기 쉬운 형태로 받아볼 수 있도록 지원하는 AI Agent 시스템입니다. 복잡한 SQL 작성 없이도 클라우드 최적화에 필요한 정보를 얻을 수 있도록 설계되었습니다.

## 주요 기능
- 자연어 질의 이해: 사용자의 자연어 질문을 분석하여 의도를 파악합니다.
- 동적 SQL 생성: 분석된 의도와 대상 테이블(추천 또는 인사이트)에 맞춰 BigQuery SQL 쿼리를 동적으로 생성합니다.
  - 테이블 스키마 및 Google Cloud 프로젝트/데이터셋 정보를 활용합니다.
  - 사용자 질문 내의 상대적인 시간 표현(예: "지난 주", "오늘")을 해석하여 쿼리 조건에 반영합니다.
- BigQuery 쿼리 실행: 생성된 SQL 쿼리를 지정된 Google Cloud 지역의 BigQuery에서 실행합니다.
- 결과 포맷팅: 조회된 원시 데이터 또는 오류 정보를 사람이 읽기 쉬운 텍스트 (Markdown 형식)로 가공하여 제공합니다.
- 모듈식 Agent 아키텍처: 각 기능을 전문화된 Agent로 분리하여 유연성과 확장성을 확보했습니다.

## 시스템 아키텍처
본 시스템은 다음과 같은 계층적 Agent 구조로 구성됩니다:

1. 루트 Agent (Root Agent):
  - 사용자와 직접 상호작용하는 최상위 Agent입니다.
  - 사용자 질문이 Google Cloud Recommender 관련인지 판단합니다.
  - 관련 질문일 경우, Recommender 데이터 분석 Agent에게 작업을 위임합니다.
  - Recommender 데이터 분석 Agent로부터 최종적으로 포맷팅된 결과를 받아 사용자에게 전달합니다.

2. Recommender 데이터 분석 Agent (Main Orchestrator Agent):
  - 루트 Agent로부터 사용자 질문을 전달받아, 데이터 조회 및 결과 포맷팅까지의 전체 과정을 총괄하는 핵심 오케스트레이터입니다.
  - 다음과 같은 도구(AgentTool 또는 직접 함수 호출)를 순차적으로 사용합니다:
    - query_target_table_agent (AgentTool)
    - recommendations_sql_generator_agent 또는 insights_sql_generator_agent (AgentTool - 조건부 호출)
    - execute_bigquery_sql (직접 호출 Python 함수 도구)
    - result_formatter_agent (AgentTool)

## 주요 Agent 및 도구 설명
1. 루트 Agent (RECOMMENDER_ROOT_AGENT_PROMPT 사용)
  - 역할: 사용자 입력 처리 및 기본 라우팅.
  - 입력: 사용자의 자연어 질문.
  - 처리:
    - 질문의 Recommender 관련성 판단.
    - 관련 시, recommender_data_analysis_agent 호출 (입력: {"request": {"user_query": "사용자 질문"}} - user_query 객체를 JSON 문자열화).
  - 출력: recommender_data_analysis_agent로부터 받은 최종 포맷팅된 문자열 응답을 사용자에게 전달.
2. Recommender 데이터 분석 Agent (MAIN_ORCHESTRATOR_PROMPT_TEMPLATE 사용)
  - 역할: SQL 생성, 실행, 결과 포맷팅까지의 전체 워크플로우 오케스트레이션.
  - 입력: 루트 Agent로부터 받은 JSON 문자열 ({"request": {"user_query": "사용자 질문"}}). (내부적으로 JSON 파싱하여 user_query 추출)
  - 내부 도구 및 순서:
    1. query_target_table_agent 호출:
      - 입력: {"request": "추출된_사용자_질문"}
      - 출력: selected_table_name ("recommendations_export" 또는 "insights_export")
    2. 조건부 SQL 생성 Agent 호출:
      - selected_table_name에 따라 recommendations_sql_generator_agent 또는 insights_sql_generator_agent 호출.
      - 입력: {"request": {"user_query": "추출된_사용자_질문"}} (각 SQL 생성 Agent는 자체 프롬프트에 스키마, Project ID, Dataset ID 내장)
      - 출력: generated_sql_query (완전 정규화된 SQL)
    3. execute_bigquery_sql 직접 함수 호출:
      - 입력: query=generated_sql_query, location=QUERY_EXECUTION_REGION (상수 값)
      - 출력: execution_outcome 딕셔너리 (실행된 쿼리, 상태, 데이터/오류 메시지, 사용된 위치 등 포함)
    4. result_formatter_agent 호출:
      - 입력 객체: {"query_execution_result": execution_outcome, "original_user_query": "추출된_사용자_질문"}
      - 이 객체를 JSON 문자열로 변환하여 {"request": "변환된_JSON_문자열"} 형태로 전달.
      - 출력: formatted_user_response (사람이 읽기 쉬운 문자열)
  - 출력: formatted_user_response 문자열을 루트 Agent에게 반환.

3. query_target_table_agent (QUERY_TARGET_TABLE_PROMPT 사용)
  - 역할: 사용자 질문을 분석하여 recommendations_export 또는 insights_export 중 어떤 테이블을 조회해야 하는지 결정.
  - 입력: 사용자 질문 문자열 (request 키 아래).
  - 출력: 테이블 이름 문자열 ("recommendations_export" 또는 "insights_export").

4. recommendations_sql_generator_agent (RECOMMENDATIONS_SQL_GENERATOR_PROMPT 사용)
  - 역할: recommendations_export 테이블에 대한 SQL 쿼리 생성.
  - 내부 지식: recommendations_export의 간결화된 스키마, PROJECT_ID, DATASET_ID가 프롬프트에 내장.
  - 입력: user_query가 포함된 객체를 request 키 아래 JSON 문자열로 받음 (예: {"request": {"user_query": "사용자 질문"}}). 내부적으로 JSON 파싱.
  - 처리: user_query 내의 상대 시간 표현을 자체 실행 시점 기준으로 해석하여 SQL 조건 생성.
  - 출력: PROJECT_ID.DATASET_ID.recommendations_export를 대상으로 하는 완전 정규화된 SQL 쿼리 문자열.

5. insights_sql_generator_agent (INSIGHTS_SQL_GENERATOR_PROMPT 사용)
  - 역할: insights_export 테이블에 대한 SQL 쿼리 생성.
  - 내부 지식: insights_export의 간결화된 스키마, PROJECT_ID, DATASET_ID가 프롬프트에 내장.
  - 입력/처리/출력: recommendations_sql_generator_agent와 유사하나, 대상 테이블과 스키마가 다름.

6. execute_bigquery_sql (Python 함수)
  - 역할: 전달받은 SQL 쿼리를 BigQuery에서 지정된 위치(region)에서 실행.
  - 입력: query (SQL 문자열), location (지역 문자열, optional).
  - 출력: 실행 결과를 담은 Python 딕셔너리 (실행된 쿼리, 상태, 데이터 또는 오류 메시지, 사용된 위치 등 포함). datetime 객체는 JSON 직렬화를 위해 ISO 문자열로 변환됨.

7. result_formatter_agent (RESULT_FORMATTER_AGENT_PROMPT 사용)
  - 역할: execute_bigquery_sql의 결과(성공 데이터 또는 오류 정보)와 원본 사용자 질문을 받아 사람이 읽기 쉬운 텍스트/Markdown으로 변환.
  - 입력: query_execution_result 객체와 original_user_query 문자열을 포함하는 객체를 request 키 아래 JSON 문자열로 받음. 내부적으로 JSON 파싱.
  - 출력: 최종 사용자에게 보여줄 포맷팅된 문자열.

## 데이터 흐름 요약
- 사용자: 자연어 질문 입력.
- 루트 Agent: 질문 수신 -> recommender_data_analysis_agent 호출 (입력: {"request": {"user_query": "질문"}}).
- Recommender 데이터 분석 Agent:
  1. query_target_table_agent 호출 -> selected_table_name 획득.
  2. selected_table_name에 따라 recommendations_sql_generator_agent 또는 insights_sql_generator_agent 호출 (입력: {"request": {"user_query": "질문"}}) -> generated_sql_query 획득.
  3. execute_bigquery_sql 함수 호출 (입력: generated_sql_query, location) -> execution_outcome 획득.
  4. result_formatter_agent 호출 (입력: {"request": {"query_execution_result": execution_outcome, "original_user_query": "질문"}}) -> formatted_user_response 획득.
  5. formatted_user_response를 루트 Agent에게 반환.
- 루트 Agent: formatted_user_response를 사용자에게 최종 표시.

## 주요 설정 및 가정
- 상수 값: BigQuery PROJECT_ID, DATASET_ID, QUERY_EXECUTION_REGION 등은 Python 상수 파일 (예: constants.py)에 정의되어 있으며, 각 Agent 프롬프트 생성 시 동적으로 주입됩니다.
- 스키마 파일: recommendations_export 및 insights_export 테이블의 간결화된 스키마 정의는 별도의 Python 파일 (예: table_recommendations_export.py)에 문자열 변수로 저장되어 있으며, 필요한 Agent 프롬프트 생성 시 주입됩니다.
- ADK (Agent Development Kit): 특정 ADK를 사용하여 Agent 및 Tool을 구성하고 있으며, AgentTool로 호출되는 Agent는 입력 인자를 {"request": 실제_입력_또는_JSON화된_입력} 형태로 받습니다. 복잡한 입력은 호출하는 쪽에서 JSON 문자열로 변환하여 전달하고, 호출받는 Agent는 이를 파싱합니다.

## 오류 처리
- 각 Agent는 작업 실패 시 오류 정보를 반환하도록 설계되었습니다.
- Recommender 데이터 분석 Agent는 하위 도구에서 오류 발생 시, 해당 오류 정보를 result_formatter_agent에 전달하여 사용자 친화적인 오류 메시지를 생성하려고 시도합니다.
- execute_bigquery_sql 함수는 BigQuery 클라이언트 오류 및 쿼리 실행 오류를 감지하고 구조화된 오류 객체를 반환합니다. datetime 객체는 JSON 직렬화 가능한 형태로 변환합니다.