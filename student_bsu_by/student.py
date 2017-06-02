import requests
import re
import os
from .exceptions import NotImplementedYet, InvalidCaptchaError, InvalidCredentialsError


class Student:
    _DOMAIN = "http://student.bsu.by"
    _CAPTCHA_FILENAME = "captcha.jpg"

    def __init__(self, surname, student_id='', contract_num='', captcha_solver=None):
        if not student_id and not contract_num:
            raise AttributeError("Either student id or contract number must be specified")
        self.surname = str(surname)
        self.student_id = str(student_id)
        self.contract_num = str(contract_num)
        self.captcha_solver = captcha_solver
        self._s = requests.session()

        self.logged_in = False
        self._login()

    def _login(self):
        self._s.get(self._DOMAIN + "/Login.aspx")

        # Save captcha_image
        captcha_image = self._s.get(self._DOMAIN + "/CaptchaImage.aspx", stream=True)
        with open(self._CAPTCHA_FILENAME, "wb") as handle:
            for block in captcha_image.iter_content(1024):
                handle.write(block)

        # Solve captcha
        if self.captcha_solver:
            captcha_result = self.captcha_solver(os.path.abspath(self._CAPTCHA_FILENAME))
        else:
            captcha_result = input("Please type in digits from " + os.path.abspath(self._CAPTCHA_FILENAME) + ": ")

        # Make auth request
        auth_data = {"tbFam": self.surname,
                     "tbNumStud": self.student_id,
                     "tbNumDogovor":  self.contract_num,
                     "TextBox1": str(captcha_result),
                     # Some magic data below
                     "Button1": "Вход",
                     "__VIEWSTATEGENERATOR": "C2EE9ABB",
                     "__EVENTVALIDATION": "/wEWBgLx/JebDAKJuu3nBALTjay9DgKMxcDMCQLs0bLrBgKM54rGBhmMJB78DS+e7nGFEIIXUn4MKSCk",
                     "__VIEWSTATE": "/wEPDwULLTExOTE1MDI5OTBkZAi0szVD4ripentWVjh2xfHtlHZt",
                     "__EVENTTARGET": "",
                     "__EVENTARGUMENT": ""
                     }
        result_html = self._s.post(self._DOMAIN + "/Login.aspx", data=auth_data).text

        # Check for errors
        if "lError" in result_html:
            error_msg = re.search('<font color="Red">(.*?)</font>', result_html).group(1)
            raise InvalidCredentialsError(error_msg)
        elif "Label6" in result_html:
            error_msg = re.search('<font color="Red">(.*?)</font>', result_html).group(1)
            raise InvalidCaptchaError(error_msg)
        elif "Выход" in result_html:
            self.logged_in = True

    def get_term_data(self, term=0):
        if not self.logged_in:
            self._login()
        raise NotImplementedYet()

    def get_general_data(self):
        if not self.logged_in:
            self._login()
        raise NotImplementedYet()

    def get_debt_data(self):
        if not self.logged_in:
            self._login()
        raise NotImplementedYet()

    def get_credentials(self):
        if not self.logged_in:
            self._login()
        raise NotImplementedYet()

