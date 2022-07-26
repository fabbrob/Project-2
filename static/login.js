const loginDiv = document.querySelector('#loginDiv');
const signupDiv = document.querySelector('#signupDiv');
const userForm = document.querySelector('#userForm')

function select(element) {
    if(element.isSameNode(signupDiv)){
        otherElement = loginDiv;
        createSignupForm();
    } else {
        otherElement = signupDiv;
        createLoginForm();
    }
    
    if(element.classList.contains('selected')){
        return
    } else {
        element.classList.replace('not-selected', 'selected');
        otherElement.classList.replace('selected', 'not-selected');
    }
}

function createSignupForm() {
    while(userForm.hasChildNodes()) {
        userForm.removeChild(userForm.firstChild);
    }

    //turn the form into a signin form
    const usernameInput = document.createElement('input');
    usernameInput.classList.add('login-input');
    usernameInput.type = 'text';
    usernameInput.name = 'username'
    usernameInput.placeholder = 'Username';

    const emailInput = document.createElement('input');
    emailInput.classList.add('login-input');
    emailInput.type = 'text';
    emailInput.name = 'email';
    emailInput.placeholder = 'Email';

    const passwordInput = document.createElement('input');
    passwordInput.classList.add('login-input');
    passwordInput.type = 'password';
    passwordInput.name = 'password';
    passwordInput.placeholder = 'Password';

     const confirmPasswordInput = document.createElement('input');
    confirmPasswordInput.classList.add('login-input');
    confirmPasswordInput.type = 'password';
    confirmPasswordInput.name = 'confirm_password'
    confirmPasswordInput.placeholder = 'Confirm Password';

    const signupButton = document.createElement('button');
    signupButton.classList.add('login-button');
    signupButton.type = 'submit';
    signupButton.innerText = 'SIGN UP'

    userForm.action = '/signup'
    userForm.appendChild(usernameInput);
    userForm.appendChild(emailInput);
    userForm.appendChild(passwordInput);
    userForm.appendChild(confirmPasswordInput);
    userForm.appendChild(signupButton);
}

function createLoginForm() {
    while(userForm.hasChildNodes()) {
        userForm.removeChild(userForm.firstChild);
    }

    const emailInput = document.createElement('input');
    emailInput.classList.add('login-input');
    emailInput.type = 'text';
    emailInput.name = 'email'
    emailInput.placeholder = 'Email';

    const passwordInput = document.createElement('input');
    passwordInput.classList.add('login-input');
    passwordInput.type = 'password';
    passwordInput.name = 'password'
    passwordInput.placeholder = 'Password';

    const loginButton = document.createElement('button');
    loginButton.classList.add('login-button');
    loginButton.type = 'submit';
    loginButton.innerText = 'LOG IN'

    userForm.action = '/login'
    userForm.appendChild(emailInput);
    userForm.appendChild(passwordInput);
    userForm.appendChild(loginButton);
}

loginDiv.addEventListener('click', e => select(e.target));
signupDiv.addEventListener('click', e => select(e.target));