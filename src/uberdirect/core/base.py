from abc import ABC
from time import sleep
from types import FunctionType
from typing import Any, Callable, Literal, NotRequired, TypedDict, Unpack

import requests

type URL = str | int
type Body = dict
type Params = dict
type Method = Literal['GET', 'PUT', 'POST', 'PATCH', 'DELETE']
type Headers = dict
type APIVersion = Literal['v1']
type OAuthVersion = Literal['v2']
type AccessToken = str | Callable[[], str]

BASE_URL = 'https://api.uber.com/{version}/customers/{customer_id}'
OATH_URL = 'https://auth.uber.com/oauth'
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRIABLE_HTTP_CODES = {
    401,
    429,
    500,
    502,
    503,
    504,
}


class OptionalArguments(TypedDict):
    params: NotRequired[Params | None]
    headers: NotRequired[Headers | None]


class Base(ABC):
    def __init__(
        self,
        customer_id: str,
        access_token: AccessToken,
        /,
        *,
        version: APIVersion,
        max_retries: int | None = None,
        retriable_http_codes: set[int] | None = None,
    ) -> None:
        self._api_root = BASE_URL.format(version=version, customer_id=customer_id)
        self._max_retries = max_retries or DEFAULT_MAX_RETRIES
        self._customer_id = customer_id
        self._access_token = access_token
        self._retriable_http_codes = (
            retriable_http_codes or DEFAULT_RETRIABLE_HTTP_CODES
        )

    def _get(
        self,
        /,
        *args: URL,
        **kwargs: Unpack[OptionalArguments],
    ):
        return self._wrapper(
            *args,
            **kwargs,
            method='GET',
        )

    def _put(
        self,
        body: Body,
        /,
        *args: URL,
        **kwargs: Unpack[OptionalArguments],
    ):
        return self._wrapper(
            *args,
            **kwargs,
            body=body,
            method='PUT',
        )

    def _post(
        self,
        body: Body,
        /,
        *args: URL,
        **kwargs: Unpack[OptionalArguments],
    ):
        return self._wrapper(
            *args,
            **kwargs,
            body=body,
            method='POST',
        )

    def _patch(
        self,
        body: Body,
        /,
        *args: URL,
        **kwargs: Unpack[OptionalArguments],
    ):
        return self._wrapper(
            *args,
            **kwargs,
            body=body,
            method='PATCH',
        )

    def _delete(
        self,
        /,
        data: Body | None = None,
        *args: URL,
        **kwargs: Unpack[OptionalArguments],
    ):
        return self._wrapper(
            *args,
            **kwargs,
            body=data,
            method='DELETE',
        )

    def _wrapper(
        self,
        *args: URL,
        body: Body | None = None,
        params: Params | None = None,
        method: Method,
        headers: Headers | None = None,
    ) -> dict[str, Any]:
        retries = 0
        exception = None
        while retries <= self._max_retries:
            try:
                return self._request(
                    *args,
                    body=body,
                    params=params,
                    method=method,
                    headers=headers,
                )
            except requests.HTTPError as e:
                exception = e
                if e.response.status_code in self._retriable_http_codes:
                    backoff = min(2**retries, 20)
                    sleep(backoff)
                    retries += 1
                    continue
                raise
        raise (
            exception
            if exception
            else RuntimeError('An exception should have been thrown')
        )

    def _request(
        self,
        *args: URL,
        body: Body | None = None,
        params: Params | None = None,
        method: Method,
        headers: Headers | None = None,
    ) -> dict[str, Any]:
        if not headers:
            headers = {}

        access_token = self._access_token
        if isinstance(access_token, FunctionType):
            access_token = access_token()

        headers['Authorization'] = f'Bearer {access_token}'

        url = self._api_root + '/' + '/'.join(str(arg) for arg in args)

        response = requests.request(
            url=url,
            data=body,
            method=method,
            params=params,
            headers=headers,
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def get_access_token(
        *,
        version: OAuthVersion = 'v2',
        client_id: str,
        client_secret: str,
    ) -> str:
        # oauth endpoint
        url = '/'.join([OATH_URL, version, 'token'])

        # data
        data = {
            'scope': 'eats.deliveries',
            'client_id': client_id,
            'grant_type': 'client_credentials',
            'client_secret': client_secret,
        }

        # request
        response = requests.post(
            url=url,
            data=data,
        )

        # assert response
        response.raise_for_status()

        # decode jwt
        jwt = response.json()

        return jwt['access_token']
