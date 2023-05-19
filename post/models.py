from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from database import Base

class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(130), nullable=False)
    slug = Column(String(130), nullable=False)
    content = Column(Text(), nullable=False)
    tagline = Column(String(255), nullable=False)
    date = Column(Date(), nullable=True)
    img_file = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'<Post {self.title!r}>'