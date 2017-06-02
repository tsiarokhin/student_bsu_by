# student_bsu_by
Tool for getting various student information from [student.bsu.by](http://http://student.bsu.by) website.

## Installation

TODO

## Documentation
```python
class student_bsu_by.Student(surname, student_id='', contract_num='', captcha_solver=None)
```
  * **surname** (*str*) - student's surname
  * **student_id** (*str*) - student's ID
  * **contract_num** (*str*) - student's contract number
  * **captcha_solver** (*function(str)*) - function, that receives `captcha.jpg` file path and must return valid captcha result. If not specified, command-line prompt will be used
