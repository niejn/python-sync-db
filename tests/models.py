from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dbsync import models, core, client


engine = create_engine("sqlite://")
Session = sessionmaker(bind=engine)


Base = declarative_base()


@client.track
class A(Base):
    __tablename__ = "test_a"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return u"<A id:{0} name:{1}>".format(self.id, self.name)


@client.track
class B(Base):
    __tablename__ = "test_b"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    a_id = Column(Integer, ForeignKey("test_a.id"))

    a = relationship(A, backref="bs")

    def __repr__(self):
        return u"<B id:{0} name:{1} a_id:{2}>".format(
            self.id, self.name, self.a_id)


Base.metadata.create_all(engine)
models.Base.metadata.create_all(engine)
core.set_engine(engine)
core.generate_content_types()
