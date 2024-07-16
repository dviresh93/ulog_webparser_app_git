// Collapsible.js
import React from 'react';
import './Collapsible.css';

const Collapsible = ({ title, content }) => {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <div className="collapsible">
      <button onClick={() => setIsOpen(!isOpen)}>{title}</button>
      <div className={`collapsible-content ${isOpen ? 'open' : ''}`}>{content}</div>
    </div>
  );
};

export default Collapsible;