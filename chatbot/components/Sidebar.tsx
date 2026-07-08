'use client';

import { useState } from 'react';
import './Sidebar.css';

interface SidebarProps {
  documents: any[];
  selectedDocument: string | null;
  onSelectDocument: (doc: string | null) => void;
  onNewChat: () => void;
}

export default function Sidebar({
  documents,
  selectedDocument,
  onSelectDocument,
  onNewChat,
}: SidebarProps) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <div className="sidebar-header">
        <h2>📚 Documents</h2>
        <button
          className="toggle-button"
          onClick={() => setIsOpen(!isOpen)}
          title="Toggle sidebar"
        >
          {isOpen ? '◀' : '▶'}
        </button>
      </div>

      {isOpen && (
        <div className="sidebar-content">
          <button className="new-chat-button" onClick={onNewChat}>
            ➕ New Chat
          </button>

          <div className="documents-section">
            <button
              className={`document-item ${selectedDocument === null ? 'active' : ''}`}
              onClick={() => onSelectDocument(null)}
            >
              🌐 All Documents
            </button>

            <div className="documents-list">
              {documents.map((doc) => (
                <button
                  key={doc.name}
                  className={`document-item ${selectedDocument === doc.name ? 'active' : ''}`}
                  onClick={() => onSelectDocument(doc.name)}
                  title={`${doc.chunk_count} chunks`}
                >
                  📄 {doc.name}
                  <span className="chunk-count">{doc.chunk_count}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="sidebar-footer">
            <p className="footer-text">
              💡 Select a document to search within it, or search all documents.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
