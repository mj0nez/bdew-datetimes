===============
energy-datetime-utils
===============

A fast, efficient Python library for datetime utils in the german energy market 
* specific sets of government-designated holidays on the fly.
It aims to make determining whether a specific date is a holiday as fast and
flexible as possible.



Quick Start
-----------

.. code-block:: python

    from datetime import date, datetime
    from energy-datetime-utils import 

    us_holidays = holidays.US()  # this is a dict
    # the below is the same, but takes a string:
    us_holidays = holidays.country_holidays('US')  # this is a dict

    nyse_holidays = holidays.NYSE()  # this is a dict
    # the below is the same, but takes a string:
    nyse_holidays = holidays.financial_holidays('NYSE')  # this is a dict

    date(2015, 1, 1) in us_holidays  # True
    date(2015, 1, 2) in us_holidays  # False
    us_holidays.get('2014-01-01')  # "New Year's Day"

The HolidayBase dict-like class will also recognize date strings and Unix
timestamps:

.. code-block:: python

    '2014-01-01' in us_holidays  # True
    '1/1/2014' in us_holidays    # True
    1388597445 in us_holidays    # True

Some holidays may be only present in parts of a country:

.. code-block:: python

    us_pr_holidays = holidays.country_holidays('US', subdiv='PR')
    '2018-01-06' in us_holidays     # False
    '2018-01-06' in us_pr_holidays  # True

.. _documentation: https://python-holidays.readthedocs.io/

Please see the `documentation`_ for additional examples and detailed
information.

License
-------

.. __: LICENSE

Code and documentation are available according to the MIT License
(see LICENSE__).
