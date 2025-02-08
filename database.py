from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, update, select
import logging

from config import DATABASE_URL
from moduls.images import Images




# Устанавливаем уровень логирования для SQLAlchemy engine на WARNING
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

class ClsDataBase:
    # Создаем асинхронный движок
    engine = create_async_engine(DATABASE_URL, echo=False)
    # Создаем фабрику сессий для работы с базой
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    

    
    async def add_news(self,save_path: str, title: str, description:str):
        async with self.async_session() as session:
            new_record = Images(image=save_path, title=title,description=description)
            session.add(new_record)
            await session.commit()


    async def get_all_news(self):
        async with self.async_session() as session:
            # Выполняем SQL-запрос для получения id и title из таблицы images
            result = await session.execute(text("SELECT id, title FROM images"))  # <-- исправлено
            news_list = result.fetchall()
            return news_list

    async def get_one_news(self,news_id) -> dict:
        async with self.async_session() as session:
            result = await session.execute(
                text("SELECT id, image, title, description FROM images WHERE id = :id"),
                {"id": news_id}
            )
            row = result.fetchone()  # Получаем одну запись
            if row:
                _id, image, title, description = row
                return {"id": _id, "image": image, "title":title, "description":description}
            return None  # Если записи нет, возвращаем None


    async def update_one_news(self,news_id, image, title, description,logger):
        async with self.async_session() as session:
            try:
                stmt = (
                    update(Images)
                    .where(Images.id == news_id)
                    .values(image=image, title=title, description=description)
                )
                result = await session.execute(stmt)
                await session.commit()

                # Проверяем, была ли обновлена хотя бы одна строка
                return result.rowcount > 0
            except Exception as e:
                logger.error(f'Ошибка обновления новости: {e} - data {news_id}, img:{image}')
                await session.rollback()
                return False




    async def serch_by_title(self,title):
        async with self.async_session() as session:
            query = select(Images.id, Images.Images, Images.title).where(
            Images.title.ilike(f"%{title}%")
            ).limit(10)

            result = await session.execute(query)
            return result.fetchall()
