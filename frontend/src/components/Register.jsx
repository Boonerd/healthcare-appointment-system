// src/components/Register.jsx
import React from 'react';
import './Register.css'; // or reuse Login.css if preferred

const Register = () => {
  return (
    <div className="wrapper">
      <form action="#">
        <h2>Register</h2>

        <div className="input-field">
          <input type="email" required />
          <label>Email Address</label>
        </div>

        <div className="input-field">
          <input type="text" required />
          <label>Full Name</label>
        </div>

        <div className="input-field">
          <input type="text" required />
          <label>National ID</label>
        </div>

        <div className="input-field">
          <input type="text" required />
          <label>Phone Number</label>
        </div>

        <div className="input-field">
          <input type="password" required />
          <label>Password</label>
        </div>

        <div className="input-field">
          <select required>
            <option value="admin">Admin</option>
            <option value="practitioner">Practitioner</option>
            <option value="student">Student</option>
          </select>
          <label style={{ top: '-10px', fontSize: '0.8rem' }}>Role</label>
        </div>

        <button type="submit">Register</button>

        <div className="register">
          <p>Already have an account? <a href="/">Login</a></p>
        </div>
      </form>
    </div>
  );
};

export default Register;
