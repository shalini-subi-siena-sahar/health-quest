import sqlite3
import schedule
import time
from datetime import datetime

# Connect to SQLite database (or create it)
conn = sqlite3.connect('habit_tracker.db')
c = conn.cursor()

# Create table to store habit data
c.execute('''
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    streak INTEGER DEFAULT 0,
    last_completed DATE
)
''')
conn.commit()

# Function to add a new habit
def add_habit(name):
    c.execute('''
    INSERT INTO habits (name, streak, last_completed)
    VALUES (?, ?, ?)
    ''', (name, 0, None))
    conn.commit()
    print(f'Habit "{name}" added successfully!')

# Function to mark a habit as completed
def complete_habit(habit_id):
    today = datetime.today().date()
    c.execute('''
    SELECT streak, last_completed FROM habits WHERE id = ?
    ''', (habit_id,))
    habit = c.fetchone()
    if habit:
        streak, last_completed = habit
        if last_completed != today:
            streak += 1
            c.execute('''
            UPDATE habits SET streak = ?, last_completed = ? WHERE id = ?
            ''', (streak, today, habit_id))
            conn.commit()
            print(f'Habit {habit_id} completed! Current streak: {streak} days.')
        else:
            print(f'Habit {habit_id} already completed today.')
    else:
        print(f'Habit {habit_id} not found.')

# Function to view all habits
def view_habits():
    c.execute('SELECT * FROM habits')
    habits = c.fetchall()
    if habits:
        for habit in habits:
            print(f'ID: {habit[0]}, Name: {habit[1]}, Streak: {habit[2]} days, Last Completed: {habit[3]}')
    else:
        print('No habits found.')

# Function to send push notifications (simulated)
def send_push_notifications():
    print('Sending push notifications to users...')

# Schedule push notifications daily at 8:00 AM
schedule.every().day.at("08:00").do(send_push_notifications)

# Example usage
if __name__ == '__main__':
    while True:
        # Display menu
        print('\nHabit Tracker')
        print('1. Add Habit')
        print('2. Complete Habit')
        print('3. View Habits')
        print('4. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            habit_name = input('Enter habit name: ')
            add_habit(habit_name)
        elif choice == '2':
            habit_id = int(input('Enter habit ID to mark as completed: '))
            complete_habit(habit_id)
        elif choice == '3':
            view_habits()
        elif choice == '4':
            break
        else:
            print('Invalid choice. Please try again.')
        # Run scheduled tasks
        schedule.run_pending()
        time.sleep(1)
    # Close the database connection
    conn.close()
