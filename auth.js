/* =========================================================
   Solace Authentication
   auth.js
   ========================================================= */

/*
 * Make sure api.js is loaded BEFORE this file:
 *
 * <script src="api.js"></script>
 * <script src="auth.js"></script>
 */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       LOGIN
    ===================================================== */

    const loginForm = document.getElementById("login-form");

    if (loginForm) {

        const emailInput =
            document.getElementById("email");

        const passwordInput =
            document.getElementById("password");

        const loginButton =
            document.getElementById("login-button");

        const loginButtonText =
            document.getElementById("login-button-text");

        const loginSpinner =
            document.getElementById("login-spinner");

        const loginArrow =
            document.getElementById("login-arrow");

        const errorMessage =
            document.getElementById("error-message");

        const successMessage =
            document.getElementById("success-message");


        function showLoginError(message) {

            if (!errorMessage) return;

            errorMessage.textContent = message;
            errorMessage.classList.remove("hidden");

            if (successMessage) {
                successMessage.classList.add("hidden");
            }
        }


        function showLoginSuccess(message) {

            if (!successMessage) return;

            successMessage.textContent = message;
            successMessage.classList.remove("hidden");

            if (errorMessage) {
                errorMessage.classList.add("hidden");
            }
        }


        function setLoginLoading(isLoading) {

            if (loginButton) {
                loginButton.disabled = isLoading;
            }

            if (loginSpinner) {
                loginSpinner.classList.toggle(
                    "hidden",
                    !isLoading
                );
            }

            if (loginArrow) {
                loginArrow.classList.toggle(
                    "hidden",
                    isLoading
                );
            }

            if (loginButtonText) {
                loginButtonText.textContent =
                    isLoading
                        ? "Signing in..."
                        : "Sign In";
            }
        }


        loginForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();

                if (errorMessage) {
                    errorMessage.classList.add("hidden");
                }

                if (successMessage) {
                    successMessage.classList.add("hidden");
                }


                const email =
                    emailInput?.value.trim() || "";

                const password =
                    passwordInput?.value || "";


                if (!email) {

                    showLoginError(
                        "Please enter your email address."
                    );

                    emailInput?.focus();

                    return;
                }


                if (!password) {

                    showLoginError(
                        "Please enter your password."
                    );

                    passwordInput?.focus();

                    return;
                }


                setLoginLoading(true);


                try {

                    /*
                     * FastAPI OAuth2PasswordRequestForm
                     *
                     * Your backend expects:
                     *
                     * username = email
                     * password = password
                     */

                    const formData =
                        new URLSearchParams();

                    formData.append(
                        "username",
                        email
                    );

                    formData.append(
                        "password",
                        password
                    );


                    const response =
                        await fetch(
                            `${API_BASE}/auth/login`,
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/x-www-form-urlencoded"
                                },

                                body: formData
                            }
                        );


                    let data = {};

                    try {

                        data =
                            await response.json();

                    } catch {

                        data = {};

                    }


                    if (!response.ok) {

                        throw new Error(
                            data.detail ||
                            "Invalid email or password."
                        );

                    }


                    /*
                     * Save authentication information
                     */

                    if (!data.access_token) {

                        throw new Error(
                            "Login succeeded, but the server did not return an access token."
                        );

                    }


                    localStorage.setItem(
                        "access_token",
                        data.access_token
                    );


                    if (data.user_id !== undefined) {

                        localStorage.setItem(
                            "user_id",
                            String(data.user_id)
                        );

                    }


                    if (data.token_type) {

                        localStorage.setItem(
                            "token_type",
                            data.token_type
                        );

                    }


                    showLoginSuccess(
                        "Welcome back to Solace."
                    );


                    /*
                     * Redirect to dashboard
                     */

                    setTimeout(
                        () => {

                            window.location.href =
                                "dashboard.html";

                        },
                        500
                    );


                } catch (error) {

                    console.error(
                        "Solace login error:",
                        error
                    );

                    showLoginError(
                        error.message ||
                        "Unable to sign in. Please try again."
                    );

                } finally {

                    setLoginLoading(false);

                }

            }
        );


        /*
         * Toggle password visibility
         */

        const togglePassword =
            document.getElementById(
                "toggle-password"
            );

        const passwordIcon =
            document.getElementById(
                "password-icon"
            );


        if (
            togglePassword &&
            passwordInput
        ) {

            togglePassword.addEventListener(
                "click",
                () => {

                    const isHidden =
                        passwordInput.type ===
                        "password";


                    passwordInput.type =
                        isHidden
                            ? "text"
                            : "password";


                    if (passwordIcon) {

                        passwordIcon.textContent =
                            isHidden
                                ? "visibility_off"
                                : "visibility";

                    }

                }
            );

        }

    }



    /* =====================================================
       REGISTER
    ===================================================== */

    const registerForm =
        document.getElementById(
            "register-form"
        );


    if (registerForm) {

        const emailInput =
            document.getElementById("email");

        const passwordInput =
            document.getElementById("password");

        const confirmPasswordInput =
            document.getElementById(
                "confirm-password"
            );

        const registerButton =
            document.getElementById(
                "register-button"
            );

        const registerButtonText =
            document.getElementById(
                "register-button-text"
            );

        const registerSpinner =
            document.getElementById(
                "register-spinner"
            );

        const registerArrow =
            document.getElementById(
                "register-arrow"
            );

        const errorMessage =
            document.getElementById(
                "error-message"
            );

        const successMessage =
            document.getElementById(
                "success-message"
            );


        function showRegisterError(message) {

            if (!errorMessage) return;

            errorMessage.textContent =
                message;

            errorMessage.classList.remove(
                "hidden"
            );

            if (successMessage) {
                successMessage.classList.add(
                    "hidden"
                );
            }
        }


        function showRegisterSuccess(message) {

            if (!successMessage) return;

            successMessage.textContent =
                message;

            successMessage.classList.remove(
                "hidden"
            );

            if (errorMessage) {
                errorMessage.classList.add(
                    "hidden"
                );
            }
        }


        function setRegisterLoading(isLoading) {

            if (registerButton) {
                registerButton.disabled =
                    isLoading;
            }

            if (registerSpinner) {

                registerSpinner.classList.toggle(
                    "hidden",
                    !isLoading
                );

            }

            if (registerArrow) {

                registerArrow.classList.toggle(
                    "hidden",
                    isLoading
                );

            }

            if (registerButtonText) {

                registerButtonText.textContent =
                    isLoading
                        ? "Creating account..."
                        : "Create Account";

            }

        }


        registerForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();


                if (errorMessage) {
                    errorMessage.classList.add(
                        "hidden"
                    );
                }

                if (successMessage) {
                    successMessage.classList.add(
                        "hidden"
                    );
                }


                const email =
                    emailInput?.value.trim() || "";

                const password =
                    passwordInput?.value || "";

                const confirmPassword =
                    confirmPasswordInput?.value || "";


                /*
                 * Basic validation
                 */

                if (!email) {

                    showRegisterError(
                        "Please enter your email address."
                    );

                    emailInput?.focus();

                    return;
                }


                if (!isValidEmail(email)) {

                    showRegisterError(
                        "Please enter a valid email address."
                    );

                    emailInput?.focus();

                    return;
                }


                if (password.length < 8) {

                    showRegisterError(
                        "Password must contain at least 8 characters."
                    );

                    passwordInput?.focus();

                    return;
                }


                if (password !== confirmPassword) {

                    showRegisterError(
                        "Passwords do not match."
                    );

                    confirmPasswordInput?.focus();

                    return;
                }


                setRegisterLoading(true);


                try {

                    /*
                     * Your current FastAPI backend expects:
                     *
                     * POST /auth/register
                     *
                     * email
                     * password
                     */

                    const formData =
                        new URLSearchParams();

                    formData.append(
                        "email",
                        email
                    );

                    formData.append(
                        "password",
                        password
                    );


                    const response =
                        await fetch(
                            `${API_BASE}/auth/register`,
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/x-www-form-urlencoded"
                                },

                                body: formData
                            }
                        );


                    let data = {};

                    try {

                        data =
                            await response.json();

                    } catch {

                        data = {};

                    }


                    if (!response.ok) {

                        throw new Error(
                            data.detail ||
                            "Unable to create your account."
                        );

                    }


                    /*
                     * Registration successful
                     */

                    showRegisterSuccess(
                        "Your Solace account was created successfully."
                    );


                    /*
                     * Redirect to login
                     */

                    setTimeout(
                        () => {

                            window.location.href =
                                "login.html";

                        },
                        900
                    );


                } catch (error) {

                    console.error(
                        "Solace registration error:",
                        error
                    );

                    showRegisterError(
                        error.message ||
                        "Unable to create your account."
                    );

                } finally {

                    setRegisterLoading(false);

                }

            }
        );


        /*
         * Password visibility
         */

        const togglePassword =
            document.getElementById(
                "toggle-password"
            );

        const passwordIcon =
            document.getElementById(
                "password-icon"
            );


        if (
            togglePassword &&
            passwordInput
        ) {

            togglePassword.addEventListener(
                "click",
                () => {

                    const isHidden =
                        passwordInput.type ===
                        "password";


                    passwordInput.type =
                        isHidden
                            ? "text"
                            : "password";


                    if (passwordIcon) {

                        passwordIcon.textContent =
                            isHidden
                                ? "visibility_off"
                                : "visibility";

                    }

                }
            );

        }


        /*
         * Password strength indicator
         */

        const strengthBar =
            document.getElementById(
                "strength-bar"
            );

        const strengthText =
            document.getElementById(
                "strength-text"
            );


        if (passwordInput) {

            passwordInput.addEventListener(
                "input",
                () => {

                    updatePasswordStrength(
                        passwordInput.value,
                        strengthBar,
                        strengthText
                    );

                }
            );

        }

    }



    /* =====================================================
       LOGOUT
    ===================================================== */

    const logoutButton =
        document.getElementById(
            "logout-button"
        );


    if (logoutButton) {

        logoutButton.addEventListener(
            "click",
            () => {

                logout();

            }
        );

    }



    /* =====================================================
       FORGOT PASSWORD
    ===================================================== */

    const forgotPassword =
        document.getElementById(
            "forgot-password"
        );


    if (forgotPassword) {

        forgotPassword.addEventListener(
            "click",
            async () => {

                const emailInput =
                    document.getElementById(
                        "email"
                    );

                const email =
                    emailInput?.value.trim() || "";


                if (!email) {

                    showGenericAuthError(
                        "Enter your email address first."
                    );

                    emailInput?.focus();

                    return;
                }


                /*
                 * IMPORTANT:
                 *
                 * Your current backend reset endpoint is
                 * a development-style reset endpoint.
                 *
                 * It should NOT be used as a production
                 * password-reset mechanism without proper
                 * email/token verification.
                 */

                const newPassword =
                    window.prompt(
                        "Enter your new password:"
                    );


                if (!newPassword) {
                    return;
                }


                if (newPassword.length < 8) {

                    showGenericAuthError(
                        "New password must contain at least 8 characters."
                    );

                    return;
                }


                try {

                    const formData =
                        new URLSearchParams();

                    formData.append(
                        "email",
                        email
                    );

                    formData.append(
                        "new_password",
                        newPassword
                    );


                    const response =
                        await fetch(
                            `${API_BASE}/auth/reset-password`,
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/x-www-form-urlencoded"
                                },

                                body: formData
                            }
                        );


                    let data = {};

                    try {

                        data =
                            await response.json();

                    } catch {

                        data = {};

                    }


                    if (!response.ok) {

                        throw new Error(
                            data.detail ||
                            "Password reset failed."
                        );

                    }


                    showGenericAuthSuccess(
                        "Password reset successfully. You can now sign in."
                    );


                } catch (error) {

                    console.error(
                        "Password reset error:",
                        error
                    );

                    showGenericAuthError(
                        error.message ||
                        "Password reset failed."
                    );

                }

            }
        );

    }

});



