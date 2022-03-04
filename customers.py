"""Customers at Ubermelon."""


import email


class Customer(object):
    """Ubermelon customer."""
    
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.firstname} {self.lastname} {self.email}>"


    
def read_customers(filename):
    customers_dict = {}
    with open(filename) as file:
        for line in file:
            firstname, lastname, email, password = line.strip().split('|')
            customers_dict[email] = Customer(firstname, lastname, email, password)
    return customers_dict

def get_by_email(email):
    return customers[email]


        

customers = read_customers("customers.txt")

