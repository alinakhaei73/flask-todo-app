document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const taskForm = document.getElementById('add-task-form');
    const taskInput = document.getElementById('task-input');
    const prioritySelect = document.getElementById('priority-select');
    const dateInput = document.getElementById('date-input');
    const taskList = document.getElementById('task-list');
    const taskCountElement = document.getElementById('task-count');
    const filterBtns = document.querySelectorAll('.filter-btn');
    // const currentDateElement = document.getElementById('current-date'); // Date now set by Flask

    // --- State ---
    let tasks = []; // Will be fetched from server
    let currentFilter = 'all'; // 'all', 'active', 'completed'

    // --- Functions ---

    // Format date for display (e.g., "Apr 16") - Adjusted for potential null dates
    function formatDate(dateString) {
        if (!dateString || dateString === 'None') return null; // Handle Python's None or empty string
        try {
            // Ensure we handle YYYY-MM-DD format correctly, assuming UTC if no timezone
            const date = new Date(dateString + 'T00:00:00Z');
             if (isNaN(date.getTime())) { // Check if the date is valid
                 console.error("Invalid date string received:", dateString);
                 return null;
             }
            const options = { month: 'short', day: 'numeric', timeZone: 'UTC' }; // Specify UTC to avoid timezone shifts
            return date.toLocaleDateString('en-US', options);
        } catch (e) {
            console.error("Error formatting date:", dateString, e);
            return null; // Return null or some default if formatting fails
        }
    }

    // Fetch tasks from the server
    async function fetchTasks() {
        try {
            const response = await fetch('/tasks'); // Fetch from Flask endpoint
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            tasks = await response.json();
            console.log("Fetched tasks:", tasks); // Debugging
            renderTasks(); // Render after fetching
        } catch (error) {
            console.error("Could not fetch tasks:", error);
            taskList.innerHTML = '<li class="error-message">Could not load tasks. Please try again later.</li>';
        }
    }

    // Render tasks based on the current filter
    function renderTasks() {
        taskList.innerHTML = ''; // Clear current list

        let tasksToRender = tasks;

        if (currentFilter === 'active') {
            tasksToRender = tasks.filter(task => !task.completed);
        } else if (currentFilter === 'completed') {
            tasksToRender = tasks.filter(task => task.completed);
        }

        console.log(`Rendering filter: ${currentFilter}`, tasksToRender); // Debugging

        if (tasksToRender.length === 0 && tasks.length === 0) {
             taskList.innerHTML = '<li class="no-tasks">No tasks yet. Add one above!</li>';
        } else if (tasksToRender.length === 0) {
             taskList.innerHTML = `<li class="no-tasks">No ${currentFilter} tasks found.</li>`;
        } else {
            tasksToRender.forEach(task => {
                const li = document.createElement('li');
                li.className = `task-item ${task.completed ? 'completed' : ''}`;
                li.dataset.id = task.id; // Use the ID from the server

                const formattedDueDate = formatDate(task.dueDate);
                const priorityClass = task.priority ? `priority-${task.priority.toLowerCase()}` : 'priority-medium'; // Default class

                li.innerHTML = `
                    <div class="task-main">
                        <input type="checkbox" class="task-checkbox" data-id="${task.id}" ${task.completed ? 'checked' : ''}>
                        <span class="task-name">${task.text || 'No Text'}</span>
                    </div>
                    <div class="task-details">
                        ${formattedDueDate ? `<span class="task-due-date">${formattedDueDate}</span>` : ''}
                        <span class="task-priority ${priorityClass}">${task.priority || 'Medium'}</span>
                        <button class="delete-btn" data-id="${task.id}"><i class="fas fa-trash-alt"></i></button>
                    </div>
                `;
                // Add event listeners using event delegation on the list later
                taskList.appendChild(li);
            });
        }
        updateTaskCount();
    }

    // Update the task count display
    function updateTaskCount() {
        const totalTasks = tasks.length; // Use the master task list length
        taskCountElement.textContent = `${totalTasks} ${totalTasks === 1 ? 'task' : 'tasks'}`;
    }

    // Add a new task (Send to Server)
    async function addTask(event) {
        event.preventDefault();
        const text = taskInput.value.trim();
        const priority = prioritySelect.value;
        const dueDate = dateInput.value || null; // Send null if empty

        if (text === '') return;

        const newTaskData = {
            text: text,
            priority: priority,
            dueDate: dueDate
        };

        try {
            const response = await fetch('/add', { // Send POST to Flask endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newTaskData),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const addedTask = await response.json(); // Get the task back with its new ID
            tasks.push(addedTask); // Add to local array
            renderTasks(); // Re-render

            // Reset form
            taskInput.value = '';
            prioritySelect.value = 'Medium';
            dateInput.value = '';

        } catch (error) {
            console.error("Could not add task:", error);
            // Optionally display an error message to the user
        }
    }

    // Toggle task completion status (Send to Server)
    async function toggleTaskComplete(taskId) {
        const task = tasks.find(t => t.id === taskId);
        if (!task) return;

        try {
            const response = await fetch(`/toggle/${taskId}`, { // Send POST to Flask endpoint
                method: 'POST',
                 headers: { // Optional headers if needed
                     'Content-Type': 'application/json',
                 },
                 // body: JSON.stringify({ completed: !task.completed }) // Can optionally send new state
            });

            if (!response.ok) {
                 throw new Error(`HTTP error! status: ${response.status}`);
            }

            const updatedTask = await response.json();

             // Update the local task array
             tasks = tasks.map(t => t.id === taskId ? updatedTask : t);
             renderTasks(); // Re-render the list based on current filter

        } catch (error) {
             console.error(`Could not toggle task ${taskId}:`, error);
             // Optionally revert UI change or show error
        }
    }

    // Delete a task (Send to Server)
    async function deleteTask(taskId) {
        if (!confirm('Are you sure you want to delete this task?')) { // Confirmation
            return;
        }

        try {
            const response = await fetch(`/delete/${taskId}`, { // Send POST or DELETE to Flask endpoint
                method: 'POST', // Or 'DELETE', adjust Flask route accordingly
            });

            if (!response.ok) {
                 throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

             if (result.success) {
                 // Remove from local array
                 tasks = tasks.filter(task => task.id !== taskId);
                 renderTasks(); // Re-render
             } else {
                 console.error("Server could not delete task:", result.message);
                 // Display error message
             }

        } catch (error) {
             console.error(`Could not delete task ${taskId}:`, error);
             // Display error message
        }
    }

    // Handle filter button clicks
    function handleFilterClick(event) {
        const clickedButton = event.target;
        filterBtns.forEach(btn => btn.classList.remove('active'));
        clickedButton.classList.add('active');
        currentFilter = clickedButton.dataset.filter;
        renderTasks(); // Re-render tasks based on the new filter
    }

    // --- Event Listeners ---
    taskForm.addEventListener('submit', addTask);

    filterBtns.forEach(btn => btn.addEventListener('click', handleFilterClick));

    // Event delegation for task list items (checkboxes and delete buttons)
    taskList.addEventListener('click', (event) => {
        // Check if a checkbox was clicked
        if (event.target.classList.contains('task-checkbox')) {
            const taskId = parseInt(event.target.dataset.id);
            toggleTaskComplete(taskId);
        }
        // Check if a delete button (or its icon) was clicked
        if (event.target.closest('.delete-btn')) {
             const button = event.target.closest('.delete-btn');
             const taskId = parseInt(button.dataset.id);
             deleteTask(taskId);
        }
    });

    // --- Initial Setup ---
    fetchTasks(); // Fetch tasks from server on page load
});