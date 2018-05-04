

Reports templating
------------------

In query definitions (or other templates inside laika) you can specify
dynamic dates this way:

.. code:: sql

    select * from some_table where date >= '{m}' and date < '{m+1m}'

laika will replace this dates by (supposing current month is February of
2016):

.. code:: sql

    select * from some_table where date >= '2016-02-01 00:00:00' and date < '2016-03-01 00:00:00'

Dates are UTC by default, but you can modify that changing ``timezone``
configuration.

These are all the template variables you can use:

-  ``{now}``: current date.
-  ``{d}`` o ``{t}``: start of current date (00:00:00 of today)
-  ``{m}``: start of first day of current month
-  ``{y}``: start of current year (first day of January)
-  ``{H}``: start of current hour
-  ``{M}``: start of current minute
-  ``{w}``: start of current week (Monday)

These variables may also receive modifiers. Modifier expression must
start with one of these variables, continue with a sign (``+`` o ``-``),
a number and finally, a measure. This measures can be:

-  ``{y}``: years
-  ``{m}``: months
-  ``{d}``: days
-  ``{h}``: hours
-  ``{M}``: minutes
-  ``{w}``: weeks

For example:

::

    {now}, {now-1d}, {now+1y}, {now+15h}, {t-3m}

Results in:

::

    2016-02-12 18:19:09, 2016-02-11 18:19:09, 2017-02-12 18:19:09, 2016-02-13 09:19:09, 2015-11-12 00:00:00

Another possibility is to specify a start of week with ``{f}``. For
example, ``{d-1f}`` will move the date to Monday of the current week,
and ``{d+2f}`` will move the date to Monday within two weeks.

Query templating
~~~~~~~~~~~~~~~~

If the report has a dictionary of variables specified they will be
replaced in the specified query file. For example, if you define a query
like this:

.. code:: sql

    select something from some_table where type = '{my_type}'

You can then pass the variables through configuration this way:

.. code:: json

    {
      "variables": {
        "my_type": "some custom type"
      }
    }

The query that will end up executing is this:

.. code:: sql

    select something from some_table where type = 'some custom type'

These variables will be replaced first, and then laika will replace the
dates, so you can define in your configuration variables like this:

.. code:: json

    {
      "variables": {
        "yesterday": "{t-1d}"
      }
    }

``{yesterday}`` will be converted into ``2016-02-12 17:19:09``.

Filenames templating
~~~~~~~~~~~~~~~~~~~~

``filename`` configuration in all the reports and results can be
formatted in a similar way. For example, if you specify:

.. code:: json

    {
      "filename": "report_{Y}-{m}"
    }

This will be formatted as ``report_2016-02`` (assuming the report ran in
February of 2016).

You can also use the same modifiers:

.. code:: json

    {
      "filename": "report_{Y}-{m-1m}"
    }

Will result in ``report_2016-01``.
