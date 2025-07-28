import React from 'react';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="wrapper dashboard-wrapper">
      <h2>Dashboard</h2>
      <p className="protected-text">Welcome, Patriciah 👋</p>
      
      <div className="dashboard-cards">
        <div className="card">
          <h3>Upcoming Appointments</h3>
          <p>You have 2 appointments this week.</p>
        </div>
        <div className="card">
          <h3>Messages</h3>
          <p>No new messages</p>
        </div>
        <div className="card">
          <h3>Profile</h3>
          <p>Update your personal information</p>
        </div>
      </div>

      <button className="logout-btn">Logout</button>
    </div>
  );
};

export default Dashboard;
