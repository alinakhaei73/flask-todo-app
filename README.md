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


1.  **Create and Activate Virtual Environment:**
    ```bash
    # Create the virtual environment
    cd todo-App-main
    python -m venv venv

    # Activate it
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the Database:**
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

## Building the Flask To-Do App: File Creation Steps
This guide outlines the files to create at each stage when building the Flask To-Do application.

### Phase 1: Project Setup & Environment
1.  **Create Project Directory:** Make the main folder (e.g., `todo_App`).
2.  **Set Up Virtual Environment:** Inside the project directory, create and activate a Python virtual environment (`python -m venv venv`, `venv\Scripts\activate`).
3.  **Install Dependencies:** Use `pip install Flask Click`. (This prepares the environment).
4.  **Create Folder Structure:** Inside the main project directory, create:
    *   `static/`
    *   `templates/`

### Phase 2: Backend Foundation
5.  **Create Flask App File:** In the main project directory, create `app.py`.

### Phase 3: Frontend Structure & Styling
6.  **Create HTML Template:** Inside `templates/`, create `templates/index.html`.
7.  **Create CSS File:** Inside `static/`, create `static/style.css`.

### Phase 4: Frontend Interactivity
8.  **Create JavaScript File:** Inside `static/`, create `static/script.js`.

### Phase 5: Backend Logic (Populating `app.py`)
9.  **Modify Flask App File:** Edit `app.py` to add the Python backend logic (database handling, routes, API endpoints, etc.).

### Phase 6: Project Management Files
10. **Create Git Ignore File:** In the main project directory, create `.gitignore`.
11. **Generate Requirements File:** Run `pip freeze > requirements.txt` to create `requirements.txt`.
12. **Create Readme File:** In the main project directory, create `README.md`.

### Phase 7: Database Initialization
13. **Initialize Database:** Run `flask init-db` . This creates `database.db`.

### Phase 8: Running the Application
14. **Run Flask Server:** Execute `python app.py` in the terminal.


