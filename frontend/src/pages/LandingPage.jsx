import React from 'react';
import { Link } from 'react-router-dom';
import { Camera, Brain, Volume2, Globe, Users, MessageSquare } from 'lucide-react';
import PageWrapper from '../components/layout/PageWrapper';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <PageWrapper>
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container hero-container">
          <div className="hero-content">
            <div className="badge glass-panel">AI-Powered Accessibility</div>
            <h1 className="hero-title">
              Transforming <span className="text-gradient">Indian Sign Language</span> into Digital Communication
            </h1>
            <p className="hero-subtitle">
              Bridge the communication gap with real-time AI recognition. SignSpeak AI instantly translates gestures into text and speech, empowering the hearing-impaired community.
            </p>
            <div className="hero-actions">
              <Link to="/recognize" className="btn-primary btn-lg">
                Start Recognition
              </Link>
              <a href="#how-it-works" className="btn-secondary btn-lg">
                Learn More
              </a>
            </div>
          </div>
          <div className="hero-visual">
            <div className="visual-card glass-panel">
              <div className="mockup-header">
                <div className="dot red"></div>
                <div className="dot yellow"></div>
                <div className="dot green"></div>
              </div>
              <div className="mockup-body">
                <div className="mockup-video-placeholder">
                  <Camera size={48} className="placeholder-icon" />
                  <p>Live Feed Active</p>
                </div>
                <div className="mockup-result">
                  <p className="detected-text">"Namaste" 🙏</p>
                  <p className="confidence">Confidence: 98.2%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <div className="section-header">
            <h2>Powerful Features</h2>
            <p>Built with cutting-edge AI to ensure accurate and fast recognition.</p>
          </div>
          <div className="features-grid">
            <div className="feature-card card">
              <div className="feature-icon-wrapper"><Brain className="feature-icon" /></div>
              <h3>AI-Powered Detection</h3>
              <p>Advanced neural networks analyze hand gestures with high precision in real-time.</p>
            </div>
            <div className="feature-card card">
              <div className="feature-icon-wrapper"><Volume2 className="feature-icon" /></div>
              <h3>Speech Conversion</h3>
              <p>Instantly convert recognized sign language into natural-sounding speech.</p>
            </div>
            <div className="feature-card card">
              <div className="feature-icon-wrapper"><Globe className="feature-icon" /></div>
              <h3>ISL Focus</h3>
              <p>Specifically trained on Indian Sign Language vocabulary and grammatical nuances.</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="how-it-works-section">
        <div className="container">
          <div className="section-header">
            <h2>How It Works</h2>
            <p>Four simple steps to seamless communication.</p>
          </div>
          <div className="steps-container">
            {[
              { step: 1, title: 'Open Camera', desc: 'Allow webcam access in your browser' },
              { step: 2, title: 'Perform Sign', desc: 'Clearly perform the ISL gesture' },
              { step: 3, title: 'AI Detects', desc: 'Our model analyzes the frame' },
              { step: 4, title: 'Output', desc: 'Text and speech are generated instantly' }
            ].map((item) => (
              <div key={item.step} className="step-card">
                <div className="step-number">{item.step}</div>
                <h3>{item.title}</h3>
                <p>{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="team-section">
        <div className="container">
          <div className="section-header">
            <h2>Meet The Team</h2>
            <p>The minds behind SignSpeak AI.</p>
          </div>
          <div className="team-grid">
            <div className="team-member card">
              <div className="member-avatar">PB</div>
              <h3>Pabitra Basumatary</h3>
              <p className="role text-gradient">Full Stack Web Developer</p>
              <p className="bio">Architecting the scalable frontend and backend integration ready structures.</p>
            </div>
            <div className="team-member card">
              <div className="member-avatar">SA</div>
              <h3>Sajid Ahmed</h3>
              <p className="role text-gradient">AI/ML Engineer</p>
              <p className="bio">Developing and training the core computer vision model for gesture recognition.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="contact-section">
        <div className="container contact-container card">
          <div className="contact-info">
            <h2>Get in Touch</h2>
            <p>Have questions about the project or want to collaborate? Send us a message.</p>
            <div className="contact-detail">
              <MessageSquare className="detail-icon" />
              <span>contact@signspeak.ai</span>
            </div>
          </div>
          <form className="contact-form" onSubmit={(e) => e.preventDefault()}>
            <div className="form-group">
              <label>Name</label>
              <input type="text" placeholder="John Doe" className="form-input" />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input type="email" placeholder="john@example.com" className="form-input" />
            </div>
            <div className="form-group">
              <label>Message</label>
              <textarea placeholder="How can we help?" className="form-input" rows="4"></textarea>
            </div>
            <button className="btn-primary" type="submit">Send Message</button>
          </form>
        </div>
      </section>
    </PageWrapper>
  );
};

export default LandingPage;
