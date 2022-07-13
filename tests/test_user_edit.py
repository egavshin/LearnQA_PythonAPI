import random
import string
import time
import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Edit information for user testcases")
class TestUserEdit(BaseCase):
    @allure.description("This test checks that we can update 'first name' for just created user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test checks that we can't update user without authorization")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_not_authorized_user(self):
        register_data = self.prepare_registration_data()
        # REGISTER
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_name = 'Changed name'
        letters = string.ascii_letters

        auth_sid = ''.join(random.choice(letters) for i in range(64))
        token = ''.join(random.choice(letters) for i in range(72))

        response2 = MyRequests.put(
            f"users/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response2, 404)

    @allure.description("This test checks that we can't edit the user information if we authorized by another user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_user_authorized_by_another_user(self):
        # REGISTER FIRST USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        time.sleep(1)

        # REGISTER SECOND USER
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        second_email = register_data["email"]
        second_password = register_data['password']

        # LOGIN SECOND USER
        login_data = {
            'email': second_email,
            'password': second_password
        }
        response3 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # EDIT USER_ID FROM FIRST USER AUTH INFO FROM SECOND USER
        new_name = "Changed Name"

        response4 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response4, 200)

        # LOGIN FIRST USER FOR CHECKING GET
        login_data = {
            'email': email,
            'password': password
        }
        response5 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response5, "auth_sid")
        token = self.get_header(response5, "x-csrf-token")

        # GET
        response6 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response6,
            "firstName",
            first_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test checks email validator while we update info for user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_user_update_incorrect_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        incorrect_email = "ChangedMail.com"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": incorrect_email}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_text(response3, 'Invalid email format')

    @allure.description("This test checks validator for fields while we update the user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_user_add_short_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "X"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_text(response3, '{"error":"Too short value for field firstName"}')
