from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from llm_web_kit.model.resource_utils.boto3_ext import (get_s3_client,
                                                        get_s3_config,
                                                        head_s3_object,
                                                        is_s3_404_error,
                                                        is_s3_path,
                                                        split_s3_path)


def test_is_s3_path():
    assert is_s3_path('s3://bucket/key')
    assert not is_s3_path('bucket/key')


def test_is_s3_404_error():
    not_found_error = ClientError(
        error_response={
            'Error': {
                'Code': '404',
                'Message': 'Not Found'
            },
            'ResponseMetadata': {
                'HTTPStatusCode': 404
            },
        },
        operation_name='test',
    )
    assert is_s3_404_error(not_found_error)

    not_404_error = ClientError(
        error_response={
            'Error': {
                'Code': '403',
                'Message': 'Forbidden'
            },
            'ResponseMetadata': {
                'HTTPStatusCode': 403
            },
        },
        operation_name='test',
    )
    assert not is_s3_404_error(not_404_error)


def test_split_s3_path():
    assert split_s3_path('s3://bucket/key') == ('bucket', 'key')
    assert split_s3_path('s3://bucket/') == ('bucket', '')
    assert split_s3_path('s3://bucket') == ('bucket', '')


@patch('llm_web_kit.model.resource_utils.boto3_ext.load_config')
def test_get_s3_config(get_config_mock):
    get_config_mock.return_value = {'s3': {'bucket': {'ak': 'test_ak', 'sk': 'test_sk', 'endpoint': 'test_endpoint'}}}
    assert get_s3_config('s3://bucket/key') == {
        'ak': 'test_ak',
        'sk': 'test_sk',
        'endpoint': 'test_endpoint',
    }
    with pytest.raises(ValueError):
        get_s3_config('s3://nonexistent_bucket/key')


@patch('llm_web_kit.model.resource_utils.boto3_ext.load_config')
@patch('llm_web_kit.model.resource_utils.boto3_ext.boto3.client')
def test_get_s3_client(boto3_client_mock, get_config_mock):
    get_config_mock.return_value = {'s3': {'bucket': {'ak': 'test_ak', 'sk': 'test_sk', 'endpoint': 'test_endpoint'}}}
    mock_client = MagicMock()
    boto3_client_mock.return_value = mock_client
    assert get_s3_client('s3://bucket/key') == mock_client


@patch('llm_web_kit.model.resource_utils.boto3_ext.is_s3_404_error')
@patch('llm_web_kit.model.resource_utils.boto3_ext.boto3.client')
def test_head_s3_object(boto3_client_mock, is_s3_404_error_mock):
    s3_client_mock = MagicMock()
    boto3_client_mock.return_value = s3_client_mock
    s3_client_mock.head_object.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

    assert head_s3_object(s3_client_mock, 's3://bucket/key') == {'ResponseMetadata': {'HTTPStatusCode': 200}}

    s3_client_mock.head_object.side_effect = ClientError(
        error_response={
            'Error': {
                'Code': '404',
                'Message': 'Not Found'
            },
            'ResponseMetadata': {
                'HTTPStatusCode': 404
            },
        },
        operation_name='test',
    )
    is_s3_404_error_mock.return_value = True

    assert head_s3_object(s3_client_mock, 's3://bucket/key', raise_404=False) is None
    with pytest.raises(ClientError):
        head_s3_object(s3_client_mock, 's3://bucket/key', raise_404=True)
