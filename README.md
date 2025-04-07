# Flask To-Do App

![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Flask](https://img.shields.io/badge/Flask-2.x-green.svg) ![Frontend](https://img.shields.io/badge/Frontend-HTML/CSS/JS-orange.svg)

A simple, clean web-based To-Do List application built using the Python Flask framework for the backend and vanilla JavaScript for the frontend interactions.

## Description

This application provides a user-friendly interface to manage daily tasks. Users can add new tasks, set priorities (High, Medium, Low), assign optional due dates, mark tasks as completed, and delete tasks they no longer need. The tasks are filtered into All, Active, and Completed views.

**Note:** Currently, the task data is stored in server memory, meaning all tasks will be lost when the Flask server is stopped or restarted.

## Features

*   **Add Tasks:** Quickly add new tasks via the input form.
*   **Set Priority:** Assign High, Medium (default), or Low priority to tasks.
*   **Set Due Date:** Optionally add a due date using a date picker.
*   **Mark Complete:** Toggle task completion status using checkboxes.
*   **Delete Tasks:** Remove tasks individually using the trash icon.
*   **Filter Views:** View tasks based on their status (All, Active, Completed).
*   **Task Count:** Displays the total number of tasks.
*   **Clean UI:** Interface designed for clarity and ease of use.

## Technologies Used

*   **Backend:** Python 3, Flask
*   **Frontend:** HTML5, CSS3, JavaScript (ES6+)
*   **Data Storage:** Python List (In-Memory - Non-persistent)
*   **Icons:** Font Awesome (via CDN)

## Setup and Installation

Follow these steps to run the application locally:

1.  **Prerequisites:**
    *   Python 3 installed on your system.
    *   `pip` (Python package installer).

2.  **Get the Code:**
    *   Download the project files as a ZIP from GitHub and extract them. Navigate into the extracted folder using your terminal.

3.  **Create and Activate Virtual Environment:** (Recommended)
    *   Create a virtual environment to isolate project dependencies:
        ```bash
        python -m venv venv
        ```
    *   Activate the environment:
        *   **Windows:** `venv\Scripts\activate`
        *   **macOS/Linux:** `source venv/bin/activate`
    *   *(Your terminal prompt should now be prefixed with `(venv)`)*

4.  **Install Dependencies:**
    *   Install the required Python packages listed in `requirements.txt`:
        ```bash
        pip install -r requirements.txt
        ```

5.  **Run the Application:**
    *   Execute the main application file:
        ```bash
        python app.py
        ```

6.  **Access the App:**
    *   Open your web browser and navigate to:
        `http://127.0.0.1:5000` (or the address shown in the terminal output).


*   **Improved Error Handling:** Add more robust validation and user-friendly error messages.
*   **Deployment:** Add instructions or scripts for deploying to platforms like Heroku, PythonAnywhere, or Docker.

## Contributing

Contributions are welcome! If you have suggestions or find bugs, please open an issue on the GitHub repository. If you'd like to contribute code, please fork the repository and submit a pull request.
