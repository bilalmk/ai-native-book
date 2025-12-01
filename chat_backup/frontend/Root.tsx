import React from 'react';
import RAGChatbot from '../components/RAGChatbot';

// Default implementation, that you can customize
export default function Root({ children }) {
  return (
    <>
      {children}
      <RAGChatbot apiUrl="http://localhost:8000" />
    </>
  );
}
