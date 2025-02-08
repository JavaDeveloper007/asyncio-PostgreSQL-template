from sqlalchemy import Column, Integer, String, Text
from config import Base

class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    imageName = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)


    def __repr__(self):
        return f"<News(id={self.id}, title={self.title})>"
