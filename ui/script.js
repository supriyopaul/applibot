// Define the base URL for your backend API
const apiBaseUrl = 'http://localhost:9999';

document.addEventListener('DOMContentLoaded', () => {
    // Check if the applibotAccessToken is not present in localStorage
    if (!localStorage.getItem('applibotAccessToken')) {
        // Select all nav-links and the logout button
        const navLinks = document.querySelectorAll('.nav-links a');
        const logoutButton = document.querySelector('.nav-button');

        // Disable all navigation links
        navLinks.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault(); // Prevent the link from navigating
                window.location.href = 'login.html'; // Redirect to login.html
            });
        });

        // Disable the logout button and redirect to login.html when clicked
        logoutButton.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent the default button action
            window.location.href = 'login.html'; // Redirect to login.html
        });
    }
});

document.addEventListener('DOMContentLoaded', (event) => {
    // Get the signup form and add an event listener to it
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function (event) {
            event.preventDefault();

            var email = document.getElementById('email').value;
            var password = document.getElementById('password').value;
            var confirmPassword = document.getElementById('confirm-password').value;

            if (password !== confirmPassword) {
                alert("Passwords do not match!");
                return;
            }

            // Prepare the data to be sent in the POST request
            var signupData = {
                email: email,
                password: password
            };

            // Call the backend API for signup
            fetch(`${apiBaseUrl}/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'accept': 'application/json'
                },
                body: JSON.stringify(signupData)
            })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(errorData => {
                            throw errorData; // Throw the error data for the catch block to handle
                        });
                    }
                    return response.json(); // If OK, proceed to convert the response body to JSON
                })
                .then(data => {
                    // Handle the response from the server
                    alert("Sign up successful!");
                    // Redirect to login page
                    window.location.href = 'login.html';
                })
                .catch(error => {
                    // Check if the error has 'detail' property
                    if (error && error.detail) {
                        if (error.detail === "Email already registered") {
                            // Redirect to the login page if the email is already registered
                            window.location.href = 'login.html';
                        } else {
                            alert(error.detail);
                        }
                    } else {
                        console.error('Error:', error);
                        alert("An error occurred during sign up.");
                    }
                });
        });
    } else {
        console.error('Signup form not found.');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    // Select the logout button
    const logoutButton = document.querySelector('.nav-button');

    // Add click event listener to the logout button
    logoutButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent any default action

        // Remove the applibotAccessToken from localStorage
        localStorage.removeItem('applibotAccessToken');

        // Redirect the user to index.html
        window.location.href = 'index.html';
    });
});


// Wait for the DOM to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', (event) => {

    // Get the login form and add an event listener to it
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent the default form submit action

            // Get the email and password values from the form
            var email = document.getElementById('login-email').value;
            var password = document.getElementById('login-password').value;

            // Encode the credentials as URLSearchParams
            var formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            // Call the backend API for login
            fetch(`${apiBaseUrl}/token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept': 'application/json'
                },
                body: formData
            })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(errorData => {
                            throw new Error(errorData.detail || 'An error occurred');
                        });
                    }
                    return response.json(); // If OK, convert the response body to JSON
                })
                .then(data => {
                    // Store the token in local storage
                    localStorage.setItem('applibotAccessToken', data.access_token);

                    // Redirect to generate.html
                    window.location.href = 'generate.html';
                })
                .catch(error => {
                    // Display an error alert if there is a problem logging in
                    alert(error.message);
                });
        });
    } else {
        console.error('Login form not found.');
    }
});

// generate
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

    document.getElementById(tabName).classList.add('active-content');
}

// Get the first tab to click on it by default
document.getElementsByClassName('tablinks')[0].click();

function copyToClipboard(elementId) {
    var element = document.getElementById(elementId);

    // Check if the element is a textarea or input
    if (element.tagName === 'TEXTAREA' || element.tagName === 'INPUT') {
        element.select();
        document.execCommand("copy");
    } else {
        // If it's not a textarea or input, use a temporary textarea to copy text
        var elem = document.createElement("textarea");
        document.body.appendChild(elem);
        elem.value = element.innerText || element.textContent; // Get the text content
        elem.select();
        document.execCommand("copy");
        document.body.removeChild(elem);
    }
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
    var text = document.getElementById(elementId).value; // Changed to .value
    var elem = document.createElement("textarea");
    document.body.appendChild(elem);
    elem.value = text;
    elem.select();
    document.execCommand("copy");
    document.body.removeChild(elem);
}

// Get the first tab to click on it by default
document.getElementsByClassName('tablinks')[0].click();

