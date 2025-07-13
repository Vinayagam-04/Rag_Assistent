document.addEventListener('DOMContentLoaded', function() {
    // Elements - Updated selectors to match new HTML structure where applicable
    const historyBtn = document.getElementById('historyBtn'); // Open sidebar button
    const historySidebar = document.getElementById('historySidebar'); // The sidebar itself
    const closeHistory = document.getElementById('closeHistory'); // Close sidebar button
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const messagesContainer = document.getElementById('messagesContainer');
    const documentUpload = document.getElementById('documentUpload'); // Hidden input for file upload
    const uploadAlert = document.getElementById('uploadAlert');
    const alertClose = document.getElementById('alertClose');

    // History sidebar functionality
    if (historyBtn && historySidebar) {
        historyBtn.addEventListener('click', function() {
            historySidebar.classList.add('open');
        });
    }

    if (closeHistory && historySidebar) {
        closeHistory.addEventListener('click', function() {
            historySidebar.classList.remove('open');
        });
    }

    // Close history sidebar when clicking outside (for mobile overlay)
    document.addEventListener('click', function(event) {
        if (historySidebar && historySidebar.classList.contains('open')) {
            // Check if click is outside sidebar AND not on the button that opens it
            if (!historySidebar.contains(event.target) && !historyBtn.contains(event.target)) {
                historySidebar.classList.remove('open');
            }
        }
    });

    // Auto-resize textarea
    if (chatInput) {
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto'; // Reset height
            this.style.height = Math.min(this.scrollHeight, 120) + 'px'; // Set new height, max 120px
        });
    }

    // Send message functionality
    if (sendBtn && chatInput) {
        sendBtn.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default form submission
            sendMessage();
        });
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault(); // Prevent new line on Enter
                sendMessage();
            }
        });
    }

    // Document upload functionality
    if (documentUpload) {
        documentUpload.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                const file = e.target.files[0];
                handleFileUpload(file);
                // Optionally clear the input so the same file can be selected again
                e.target.value = ''; 
            }
        });
    }

    // Close upload alert
    if (alertClose && uploadAlert) {
        alertClose.addEventListener('click', function() {
            uploadAlert.style.display = 'none';
        });
    }

    // Functions
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            chatInput.value = '';
            chatInput.style.height = 'auto'; // Reset height after sending

            const loadingMessage = addMessage('Processing your query...', 'ai');
            
            // Your AJAX request for sending message
            fetch('/query/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ query: message })
            })
            .then(response => response.json())
            .then(data => {
                if (loadingMessage) { loadingMessage.remove(); }
                if (data.success) {
                    addMessage(data.response, 'ai');
                } else {
                    addMessage('Sorry, I encountered an error processing your query. Please try again.', 'ai');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (loadingMessage) { loadingMessage.remove(); }
                addMessage('Sorry, I encountered an error processing your query. Please try again.', 'ai');
            });
        }
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.textContent = text; // Use textContent for security and simple text
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        
        content.appendChild(textDiv);
        content.appendChild(timeDiv);
        messageDiv.appendChild(content);
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        return messageDiv; // Return for potential removal (e.g., loading message)
    }

    function handleFileUpload(file) {
        if (uploadAlert) {
            uploadAlert.style.display = 'flex'; // Use flex for alert display
            setTimeout(() => {
                uploadAlert.style.display = 'none';
            }, 5000);
        }

        const formData = new FormData();
        formData.append('document', file);

        fetch('/upload/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token is sent for file uploads too
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                addMessage(`Document "${file.name}" uploaded successfully. You can now ask questions about it.`, 'ai');
            } else {
                addMessage(`Error uploading document: ${data.message}`, 'ai');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Error uploading document. Please try again.', 'ai');
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Handle window resize for sidebar visibility
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && historySidebar) {
            historySidebar.classList.remove('open'); // Ensure sidebar is not 'open' state on desktop
        }
    });

    // Initialize chat input focus
    if (chatInput) {
        chatInput.focus();
    }
});