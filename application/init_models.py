from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

DATABASE_URL = "postgresql://username:password@localhost:5432/my_database"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(String(50), nullable=False)
    brand = Column(String(50), nullable=False)
    appearance = Column(String(50), nullable=True)
    power = Column(Integer, nullable=True)
    max_speed = Column(Integer, nullable=True)
    created_at = Column(Date, nullable=False)

    changes = relationship("Change", back_populates="car")


class Detail(Base):
    __tablename__ = "details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    car_part = Column(String(50), nullable=True)
    firm = Column(String(50), nullable=True)
    price = Column(Float, nullable=False)
    guarantee = Column(Date, nullable=True)


class Change(Base):
    __tablename__ = "changes"

    issue_id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    mechanic_name = Column(String(50), nullable=False)
    issue_date = Column(Date, nullable=False)
    appearance_change = Column(Integer, ForeignKey("details.id"), nullable=True)
    max_speed_change = Column(Integer, ForeignKey("details.id"), nullable=True)
    power_change = Column(Integer, ForeignKey("details.id"), nullable=True)

    car = relationship("Car", back_populates="changes")
    appearance_detail = relationship("Detail", foreign_keys=[appearance_change])
    max_speed_detail = relationship("Detail", foreign_keys=[max_speed_change])
    power_detail = relationship("Detail", foreign_keys=[power_change])


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
