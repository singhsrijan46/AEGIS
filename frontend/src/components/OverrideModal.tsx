import React, { useState } from 'react';
import { Finding } from '../types';
import { X, CheckCircle, AlertTriangle } from 'lucide-react';

interface OverrideModalProps {
  finding: Finding;
  onClose: () => void;
  onSubmit: (reasonCode: string, note: string) => void;
}

export const OverrideModal: React.FC<OverrideModalProps> = ({ finding, onClose, onSubmit }) => {
  const [reasonCode, setReasonCode] = useState('STYLISTIC_CHOICE');
  const [note, setNote] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(reasonCode, note);
  };

  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertTriangle size={18} color="var(--amber-warning)" />
            <h3 style={{ fontSize: '16px' }}>Creator Override Request</h3>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
            <X size={18} />
          </button>
        </div>

        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '16px', lineHeight: '1.5' }}>
          Per the <strong>Anti-Overruling Mandate (Co-Writing CHI [16])</strong>, you retain ultimate editorial agency.
          Explain your rationale for overriding <strong>"{finding.title}"</strong>. This will be logged in governance telemetry.
        </p>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, marginBottom: '6px', color: 'var(--text-primary)' }}>
              Override Classification
            </label>
            <select
              value={reasonCode}
              onChange={(e) => setReasonCode(e.target.value)}
              style={{
                width: '100%',
                padding: '8px 12px',
                background: 'rgba(0,0,0,0.3)',
                border: '1px solid var(--border-glass)',
                borderRadius: '6px',
                color: '#fff',
                fontSize: '13px'
              }}
            >
              <option value="STYLISTIC_CHOICE">Intentional Stylistic / Rhetorical Choice</option>
              <option value="CLIENT_EXCEPTION">Approved Client or Channel Exception</option>
              <option value="METAPHOR">Contextual Metaphor (Non-Literal)</option>
              <option value="OUTDATED_RULE">Confusing or Overly Restrictive Brand Rule</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, marginBottom: '6px', color: 'var(--text-primary)' }}>
              Editorial Justification Note
            </label>
            <textarea
              rows={3}
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="e.g. Approved by Head of Brand for Q4 social campaign..."
              required
              style={{
                width: '100%',
                padding: '10px 12px',
                background: 'rgba(0,0,0,0.3)',
                border: '1px solid var(--border-glass)',
                borderRadius: '6px',
                color: '#fff',
                fontSize: '13px',
                resize: 'none'
              }}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '10px' }}>
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              <CheckCircle size={14} />
              Confirm Override & Log
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
