# student_bsu_by
Tool for getting various student information from [student.bsu.by](http://http://student.bsu.by) website.

## Installation

TODO

## Usage

TODO

## Documentation
```python
class student_bsu_by.Student(surname, student_id='', contract_num='', captcha_solver=None)
```
  * **surname** (*str*) - student's surname
  * **student_id** (*str*) - student's ID
  * **contract_num** (*str*) - student's contract number
  * **captcha_solver** (*function(str)*) - function, that receives `captcha.jpg` file path and must return valid captcha result. If not specified, command-line prompt will be used

### Properties
```python
Student.term_data = [ # list of terms
  [ # list of subjects
    {
      "subject": str,
      "сredit_test": str,
      "exam": str
    },
    {...},
    ...
  ],
  [...],
  ...
]
```

```python
Student.general_data = {
  "full_name": str,
  "faculty": str,
  "course": int,
  "group": int,
  "education_form": str,
  "specialty": str,
  "average_score": float
}
```

```python
Student.debt_data = {
  "debt": float,
  "fine": float
}
```

```python
Student.credentials_data = {
  "surname": str,
  "contract_num": str,
  "id": str
}
```
