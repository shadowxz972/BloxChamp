import React, { useState } from 'react';
import '../css/LogInSignUp.css';

function LogInSignUp() {
    const [signupData, setSignupData] = useState({ username: '', email: '', password: '' });
    const [loginData, setLoginData] = useState({ email: '', password: '' });

    const handleSignupChange = (e) => {
        setSignupData({ ...signupData, [e.target.name]: e.target.value });
    };

    const handleLoginChange = (e) => {
        setLoginData({ ...loginData, [e.target.name]: e.target.value });
    };

    const handleSignupSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/sing-up/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(signupData),
            });
            const data = await response.json();
            console.log('Sign Up Response:', data);
        } catch (error) {
            console.error('Error during Sign Up:', error);
        }
    };

    const handleLoginSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`http://localhost:5000/log-in/?email=${loginData.email}&password=${loginData.password}`, {
                method: 'GET',
            });
            const data = await response.json();
            console.log('Log In Response:', data);
        } catch (error) {
            console.error('Error during Log In:', error);
        }
    };

    return (
        <div className="main">
            <input type="checkbox" id="chk" aria-hidden="true" />

            <div className="singup">
                <form onSubmit={handleSignupSubmit}>
                    <label htmlFor="chk" aria-hidden="true">Sign Up</label>
                    <input
                        type="text"
                        name="username"
                        placeholder="User Name"
                        value={signupData.username}
                        onChange={handleSignupChange}
                        required
                    />
                    <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        value={signupData.email}
                        onChange={handleSignupChange}
                        required
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        value={signupData.password}
                        onChange={handleSignupChange}
                        required
                    />
                    <button type="submit">Sign Up</button>
                </form>
            </div>

            <div className="login">
                <form onSubmit={handleLoginSubmit}>
                    <label htmlFor="chk" aria-hidden="true">Login</label>
                    <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        value={loginData.email}
                        onChange={handleLoginChange}
                        required
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        value={loginData.password}
                        onChange={handleLoginChange}
                        required
                    />
                    <button type="submit">Log In</button>
                </form>
            </div>
        </div>
    );
}

export default LogInSignUp;
