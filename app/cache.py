from redis.asyncio import Redis
from logger import logger

r = Redis(host='0.0.0.0', port=6379, db=0, decode_responses=True)

async def set_value(key, value, expiration=None):
    try:
        if expiration:
            await r.set(key, value, ex=expiration)
        await r.set(key, value)
        logger.info("Valor definido no Redis com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao definir valor no Redis: {e}")
        return False