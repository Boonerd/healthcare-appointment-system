import React from 'react';
import './Register.css';

const Register = () => {
  return (
    <div className="wrapper">
      <form action="#">
        <h2>Register</h2>
        <div className="input-field">
          <input type="text" required />
          <label>Enter your email</label>
        </div>
        <div className="input-field">
          <input type="password" required />
          <label>Create a password</label>
        </div>
        <div className="input-field">
          <input type="password" required />
          <label>Confirm password</label>
        </div>
        <button type="submit">Register</button>
        <div className="register">
          <p>Already have an account? <a href="/login">Login</a></p>
        </div>
      </form>
    </div>
  );
};

export default Register;
