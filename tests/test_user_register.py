import string
import random
import pytest
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Create user test cases")
class TestUserRegister(BaseCase):
    exclude_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    @allure.description("Creates user successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    @allure.description("Checks that we can't create new user with existing email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.description("Checks email validator while creating a new user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_text(response, 'Invalid email format')

    @allure.description("Checks all mandatory fields while creating the user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.step
    @pytest.mark.parametrize('param', exclude_params)
    def test_create_user_without_one_of_parameter(self, param):
        data = self.prepare_registration_data()
        del data[param]

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_text(response, f"The following required params are missed: {param}")

    @allure.description("Checks if empty values in mandatory fields while creating the user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('param', exclude_params)
    def test_create_user_without_value_one_of_parameter(self, param):
        data = self.prepare_registration_data()
        data[param] = ''

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_text(response, f"The value of '{param}' field is too short")

    @allure.description("Checks validator, if short value in 'username' field while creating the user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = 'l'

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_text(response, f"The value of 'username' field is too short")

    @allure.description("Checks validator, if long value in 'username' field while creating the user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        letters = string.ascii_letters
        data['username'] = ''.join(random.choice(letters) for i in range(251))

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_text(response, f"The value of 'username' field is too long")
