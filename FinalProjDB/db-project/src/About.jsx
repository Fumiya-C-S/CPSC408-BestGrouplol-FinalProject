import React from 'react';
import './About.css';
import NavBar from './NavBar';

function About() {
  return (
    <>
      <NavBar /> {/* Have a navigaiton bar instance */}
      <div className="about-container"> {/* Div for the about container */}
        <header className="about-header"> {/*Div for the about header */}
          {/* Header and information about our website */}
          <h1>About Our E-Commerce Platform</h1>
          <p className="tagline">A Database Management Systems Final Project</p>
        </header>
        {/* Goes over our project overview section using h2 and p tags */}
        <section className="about-section">
          <h2>Project Overview</h2>
          <p>
            This e-commerce platform was developed as our final project for CPSC 408 - Database Management Systems 
            at Chapman University. We chose to build an online shopping platform because it provides an excellent 
            opportunity to demonstrate the core concepts of database design and management in a real-world context.
          </p>
        </section>
        {/* Goes over why we chose E-Commerce */}
        <section className="about-section">
          <h2>Why E-Commerce?</h2>
          <p>
            E-commerce platforms are perfect for showcasing database principles because they involve:
          </p>
          {/* Goes into more detail about the reason for choosing it.  */}
          <div className="features">
            <div className="feature">
              <h3>Complex Relationships</h3>
              <p>Multiple interconnected entities like customers, products, orders, and inventory demonstrate 
              foreign keys, joins, and relational database design</p>
            </div>
            <div className="feature">
              <h3>CRUD Operations</h3>
              <p>Create, Read, Update, and Delete operations are essential for managing products, 
              processing orders, and maintaining customer data</p>
            </div>
            <div className="feature">
              <h3>Real-World Application</h3>
              <p>E-commerce mirrors actual business systems, making our database design practical 
              and applicable to industry scenarios</p>
            </div>
          </div>
        </section>
        {/* Explains what we used in our project */}
        <section className="about-section">
          <h2>Technical Implementation</h2>
          <p>
            Our platform leverages a robust technology stack including MySQL for database management, 
            Python with FastAPI for the backend, and React with Vite for a responsive frontend. 
            This architecture demonstrates our understanding of full-stack development and how databases 
            integrate with modern web applications.
          </p>
        </section>
        {/* Introduces the team  */}
        <section className="about-section team-section">
          <h2>Meet Our Team</h2>
          <div className="team-grid">
            <div className="team-member">
              <div className="member-avatar">M</div>
              <h3>Miguel Tellez</h3>
              <p>Backend Developer</p>
              <p className="member-email">mtellez@chapman.edu</p>
            </div>
            <div className="team-member">
              <div className="member-avatar">F</div>
              <h3>Fumi Shinagawa</h3>
              <p>Database Administrator</p>
              <p className="member-email">shinagawa@chapman.edu</p>
            </div>
            <div className="team-member">
              <div className="member-avatar">C</div>
              <h3>Christopher Uy</h3>
              <p>Frontend Developer</p>
              <p className="member-email">chuy@chapman.edu</p>
            </div>
            <div className="team-member">
              <div className="member-avatar">J</div>
              <h3>Jeffrey Bok</h3>
              <p>UI/UX Designer</p>
              <p className="member-email">bok@chapman.edu</p>
            </div>
          </div>
        </section>
        {/* Course info */}
        <section className="about-section contact-section">
          <h2>Course Information</h2>
          <p>CPSC 408 - Database Management Systems</p>
          <div className="contact-info">
            <p>Chapman University</p>
            <p>Orange, California</p>
            <p>Fall 2025</p>
          </div>
        </section>
      </div>
    </>
  );
}

export default About;
