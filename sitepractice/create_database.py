import sqlite3


def create_database():
    conn = sqlite3.connect('resumes.db')
    cursor = conn.cursor()

    #таблицф resumes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            job_title TEXT,
            skills TEXT
        )
    ''')

    conn.commit()
    conn.close()


# Вызываем функцию создания базы данных
create_database()
