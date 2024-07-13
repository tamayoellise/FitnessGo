from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.pickers import MDDatePicker
from kivymd.app import MDApp
import requests
from kivymd.uix.snackbar import MDSnackbar

from info_db import auth_tbl
from models import AuthModel
from food_db import fc
from datetime import datetime

Window.size = (380, 650)


class MainWidget(Widget):
    rect = None


class WelcomeWindow(Screen):
    pass


class LogInWindow(Screen):
    pass


class SignUpWindow(Screen):
    pass


class HomePageWindow(Screen):
    pass


class CalorieWindow(Screen):
    def on_enter(self):
        self.update_date()

    def update_date(self):
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.ids.date_label.text = current_date


class GWeightWindow(Screen):
    pass


class GWeight1(Screen):
    pass


class GWeight2(Screen):
    pass


class GWeight3(Screen):
    pass


class GWeight4(Screen):
    pass


class GWeight5(Screen):
    pass


class GMusclesWindow(Screen):
    pass


class GMuscles1(Screen):
    pass


class GMuscles2(Screen):
    pass


class GMuscles3(Screen):
    pass


class GMuscles4(Screen):
    pass


class GMuscles5(Screen):
    pass


class LWeightWindow(Screen):
    pass


class LWeight1(Screen):
    pass


class LWeight2(Screen):
    pass


class LWeight3(Screen):
    pass


class LWeight4(Screen):
    pass


class LWeight5(Screen):
    pass


class MWeightWindow(Screen):
    pass


class MWeight1(Screen):
    pass


class MWeight2(Screen):
    pass


class MWeight3(Screen):
    pass


class MWeight4(Screen):
    pass


class MWeight5(Screen):
    pass


class ProfileWindow(Screen):
    pass


class PData(Screen):
    pass


class PGoals(Screen):
    pass


class DiaryWindow(Screen):
    def on_enter(self):
        self.update_date()

    def update_date(self):
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.ids.date_button.text = current_date


class SettingsWindow(Screen):
    pass


class AboutWindow(Screen):
    pass


class PersonalInfoWindow(Screen):
    pass


class FitnessObjectiveWindow(Screen):
    pass


class CongratulationWindow(Screen):
    pass


sm = ScreenManager()
sm.add_widget(WelcomeWindow(name="welcome"))
sm.add_widget(LogInWindow(name="login"))
sm.add_widget(SignUpWindow(name="signup"))


def on_cancel(instance):
    instance.dismiss()


