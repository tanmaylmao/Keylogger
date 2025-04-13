// Update the status of the keylogger
function updateStatus() {
    eel.get_status()(status => {
        document.getElementById("status").innerText = status;
    });
}

// Toggle the keylogger (start/stop)
function toggleKeylogger(action) {
    eel.toggle_keylogger(action)((response) => {
        alert(response);
        updateStatus();
        if (action === "stop") {
            fetchKeystrokes();
        }
    });
}

// Fetch logged keystrokes and display them
function fetchKeystrokes() {
    eel.get_keystrokes()(keystrokes => {
        const logContainer = document.getElementById("log");
        logContainer.innerHTML = ""; // Clear the current log display

        keystrokes.forEach((entry, index) => {
            const logItem = document.createElement("p");
            logItem.innerText = `${index + 1}: ${entry}`;
            logContainer.appendChild(logItem);
        });
    });
}

// Automatically update the status on page load
window.onload = function () {
    updateStatus();
};
