'use client';

import React from 'react';
import './ChatMessage.css';

interface ChatMessageProps {
  message: {
    type: 'user' | 'assistant';
    content: string;
    sources?: Array<{
      document: string;
      text: string;
      metadata?: Record<string, any>;
    }>;
  };
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const [showSources, setShowSources] = React.useState(false);

  return (
    <div className={`message ${message.type}-message`}>
      <div className="message-avatar">
        {message.type === 'user' ? '👤' : '🤖'}
      </div>
      <div className="message-content">
        <p>{message.content}</p>
        {message.sources && message.sources.length > 0 && (
          <div className="sources-section">
            <button
              className="sources-toggle"
              onClick={() => setShowSources(!showSources)}
            >
              📚 Sources ({message.sources.length})
            </button>
            {showSources && (
              <div className="sources-list">
                {message.sources.map((source, idx) => (
                  <div key={idx} className="source-item">
                    <div className="source-document">{source.document}</div>
                    <div className="source-text">{source.text}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
