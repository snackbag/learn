import logging

from sqlalchemy import Column, String, create_engine, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)


class User(Base):
    """
    0 = personal
    1 = teacher
    2 = student
    """
    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, primary_key=True)

    # 0 = personal
    # 1 = teacher
    # 2 = student
    account_type = Column(Integer)

    email = Column(String, nullable=True)
    username = Column(String)
    salt = Column(String)
    password = Column(String)
    creation_date = Column(Integer)
    last_login_date = Column(Integer)

    xp = Column(Integer)
    coins = Column(Integer)
    avatar = Column(String)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.user_id=}, {self.account_type=}, {self.email=}, {self.username=}, {self.salt=}, {self.password=})>"


class Class(Base):
    __tablename__ = "classes"

    class_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.class_id=}, {self.name=})>"


class UserClassLink(Base):
    __tablename__ = "user_class_links"

    index = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer)
    class_id = Column(Integer)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.index=}, {self.user_id=}, {self.class_id=})>"


class ClassCode(Base):
    __tablename__ = "class_codes"

    index = Column(Integer, autoincrement=True, primary_key=True)
    key = Column(String)
    class_id = Column(Integer)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.index=}, {self.key=}, {self.class_id})>"


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id = Column(Integer, autoincrement=True, primary_key=True)
    creation_date = Column(Integer)
    owner = Column(Integer)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id=}, {self.creation_date=}, {self.owner=})>"


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    creation_date = Column(Integer)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id=}, {self.name=}, {self.creation_date=})>"


class Island(Base):
    """
    Types:
    0 - flashcard (for language islands)
    """
    __tablename__ = "islands"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # 0 = flashcards (for language islands)
    type = Column(Integer)
    assigned_subject = Column(Integer)
    name = Column(String)
    owner = Column(Integer)  # a user
    creation_date = Column(Integer)
    last_study_date = Column(Integer)
    visibility = Column(Integer)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id=}, {self.type=}, {self.assigned_subject=}, {self.name=}, {self.owner=}, {self.creation_date=}, {self.last_study_date=}, {self.visibility=})>"


class LanguageIsland(Base):
    __tablename__ = "learning_islands"

    island_id = Column(Integer, primary_key=True)
    last_correct_answers = Column(Integer)
    last_wrong_answers = Column(Integer)


class LanguageIslandCard(Base):
    __tablename__ = "language_island_cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    island = Column(Integer)
    question = Column(String)
    question_img = Column(String, nullable=True)
    answer = Column(String)
    answer_img = Column(String, nullable=True)
    description = Column(String)


engine = create_engine(f"sqlite:///database.db", echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
