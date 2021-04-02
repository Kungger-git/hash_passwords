import hashlib
import os
import argparse
import json
from base64 import b64encode, b64decode


class Register:

    def __init__(self, register):
        self.username = register[0]
        self.password = register[1]

    def hash_password(self):
        users = {}

        salt = b64encode(os.urandom(64)).decode('utf-8')
        key = b64encode(hashlib.pbkdf2_hmac('sha256', self.password.encode('utf-8'), b64decode(salt.encode('utf-8')), 100000)).decode('utf-8')
        users[self.username] = {
            'password': salt+key,
        }
        with open('user.json', 'w', encoding='utf-8') as f_source:
            json.dump(users, f_source, indent=2)
            for dict in users:
                print(f'{dict} has been added')


class Login:

    def __init__(self, login):
        self.username = login[0]
        self.password = login[1]

    def verify_user(self):
        with open('user.json', encoding='utf-8') as j_source:
            source = json.load(j_source)

        for dict in source:
            if not self.username == dict:
                print('Wrong Username')
            else:
                new_key = hashlib.pbkdf2_hmac('sha256', self.password.encode('utf-8'), b64decode(source[self.username]['password'][:88].encode('utf-8')), 100000)

                if not b64decode(source[self.username]['password'][88:].encode('utf-8')) == new_key:
                    print('Wrong Password')
                else:
                    print(f'Successfully logged in as {dict}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hash Passwords.')

    parser.add_argument('-r', '--register',
                        nargs=2, metavar='REGISTER',
                        action='store', help='Register Account (Username & Password)')

    parser.add_argument('-l', '--login',
                        nargs=2, metavar='LOGIN',
                        action='store', help='Login Account (Username & Password)')

    args = parser.parse_args()

    if args.register:
        Register([x for x in args.register]).hash_password()

    if args.login:
        Login([x for x in args.login]).verify_user()
