import logging
from common.log_handler import AsyncMongoLogHandler

# 로그 핸들러 생성 (Mongo에 저장)
mongo_handler = AsyncMongoLogHandler()
mongo_handler.setLevel(logging.INFO)


def get_mongo_handler():
    return mongo_handler


def get_logger(name: str = "App Logger"):
    # 커스텀 로거 생성 및 구성
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(mongo_handler)
    return logger
