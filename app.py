from flask import Flask, render_template, request, jsonify, redirect, url_for
import datetime

app = Flask(__name__)

# --- Data Storage (In-Memory - Not Persistent!) ---
tasks = [
    {"id": 1, "text": "Learn Flask", "priority": "High", "dueDate": "2025-04-10", "completed": False},
    {"id": 2, "text": "Build To-Do App", "priority": "Medium", "dueDate": "2025-04-15", "completed": False},
    {"id": 3, "text": "Deploy App", "priority": "Low", "dueDate": None, "completed": True},
]
next_id = 4 # Start ID after examples

# --- Routes ---

@app.route('/')
def index():
    """Renders the main page."""
    # No need to pass tasks here if JS fetches them
    return render_template('index.html') # Simpler now

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """API endpoint to get all tasks."""
    print(f"Returning tasks: {tasks}") # Server-side log
    return jsonify(tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Adds a new task."""
    global next_id # Declare intent to modify the global variable
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    print(f"Received data for add: {data}") # Server-side log

    text = data.get('text')
    priority = data.get('priority', 'Medium') # Default priority
    due_date = data.get('dueDate') # Can be None or empty string

    if not text:
        return jsonify({"error": "Task text is required"}), 400

    new_task = {
        "id": next_id,
        "text": text,
        "priority": priority,
        "dueDate": due_date if due_date else None, # Store null/None consistently
        "completed": False
    }
    tasks.append(new_task)
    next_id += 1
    print(f"Task added: {new_task}") # Server-side log
    print(f"Tasks list now: {tasks}") # Server-side log
    return jsonify(new_task), 201 # Return the added task with 201 Created status

@app.route('/toggle/<int:task_id>', methods=['POST']) # Use POST for simplicity from JS fetch
def toggle_task(task_id):
    """Toggles the completion status of a task."""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['completed'] = not task['completed']
        print(f"Toggled task {task_id}: {task}") # Server-side log
        return jsonify(task) # Return the updated task
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/delete/<int:task_id>', methods=['POST']) # Use POST for simplicity, could be DELETE
def delete_task(task_id):
    """Deletes a task."""
    global tasks # To reassign the filtered list back to the global variable
    initial_length = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    if len(tasks) < initial_length:
        print(f"Deleted task {task_id}") # Server-side log
        return jsonify({"success": True, "message": "Task deleted"})
    else:
        return jsonify({"success": False, "error": "Task not found"}), 404


# --- Helper Functions ---
def get_current_date_formatted():
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y")

@app.context_processor
def inject_current_date():
    return dict(current_date=get_current_date_formatted())

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)