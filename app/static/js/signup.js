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

// --- AJAX form submission ---
document.getElementById('registerForm').addEventListener('submit', function(e){
    e.preventDefault();  // prevent page reload
    const formData = new FormData(this);
    formData.append("register","1");
    
    fetch(SIGNUP_URL, {
        method: "POST",
        headers: {'X-CSRFToken': CSRF_TOKEN},
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            showToast('Success', data.message);
            this.reset();
            container.classList.remove('active')
        } else {
            showToast('Error', data.message);
        }
    })
    .catch(err => console.log(err));
});

document.getElementById('loginForm').addEventListener('submit', function(e){
    e.preventDefault();
    const formData = new FormData(this);
    formData.append("login","1");

    fetch(SIGNUP_URL, {
        method: "POST",
        headers: {'X-CSRFToken': CSRF_TOKEN},
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            showToast('Success', data.message);
            window.location.href = EXPENSE_URL;  // redirect after login
        } else {
            showToast('Error', data.message);
        }
    })
    .catch(err => console.log(err));
});
