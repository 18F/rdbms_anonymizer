# -*- coding: utf-8 -*-

from sqlalchemy_utils.functions import get_referencing_foreign_keys
from sqlalchemy import exc, sql

from faker import Factory
fake = Factory.create()


def set_parents(child_column, row, new_value, connection):
    for fk in get_referencing_foreign_keys(child_column.table):
        if fk.column.name == child_column.name:
            update = fk.parent.table.update()
            update = update.where(fk.parent == row[child_column.name])
            set_clause = {fk.parent.name: new_value}
            connection.execute(update, set_clause)


def find_fake_type(old_data):
    if isinstance(old_data, int):
        result = 'pyint'
    else:
        result = 'word'
    return result


def value_exists(val, connection, columns):
    return any(connection.execute(sql.expression.select([sql.expression.exists(
        col.table.select().where(col == val)), ])).scalar() for col in columns)


def update(connection, fake_type, columns, old_value):
    new_value = fake_type()
    while value_exists(new_value, connection, columns):
        new_value = fake_type()
    for col in columns:
        update = col.table.update().where(col == old_value)
        connection.execute(update, {col.name: new_value})


def anon(columns, engine, fake_type='None'):
    """
    Replace the values in `columns` with fake data.

    Usually, you should just pass a single column to `columns`.

    Multiple columns are supported for the corner case where you
    need to anonymize an undeclared foreign key.  The parent column -
    the one with the least rows - must be the first argument.

    If the database supports it, however, the best solution is to
    define the foreign key columns as ON UPDATE CASCADE, then call
    `anon` with just one column after all.

    Better yet, don't use PII requiring anonymization in foreign key
    columns!

    By default, replaces integers with integers, and strings with
      `faker.providers.lorem.word`
      http://fake-factory.readthedocs.io/en/latest/providers/faker.providers.lorem.html
      Otherwise, pass the name of a fake-factory provider.

    """

    if not hasattr(columns, '__iter__'):
        columns = [columns, ]

    with engine.begin() as connection:
        column = columns[0]
        for row in connection.execute(column.table.select()):
            old_value = row[column.name]
            fake_type = getattr(fake, find_fake_type(old_value))
            update(connection, fake_type, columns, old_value)
