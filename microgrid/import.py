import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect('microgrid.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS calculations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monthly_kwh REAL NOT NULL,
        panels_needed INTEGER NOT NULL,
        monthly_savings REAL NOT NULL,
        annual_savings REAL NOT NULL,
        calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()


print("done")
