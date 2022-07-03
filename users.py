import argparse
from models import User
from sql_utils import Connection
from psycopg2.errors import UniqueViolation
from pass_hasher import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new Password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()
conn = Connection()


def create_user(username, password):
    if len(password) > 7:
        try:
            new_user = User(username, password)
            new_user.save_to_db(conn.get_cursor())
        except UniqueViolation:
            print("Username already exist")
    else:
        print("Password should be at least 8 characters long")


def edit_user(username, password, new_pass):
    if len(new_pass) > 7:
        user_to_edit = User.load_user_by_username(conn.get_cursor(), username)
        if user_to_edit:
            if check_password(password, user_to_edit.hashed_password):
                user_to_edit.set_password(new_pass)
                user_to_edit.save_to_db(conn.get_cursor())
                return True
            else:
                print("Wrong Password")
        else:
            print("User doesn't exist")
            return False
    else:
        print("New password should be at least 8 characters long")
        return False


def delete_user(username, password):
    user_to_edit = User.load_user_by_username(conn.get_cursor(), username)
    if user_to_edit:
        if check_password(password, user_to_edit.hashed_password):
            user_to_edit.delete(conn.get_cursor())
            return True
        else:
            print("Wrong Password")
            return False
    else:
        print("User not found")
        return False


def list_all_users():
    users = []
    users = User.load_all_users(conn.get_cursor())
    [print(user.username) for user in users]


if __name__ == '__main__':
    # pass
    # create_user("Bati13", "12345678")
    # edit_user("Bati13", "lolrotflmao", "lolrotflmao37777")
    # delete_user("Bati13", "lolrotflmao37777")
    # list_all_users()
    if args.username and args.password and not args.edit and not args.delete:
        create_user(args.username, args.password)
    elif args.username and args.password and args.edit and args.new_pass and not args.delete:
        edit_user(args.username, args.password, args.new_pass)
    elif args.username and args.password and args.delete and not args.edit and not args.new_pass:
        delete_user(args.username, args.password)
    else:
        parser.print_help()
    if args.list:
        list_all_users()
if conn:
    conn.close()
