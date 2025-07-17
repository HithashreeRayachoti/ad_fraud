import React, { useEffect } from "react";
import './App.css';
import { startTracking, endTracking } from "./clickceaseTracker";

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
    <div className="App">
      <h1 className="heading">Welcome to Our Ad Landing Page</h1>
      <p className="subheading">This simulates what happens when someone clicks on your ad.</p>

      {/* ✅ Centered image below heading */}
     <img
  src="/kpmg-logo-1.png"
  alt="KPMG Logo"
  className="center-logo"
/>


      <div className="link-grid">
        <a className='link' href="https://www.example.com/product1" target="_blank" rel="noopener noreferrer">
          Product 1
        </a>
        <a className='link' href="https://www.example.com/product2" target="_blank" rel="noopener noreferrer">
          Product 2
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
    </div>
  );
}

export default App;
