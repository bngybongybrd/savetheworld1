import sqlite3


def posts():
  # Connect to database and Create a cursor
  conn = sqlite3.connect('posts.db')
  c = conn.cursor()
  c.execute("SELECT * FROM posts")
  items = c.fetchall()
  items = items[::-1]

  # Commit our command and Close the connection
  conn.commit()
  conn.close()

  return items


# -------------------------------
# USEFUL


def show_all_users():
  # Connect to database and Create a cursor
  conn = sqlite3.connect('user_database.db')
  c = conn.cursor()
  c.execute("SELECT * FROM user_database")

  items = c.fetchall()
  #for item in items:
  #    print(item)
  #items = [str(i) for i in items]
  # Commit our command and Close the connection
  conn.commit()
  conn.close()
  return items


def add_user(username, email, password):
  # Connect to database and Create a cursor
  conn = sqlite3.connect('user_database.db')
  c = conn.cursor()
  c.execute("INSERT INTO user_database VALUES (?,?,?)",
            [username, email, password])
  # Commit our command and Close the connection
  conn.commit()
  conn.close()


def user_lookup(username):
  # Connect to database and Create a cursor
  conn = sqlite3.connect('user_database.db')
  c = conn.cursor()
  c.execute("SELECT rowid, * from user_database WHERE username = (?)",
            [username])
  # Commit our command and Close the connection
  user = c.fetchone()
  conn.commit()
  conn.close()
  if user:
    return True
  else:
    return False


def email_lookup(email):
  # Connect to database and Create a cursor
  conn = sqlite3.connect('user_database.db')
  c = conn.cursor()
  c.execute("SELECT * from user_database WHERE email = (?)", [email])
  # Commit our command and Close the connection
  email_check = c.fetchone()
  conn.commit()
  conn.close()
  if email_check:
    return True
  else:
    return False


def pw_check(password_typed, email):
  # Connect to database and Create a cursor
  conn = sqlite3.connect('user_database.db')
  c = conn.cursor()
  c.execute("SELECT rowid, * from user_database WHERE email = (?)", [email])
  # Commit our command and Close the connection
  usr = c.fetchone()
  conn.commit()
  conn.close()
  if password_typed == usr[3]:
    return True
  else:
    return False


def get_user_with_email(email):
  # Connect to database and Create a cursor
  conn = sqlite3.connect('user_database.db')
  c = conn.cursor()
  c.execute("SELECT rowid, * from user_database WHERE email = (?)", [email])
  usr = c.fetchone()
  usr = list(usr)
  # Commit our command and Close the connection
  conn.commit()
  conn.close()
  return usr


def get_user_with_rowid(rowid):
  # Connect to database and Create a cursor
  conn = sqlite3.connect('user_database.db')
  c = conn.cursor()
  c.execute("SELECT rowid, * from user_database WHERE rowid = (?)", [rowid])
  usr = c.fetchone()
  usr = list(usr)
  # Commit our command and Close the connection
  conn.commit()
  conn.close()
  return usr


def add_post(author, title, content, date):
  # Connect to database and Create a cursor
  conn = sqlite3.connect('posts.db')
  c = conn.cursor()
  c.execute("INSERT INTO posts VALUES (?,?,?,?)",
            [author, title, content, date])
  # Commit our command and Close the connection
  conn.commit()
  conn.close()


def show_all_posts():
  # Connect to database and Create a cursor
  conn = sqlite3.connect('posts.db')
  c = conn.cursor()
  c.execute("SELECT * FROM posts")

  items = c.fetchall()

  # Commit our command and Close the connection
  conn.commit()
  conn.close()
  return items


'''
# posts.db | Table 'posts' format
CREATE TABLE posts (
            user text,
            title text,
            content text,
            date text
          )

# user_database | Table 'user_database' format
CREATE TABLE user_database (
            username text,
            email text,
            password text
          )

# Connect to database and Create a cursor
conn = sqlite3.connect('.db')
c = conn.cursor()
c.execute()
# Commit our command and Close the connection
conn.commit()
conn.close()
'''
