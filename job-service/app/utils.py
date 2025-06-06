import httpx

AUTH_SERVICE_URL = "http://auth-service:8001/auth/protected"

async def verify_token(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(AUTH_SERVICE_URL, headers=headers)
            if response.status_code == 200:
                return response.json()
    except Exception as e:
        print("Token verification failed:", e)
    return None
