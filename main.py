from user import User, InvalidUserDataError
from chat import Chat
from attachment import Attachment
from Contacts import ContactList
from admin import Admin



def main():


    admin = Admin(json_path="data.json", xml_path="data.xml")

    try:
        user1 = User(username="Semen", phone="1234567890", mail="bublic@gmail.com")
        user2 = User(username="Roman", phone="987654321", mail="cucumber@mail.com")
        user3 = User(username="Artem", phone="88005553535", mail="Artem228@mail.com")

        contacts = ContactList(owner=user1)
        contacts.add(user2)
        contacts.add(user3)

        Super_Max = Chat(name="Work Chat", members=[user1, user2, user3])

        Super_Max.send_message(user1,
                               "Привет, коллеги! Мы с вами находимся в лучшем мессенджере, его ловит даже на парковке!")
        Super_Max.send_message(user2, "Привет! Я очень рад.")
        Super_Max.send_message(
            user3,
            "Я отправила файл",
            attachment=Attachment(file_name="report.pdf", file_size=1024),
        )

        admin.add(user1)
        admin.add(user2)
        admin.add(user3)
        admin.add(Super_Max)
        admin.add(contacts)

        admin.save_json()
        admin.save_xml()

        loaded = admin.load_json()
        admin.data = loaded

        admin.save_json()
    except InvalidUserDataError as e:
        print(f"Ошибка создания пользователя: {e}")
        return



if __name__ == "__main__":
    main()