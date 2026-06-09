const greetingText = document.getElementById('greetingText');
const nameInput = document.getElementById('nameInput');
const submitBtn = document.getElementById('submitBtn');

const defaultGreeting = "Hello, type your name";

function updateGreeting(name) {
    if (name && name.trim().length > 0) {
        // textContent prevents XSS injection
        greetingText.textContent = `Hello ${name}`;
    } else {
        greetingText.textContent = defaultGreeting;
    }
}

// Fetch the current name from the server
async function fetchName() {
    try {
        const response = await fetch('/api/name');
        if (response.ok) {
            const data = await response.json();
            updateGreeting(data.name);
        }
    } catch (e) {
        console.error('Failed to fetch name');
    }
}

// Poll every 2 seconds for real-time updates
setInterval(fetchName, 2000);
// Initial fetch
fetchName();

// Handle send action
async function sendName() {
    const newName = nameInput.value;
    if (newName.trim() !== '') {
        try {
            await fetch('/api/name', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: newName })
            });
            nameInput.value = ''; // clear input
            fetchName(); // update immediately
        } catch (e) {
            console.error('Failed to update name');
        }
    }
}

submitBtn.addEventListener('click', sendName);

nameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendName();
    }
});
