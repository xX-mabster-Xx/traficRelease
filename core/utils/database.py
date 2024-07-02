import sqlite3
from typing import Union


class DbRequest:
    def __init__(self, connection) -> None:
        self.connection = connection

    def create_if_not_exists(self):
        cur = self.connection.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS links(user_id INTEGER PRIMARY KEY, link TEXT, invited_by TEXT,'
                    ' balance INTEGER, timestamp integer)')
        self.connection.commit()

    def get_bd(self):
        cur = self.connection.cursor()
        self.create_if_not_exists()
        cur.execute('SELECT * FROM links')
        rows = cur.fetchall()
        for row in rows:
            print(row)
        self.connection.commit()

    def insert_link(self, user_id: int, link: str, invited_by: Union[str, int, None]):
        cur = self.connection.cursor()
        self.create_if_not_exists()
        if type(invited_by) is int:
            cur.execute('INSERT OR IGNORE INTO links(user_id, link, invited_by, timestamp) '
                        'VALUES (?, ?, ?, strftime("%s", "now"))',
                        (user_id, link, invited_by))
        else:
            cur.execute('INSERT OR IGNORE INTO links(user_id, link, invited_by, timestamp) '
                        'VALUES (?, ?, (SELECT user_id FROM links WHERE link==?), strftime("%s", "now"))',
                        (user_id, link, invited_by))

        self.connection.commit()

    def get_by_id(self, user_id: int):
        cur = self.connection.cursor()
        self.create_if_not_exists()
        cur.execute('SELECT * FROM links WHERE user_id==?', (user_id,))
        rows = cur.fetchall()
        return rows

    def get_balance(self, user_id: int):
        cur = self.connection.cursor()
        self.create_if_not_exists()
        cur.execute('SELECT balance FROM links WHERE user_id==?', (user_id,))
        bal = cur.fetchone()
        return bal[0]

    def get_refs(self, user_id: int):
        cur = self.connection.cursor()
        self.create_if_not_exists()
        cur.execute('SELECT user_id FROM links WHERE invited_by==?', (user_id,))
        rows = cur.fetchall()
        return rows

    def get_pool_info(self):
        cur = self.connection.cursor()
        cur.execute('SELECT size, money FROM poolsize ORDER BY timestamp DESC LIMIT 1')
        res = cur.fetchone()
        return res

    def insert_pool_info(self, size: int, money: int):
        cur = self.connection.cursor()
        cur.execute('INSERT INTO poolsize(timestamp, size, money) '
                    'VALUES (strftime("%s", "now"), ?, ?)',
                    (size, money))
        self.connection.commit()

    def edit_link(self, user_id: int, new_link: str):
        cur = self.connection.cursor()
        self.create_if_not_exists()
        cur.execute('UPDATE links SET link = ? WHERE user_id = ?', (new_link, user_id))
        self.connection.commit()

    def get_users(self):
        cur = self.connection.cursor()
        self.create_if_not_exists()
        cur.execute('SELECT user_id FROM links')
        rows = cur.fetchall()
        return rows

if __name__ == '__main__':
    pass