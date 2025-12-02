/**
 * TextSelection component.
 *
 * Yellow banner showing selected text context.
 */

import React from 'react';
import styles from './styles.module.css';

interface TextSelectionProps {
  selectedText: string;
  onClear: () => void;
}

export default function TextSelection({ selectedText, onClear }: TextSelectionProps): JSX.Element {
  if (!selectedText) {
    return null;
  }

  const preview = selectedText.length > 100
    ? selectedText.substring(0, 100) + '...'
    : selectedText;

  return (
    <div className={styles.textSelectionBanner}>
      <span>📝 Using selected text: "{preview}"</span>
      <button
        className={styles.clearTextButton}
        onClick={onClear}
        aria-label="Clear selected text"
      >
        ✕
      </button>
    </div>
  );
}
