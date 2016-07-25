#!/usr/bin/env python
# -*- coding: utf-8 -*-

import factory
from . import models


class CityFactory(factory.Factory):
    class Meta:
        model = models.City

    name = factory.Faker('city')
    state = factory.Faker('state')
    population = factory.Faker('pyint')


class PersonFactory(factory.Factory):
    class Meta:
        model = models.Person

    name = factory.Faker('name')
    ssn = factory.Faker('ssn')
    category = factory.Faker('word')
    city = factory.SubFactory(CityFactory)


class PetFactory(factory.Factory):
    class Meta:
        model = models.Pet

    name = factory.Faker('name')
    species = factory.Faker('word')
    kg = factory.Faker('pydecimal',
                       left_digits=1,
                       right_digits=1,
                       positive=True)
    owner = factory.SubFactory(PersonFactory)
