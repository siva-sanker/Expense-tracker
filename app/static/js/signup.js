const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

registerBtn.addEventListener('click', () => {
    container.classList.add('active');
})

loginBtn.addEventListener('click', () => {
    container.classList.remove('active');
})

// Function to show toast
function showToast(title, message) {
    const iconMap = {
        success: 'fa-circle-check text-success',
        error: 'fa-circle-xmark text-danger',
        warning: 'fa-triangle-exclamation text-warning',
        info: 'fa-circle-info text-primary',
        delete: 'fa-trash text-danger',
        update: 'fa-pen text-info'
    };
    const iconClass = iconMap[title.toLowerCase()] || 'fa-bell text-secondary';
    document.getElementById('toastIcon').className = `fa-solid ${iconClass}`;   
    document.getElementById('toastTitle').innerText = title;
    document.getElementById('toastBody').innerText = message;
    $('#messageToast').toast('show');    
}

// Example usage:
// showToast('Success', 'Category added successfully!');