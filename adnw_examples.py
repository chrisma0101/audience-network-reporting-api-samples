from adnw_requests import *
from adnw_utils import *
from adnw_response import *
from time import sleep


""" Run sync request, but there are some limitations.
    Support only one metric and two max breakdowns per request. 
"""
def run_sync_request(app_id, access_token):
    builder = ADNWRequestBuilder(app_id, access_token)
    builder.add_metric(Metric.ADNW_IMPRESSION)
    builder.add_filter(Filter(Breakdown.COUNTRY, FilterOperator.IN, ['US', 'JP']))
    builder.add_filter(Filter(Breakdown.PLATFORM, FilterOperator.IN, ['ios', 'android', 'unknown']))
    builder.add_breakdown(Breakdown.COUNTRY)
    builder.add_breakdown(Breakdown.PLATFORM)
    sync_request = builder.build_sync_request()
    ADNWResponse.get_instance().validate_response(sync_request)
    adnw_utils.write_to_csv(sync_request.json())
    print("Finish writing to csv, check 'csv_reports/report.csv' in root directory.")


""" Run async request to get request id (no limitations on params),
    then run sync request with request id.
    No max metric and breakdowns per request. 
"""
def run_async_request_1(app_id, access_token):
    builder = ADNWRequestBuilder(app_id, access_token)
    builder.add_metric(Metric.ADNW_IMPRESSION)
    builder.add_metric(Metric.ADNW_REQUEST)
    builder.add_filter(Filter(Breakdown.COUNTRY, FilterOperator.IN, ['US', 'JP']))
    builder.add_filter(Filter(Breakdown.PLATFORM, FilterOperator.IN, ['ios', 'android']))
    builder.add_breakdown(Breakdown.COUNTRY)
    builder.add_breakdown(Breakdown.DELIVERY_METHOD)
    async_request = builder.build_async_request()
    adnw_response = ADNWResponse.get_instance()
    adnw_response.validate_response(async_request)
    query_id = adnw_response.get_query_id(async_request.json())
    print("Successfully get valid query id: " + query_id)
    return query_id


""" Run multiple async request to get request ids (no limitations on params),
    then run sync request with multiple request ids.
    No max metric and breakdowns per request. 
"""
def run_async_request_2(app_id, access_token):
    builder = ADNWRequestBuilder(app_id, access_token)
    builder.add_metric(Metric.ADNW_CMP)
    builder.add_metric(Metric.ADNW_CLICK)
    builder.add_filter(Filter(Breakdown.COUNTRY, FilterOperator.IN, ['MK', 'SB']))
    builder.add_filter(Filter(Breakdown.PLATFORM, FilterOperator.IN, ['ios', 'unknown']))
    builder.add_breakdown(Breakdown.PLATFORM)
    builder.add_breakdown(Breakdown.PLACEMENT)
    async_request = builder.build_async_request()
    adnw_response = ADNWResponse.get_instance()
    adnw_response.validate_response(async_request)
    query_id = adnw_response.get_query_id(async_request.json())
    print("Successfully get valid query id: " + query_id)
    return query_id


def run_async_request_for_result_1(app_id, access_token):
    query_id = run_async_request_1(app_id, access_token)
    try_run_async_request_with_query_ids(app_id, access_token, [query_id])


def run_async_request_for_result_2(app_id, access_token):
    query_id_1 = run_async_request_1(app_id, access_token)
    query_id_2 = run_async_request_2(app_id, access_token)
    try_run_async_request_with_query_ids(app_id, access_token, [query_id_1, query_id_2])


def try_run_async_request_with_query_ids(app_id, access_token, query_ids: [string]):
    for i in range(0, 3):
        try:
            run_async_request_with_query_ids(app_id, access_token, query_ids)
            break
        except adnw_exception.ValidationError as error:
            print(error.message)
            sleep(0.3)
            continue


def run_async_request_with_query_ids(app_id, access_token, query_ids: [string]):
    builder = ADNWRequestBuilder(app_id, access_token)
    builder.set_query_ids(query_ids)
    sync_request = builder.build_sync_request_with_query_ids()
    ADNWResponse.get_instance().validate_response(sync_request)
    adnw_utils.write_to_csv(sync_request.json())
    print("Finish writing to csv, check 'csv_reports/report.csv' in root directory.")


if __name__ == '__main__':

    """Replace with your app_id and valid access_token to start your testing."""
    _app_id = "YOUR_APP_ID"
    _access_token = "USER_ACCESS_TOKEN"

    """Uncomment corresponding function for testing."""
    # run_sync_request(_app_id, _access_token)

    # run_async_request_for_result_1(_app_id, _access_token)

    run_async_request_for_result_2(_app_id, _access_token)