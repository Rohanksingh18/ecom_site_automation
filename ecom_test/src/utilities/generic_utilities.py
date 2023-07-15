import logging as logger
import random
import string
from html.parser import HTMLParser


# define a class that uses to generate random email and password
def generate_random_email_and_password(domain=None, email_prefix=None):
    logger.debug("Generating random email and password.")

    if not domain:
        domain = 'gmail.com'
    if not email_prefix:
        email_prefix = 'testuser'

    random_email_sting_length = 10
    random_string = ''.join(random.choices(string.ascii_lowercase, k=random_email_sting_length))

# email format
    email = email_prefix + '_' + random_string + '@' + domain

    password_length = 10
    password_string = ''.join(random.choices(string.ascii_letters, k=password_length))

    random_info = {'email': email, 'password': password_string}
    logger.debug(f"randomly generated email and password: {random_info}")

    return random_info


# to generate random string
def generate_random_string(length=8, prefix=None, suffix=None):

    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))

    if prefix:
        random_string = prefix + random_string
    if suffix:
        random_string = random_string + suffix

    return random_string


# define a class used to generate coupon code
def generate_random_coupon_code(suffix=None, length=10):

    code = ''.join(random.choices(string.ascii_uppercase, k=length))
    if suffix:
        code += suffix

    return code


# define a class used to convert html to text
def convert_html_to_text(input_html_string):

    class HTMLFilter(HTMLParser):
        text = ""

        def handle_data(self, data):
            self.text += data

    f = HTMLFilter()
    f.feed(input_html_string)
    return f.text