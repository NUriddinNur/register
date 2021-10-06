import platform
import os
import time
import mysql.connector


class User:
    def __init__(self):
        self.name = None
        self.age = None
        self.login = None
        self.password = None
        self.single = 1
        self.user_id = None

        self.selection_options()

    def selection_options(self) -> None:
        self.clear_window()
        self.init_message()
        if self.register_or_login():
            self.register()
        else:
            self.log_in()

    def register_or_login(self) -> bool:
        init_input = input("[1/2]: ").strip()
        register_option = ["1", "2"]
        while init_input not in register_option:
            self.clear_window()
            print("invalid input !!!")
            init_input = input("[1/2]: ").strip()
        return True if init_input == "1" else False

    def register(self) -> None:
        self.clear_window()
        input_name = input("ismingizni kiriting: ").strip().capitalize()
        while not input_name.isalpha():
            self.clear_window()
            print("Ismingizni qayta kiriting:")
            input_name = input("ismingizni kiriting: ").strip().capitalize()

        input_login = input("Login kiriting: ").strip().lower()
        while not input_login.isalnum() or self.login_exists(input_login):
            self.clear_window()
            if self.login_exists(input_login):
                print("bunday login mavjud")
            print("Login qayta kiriting !!!")
            input_login = input("Login kiriting: ").strip().lower()

        input_password = input("Parol kiriting: ").strip()
        check_password = input("Parolni takroran kiriting: ").strip()
        while self.is_str_emtpy(input_password) or input_password != check_password:
            self.clear_window()
            print("Parolni qaytadan kiriting !!!")
            input_password = input("Parol kiriting: ").strip()
            check_password = input("Parolni takroran kiriting: ").strip()

        input_age = input("Yoshingizni kiriting: ").strip()
        while not input_age.isnumeric():
            self.clear_window()
            print("yoshingizni qayta kiriting: ")
            input_age = input("Yoshingizni kiriting: ").strip()

        single_options = ["y", "yes", "n", "no"]
        input_single = input("Are you single? [y/n]: ").strip().lower()
        while input_single not in single_options:
            self.clear_window()
            print("qayta kiriting: ")
            print(single_options)
            single_options = ["y", "yes", "n", "no"]
            input_single = input("Are you single? [y/n]: ").strip().lower()

        self.name = input_name
        self.login = input_login
        self.password = input_password
        self.age = int(input_age)
        if input_single in single_options[:2]:
            self.single = 0
        self.write_to_db()

        self.clear_window()
        self.message_registration(input_name)
        self.clear_window()
        self.selection_options()

    def log_in(self):
        self.clear_window()
        input_login = input("Login kiriting: ").strip()
        input_password = input("Password kiriting: ").strip()
        while not self.check_log_pass(input_login, input_password):
            self.clear_window()
            print("Login yoki parol xato !!!")
            print("login va parolni qayta kiriting")
            input_login = input("Login kiriting: ").strip()
            input_password = input("Password kiriting: ").strip()
        self.user_page()

    def login_exists(self, user1) -> bool:
        users_ = self.read_database()
        for i in range(len(users_)):
            if user1 in users_[i]:
                return True
        return False

    def check_log_pass(self, log, pasw):
        result = self.read_database()
        for i in range(len(result)):
            if result[i][3] == log and result[i][4] == pasw:
                self.user_id = result[i][0]
                print(self.user_id)
                return True
        return False

    def write_to_db(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="abdulla",
            password="123456789",
            database="users"
        )
        mycursor = mydb.cursor()
        mycursor.execute(
            f"insert into user1(name, age, login, password, single) values('{self.name}', '{self.age}', '{self.login}', '{self.password}', '{self.single}');")
        mydb.commit()

    def user_page(self):
        self.clear_window()
        self.message_logged()
        input_create_account = input("[1/2/3/4]: ").strip()
        create_options = ["1", "2", "3", "4"]
        while not input_create_account.isnumeric() or input_create_account not in create_options:
            self.clear_window()
            self.message_logged()
            input_create_account = input("[1/2/3/4]: ").strip()

        while input_create_account != "4":

            if input_create_account == "1":
                self.update_login()
            elif input_create_account == "2":
                self.update_password()
            else:
                self.delete_account()
                self.clear_window()
                print("\n\n\n\t\tAccaunt o'chirildi !!!")
                time.sleep(2)
                self.__init__()
        self.clear_window()
        self.__init__()

    def update_login(self):
        new_login = input("Yangi login kiriting: ").strip().lower()
        while not (new_login.isalnum() and not self.login_exists(new_login)):
            self.clear_window()
            if self.login_exists(new_login):
                print("bunday login mavjud")
            print("Login qayta kiriting !!!")
            new_login = input("Login kiriting: ").strip().lower()
        self.add_to_db(new_login, "login")
        self.clear_window()
        print("\n\n\n\t\tLogin o'zgartirildi !!!")
        time.sleep(2)
        self.user_page()

    def update_password(self):
        new_password = input("Parol kiriting: ").strip()
        check_password = input("Parolni takroran kiriting: ").strip()
        while self.is_str_emtpy(new_password) or new_password != check_password:
            self.clear_window()
            print("Parolni qaytadan kiriting !!!")
            input_password = input("Parol kiriting: ").strip()
            check_password = input("Parolni takroran kiriting: ").strip()
        self.add_to_db(new_password, "password")
        self.clear_window()
        print("\n\n\n\t\tpassword o'zgartirildi !!!")
        time.sleep(2)
        self.user_page()

    def delete_account(self):
        self.delete_from_db()

    def add_to_db(self, new_data, eski_data):
        mydb = mysql.connector.connect(
            host="localhost",
            user="abdulla",
            password="123456789",
            database="users"
        )
        mycursor = mydb.cursor()
        mycursor.execute(f"update user1 set {eski_data}='{new_data}' where id={self.user_id};")
        mydb.commit()

    def delete_from_db(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="abdulla",
            password="123456789",
            database="users"
        )
        mycursor = mydb.cursor()
        mycursor.execute(f"delete from user1 where id='{self.user_id}'")
        mydb.commit()

    @staticmethod
    def read_database():
        mydb = mysql.connector.connect(
            host="localhost",
            user="abdulla",
            password="123456789",
            database="users"
        )
        mycursor = mydb.cursor()
        mycursor.execute("select * from user1")
        result = mycursor.fetchall()
        return result

    # ________________________________________________ message function ______________________________________
    @staticmethod
    def message_registration(new_user) -> None:
        print(f"""
                    {new_user}  Siz muvofaqiyatli ro'yxatdan o'tdingiz !!!
            """)
        time.sleep(3)

    @staticmethod
    def init_message() -> None:
        print("""
                    Tizimga kirish:
                    Register:   [1]
                    log_in:     [2]
                """)

    @staticmethod
    def clear_window() -> None:
        if platform.system() == "Linux":
            os.system("clear")
        elif platform.system() == "windows":
            os.system("cls")

    @staticmethod
    def is_str_emtpy(input_: str) -> bool:
        return not input_

    def message_logged(self) -> None:
        self.clear_window()
        print("""
                                    Tizimga kirdingiz !!!
                                Loginni o'zgartirish    [1]
                                Passwordni o'zgartirish [2]
                                Accaunt o'chirish       [3]
                                Log out                 [4]
                        """)


user = User()
