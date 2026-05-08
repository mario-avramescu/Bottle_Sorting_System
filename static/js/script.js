function startSystem() {
    const connectionStatus = document.getElementById('connection_status');
    const startWarning = document.getElementById('start-warning');

    if (connectionStatus.classList.contains('connected')) {
        startWarning.classList.add('hidden');
        // Here you can add code to send a request to the server to start the system
    } else {
        startWarning.classList.remove('hidden');
    }
}

function connectToRaspberry() {
    const ipInput = document.getElementById('raspberry-ip');
    const portInput = document.getElementById('raspberry-port');
    const usernameInput = document.getElementById('raspberry-username');
    const passwordInput = document.getElementById('raspberry-password');
    const connectionStatus = document.getElementById('connection_status');

    const ip = ipInput.value.trim();
    const port = portInput.value.trim();
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (ip && port && username && password) {
        connectionStatus.classList.remove('not_connected');
        connectionStatus.classList.add('connected');

        // Here you can add code to send a request to the server to connect to the Raspberry Pi
    } else {
        alert('Please fill in all fields to connect to the Raspberry Pi.');
    }
}