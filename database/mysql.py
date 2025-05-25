import aiomysql
from typing import Any

# 환경변수 또는 설정 파일에서 가져온 값들이라고 가정
MYSQL_USER = "your_user"
MYSQL_PASSWORD = "your_password"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "your_database"
CONNECT_TIMEOUT = 10  # 초 단위


async def get_async_mysql_connection() -> aiomysql.Connection:

    return await aiomysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        connect_timeout=CONNECT_TIMEOUT,
        autocommit=True,  # 필요시
    )
