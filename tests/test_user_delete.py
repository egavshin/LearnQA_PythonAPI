import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import time
import allure


@allure.epic("Delete users cases")
class TestUserDelete(BaseCase):

    @allure.description("This test checks that we can't delete first 5 reserved users")
    @allure.link("https://software-testing.ru/lms/mod/assign/view.php?id=267097")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_untouchable_user(self):
        # LOGIN
        login_data = {
            'email': "vinkotov@example.com",
            'password': "1234"
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        # DELETE
        response2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_text(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.description("This test checks delete method for users")
    @allure.link("https://software-testing.ru/lms/mod/assign/view.php?id=267097")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_just_created_user(self):
        # REGISTER NEW USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
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

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)

        # GET INFO ABOUT DELETED USER
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 404)
        Assertions.assert_text(response4, "User not found")

    @allure.description("This test checks that you cannot delete user if you are not authorized by this user")
    @allure.link("https://software-testing.ru/lms/mod/assign/view.php?id=267097")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_authorized_by_another_user(self):
        # REGISTER FIRST USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
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

        # DELETE FIRST USER

        response4 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
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

        Assertions.assert_code_status(response6, 200)
