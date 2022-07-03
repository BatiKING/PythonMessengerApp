import argparse
from models import Message, User
from sql_utils import Connection
from pass_hasher import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="recipient username")
parser.add_argument("-s", "--send", help="Message text")
parser.add_argument("-l", "--list", help="print all messages", action="store_true")

args = parser.parse_args()
conn = Connection()


def list_user_messages(username, password):
    user = User.load_user_by_username(conn.get_cursor(), username)
    messages = []
    if user:
        if check_password(password, user.hashed_password):
            messages = Message.load_user_messages(conn.get_cursor(), user.id)
            if messages:
                for message in messages:
                    sender_user = User.load_user_by_id(conn.get_cursor(), message.from_id)
                    print(
                        f"Sender: {sender_user.username}\nDateTime: {message.creation_date}\nMessage: {message.text}\n")
            else:
                print("No messages found")
        else:
            print("Wrong password")
    else:
        print("User not found")


def send_message(username, password, to_username, message):
    user = User.load_user_by_username(conn.get_cursor(), username)
    if user:
        if check_password(password, user.hashed_password):
            to_user = User.load_user_by_username(conn.get_cursor(), to_username)
            if to_user:
                if len(message) < 255:
                    recipient_id = to_user.id
                    recipient_username = to_user.username
                    msg = Message(user.id, recipient_id, message)
                    msg.save_to_db(conn.get_cursor())
                else:
                    print("Message is too long - max length is 254 characters")
            else:
                print("Recipient not found")
        else:
            print("Wrong password")
    else:
        print("User not found")


if __name__ == '__main__':
    # list_user_messages("user1", "12345678")
    # text_message = """Lubie placki - 4"""
    # send_message("Batman5", "TekkenPinaczoPulos", "user1", text_message)

    if args.username and args.password and args.list and not args.to and not args.send:
        list_user_messages(args.username, args.password)
    elif args.username and args.password and not args.list and args.to and args.send:
        send_message(args.username, args.password, args.to, args.send)
    else:
        parser.print_help()

if conn:
    conn.close()
