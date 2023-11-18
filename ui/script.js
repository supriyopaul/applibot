// Define the base URL for your backend API
const apiBaseUrl = 'http://localhost:9999';

document.addEventListener('DOMContentLoaded', () => {
    handleNavigationRestrictions();
    handleSignupForm();
    handleLogoutButton();
    handleLoginForm();
    initializeTabFunctionality();
});

function handleNavigationRestrictions() {
    if (!localStorage.getItem('applibotAccessToken')) {
        const navLinks = document.querySelectorAll('.nav-links a');
        const logoutButton = document.querySelector('.nav-button');

        navLinks.forEach(link => {
            link.addEventListener('click', event => {
                event.preventDefault();
                window.location.href = 'login.html';
            });
        });

        logoutButton.addEventListener('click', event => {
            event.preventDefault();
            window.location.href = 'login.html';
        });
    }
}

function handleSignupForm() {
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function (event) {
            event.preventDefault();
            processSignupForm();
        });
    } else {
        console.error('Signup form not found.');
    }
}

function processSignupForm() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm-password').value;

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    var signupData = {
        email: email,
        password: password
    };

    fetch(`${apiBaseUrl}/signup`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        },
        body: JSON.stringify(signupData)
    })
    .then(handleApiResponse)
    .then(() => {
        alert("Sign up successful!");
        window.location.href = 'login.html';
    })
    .catch(handleApiError);
}

function handleLogoutButton() {
    const logoutButton = document.querySelector('.nav-button');
    logoutButton.addEventListener('click', event => {
        event.preventDefault();
        localStorage.removeItem('applibotAccessToken');
        window.location.href = 'index.html';
    });
}

function handleLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            processLoginForm();
        });
    } else {
        console.error('Login form not found.');
    }
}

function processLoginForm() {
    var email = document.getElementById('login-email').value;
    var password = document.getElementById('login-password').value;

    var formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    fetch(`${apiBaseUrl}/token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
        },
        body: formData
    })
    .then(handleApiResponse)
    .then(data => {
        localStorage.setItem('applibotAccessToken', data.access_token);
        window.location.href = 'generate.html';
    })
    .catch(handleApiError);
}

function handleApiResponse(response) {
    if (!response.ok) {
        return response.json().then(errorData => {
            throw new Error(errorData.detail || 'An error occurred');
        });
    }
    return response.json();
}

function handleApiError(error) {
    alert(error.message || "An error occurred.");
}

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function copyToClipboard(elementId) {
    var element = document.getElementById(elementId);
    if (element.tagName === 'TEXTAREA' || element.tagName === 'INPUT') {
        element.select();
        document.execCommand("copy");
    } else {
        var elem = document.createElement("textarea");
        document.body.appendChild(elem);
        elem.value = element.innerText || element.textContent;
        elem.select();
        document.execCommand("copy");
        document.body.removeChild(elem);
    }
}

function initializeTabFunctionality() {
    document.getElementsByClassName('tablinks')[0].click();
}

function generateText(inputId, outputId) {
    // Retrieve the input text and the output textarea element
    var inputText = document.getElementById(inputId).value;
    var outputTextarea = document.getElementById(outputId);
    var generateButton = event.target; // Get the button that triggered the event

    // Check if the input text is not empty
    if (!inputText.trim()) {
        alert("Please enter the required information.");
        return;
    }

    // Retrieve the access token from local storage
    var applibotAccessToken = localStorage.getItem('applibotAccessToken');

    // Initialize an object to hold the API body parameters
    var apiBodyParams = new URLSearchParams();

    // Determine the appropriate URL and parameters for the backend call based on the inputId
    var apiUrl;
    if (inputId === 'coverInput' || inputId === 'expressionInput' || inputId === 'skillMatchInput') {
        // Determine the correct API endpoint based on the input ID
        if (inputId === 'coverInput') {
            apiUrl = `${apiBaseUrl}/cover-letter/`;
        } else if (inputId === 'expressionInput') {
            apiUrl = `${apiBaseUrl}/eoi/`;
        } else if (inputId === 'skillMatchInput') {
            apiUrl = `${apiBaseUrl}/skill-match/`;
        }
        apiBodyParams.append('job_description', inputText);
    } else if (inputId === 'formInput') {
        apiUrl = `${apiBaseUrl}/questions/`;
        apiBodyParams.append('question', inputText);
    } else if (inputId === 'dmInput') {
        apiUrl = `${apiBaseUrl}/dm-reply/`;
        var dmText = document.getElementById('dmJdInput').value;
        if (!dmText.trim()) {
            alert("Please enter the recruiter's DM.");
            return;
        }
        apiBodyParams.append('job_description', inputText);
        apiBodyParams.append('dm', dmText);
    } else {
        alert("Invalid input ID.");
        return;
    }

    generateButton.classList.add('loading');
    // Call the backend API to generate the text
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json',
            'token': applibotAccessToken
        },
        body: apiBodyParams
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail || 'An error occurred during the request.');
                });
            }
            return response.json(); // If OK, convert the response body to JSON
        })
        .then(data => {
            // Remove the loading class whether the fetch was successful
            generateButton.classList.remove('loading');
            outputTextarea.value = data;
        })
        .catch(error => {
            // Remove the loading class if an error occurs
            generateButton.classList.remove('loading');
            console.error('Error:', error);
            alert(error.message || "An error occurred during text generation.");
        });
}
