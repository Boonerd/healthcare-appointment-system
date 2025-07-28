// src/components/Login.jsx
import React from 'react';
import './Login.css';

const Login = () => {
  return (
    <div className="wrapper">
      <form action="#">
        <h2>Login</h2>

        <div className="input-field">
          <input type="text" required />
          <label>Enter your National ID</label>
        </div>

        <div className="input-field">
          <input type="password" required />
          <label>Enter your Password</label>
        </div>

        <div className="forget">
          <label htmlFor="remember">
            <input type="checkbox" id="remember" />
            <p>Remember me</p>
          </label>
          <a href="#">Forgot password?</a>
        </div>

        <button type="submit">Log In</button>

        <div className="register">
          <p>Don't have an account? <a href="/register">Register</a></p>
        </div>
      </form>
    </div>
  );
};

export default Login;
