from pass_hasher import hash_password, check_password, generate_salt
from sql_utils import Connection


class User:
    def __init__(self, username='', password='', salt=None):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    def __str__(self):
        return f"id: {self._id}\nusername: {self.username}\npass_hash: {self._hashed_password}\n"

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=None):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()['id']
            print(self._id)
            cursor.close()
            return True
        else:
            sql = """UPDATE users SET username=%s, hashed_password=%s WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            cursor.close()
            return True

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        if self._id != -1:
            sql = "DELETE FROM users WHERE id=%s"
            cursor.execute(sql, (self.id,))
            self._id = -1
            return True
        return False


class Message:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None

if __name__ == '__main__':
    conn = Connection()

    # create user example
    # us = User('Bati', 'dzikus')
    # us.save_to_db(conn.get_cursor())

    # fetch user by ID example
    # user1 = User.load_user_by_id(conn.get_cursor(), 15)
    # if user1:
    #     print(user1.id)
    #     print(user1.username)
    #     print(user1.hashed_password)
    # else:
    #     print("No such user")

    # fetch all users example
    # users = User.load_all_users(conn.get_cursor())
    # [print(user) for user in users]

    # update user example
    # user1 = User.load_user_by_id(conn.get_cursor(), 13)
    # user1.set_password("TestoweHaslo")
    # user1.save_to_db(conn.get_cursor())

    # delete user example
    # user1 = User.load_user_by_id(conn.get_cursor(), 13)
    # if user1:
    #     user1.delete(conn.get_cursor())
    # else:
    #     print("no such user")

    conn.close()
