# officehours 

[![NPM info](https://travis-ci.org/Funk66/officehours.svg?branch=master)](https://travis-ci.org/Funk66/officehours.svg?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ce673e64dfc64ee682bb139d9166cfd4)](https://www.codacy.com/app/Funk66/officehours?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Funk66/officehours&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/ce673e64dfc64ee682bb139d9166cfd4)](https://www.codacy.com/app/Funk66/officehours?utm_source=github.com&utm_medium=referral&utm_content=Funk66/officehours&utm_campaign=Badge_Coverage)

Utility to calculate time intervals in working hours


## Installation

```bash
$ pip install officehours
```


## Usage

Create an instance of `officehours.Calculator`. You can optionally provide
the required opening/closing hours (defaults to 9:00 and 17:00 respectively)
and a list of date objects corresponding to bank holidays. You can use
other modules such as [Workalendar](https://github.com/novafloss/workalendar)
to obtain the list of non-working days.


```python
from datetime import datetime, date
from officehours import Calculator
import workalendar.europe import Germany

germany = Germany()
holidays = [day[0] for day in germany.holidays(2017)]
calculator = Calculator('8:00', '16:00', holidays)
```

### How many working hours transcurred between two dates?

```python
from_day = datetime(2017, 3, 1, 12, 45)  # Wednesday at 12:45
to_day = datetime(2017, 3, 6, 10, 15)  # Monday at 10:45
calculator.working_hours(from_day, to_day)  # Returns 21.5
```

### When is the next office opening time after a given date?

```python
day = date(2017, 4, 29)  # Saturday
calculator.next_office_open(day)  # Returns May 2nd at 8:00, since May 1st is a bank holiday
```

### A deliverable requires X working hours. When will it be ready?

```python
from_day = datetime(2017, 6, 1, 11, 20)
working_hours = 36.5
calculator.due_date(working_hours, from_day)  # Returns June 8th at 15:50
```

### When should work start considering it has to be ready by day D?

```python
deadline = datetime(2017, 6, 15, 12)
working_hours = 15
calculator.start_time(working_hours, deadline)  # Returns June 13th at 13:00
```


## Contributing

In lieu of a formal style guide, take care to maintain the existing coding style.
Add unit tests for any new or changed functionality. Lint and test your code.
