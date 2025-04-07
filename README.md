#  To-Do App

A simple web-based To-Do list application built with Python, Flask, and SQLite for persistent storage.

## Features

*   Add new tasks with text, priority, and optional due date.
*   View all tasks.
*   Filter tasks by "All", "Active", and "Completed".
*   Mark tasks as complete or incomplete.
*   Delete tasks.
*   Task data persists in an SQLite database.

## Technology Stack

*   **Backend:** Python, Flask
*   **Database:** SQLite
*   **Frontend:** HTML, CSS, JavaScript
*   **CLI Commands:** Flask-Click

## Setup and Installation

Follow these steps to set up and run the project locally:

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd flask_todo_sqlite
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate it
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the Database:**
    This command creates the `database.db` file and the necessary `tasks` table.
    ```bash
    flask init-db
    ```
    *(You only need to run this once initially.)*

## Running the Application

1.  Make sure your virtual environment is activated.
2.  Start the Flask development server:
    ```bash
    python app.py
    ```
    *(Alternatively, you might use `flask run`)*

3.  Open your web browser and navigate to: `http://127.0.0.1:5000` (or the address provided in the terminal).

## Project Structure

```
flask_todo_sqlite/
├── venv/                   # Virtual environment (ignored by Git)
├── static/                 # Static files (CSS, JS)
│   ├── style.css
│   └── script.js
├── templates/              # HTML templates
│   └── index.html
├── app.py                  # Main Flask application logic and routes
├── database.db             # SQLite database file (ignored by Git after creation)
├── requirements.txt        # Python package dependencies
├── .gitignore              # Files and directories ignored by Git
└── README.md               # This file
```
