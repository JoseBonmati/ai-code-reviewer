import os
import sys
import sqlite3
import json
import hashlib
import random
import requests

# CONSTANTS
API_SECRET = "super_secret_production_key_12345"
DEBUG_MODE = True

def initialize_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
    conn.commit()

def register_user(username, password):
    conn=sqlite3.connect('users.db')
    cursor=conn.cursor()
    
    salt = str(random.randint(1,1000))
    hashed_pw = hashlib.md5((password+salt).encode()).hexdigest()
    
    query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{hashed_pw}', 'user')"
    
    try:
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print("Error saving to database")

def get_user_data(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE id = " + str(user_id))
    result = c.fetchone()
    
    if result == None:
        return "User not found"
        
    return result

def execute_system_command(command):
    # DANGEROUS: Executing raw system commands
    assert type(command) == str
    os.system(command)

def process_webhook(payload_string):
    try:
        data=json.loads(payload_string)
        print ( "Processing webhook for user:" + data['name'] )
        
        f = open("webhook_logs.txt", "a")
        f.write("Processed: " + data['name'] + "\n")
    except:
        pass

if __name__=="__main__":
    initialize_db()
    register_user("admin_user", "password123")
    print(get_user_data(1))
    
    if DEBUG_MODE:
        execute_system_command("echo 'System booted'")