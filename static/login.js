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
    
    if(element.classList.contains('trl-b')){
        return
    } else {
        element.classList.replace('b-b', 'trl-b');
        otherElement.classList.replace('trl-b', 'b-b');
    }
}

function createSignupForm() {
    while(userForm.hasChildNodes()) {
        userForm.removeChild(userForm.firstChild);
    }

    //turn the form into a signin form
    const usernameInput = document.createElement('input');
    usernameInput.classList.add('f-w', 'fry-h', 'ft-p', 'n-o', 'bb', 'xt-fs');
    usernameInput.type = 'text';
    usernameInput.placeholder = 'Username';

    const emailInput = document.createElement('input');
    emailInput.classList.add('f-w', 'fry-h', 'ft-p', 'n-o', 'bb', 'xt-fs');
    emailInput.type = 'text';
    emailInput.placeholder = 'Email';

    const passwordInput = document.createElement('input');
    passwordInput.classList.add('f-w', 'fry-h', 'ft-p', 'n-o', 'bb', 'xt-fs');
    passwordInput.type = 'password';
    passwordInput.placeholder = 'Password';

     const confirmPasswordInput = document.createElement('input');
    confirmPasswordInput.classList.add('f-w', 'fry-h', 'ft-p', 'n-o', 'bb', 'xt-fs');
    confirmPasswordInput.type = 'password';
    confirmPasswordInput.placeholder = 'Confirm Password';

    const signupButton = document.createElement('button');
    signupButton.classList.add('f-w', 'th-xw', 'fry-h');
    signupButton.type = 'submit';
    signupButton.innerText = 'SIGN UP'

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
    emailInput.classList.add('f-w', 'fry-h', 'ft-p', 'n-o', 'bb', 'xt-fs');
    emailInput.type = 'text';
    emailInput.placeholder = 'Email';

    const passwordInput = document.createElement('input');
    passwordInput.classList.add('f-w', 'fry-h', 'ft-p', 'n-o', 'bb', 'xt-fs');
    passwordInput.type = 'password';
    passwordInput.placeholder = 'Password';

    const loginButton = document.createElement('button');
    loginButton.classList.add('f-w', 'th-xw', 'fry-h');
    loginButton.type = 'submit';
    loginButton.innerText = 'LOG IN'

    userForm.appendChild(emailInput);
    userForm.appendChild(passwordInput);
    userForm.appendChild(loginButton);
}

loginDiv.addEventListener('click', e => select(e.target));
signupDiv.addEventListener('click', e => select(e.target));