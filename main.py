import logging
from config import Base
from database import ClsDataBase
import asyncio

db = ClsDataBase()

async def init_db():
    async with db.engine.begin() as conn:
        # Метод run_sync запускает синхронную функцию внутри асинхронного контекста
        await conn.run_sync(Base.metadata.create_all)
    logging.info("✅ База данных проверена/создана")



if __name__ == "__main__":
    asyncio.run(init_db)