const chatbox = document.getElementById('chatbox');
let lastGesture = '';

function addMessage(message) {
    const timestamp = new Date().toLocaleTimeString();
    const line = `[${timestamp}] ${message}`;
    const p = document.createElement('p');
    p.textContent = line;
    chatbox.appendChild(p);
    chatbox.scrollTop = chatbox.scrollHeight;  // auto-scroll
}

setInterval(() => {
    fetch('/gesture')
        .then(res => res.json())
        .then(data => {
            if (data.gesture !== lastGesture) {
                lastGesture = data.gesture;
                addMessage(data.gesture);
            }
        });
}, 1000);
