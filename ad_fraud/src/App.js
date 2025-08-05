import React, { useEffect } from "react";
import './App.css';
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { startTracking, endTracking } from "./clickceaseTracker";
import Dashboard from "./dashboard";
function App() {
  useEffect(() => {
    console.log("Starting tracking...");
    startTracking();

    window.addEventListener("beforeunload", endTracking);

    return () => {
      window.removeEventListener("beforeunload", endTracking);
    };
  }, []);

  return (
    <BrowserRouter>
      <nav style={{
        display: 'flex',
        alignItems: 'center',
        background: '#1a237e',
        padding: '12px 32px',
        marginBottom: 0,
        boxShadow: '0 2px 8px rgba(0,0,0,0.04)'
      }}>
        <Link to="/" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: 18, marginRight: 24 }}>
          Home
        </Link>
        <Link to="/dashboard" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: 18 }}>
          Dashboard
        </Link>
      </nav>
      <Routes>
        <Route path="/" element={
          <div className="App">
            <h1 className="heading">Welcome to Our Ad Landing Page</h1>
            <h2 className="subheading">This is where a user or a bot will land after clicking on the ad which is present on the publisher website</h2>
            <p className="subheading">This simulates what happens when someone clicks on your ad.</p>

            {/* ✅ Centered image below heading */}
            <img
              src="/kpmg-logo-1.png"
              alt="KPMG Logo"
              className="center-logo"
            />

            <div className="link-grid">
              <a className='link' href="https://www.example.com/product1" target="_blank" rel="noopener noreferrer">
                Sample box for interaction
              </a>
              <a className='link' href="https://www.example.com/product2" target="_blank" rel="noopener noreferrer">
                Another sample box for interaction
              </a>
              <a className='link' href="https://www.example.com/about" target="_blank" rel="noopener noreferrer">
                About Us
              </a>
              <a className='link' href="https://www.example.com/services" target="_blank" rel="noopener noreferrer">
                Services
              </a>
              <a className='link' href="https://www.example.com/contact" target="_blank" rel="noopener noreferrer">
                Contact Us
              </a>
              <a className='link' href="https://www.example.com/blog" target="_blank" rel="noopener noreferrer">
                Blog
              </a>
            </div>
            <div style={{ marginTop: '2rem' }}>
            </div>
          </div>
        } />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
