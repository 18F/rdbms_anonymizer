#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_rdbms_anonymize
----------------------------------

Tests for `rdbms_anonymize` module.
"""

import pytest
import sqlalchemy as sa
from click.testing import CliRunner

from rdbms_anonymize import cli
from rdbms_anonymize.rdbms_anonymize import anon

from . import factories, models


class TestCli(object):
    @classmethod
    def setup_class(cls):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'rdbms_anonymize.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    @classmethod
    def teardown_class(cls):
        pass


class TestAnonymize(object):
    @classmethod
    def setup_class(cls):
        models.Base.metadata.create_all(models.engine)
        cls.person_tbl = models.Base.metadata.tables['person']
        cls.city_tbl = models.Base.metadata.tables['city']
        cls.state_tbl = models.Base.metadata.tables['state']

    def setup_method(self, method):
        self.session = models.sessionmaker()
        for i in range(5):
            pet = factories.PetFactory()
            self.session.add(pet)
        # Ensure that at least one state has > 1 city
        city = factories.CityFactory()
        for city in self.session.query(models.City):
            if not self.session.query(models.State).filter_by(
                    name=city.state).first():
                state = models.State(name=city.state)
                self.session.add(state)
        # Ensure that at least one state has > 1 city
        city = factories.CityFactory()
        city.state = state.name
        self.session.add(city)
        self.session.commit()

    def teardown_method(self, method):
        self.session = models.sessionmaker()
        self.session.query(models.Pet).delete()
        self.session.query(models.Person).delete()
        self.session.query(models.City).delete()
        self.session.query(models.State).delete()
        self.session.commit()

    def test_anon_callable(self):
        anon(self.person_tbl.c.category, engine=models.engine)

    def test_anon_changes_simple_values(self):
        categories = [p.category
                      for p in self.session.query(models.Person).order_by('id')
                      ]
        anon(columns=self.person_tbl.c.category, engine=models.engine)
        self.session.expire_all()
        people = self.session.query(models.Person).order_by('id')
        for (idx, person) in enumerate(people):
            assert person.category != categories[idx]

    def test_anon_cascading_fk(self):
        """
        Check that anon works when the foreign key itself is anonymized
        and the foreign key is ON UPDATE CASCADE
        """
        old_owner_names = [
            p.owner_name for p in self.session.query(models.Pet).order_by('id')
        ]
        anon(columns=self.person_tbl.c.name, engine=models.engine)
        self.session.expire_all()
        people_names_new = [p.name for p in self.session.query(models.Person)]
        pets = self.session.query(models.Pet).order_by('id')
        for (idx, pet) in enumerate(pets):
            assert pet.owner_name not in old_owner_names
            assert pet.owner_name == people_names_new[idx]

    def test_anon_not_cascading_fk_raises(self):
        """
        When the user tries to anonymize a foreign key and there is no
        update cascade, throw an error
        """
        with pytest.raises(sa.exc.IntegrityError):
            anon(columns=self.city_tbl.c.name, engine=models.engine)

    def test_anon_self_reference(self):
        """
        Check that anon works against a self-referential foreign key

        (parent object is the same model class)
        """
        # TODO
        pass

    def test_anon_columns_together(self):
        """
        Let user specify that columns should be changed together
        """
        anon([self.state_tbl.c.name, self.city_tbl.c.state],
             engine=models.engine)
        self.session.expire_all()
        new_state_names = [s.name for s in self.session.query(models.State)]
        for city in self.session.query(models.City):
            assert city.state in new_state_names

    def test_anon_columns_together_arg_order_irrelevant(self):
        """
        Verify that order of columns in call does not matter
        """
        anon([self.city_tbl.c.state, self.state_tbl.c.name],
             engine=models.engine)
        self.session.expire_all()
        new_state_names = [s.name for s in self.session.query(models.State)]
        for city in self.session.query(models.City):
            assert city.state in new_state_names

    def test_anon_numeric(self):
        """
        Check that anon works against a numeric column
        """
        populations = [c.population for c in self.session.query(models.City)]
        anon(columns=self.city_tbl.c.population, engine=models.engine)
        self.session.expire_all()
        for city in self.session.query(models.City):
            assert city.population not in populations

    @classmethod
    def teardown_class(cls):
        pass
