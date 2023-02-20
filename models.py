from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    masters = relationship('Masters', back_populates='owner')


class Masters(Base):
    __tablename__ = 'masters'

    id = Column(Integer, unique=True, primary_key=True, index=True)
    in_game_id = Column(String)
    owner_user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    birthday = Column(String)
    gender = Column(String)
    device = Column(String)
    download_date = Column(Date)
    last_access = Column(DateTime)
    master_level = Column(Integer)
    saint_quartz = Column(Integer)
    paid_saint_quartz = Column(Integer)
    rare_prisms = Column(Integer)
    unregistered_spirit_origin = Column(Integer)
    recovery_number = Column(String)

    owner = relationship('Users', back_populates='masters')
    servants = relationship('MasterServants')


class Servants(Base):
    __tablename__ = 'servants'

    id = Column(Integer, unique=True, primary_key=True, index=True)
    name = Column(String)
    name_jp = Column(String)
    servant_class = Column(String)
    rarity = Column(Integer)


class MasterServants(Base):
    __tablename__ = 'master_servants'

    id = Column(Integer, primary_key=True, index=True)
    master_id = Column(Integer, ForeignKey('masters.id'))
    servant_id = Column(Integer, ForeignKey('servants.id'))
    level = Column(Integer)
    bond_level = Column(Integer)
    np_level = Column(Integer)
    skill_1_level = Column(Integer)
    skill_2_level = Column(Integer)
    skill_3_level = Column(Integer)
    summon_date = Column(Date)
    is_favourite = Column(Boolean)

    servant_data = relationship("Servants", lazy="joined", innerjoin=True)
