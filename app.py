# app.py

import sqlite3
import datetime
from flask import Flask, render_template, request, jsonify, g, current_app
import click # Required for the CLI command function signature and echo

# --- Configuration ---
DATABASE = 'database.db' # Name for the SQLite database file

# --- Flask App Initialization ---
app = Flask(__name__)
app.config['DATABASE'] = DATABASE # Store db name in Flask app config

# --- Database Helper Functions ---

def get_db():
    """
    Connects to the specific database configured for the app.
    Uses Flask's 'g' object to store the connection per request.
    Creates connection if it doesn't exist for the current context.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES # Automatically parse declared types
        )
        # Return rows that behave like dictionaries
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Closes the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Register the close_db function to be called when the app context tears down
app.teardown_appcontext(close_db)

# --- Database Initialization CLI Command ---

@app.cli.command('init-db')
def init_db_command():
    """
    Flask CLI command: Clears existing data and creates new tables.
    Run this command from the terminal using 'flask init-db'.
    """
    try:
        # Establish connection manually for CLI command context
        conn = sqlite3.connect(current_app.config['DATABASE'])
        cursor = conn.cursor()

        # Optional: Drop table if you want a completely fresh start (Use with caution!)
        # cursor.execute('DROP TABLE IF EXISTS tasks')
        # print("Dropped existing tasks table (if any).")

        # Create the tasks table if it doesn't already exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'Medium',
                dueDate TEXT, -- Store dates as 'YYYY-MM-DD' strings or NULL
                completed INTEGER NOT NULL DEFAULT 0 -- Use 0 for false, 1 for true
            )
        ''')
        conn.commit()
        click.echo('Initialized the database and created the tasks table.')

    except sqlite3.Error as e:
        click.echo(f'An error occurred during database initialization: {e}')
    finally:
        if conn:
            conn.close()

# --- Date Helper & Context Processor ---

def get_current_date_formatted():
    """Returns the current date formatted for display."""
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y") # e.g., Tuesday, May 14, 2024

@app.context_processor
def inject_current_date():
    """Makes the current date available to all Jinja templates."""
    return dict(current_date=get_current_date_formatted())

# --- Flask Routes (API Endpoints) ---

@app.route('/')
def index():
    """Renders the main HTML page (frontend)."""
    # The date is injected via the context processor.
    # Tasks will be fetched asynchronously by JavaScript.
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks_api():
    """API: Fetches all tasks from the database."""
    try:
        db = get_db()
        cursor = db.execute('SELECT id, text, priority, dueDate, completed FROM tasks ORDER BY id DESC')
        tasks_list = cursor.fetchall()
        # Convert sqlite3.Row objects to standard dictionaries for JSON
        tasks_dict_list = [dict(row) for row in tasks_list]
        return jsonify(tasks_dict_list)
    except sqlite3.Error as e:
        print(f"Database error on GET /tasks: {e}")
        return jsonify({"error": "Failed to retrieve tasks from database"}), 500

@app.route('/add', methods=['POST'])
def add_task_api():
    """API: Adds a new task to the database."""
    if not request.is_json:
        return jsonify({"error": "Invalid request format: JSON required"}), 400

    data = request.get_json()
    text = data.get('text')
    priority = data.get('priority', 'Medium') # Default priority if not provided
    due_date = data.get('dueDate') # JS sends 'YYYY-MM-DD' or null/empty string

    if not text:
        return jsonify({"error": "Task text cannot be empty"}), 400

    db = get_db()
    try:
        cursor = db.execute(
            # Use placeholders (?) for security against SQL injection
            'INSERT INTO tasks (text, priority, dueDate, completed) VALUES (?, ?, ?, ?)',
            (text, priority, due_date if due_date else None, 0) # Store 0 for 'False' (not completed)
        )
        db.commit() # Save changes to the database
        new_task_id = cursor.lastrowid # Get the ID of the newly inserted task

        # Fetch the complete task data we just inserted to return to the client
        cursor = db.execute('SELECT * FROM tasks WHERE id = ?', (new_task_id,))
        new_task = cursor.fetchone()

        if new_task:
            return jsonify(dict(new_task)), 201 # Return the new task with 201 Created status
        else:
            # This case should be rare if insert succeeded
            return jsonify({"error": "Task added but could not be retrieved"}), 500

    except sqlite3.Error as e:
        db.rollback() # Roll back any changes if an error occurred
        print(f"Database error on POST /add: {e}")
        return jsonify({"error": "Database error occurred while adding task"}), 500


@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task_api(task_id):
    """API: Toggles the completion status (0/1) of a specific task."""
    db = get_db()
    try:
        # First, check if the task exists and get its current status
        cursor = db.execute('SELECT completed FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()

        if task is None:
            return jsonify({"error": f"Task with id {task_id} not found"}), 404

        # Calculate the new status (flip 0 to 1, or 1 to 0)
        new_status = 1 - task['completed']

        # Update the task's completed status in the database
        db.execute('UPDATE tasks SET completed = ? WHERE id = ?', (new_status, task_id))
        db.commit()

        # Fetch the full updated task data to return
        cursor = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        updated_task = cursor.fetchone()

        if updated_task:
            return jsonify(dict(updated_task))
        else:
             # Should not happen if update was successful
             return jsonify({"error": "Task status updated but could not retrieve updated task"}), 500

    except sqlite3.Error as e:
        db.rollback()
        print(f"Database error on POST /toggle/{task_id}: {e}")
        return jsonify({"error": "Database error occurred while toggling task status"}), 500


@app.route('/delete/<int:task_id>', methods=['POST']) # Using POST for simplicity from JS fetch
def delete_task_api(task_id):
    """API: Deletes a specific task from the database."""
    db = get_db()
    try:
        cursor = db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        db.commit()

        # cursor.rowcount tells how many rows were affected by the DELETE
        if cursor.rowcount == 0:
            # No task with that ID was found to delete
            return jsonify({"success": False, "error": f"Task with id {task_id} not found"}), 404
        else:
            # Task was successfully deleted
            return jsonify({"success": True, "message": f"Task {task_id} deleted successfully"})

    except sqlite3.Error as e:
        db.rollback()
        print(f"Database error on POST /delete/{task_id}: {e}")
        return jsonify({"error": "Database error occurred while deleting task"}), 500


# --- Main Execution Block ---
if __name__ == '__main__':
    # Runs the Flask development server
    # debug=True provides auto-reloading and more detailed error pages
    # Do not use debug=True in a production environment!
    app.run(debug=True)
