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
    document.getElementById('toastTitle').innerText = title;
    document.getElementById('toastBody').innerText = message;
    $('#messageToast').toast('show');
    setTimeout(() => {
        console.log('toast worked')
    }, 5000);
    
}

// Example usage:
// showToast('Success', 'Category added successfully!');