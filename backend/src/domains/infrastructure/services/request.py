from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient


class API:

    def __init__(self, headers: dict = None, cookies: dict = None):
        self.headers = headers
        self.cookies = cookies

    async def send_request(self, method: str = "GET", url: str = "", headers: dict = None, data: dict = None, timeout: float = 10.0):
        async with AsyncClient(headers=headers or self.headers, cookies=self.cookies) as client:
            response = await client.request(
                method,
                url,
                data=data,
                headers=headers,
                follow_redirects=True,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
