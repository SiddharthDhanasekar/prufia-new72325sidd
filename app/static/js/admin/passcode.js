const socket = io({
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 1000,
    debug: true,
    query: {
        'user-type': 'admin' 
    }
});
const socketStatus = document.getElementById('socket-status');

socket.on('connect', () => {
    socketStatus.textContent = 'Connected ✓';
    socketStatus.className = 'badge bg-success';
    socket.emit('join-admin-room');
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    socketStatus.textContent = 'Disconnected ✗';
    socketStatus.className = 'badge bg-danger';
});

socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
    socketStatus.textContent = 'Connection Error';
    socketStatus.className = 'badge bg-warning text-dark';
});


document.getElementById('resetAllBtn')?.addEventListener('click', async function() {
    const btn = this;
    if (!confirm('Are you sure you want to reset ALL passcodes?')) {
        return;
    }
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Resetting...';
    btn.disabled = true;
    try {
        const response = await fetch('/reset', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
            }
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || 'Failed to reset passcodes');
        }
        showNotification(`Successfully reset ${data.affected_rows || 0} passcodes`);
        setTimeout(() => {
            window.location.reload();
        }, 1500);
        
    } catch (error) {
        console.error('Reset error:', error);
        showNotification(error.message || 'Error resetting passcodes', 'danger');
    } finally {
        btn.innerHTML = '<i class="bi bi-arrow-repeat"></i> Reset All Passcodes';
        btn.disabled = false;
    }
});
function showNotificationreset(message, type = 'success') {
    const toastEl = document.getElementById('notificationToast');
    const toastBody = document.getElementById('toastMessage');
    if (toastEl && toastBody) {
        const toastHeader = toastEl.querySelector('.toast-header');
        toastHeader.className = `toast-header bg-${type} text-white`;
        toastBody.textContent = message;
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    }
}

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.content || '';
}

document.getElementById('copyPasscodeBtn')?.addEventListener('click', function() {
    const passcode = document.getElementById('generatedPasscode').textContent;
    navigator.clipboard.writeText(passcode).then(() => {
        this.innerHTML = '<i class="bi bi-check-circle"></i> Copied!';
        setTimeout(() => {
            this.innerHTML = '<i class="bi bi-clipboard"></i> Copy';
        }, 2000);
    });
});

function showNotification(message) {
    const toastEl = document.getElementById('notificationToast');
    const toastBody = document.getElementById('toastMessage');
    
    if (toastEl && toastBody) {
        toastBody.textContent = message;
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    }
}
    