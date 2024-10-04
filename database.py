import logging
from sqlalchemy import Column, String, create_engine, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()

logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
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

    # Relationships
    islands = relationship("Island", back_populates="owner_user")
    language_islands = relationship("LanguageIsland", back_populates="owner_user")  # Uses user_id ForeignKey
    user_classes = relationship("UserClassLink", back_populates="user")

    def __repr__(self):
        return f"<User({self.user_id=}, {self.account_type=}, {self.email=}, {self.username=})>"


class Class(Base):
    __tablename__ = "classes"

    class_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    # Relationships
    users = relationship("UserClassLink", back_populates="class_")
    class_codes = relationship("ClassCode", back_populates="class_")

    def __repr__(self):
        return f"<Class({self.class_id=}, {self.name=})>"


class UserClassLink(Base):
    __tablename__ = "user_class_links"

    index = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    class_id = Column(Integer, ForeignKey('classes.class_id'))

    # Relationships
    user = relationship("User", back_populates="user_classes")
    class_ = relationship("Class", back_populates="users")

    def __repr__(self):
        return f"<UserClassLink({self.index=}, {self.user_id=}, {self.class_id=})>"


class ClassCode(Base):
    __tablename__ = "class_codes"

    index = Column(Integer, autoincrement=True, primary_key=True)
    key = Column(String)
    class_id = Column(Integer, ForeignKey('classes.class_id'))

    # Relationships
    class_ = relationship("Class", back_populates="class_codes")

    def __repr__(self):
        return f"<ClassCode({self.index=}, {self.key=}, {self.class_id=})>"


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id = Column(Integer, autoincrement=True, primary_key=True)
    creation_date = Column(Integer)
    owner = Column(Integer, ForeignKey('users.user_id'))

    # Relationships
    owner_user = relationship("User")  # Link session owner to User

    def __repr__(self):
        return f"<LearningSession({self.id=}, {self.creation_date=}, {self.owner=})>"


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    creation_date = Column(Integer)

    def __repr__(self):
        return f"<Subject({self.id=}, {self.name=}, {self.creation_date=})>"


class Island(Base):
    """
    Types:
    0 - flashcard (for language islands)
    """
    __tablename__ = "islands"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer)  # 0 = flashcards (for language islands)
    assigned_subject = Column(Integer, ForeignKey('subjects.id'))
    name = Column(String)
    owner = Column(Integer, ForeignKey('users.user_id'))  # Foreign key to User
    creation_date = Column(Integer)
    last_study_date = Column(Integer)
    visibility = Column(Integer)

    # Relationships
    owner_user = relationship("User", back_populates="islands")  # Link back to User
    language_island = relationship("LanguageIsland", uselist=False, back_populates="island")  # One-to-one relationship
    subject = relationship("Subject")  # Link to Subject

    def __repr__(self):
        return f"<Island({self.id=}, {self.type=}, {self.name=}, {self.owner=})>"


class LanguageIsland(Base):
    __tablename__ = "learning_islands"

    island_id = Column(Integer, ForeignKey('islands.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))  # Add this line
    last_correct_answers = Column(Integer)
    last_wrong_answers = Column(Integer)

    # Relationships
    island = relationship("Island", back_populates="language_island")
    owner_user = relationship("User", back_populates="language_islands")  # Through ForeignKey user_id
    cards = relationship("LanguageIslandCard", back_populates="island")

    def __repr__(self):
        return f"<LanguageIsland({self.island_id=}, {self.last_correct_answers=}, {self.last_wrong_answers=})>"


class LanguageIslandCard(Base):
    __tablename__ = "language_island_cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    island_id = Column(Integer, ForeignKey('learning_islands.island_id'))
    question = Column(String)
    question_img = Column(String, nullable=True)
    answer = Column(String)
    answer_img = Column(String, nullable=True)
    description = Column(String)

    # Relationships
    island = relationship("LanguageIsland", back_populates="cards")

    def __repr__(self):
        return f"<LanguageIslandCard({self.id=}, {self.question=}, {self.answer=})>"

# Create the engine and session
engine = create_engine(f"sqlite:///database.db", echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
