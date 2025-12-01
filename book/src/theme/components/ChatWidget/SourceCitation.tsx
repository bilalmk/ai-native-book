/**
 * SourceCitation component.
 *
 * Displays source citations with title, score, and clickable link.
 */

import React from 'react';
import styles from './styles.module.css';
import { Source } from './api/chatApi';

interface SourceCitationProps {
  sources: Source[];
}

export default function SourceCitation({ sources }: SourceCitationProps): JSX.Element {
  if (sources.length === 0) {
    return null;
  }

  return (
    <div className={styles.sources}>
      <h4>📚 Sources:</h4>
      {sources.map((source, index) => (
        <div key={index} className={styles.sourceItem}>
          <a href={`/docs/${source.file_path.replace('.mdx', '').replace('.md', '')}`} target="_blank" rel="noopener noreferrer">
            {source.title}
          </a>
          <span className={styles.sourceScore}>
            ({Math.round(source.relevance_score * 100)}% relevant)
          </span>
        </div>
      ))}
    </div>
  );
}
