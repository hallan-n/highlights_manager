from external.youtube_webbot import get_login_session
import asyncio

valor = asyncio.run(get_login_session())
print(valor)
