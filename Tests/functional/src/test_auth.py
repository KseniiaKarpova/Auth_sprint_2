import pytest


@pytest.mark.parametrize(
    'in_data, out_data',
    [
        (
                {
                    "login": "test_login",
                    "password": "test_password",
                    "email": "test_email"
                },
                {'status_code': 201},
        ),
        (
                {
                    "login": "test_login",
                    "password": "test_password",
                    "email": "test_email"
                },
                {'status_code': 409},
        ),
    ]
)

@pytest.mark.asyncio
async def test_registration(make_post_request, in_data, out_data):
    body, status = await make_post_request(endpoint="/api/v1/auth/registration")
    assert status == out_data['status_code']


@pytest.mark.parametrize(
    'in_data, out_data',
    [
        (
                {
                    "login": "test_login",
                    "password": "test_password",
                    "agent": "test_agent"
                },
                {'status_code': 200},
        ),
    ]
)

@pytest.mark.asyncio
async def test_login(make_post_request, in_data, out_data):
    body, status = await make_post_request(endpoint="/api/v1/auth/login")
    assert status == out_data['status_code']
