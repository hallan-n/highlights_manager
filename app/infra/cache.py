from redis.asyncio import Redis
from app.infra.logger import logger

r = Redis(host='0.0.0.0', port=6379, db=0, decode_responses=True, encoding='utf-8')

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

async def get_value(key):
    try:
        value = await r.get(key)
        if value is None:
            logger.info("Chave não encontrada no Redis.")
            return None
        logger.info("Valor obtido do Redis com sucesso.")
        return value
    except Exception as e:
        logger.error(f"Erro ao obter valor do Redis: {e}")
        return None

async def delete_key(key):
    try:
        await r.delete(key)
        logger.info("Chave excluída do Redis com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao excluir chave do Redis: {e}")
        return False