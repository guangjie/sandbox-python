def main():
    print('create new users')

    check_config()

    input_new_user_credentials()

    create_new_user()

    email_new_user()


def check_config():
    print('checking config')


def input_new_user_credentials():
    print('will start to collect user crednetials')


def create_new_user():
    print('creating new users in database')


def email_new_user():
    print('send credentials via email')


if __name__ == '__main__':
    main()