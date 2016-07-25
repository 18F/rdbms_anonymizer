# rdbms_anonymize

[![PyPI Status](https://img.shields.io/pypi/v/rdbms_anonymize.svg)](https://pypi.python.org/pypi/rdbms_anonymize)
[![Build Status](https://img.shields.io/travis/18F/rdbms_anonymize.svg?branch=master)](https://travis-ci.org/18F/rdbms_anonymize)
[![Coverage Status](https://coveralls.io/repos/github/18F/rdbms_anonymize.svg?branch=master)](https://coveralls.io/github/18F/rdbms_anonymize?branch=master)
[![Code Climate](https://codeclimate.com/github/18F/rdbms_anonymize.svg)](https://codeclimate.com/github/18F/rdbms_anonymize)
[![Accessibility](https://continua11y.18f.gov/18F/rdbms_anonymize?branch=master)](https://continua11y.18f.gov/18F/rdbms_anonymize)

Anonymize relational database by replacing PII with fake data


* Documentation: https://rdbms-anonymize.readthedocs.io.

# Using

    >>> import sqlalchemy as sa
    >>> engine = sa.create_engine('postgresql://:@/shakes')
    >>> meta = sa.MetaData()
    >>> meta.reflect(bind=engine)
    >>> para_table = meta.tables['paragraph']
    >>> sessionmaker = sa.orm.sessionmaker()
    >>> sessionmaker.configure(bind=engine)
    >>> session = sessionmaker()

    >>> from rdbms_anonymize.rdbms_anonymize import anon
    >>> qry = session.query(para_table)
    >>> qry.filter_by(paragraphid=630879).first().charid
    'VIOLA'
    >>> anon(para_table.c.charid, session=session)
    >>> session.commit()
    >>> qry.filter_by(paragraphid=630879).first().charid
    >>> anon(para_table.c.charid, session=session, type='Name')
    >>> qry.filter_by(paragraphid=630879).first().charid



## TODO

- Check for pl/python faker; use it for one-pass update
- http://docs.sqlalchemy.org/en/latest/changelog/migration_09.html#new-for-update-support-on-select-query


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter)
and the [18F/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.

## Limitations

- Duplicate rows in a table will still exactly match after anonymizing
  (all identical rows will have identical fake data).  A primary key
  prevents rows from being duplicates.

## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
