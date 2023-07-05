import os
import csv
import sys
import time
from cryption import SimpleEnDecrypt

key = ''

def validation():
    global key
    try:
        with open('configuration.xml', 'r') as conf:
            for line in conf:
                key, password_real = line.split(',')
        e2e = SimpleEnDecrypt(key)
        password_check = input('Password: ')
        if password_check == e2e.decrypt(password_real):
            return 1
        else:
            return 0

    except FileNotFoundError:
        print('Welcome to PyPass!\nBefore you move on, you need to create your new password.')
        print('WARNING: IF YOU FORGET YOUR PASSWORD, YOU CAN NOT ACCESS TO YOUR DATABASE!\n')
        password_setup = input('New password: ')
        e2e = SimpleEnDecrypt()
        password = e2e.encrypt(password_setup)
        key = e2e.key.decode('UTF-8')
        with open('configuration.xml', 'w') as conf:
            conf.write(f'{key},{password}')
        return 1

def menu(a):
    while True:
        if a == '1' or a == '2' or a == '3' or a == '4':
            return a
        else:
            return 'Wrong'


def encrypt():
    os.system('clear')
    global key
    name = input('Name: ')
    id = input('ID or Email: ')
    os.system('clear')
    password = input('Password: ')
    os.system('clear')
    info = input('Additional info (optional): ')
    os.system('clear')
    print(f'Name: {name}')
    print(f'ID or Email: {id}')
    print(f'Password: {password}')
    print(f'Additional info: {info}\n')
    if input('Type "Y" to encrypt and save. Type anything else to cancel. ') == 'Y':
        e2e = SimpleEnDecrypt(key)
        name = e2e.encrypt(name)
        id = e2e.encrypt(id)
        password = e2e.encrypt(password)
        info = e2e.encrypt(info)
        with open('database.csv', 'a') as file:
            file.write(f'{name},{id},{password},{info}\n')
        os.system('clear')
        print('Successfully encrypted and saved in a file "database.csv"!')
        time.sleep(2)
    else:
        os.system('clear')
        print('Process Canceled.')
        time.sleep(2)

def decrypt():
    os.system('clear')
    data = []
    global key
    e2e = SimpleEnDecrypt(key)
    try:
        with open('database.csv', 'r') as file:
            rdr = csv.reader(file)
            for row in rdr:
                data.append({'name': row[0], 'id': row[1], 'password': row[2], 'info': row[3]})

        for db in sorted(data, key=lambda db: db['name']):
            name = db['name']
            id = db['id']
            password = db['password']
            info = db['info']
            name = e2e.decrypt(name)
            id = e2e.decrypt(id)
            password = e2e.decrypt(password)
            info = e2e.decrypt(info)

            if info == '':
                info = 'None'

            print(f'{name} | ID/Email: {id}, Password: {password}, Additional Info: {info}')
        input('\nType any key to continue...\n')
        return 1
    except FileNotFoundError:
        input('Nothing seems saved yet. Type any key to continue...')
        return 0


def reset():
    os.system('clear')
    print('To reset everything, type your password.\n')
    v = validation()
    if v == 0:
        print('\nInvalid password. Returning to menu...')
        time.sleep(2)
        return 0
    else:
        try:
            file_path1 = 'configuration.xml'
            os.remove(file_path1)
            file_path2 = 'database.csv'
            os.remove(file_path2)
            os.system('clear')
            return 1
        except OSError:
            os.system('clear')
            return 1

def main():
    v = validation()
    if v == 0:
        sys.exit('Invalid password. Program is now closed.')
    while True:
        os.system('clear')
        print('=== MENU ===')
        print('1. Save and encrypt')
        print('2. Decrypt and export')
        print('3. Reset')
        print('4. Quit')
        m = menu(input('\nType the number: '))
        if m == '1':
            encrypt()
        elif m == '2':
            decrypt()
        elif m == '3':
            r = reset()
            if r == 1:
                sys.exit('Everything cleared. Program is now closed.')
        elif m == '4':
            sys.exit('\nProgram is now closed.')


if __name__ == '__main__':
    main()