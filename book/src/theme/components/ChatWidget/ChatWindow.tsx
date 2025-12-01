/**
 * ChatWindow component.
 *
 * Chat window container with header, messages, and input.
 */

import React from 'react';
import styles from './styles.module.css';
import MessageList, { Message } from './MessageList';
import InputArea from './InputArea';
import LoadingIndicator from './LoadingIndicator';
import ErrorMessage from './ErrorMessage';
import TextSelection from './TextSelection';

interface ChatWindowProps {
  messages: Message[];
  onClose: () => void;
  onSend: (message: string) => void;
  isLoading: boolean;
  error: string | null;
  onRetry: () => void;
  selectedText: string;
  onClearSelection: () => void;
}

export default function ChatWindow({
  messages,
  onClose,
  onSend,
  isLoading,
  error,
  onRetry,
  selectedText,
  onClearSelection,
}: ChatWindowProps): JSX.Element {
  return (
    <div className={styles.chatWindow} role="dialog" aria-label="Chat window">
      <div className={styles.chatHeader}>
        <h3>💬 Chat Assistant</h3>
        <button
          className={styles.closeButton}
          onClick={onClose}
          aria-label="Close chat"
        >
          ✕
        </button>
      </div>

      {selectedText && (
        <TextSelection
          selectedText={selectedText}
          onClear={onClearSelection}
        />
      )}

      <MessageList messages={messages} />

      {isLoading && <LoadingIndicator />}

      {error && <ErrorMessage message={error} onRetry={onRetry} />}

      <InputArea onSend={onSend} disabled={isLoading} />
    </div>
  );
}
