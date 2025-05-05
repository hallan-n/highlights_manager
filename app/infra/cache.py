from redis.asyncio import Redis
from infra.logger import logger
from consts import REDIS_HOST, REDIS_PORT, REDIS_DB


def _get_redis(db: str):
    if db in REDIS_DB:
        return Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB[db],
            decode_responses=True,
            encoding='utf-8'
        )
    else:
        logger.error(f"Banco de dados Redis inválido: {db}")
        raise ValueError(f"Banco de dados Redis inválido: {db}")

async def set_value(key: str, value: str, db: str, expiration=None):
    r = _get_redis(db)
    try:
        if expiration:
            await r.set(key, value, ex=expiration)
        await r.set(key, value)
        logger.info("Valor definido no Redis com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao definir valor no Redis: {e}")
        return False

async def get_value(key: str, db: str):
    r = _get_redis(db)
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

async def delete_key(key: str, db: str):
    r = _get_redis(db)
    try:
        await r.delete(key)
        logger.info("Chave excluída do Redis com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao excluir chave do Redis: {e}")
        return False
    
async def get_by_prefix(pre: str, db: str):
    r = _get_redis(db)
    try:
        keys = [chave async for chave in r.scan_iter(f"{pre}*")]
        values = await r.mget(keys)
        if not values:
            logger.info("Nenhum valor encontrado com o prefixo fornecido.")
            return None
        logger.info("Valores obtidos do Redis com sucesso.")
        return values
    except Exception as e:
        logger.error(f"Erro ao obter valores do Redis: {e}")
        return None
