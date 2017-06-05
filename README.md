# student_bsu_by
Tool for getting various student information from [student.bsu.by](http://http://student.bsu.by) website.

## Installation
```bash
pip install git+https://github.com/teryokhin/student_bsu_by.git
```

## Usage
```python
from student_bsu_by import Student

student = Student("Surname", student_id=1234567)
print(student.general_data)

expelled = student.debt_data["expelled"]
if expelled:
  print("Better luck next time :)")
```

## Documentation
```python
class student_bsu_by.Student(surname, student_id='', contract_num='', captcha_solver=None)
```
  * **surname** (*str*) - student's surname
  * **student_id** (*str*) - student's ID
  * **contract_num** (*str*) - student's contract number
  * **captcha_solver** (*function(filepath: str) -> str*) - function, that receives file path of captcha image (jpg) and must return a valid captcha result. If not specified, `input()` prompt will be used

### Properties
```python
Student.term_data = [ # list of terms
  [ # list of subjects
    {
      "subject": str,
      "credit_test": str,
      "credit_test_tries": int,
      "exam": str,
      "exam_tries": int
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
  "group": str,
  "education_form": str,
  "specialty": str,
  "average_score": float
}
```

```python
Student.debt_data = {
  "debt": float,
  "fine": float,
  "expelled": bool
}
```

```python
Student.credentials_data = {
  "surname": str,
  "contract_num": str,
  "id": str
}
```