class FitnessApp(MDApp):
    menu: MDDropdownMenu
    date_text = StringProperty(datetime.now().strftime("%A, %B %d, %Y"))
    selected_date = ObjectProperty(None)

    username = ""
    password = ""
    email = ""
    user_id = ""
    customer_name = ""
    customer_age = 0
    customer_gender = ""
    customer_height = 0
    customer_weight = 0
    customer_objective = ""
    customer_activity = ""
    customer_desired = ""
    customer_months = ""

    def __init__(self):
        super().__init__()
        self.ids = None

    def build(self):
        self.title = "Fitness Go"
        self.theme_cls.primary_pallete = "Green"
        Builder.load_file("fitness.kv")
        return

    def gender(self, tf, focus):
        if not focus:
            return

        menu_items = [
            {
                "text": "Male",
                "on_release": lambda x="Male": self.gender_callback(x)
            },
            {
                "text": "Female",
                "on_release": lambda x="Female": self.gender_callback(x)
            }
        ]
        self.menu = MDDropdownMenu(caller=tf, items=menu_items, width_mult=2)
        self.menu.open()

    def gender_callback(self, selected_gender):
        self.root.get_screen("personal_info").ids.customer_gender.text = selected_gender
        self.menu.dismiss(self.customer_gender)

    def get_calories(self, food_item, food_quantity):
        app_id = "591941e8"  # Replace with your Nutritionix API ID
        app_key = "35a04046091e343b899d81de3d6a2c72"  # Replace with your Nutritionix API Key
        url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
        headers = {
            "x-app-id": app_id,
            "x-app-key": app_key,
            "Content-Type": "application/json"
        }

        data = {
            "query": f"{food_quantity} grams of {food_item}"
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            data = response.json()
            if data["foods"]:
                calories = data["foods"][0].get('nf_calories', 'Not Found')
                self.root.get_screen('calorie').ids.calorie_output.text = f"Calories: {calories}"
            else:
                self.root.get_screen('calorie').ids.calorie_output.text = "No data found"
        else:
            self.root.get_screen('calorie').ids.calorie_output.text = "Error fetching data"

    def validate_inputs(self):
        food_item = self.root.get_screen("calorie").ids.food_name.text
        quantity = self.root.get_screen("calorie").ids.food_quantity.text
        meal = self.root.get_screen("calorie").ids.meal_category.text

        get_calories_button = self.root.get_screen("calorie").ids.get_calories_button
        saved_button = self.root.get_screen("calorie").ids.saved_button

        if food_item and quantity:
            get_calories_button.disabled = False
        else:
            get_calories_button.disabled = True

        if food_item and quantity and meal:
            saved_button.disabled = False
        else:
            saved_button.disabled = True

    def category(self, tf, focus):
        if not focus:
            return

        menu_items = [
            {
                "text": "Breakfast",
                "on_release": lambda x="Breakfast": self.category_callback(x)
            },
            {
                "text": "Lunch",
                "on_release": lambda x="Lunch": self.category_callback(x)
            },
            {
                "text": "Snack",
                "on_release": lambda x="Snack": self.category_callback(x)
            },
            {
                "text": "Dinner",
                "on_release": lambda x="Dinner": self.category_callback(x)
            },
        ]
        self.menu = MDDropdownMenu(caller=tf, items=menu_items, width_mult=4)
        self.menu.open()

    def category_callback(self, selected_category):
        self.root.get_screen("calorie").ids.meal_category.text = selected_category
        self.menu.dismiss()

    def saved_food(self):
        screen = self.root.get_screen('calorie')
        food_name = screen.ids.food_name.text
        food_quantity = screen.ids.food_quantity.text
        meal_category = screen.ids.meal_category.text
        calories_label = screen.ids.calorie_output.text.strip("Calories: ").strip()
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if food_name and food_quantity and meal_category and calories_label:
            payload = {
                "food_name": food_name,
                "food_quantity": food_quantity,
                "meal_category": meal_category,
                "calories": calories_label,
                "created": created,
                "updated": created
            }

            res = fc.insert_food(
                food_name,
                food_quantity,
                meal_category,
                calories_label,
                created,
                created
            )

            if res:
                screen.ids.food_name.text = ""
                screen.ids.food_quantity.text = ""
                screen.ids.meal_category.text = ""
                screen.ids.calorie_output.text = "Calories: "

                # Update calorie left
                calorie_left = float(screen.ids.calorie_left.text.split()[2]) - float(calories_label)
                screen.ids.calorie_left.text = f"Calorie Left\n {calorie_left:.2f}  "

                self.root.current = "calorie"

    @staticmethod
    def calculate_bmr(gender, weight, height, age):
        if gender.lower() == "male":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        return bmr

    @staticmethod
    def calculate_net_calories(bmr, activity_level):
        activity_multiplier = {
            "Not Very Active": 1.2,
            "Lightly Active": 1.375,
            "Active": 1.55,
            "Very Active": 1.725,
        }
        return bmr * activity_multiplier.get(activity_level, 1.2)

    def check(self, switch_instance, is_active):
        if is_active:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def show_date_picker(self):
        date_dialog = MDDatePicker(
            min_year=2020,
            max_year=datetime.now().year)
        date_dialog.bind(on_save=self.on_save, on_cancel=on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        diary_screen = self.root.get_screen("diary")
        diary_screen.ids.date_button.text = value.strftime("%A, %B %d, %Y")
        instance.dismiss()

    def login(self):
        message = ""

        username = self.root.get_screen("login").ids.username
        password = self.root.get_screen("login").ids.pss

        if username.text != "" and password.text != "":
            login_details = auth_tbl.login(username.text, password.text)

            if login_details is not None:
                auth = AuthModel(*login_details)

                username.text = ""
                password.text = ""

                res = auth_tbl.select_by_id(auth.id)

                if res is not None:
                    user_info = AuthModel(*res)

                    if user_info.id > 0:
                        self.root.get_screen("personal_data").ids.username.text = f"Username: {user_info.username}"
                        self.root.get_screen("personal_data").ids.email.text = f"Email: {user_info.email}"
                        self.root.get_screen("personal_data").ids.password.text = f"Password: {user_info.password}"
                        self.root.get_screen("personal_data").ids.customer_name.text = f"Name: {user_info.name}"
                        self.root.get_screen("personal_data").ids.customer_age.text = f"Age: {int(user_info.age)}"
                        self.root.get_screen("personal_data").ids.customer_gender.text = f"Gender: {user_info.gender}"
                        self.root.get_screen(
                            "personal_data").ids.customer_height.text = f"Height: {int(user_info.height)}"
                        self.root.get_screen(
                            "personal_data").ids.customer_weight.text = f"Weight: {int(user_info.weight)}"

                        self.root.get_screen(
                            "Goals").ids.customer_objective.text = f"Fitness Objective: {user_info.fitness_objective}"
                        self.root.get_screen(
                            "Goals").ids.customer_activity.text = f"Activity Level: {user_info.activity_level}"
                        self.root.get_screen(
                            "Goals").ids.customer_desire.text = f"Desired Weight: {user_info.fitness_goal}"
                        self.root.get_screen(
                            "Goals").ids.customer_months.text = (f"How Many Months Process: "
                                                                 f"{int(user_info.how_many_months_process)}")

                        self.root.get_screen("home").ids.customer_name.text = f"Hi, {user_info.username}"

                        self.root.get_screen("profile").ids.user.text = f"{user_info.username}"

                        # Calculate BMR and net calories
                        bmr = self.calculate_bmr(user_info.gender, int(user_info.weight), int(user_info.height),
                                                 int(user_info.age))
                        net_calories = self.calculate_net_calories(bmr, user_info.activity_level)

                        # Save net calories to be used in CalorieWindow
                        self.root.get_screen(
                            "calorie").ids.calorie_intake.text = f"Calorie Intake\n {int(net_calories)}"
                        self.root.get_screen("calorie").ids.calorie_left.text = f"Calorie Left\n {int(net_calories)}"

                        self.root.current = "home"

                else:
                    message = "User does not exist or username/password is incorrect"
            else:
                message = "User does not exist or username/password is incorrect"
        else:
            message = "Username and/or password cannot be empty."

        if message != "":
            self.show_snackbar(message)

    def signup_user(self):
        username = self.root.get_screen("signup").ids.username
        email = self.root.get_screen("signup").ids.email
        password = self.root.get_screen("signup").ids.password
        customer_name = self.root.get_screen("personal_info").ids.customer_name
        customer_age = self.root.get_screen("personal_info").ids.customer_age
        customer_gender = self.root.get_screen("personal_info").ids.customer_gender
        customer_height = self.root.get_screen("personal_info").ids.customer_height
        customer_weight = self.root.get_screen("personal_info").ids.customer_weight
        customer_objective = self.root.get_screen("fitness_objective").ids.customer_objective
        customer_activity = self.root.get_screen("fitness_objective").ids.customer_activity
        customer_desired = self.root.get_screen("fitness_objective").ids.customer_desired
        customer_months = self.root.get_screen("fitness_objective").ids.customer_months

        if len(password.text) < 8:
            message = "Password must be at least 8 characters long."
            self.show_snackbar(message)
            return

        if (username.text != "" and email.text != "" and password.text != "" and
                customer_name.text != "" and customer_age.text != "" and customer_gender.text != "" and
                customer_height.text != "" and customer_weight.text != "" and
                customer_objective.text != "" and customer_activity.text != "" and
                customer_desired.text != "" and customer_months.text != ""):

            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            bmr = self.calculate_bmr(customer_gender.text, int(customer_weight.text),
                                     int(customer_height.text), int(customer_age.text))
            net_calories = self.calculate_net_calories(bmr, customer_activity.text)

            inserted_id = auth_tbl.insert_info(
                username.text,
                email.text,
                password.text,
                customer_name.text,
                customer_age.text,
                customer_gender.text,
                customer_height.text,
                customer_weight.text,
                customer_objective.text,
                customer_activity.text,
                customer_desired.text,
                customer_months.text,
                created_at,
                updated_at
            )

            if inserted_id:
                res = auth_tbl.select_by_id(inserted_id)

                if res is not None:
                    user_info = AuthModel(*res)

                    if user_info.id > 0:
                        self.root.get_screen("personal_data").ids.username.text = f"Name: {user_info.username}"
                        self.root.get_screen("personal_data").ids.email.text = f"Email: {user_info.email}"
                        self.root.get_screen("personal_data").ids.password.text = f"Password: {user_info.password}"
                        self.root.get_screen("personal_data").ids.customer_name.text = f"Name: {user_info.name}"
                        self.root.get_screen("personal_data").ids.customer_age.text = f"Age: {int(user_info.age)}"
                        self.root.get_screen("personal_data").ids.customer_gender.text = f"Gender: {user_info.gender}"
                        self.root.get_screen(
                            "personal_data").ids.customer_height.text = f"Height: {int(user_info.height)}"
                        self.root.get_screen(
                            "personal_data").ids.customer_weight.text = f"Weight: {int(user_info.weight)}"

                        self.root.get_screen(
                            "Goals").ids.customer_objective.text = f"Fitness Objective: {user_info.fitness_objective}"
                        self.root.get_screen(
                            "Goals").ids.customer_activity.text = f"Activity Level: {user_info.activity_level}"
                        self.root.get_screen(
                            "Goals").ids.customer_desire.text = f"Desired Weight: {user_info.fitness_goal}"
                        self.root.get_screen(
                            "Goals").ids.customer_months.text = (f"How Many Months Process:"
                                                                 f" {int(user_info.how_many_months_process)}")

                        self.root.get_screen("home").ids.customer_name.text = f"Hi, {user_info.username}"

                        self.root.get_screen("profile").ids.user.text = f"{user_info.username}"

                        congratulation_screen = self.root.get_screen('congratulations')
                        congratulation_screen.ids.congratulation_message.text = (f"Your daily net goal is: \n "
                                                                                 f"{int(net_calories)} Calories")

                        # Save net calories to be used in CalorieWindow
                        self.root.get_screen(
                            "calorie").ids.calorie_intake.text = f"Calorie Intake\n {int(net_calories)}"
                        self.root.get_screen("calorie").ids.calorie_left.text = f"Calorie Left\n {int(net_calories)}"

                        self.root.current = "congratulations"
                    else:
                        message = "Something went wrong. No data were inserted!"
                        self.root.current = "login"
                else:
                    message = "Something went wrong. No data were inserted!"
                    self.root.current = "login"

                username.text = ""
                email.text = ""
                password.text = ""
                customer_name.text = ""
                customer_age.text = ""
                customer_gender.text = ""
                customer_height.text = ""
                customer_weight.text = ""
                customer_objective.text = ""
                customer_activity.text = ""
                customer_desired.text = ""
                customer_months.text = ""

                message = f"User with ID: {inserted_id} registered successfully!"
            else:
                message = "Something went wrong. No data were inserted!"
                self.root.current = "login"
        else:
            self.root.current = "personal_info"

    def on_enter(self):
        self.update_date()
        # Initialize the calorie left value based on net calories
        calorie_intake = self.ids.calorie_intake.text.split()[2]
        self.ids.calorie_left.text = f"Calorie Left\n {calorie_intake}"

    def update_date(self):
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.ids.date_label.text = current_date

    def update_calories(self, intake):
        net_calories = int(self.ids.calorie_intake.text.split()[2])
        calorie_left = net_calories - intake
        self.ids.calorie_left.text = f"Calorie Left\n {calorie_left}"

    def show_password(self, _, value):
        self.root.get_screen("login").ids.pss.password = False if value else True

    @staticmethod
    def show_snackbar(message):
        sb = MDSnackbar()
        sb.md_bg_color = (140 / 255, 140 / 255, 140 / 255, 1)
        sb.add_widget(MDLabel(text=message))
        sb.open()

    def save_login(self):
        usr = self.root.get_screen("signup").ids.username
        pwd = self.root.get_screen("signup").ids.password
        eml = self.root.get_screen("signup").ids.email

        if usr.text != "" and pwd.text != "" and eml.text != "":
            self.username = usr.text
            self.password = pwd.text
            self.email = eml.text

            self.root.transition.direction = "left"
            self.root.current = "personal_info"
        else:
            message = "Username and/or password and/or email cannot be empty."
            self.show_snackbar(message)

    def save_personal_info(self):
        self.customer_name = self.root.get_screen("personal_info").ids.customer_name
        self.customer_age = self.root.get_screen("personal_info").ids.customer_age
        self.customer_gender = self.root.get_screen("personal_info").ids.customer_gender
        self.customer_height = self.root.get_screen("personal_info").ids.customer_height
        self.customer_weight = self.root.get_screen("personal_info").ids.customer_weight

        if (self.customer_name.text != "" and self.customer_age.text != "" and self.customer_gender.text != ""
                and self.customer_height.text != "" and self.customer_weight.text != ""):
            self.customer_name = self.customer_name.text
            self.customer_age = self.customer_age.text
            self.customer_gender = self.customer_gender.text
            self.customer_height = self.customer_height.text
            self.customer_weight = self.customer_weight.text

            self.root.transition.direction = "left"
            self.root.current = "fitness_objective"
        else:
            message = "Name and/or age and/or gender and/or height and/or weight cannot be empty."
            self.show_snackbar(message)

    def objective(self, tf, focus):
        if not focus:
            return

        menu_items = [
            {
                "text": "Lose Weight",
                "on_release": lambda x="Lose Weight": self.objective_callback(x)
            },
            {
                "text": "Gain Weight",
                "on_release": lambda x="Gain Weight": self.objective_callback(x)
            },
            {
                "text": "Maintain Weight",
                "on_release": lambda x="Maintain Weight": self.objective_callback(x)
            },
            {
                "text": "Gain Muscles",
                "on_release": lambda x="Gain Muscles": self.objective_callback(x)
            },
        ]

        self.menu = MDDropdownMenu(caller=tf, items=menu_items, width_mult=2)
        self.menu.open()

    def objective_callback(self, selected_objective):
        self.root.get_screen("fitness_objective").ids.customer_objective.text = selected_objective
        self.customer_objective = selected_objective
        self.menu.dismiss()

    def activity(self, tf, focus):
        if not focus:
            return

        menu_items = [
            {
                "text": "Active",
                "on_release": lambda x="Active": self.activity_callback(x)
            },
            {
                "text": "Not Very Active",
                "on_release": lambda x="Not Very Active": self.activity_callback(x)
            },
            {
                "text": "Lightly Active",
                "on_release": lambda x="Lightly Active": self.activity_callback(x)
            },
            {
                "text": "Very Active",
                "on_release": lambda x="Very Active": self.activity_callback(x)
            },
        ]

        self.menu = MDDropdownMenu(caller=tf, items=menu_items, width_mult=2)
        self.menu.open()

    def activity_callback(self, selected_activity):
        self.root.get_screen("fitness_objective").ids.customer_activity.text = selected_activity
        self.customer_activity = selected_activity
        self.menu.dismiss()

    @staticmethod
    def get_user_id():
        # Implement this method to retrieve the actual user ID
        return 1  # Placeholder user ID

    def on_logout_btn_pressed(self):
        md = MDDialog(
            title="Are you sure you want to logout from this account?",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: md.dismiss()  # Dismiss the dialog on cancel
                ),
                MDFlatButton(
                    text="LogOut",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                    on_release=lambda x: self.on_yes_logout_btn(md)
                ),
            ],
        )

        md.open()

    def on_yes_logout_btn(self, dialog):
        dialog.dismiss()
        self.user_id = None  # Clear the user ID after logout
        self.root.current = "welcome"  # Navigate to login screen

    @staticmethod
    def on_cancel_btn(dialog):
        dialog.dismiss()


if __name__ == '__main__':
    FitnessApp().run()
