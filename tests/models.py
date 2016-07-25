#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tables to test against (not real data)
"""

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = sa.create_engine('postgresql://:@/rdbms_anonymize_test')

sessionmaker = sa.orm.sessionmaker()
sessionmaker.configure(bind=engine)

metadata = sa.MetaData()


class State(Base):
    __tablename__ = 'state'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)


class City(Base):
    __tablename__ = 'city'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    state = sa.Column(sa.String)
    population = sa.Column(sa.Integer)


class Person(Base):
    __tablename__ = 'person'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    ssn = sa.Column(sa.String)
    category = sa.Column(sa.String, nullable=True)
    city_name = sa.Column(sa.String, sa.ForeignKey(City.name))
    city = orm.relationship(City, backref='people')
    pets = orm.relationship('Pet',
                            order_by='Pet.name',
                            # cascade='all, delete-orphan',
                            backref='owner')

    def __repr__(self):
        return '{}: {} ({})'.format(self.name, self.ssn, self.category)


class Pet(Base):
    __table__ = sa.Table(
        'pet',
        Base.metadata,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('species', sa.String),
        sa.Column('kg', sa.Numeric),
        sa.Column('owner_name', sa.String, sa.ForeignKey(Person.name)),
        sa.ForeignKeyConstraint(
            ['owner_name', ], ['person.name', ],
            onupdate='CASCADE',
            ondelete='CASCADE'))

    def __repr__(self):
        return '{}: {} ({} kg) - {}'.format(self.name, self.species, self.kg,
                                            self.owner)
