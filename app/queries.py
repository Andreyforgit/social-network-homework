def register_user_query(conn, login, hashed_pw, first_name, last_name,birth_date, gender, city):
  with conn.cursor() as cur:
    cur.execute(
      """INSERT INTO users (login, password_hash, first_name, last_name, birth_date, gender, city)
         VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
      (login, hashed_pw, first_name, last_name, birth_date, gender, city)
    )
    user_id = cur.fetchone()['id']

    # Интересы пока храним как NULL, их можно добавить отдельной таблицей в следующих ДЗ 
    return user_id

def get_user_by_login_query(conn, login):
  with conn.cursor() as cur:
    cur.execute("SELECT * FROM users WHERE login = %s", (login,))
    return cur.fetchone()

def get_user_by_id_query(conn, user_id):
  with conn.cursor() as cur:
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cur.fetchone()