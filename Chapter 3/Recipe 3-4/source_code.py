import sqlite3
import pickle
import base64

# Mock database setup
conn = sqlite3.connect(':memory:')  # Using in-memory database for simplicity
cursor = conn.cursor()

# Create a mock 'users' table
cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpass')")
cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'userpass')")

# Vulnerable user login function (SQL Injection)
def login(username, password):
    # Insecure way of formatting SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        return "Login successful"
    else:
        return "Login failed"

# Vulnerable data retrieval function (Insecure Deserialization)
def get_user_data(serialized_data):
    # Deserializing without validation or sanitation
    data = pickle.loads(base64.b64decode(serialized_data))
    return data

# Mock login attempts (SQL Injection vulnerability demonstration)
def mock_login_attempts():
    # Legitimate login attempt
    print(login('admin', 'adminpass'))

    # Malicious login attempt exploiting SQL injection
    print(login('admin\' -- ', ''))

# Mock data retrieval (Insecure Deserialization vulnerability demonstration)
def mock_data_retrieval():
    # Serialized legitimate data
    legitimate_data = base64.b64encode(pickle.dumps({'username': 'admin', 'access_level': 'user'})).decode()
    print(get_user_data(legitimate_data))

    # Malicious payload exploiting deserialization
    class Malicious:
        def __reduce__(self):
            return (exec, ('import os; os.system(\'echo You have been hacked\')',))
    
    malicious_data = base64.b64encode(pickle.dumps(Malicious())).decode()
    print(get_user_data(malicious_data))

if __name__ == '__main__':
    mock_login_attempts()
    mock_data_retrieval()

conn.close()
