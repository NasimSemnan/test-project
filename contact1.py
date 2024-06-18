import json


class contact_manager:
    def __init__(self, open):
        self.open = open

    def add_contact(self):
        name = input("enter name")
        lastname = input("enter last name")
        phone = input("enter phone namber")
        email = input("enter email adress")
        address = input("enter you home adress")
        contact = {
            "name": name,
            "lastname": lastname,
            "phone": phone,
            "email": email,
            "address": address,
        }
        return contact

    out_csv = add_contact()
    print(out_csv)


def write_contact(self, contact):
    with open(self.open, "a") as cant:
        cant.write(json.dumps(contact) + "\n")


def read_contacts(self, filename):
    with open(filename, "w") as file:
        file.read(out_csv)


contact_manager()
contact = add_contact()
write_contact(contact, "contact.json")
print("add cantact okay")