/* =========================================================
   HELPER FUNCTIONS
   ========================================================= */


/*
 * Email validation
 */

function isValidEmail(email) {

    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
        email
    );

}



/*
 * Password strength
 */

function updatePasswordStrength(
    password,
    strengthBar,
    strengthText
) {

    if (!strengthBar || !strengthText) {
        return;
    }


    let score = 0;


    if (password.length >= 8) {
        score++;
    }

    if (password.length >= 12) {
        score++;
    }

    if (/[A-Z]/.test(password)) {
        score++;
    }

    if (/[a-z]/.test(password)) {
        score++;
    }

    if (/[0-9]/.test(password)) {
        score++;
    }

    if (/[^A-Za-z0-9]/.test(password)) {
        score++;
    }


    /*
     * Convert score to percentage
     */

    const percentage =
        Math.min(
            100,
            Math.round(
                (score / 6) * 100
            )
        );


    strengthBar.style.width =
        `${percentage}%`;


    if (!password) {

        strengthBar.style.width =
            "0%";

        strengthText.textContent =
            "Use at least 8 characters.";

        return;
    }


    if (score <= 2) {

        strengthBar.style.backgroundColor =
            "#ef4444";

        strengthText.textContent =
            "Weak password.";

    } else if (score <= 4) {

        strengthBar.style.backgroundColor =
            "#eab308";

        strengthText.textContent =
            "Moderate password.";

    } else if (score === 5) {

        strengthBar.style.backgroundColor =
            "#84cc16";

        strengthText.textContent =
            "Strong password.";

    } else {

        strengthBar.style.backgroundColor =
            "#a8cfbc";

        strengthText.textContent =
            "Very strong password.";

    }

}



