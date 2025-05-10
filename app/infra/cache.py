import json

from consts import REDIS_DB, REDIS_HOST, REDIS_PORT
from domain.model import Channel, Login, Video
from infra.logger import logger
from redis.asyncio import Redis


def _get_redis(db: str):
    if db in REDIS_DB:
        return Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB[db],
            decode_responses=True,
            encoding="utf-8",
        )
    else:
        logger.error(f"Banco de dados Redis inválido: {db}")
        raise ValueError(f"Banco de dados Redis inválido: {db}")


def _get_model(db: str) -> Channel | Video | Login:
    match db:
        case "channel":
            return Channel
        case "video":
            return Video
        case "published":
            return Video
        case "login":
            return Login
        case _:
            logger.error(f"Banco de dados Redis inválido: {db}")
            raise ValueError(f"Banco de dados Redis inválido: {db}")


async def set_value(key: str, value: str, db: str, expiration=None) -> bool:
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


async def get_value(key: str, db: str) -> Channel | Video | Login | None:
    r = _get_redis(db)
    Model = _get_model(db)
    try:
        value = await r.get(key)
        if value is None:
            logger.info("Chave não encontrada no Redis.")
            return None
        logger.info("Valor obtido do Redis com sucesso.")
        return Model(**json.loads(value))
    except Exception as e:
        logger.error(f"Erro ao obter valor do Redis: {e}")
        return None


async def delete_key(key: str, db: str) -> bool:
    r = _get_redis(db)
    try:
        await r.delete(key)
        logger.info("Chave excluída do Redis com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao excluir chave do Redis: {e}")
        return False


async def get_by_prefix(pre: str, db: str) -> list[Channel | Video | Login] | None:
    r = _get_redis(db)
    Model = _get_model(db)
    try:
        keys = [chave async for chave in r.scan_iter(f"{pre}*")]
        values = await r.mget(keys)
        if not values:
            logger.info("Nenhum valor encontrado com o prefixo fornecido.")
            return None
        logger.info("Valores obtidos do Redis com sucesso.")
        return [Model(**json.loads(item)) for item in values]
    except Exception as e:
        logger.error(f"Erro ao obter valores do Redis: {e}")
        return None
