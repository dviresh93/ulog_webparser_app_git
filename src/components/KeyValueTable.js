import React from 'react';
import '../KeyValueTable.css';

const renderRows = (data) => {
  const rows = [];

  const traverse = (obj, parentKey = '') => {
    Object.entries(obj).forEach(([key, value]) => {
      if (key === 'status') return; // Skip rows with the key 'status'
      const fullKey = parentKey ? `${parentKey}.${key}` : key;
      const displayKey = fullKey.replace(/^value\./, ''); // Remove 'value.' prefix
      if (typeof value === 'object' && value !== null) {
        traverse(value, fullKey);
      } else {
        rows.push(
          <tr key={fullKey} className={value === false ? 'needs-attention' : ''}>
            <td>
              {displayKey}
              {value === false && <span className="status-indicator"></span>}
            </td>
            <td>{String(value)}</td>
          </tr>
        );
      }
    });
  };

  traverse(data);
  return rows;
};

const KeyValueTable = ({ data }) => {
  return (
    <table className="key-value-table">
      <thead>
        <tr>
          <th>Key</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {renderRows(data)}
      </tbody>
    </table>
  );
};

export default KeyValueTable;