/*
 * Logout
 */

function logout() {

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "user_id"
    );

    localStorage.removeItem(
        "token_type"
    );


    window.location.href =
        "login.html";

}



/*
 * Check whether user is logged in
 */

function isLoggedIn() {

    return Boolean(
        localStorage.getItem(
            "access_token"
        )
    );

}



/*
 * Protect a page
 *
 * Use on dashboard/insights/chat:
 *
 * requireAuth();
 */

function requireAuth() {

    if (!isLoggedIn()) {

        window.location.href =
            "login.html";

        return false;

    }

    return true;

}



/*
 * Get logged-in user ID
 */

function getCurrentUserId() {

    return localStorage.getItem(
        "user_id"
    );

}



/*
 * Generic authentication error
 */

function showGenericAuthError(message) {

    const errorMessage =
        document.getElementById(
            "error-message"
        );

    const successMessage =
        document.getElementById(
            "success-message"
        );


    if (errorMessage) {

        errorMessage.textContent =
            message;

        errorMessage.classList.remove(
            "hidden"
        );

    }


    if (successMessage) {

        successMessage.classList.add(
            "hidden"
        );

    }

}



/*
 * Generic authentication success
 */

function showGenericAuthSuccess(message) {

    const successMessage =
        document.getElementById(
            "success-message"
        );

    const errorMessage =
        document.getElementById(
            "error-message"
        );


    if (successMessage) {

        successMessage.textContent =
            message;

        successMessage.classList.remove(
            "hidden"
        );

    }


    if (errorMessage) {

        errorMessage.classList.add(
            "hidden"
        );

    }

}