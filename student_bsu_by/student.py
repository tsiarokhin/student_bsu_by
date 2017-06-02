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

        self._progress_page_html = None

        self._term_data = None
        self._general_data = None
        self._debt_data = None
        self._credentials_data = None

        self.logged_in = False

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
        auth_data = {
            "tbFam": self.surname,
            "tbNumStud": self.student_id,
            "tbNumDogovor": self.contract_num,
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

    def _load_progress_page_html(self):
        if not self._progress_page_html:
            progress_data = {
                "ctlStudProgress1$cmbSemester": "0",
                # Some magic data below
                "ctlStudProgress1$txtROWGUID": "4e46072d-28a9-4074-b137-2132be54e347",
                "__VIEWSTATEGENERATOR": "2DE91999",
                "__EVENTVALIDATION": "/wEWBwLn0/bKCALptOWgBwLXp9/NBQKc/YuICgKc4/GHBgKTgZePDwLnicyYCd2nDwXOMfNEee3SuSTHBEDAlBGa",
                "__VIEWSTATE": "/wEPDwUKMTk4MzQ1ODgxNg9kFgICAQ9kFgICBQ9kFgoCAw8PFgIeBFRleHQFMtCi0LXRgNGR0YXQuNC9INCc0LDQutGB0LjQvCDQkNC90LDRgtC+0LvRjNC10LLQuNGHZGQCBQ8PFgIfAAVW0KTQsNC60YPQu9GM0YLQtdGCINC/0YDQuNC60LvQsNC00L3QvtC5INC80LDRgtC10LzQsNGC0LjQutC4INC4INC40L3RhNC+0YDQvNCw0YLQuNC60LhkZAIHDw8WAh8ABXoxINC60YPRgNGBLCDQs9GA0YPQv9C/0LAgNCwg0YTQvtGA0LzQsCDQvtCx0YPRh9C10L3QuNGPINC00L3QtdCy0L3QsNGPLCDRgdC/0LXRhtC40LDQu9GM0L3QvtGB0YLRjDog0LjQvdGE0L7RgNC80LDRgtC40LrQsGRkAgkPDxYCHwAFITxiPtGB0YDQtdC00L3QuNC5INCx0LDQu9C7OiA3PC9iPmRkAgsPEGQPFggCAQICAgMCBAIFAgYCBwIIFggQBSUxINC60YPRgNGBLCDQt9C40LzQvdGP0Y8g0YHQtdGB0YHQuNGPBQExZxAFKTEg0LrRg9GA0YEsINCy0LXRgdC10L3QvdGP0Y8g0YHQtdGB0YHQuNGPBQEyZxAFJTIg0LrRg9GA0YEsINC30LjQvNC90Y/RjyDRgdC10YHRgdC40Y8FATNnEAUpMiDQutGD0YDRgSwg0LLQtdGB0LXQvdC90Y/RjyDRgdC10YHRgdC40Y8FATRnEAUlMyDQutGD0YDRgSwg0LfQuNC80L3Rj9GPINGB0LXRgdGB0LjRjwUBNWcQBSkzINC60YPRgNGBLCDQstC10YHQtdC90L3Rj9GPINGB0LXRgdGB0LjRjwUBNmcQBSU0INC60YPRgNGBLCDQt9C40LzQvdGP0Y8g0YHQtdGB0YHQuNGPBQE3ZxAFKTQg0LrRg9GA0YEsINCy0LXRgdC10L3QvdGP0Y8g0YHQtdGB0YHQuNGPBQE4Z2RkZLnQ5bpEnckL4zF1/63oCMc6pWJx",
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": ""
            }
            self._progress_page_html = self._s.post(self._DOMAIN + "/StudProgress.aspx", data=progress_data).text
        return self._progress_page_html

    @property
    def term_data(self):
        if not self.logged_in:
            self._login()

        if not self._term_data:
            term_data_html = re.search(
                '<table id="ctlStudProgress1_tblProgress".*?>([\s\S]*?)</table>',
                self._load_progress_page_html()
            ).group(1)

            # TODO: Table parser
            raise NotImplementedYet()
        return self._term_data

    @property
    def general_data(self):
        if not self.logged_in:
            self._login()
        if not self._general_data:
            general_data_re = re.search(
                ('<span id="ctlStudProgress1_lbStudName".*?><b>(.*?)</b></span>[\s\S]*'
                 '<span id="ctlStudProgress1_lbStudFacultet".*?>(.*?)</span>[\s\S]*'
                 '<span id="ctlStudProgress1_lbStudKurs".*?>(.) курс, группа (.*?), '
                 'форма обучения (.*?), специальность: (.*)</span>[\s\S]*средний балл: (.*?)</b>'
                 ),
                self._load_progress_page_html()
            )
            self._general_data = {
                "full_name": general_data_re.group(1),
                "faculty": general_data_re.group(2),
                "course": int(general_data_re.group(3)),
                "group": int(general_data_re.group(4)),
                "education_form": general_data_re.group(5),
                "specialty": general_data_re.group(6),
                "average_score": float(general_data_re.group(7))
            }
        return self._general_data

    @property
    def debt_data(self):
        if not self.logged_in:
            self._login()

        if not self._debt_data:
            debt_data_html = self._s.get(self._DOMAIN + "/MainInfo.aspx").text
            debt_data_re = re.search('<span id="lDolg".*?><b>(.*?)</b></span>[\s\S]*<span id="lPeny".*?><b>(.*?)</b></span>', debt_data_html)
            self._debt_data = {
                "debt": float(debt_data_re.group(1)),
                "fine": float(debt_data_re.group(2))
            }
        return self._debt_data

    @property
    def credentials_data(self):
        if not self.logged_in:
            self._login()

        if not self._credentials_data:
            credentials_html = self._s.get(self._DOMAIN + "/Results2.aspx").text
            credentials_re = re.search("№ договора: (.*?), № студенческого билета (\d{7})", credentials_html)
            self._credentials_data = {
                "surname": self.surname,
                "contract_num": credentials_re.group(1),
                "id": credentials_re.group(2)
            }
        return self._credentials_data
