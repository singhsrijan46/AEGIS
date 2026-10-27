import React, { useState } from 'react';
import { DocumentAuditResponse, Finding } from '../types';
import { SAMPLE_DRAFTS, SampleDraft } from '../data/sampleDrafts';
import { OverrideModal } from './OverrideModal';
import {
  Sparkles,
  Check,
  AlertCircle,
  FileCheck2,
  RefreshCw,
  ExternalLink,
  Lock,
  Compass,
  ArrowRight
} from 'lucide-react';

interface PreFlightEditorProps {
  auditResult: DocumentAuditResponse | null;
  text: string;
  setText: (t: string) => void;
  title: string;
  setTitle: (t: string) => void;
  department: string;
  setDepartment: (d: string) => void;
  onRunAudit: () => void;
  isAuditing: boolean;
  onApplyEdit: (originalSpan: string, replacement: string) => void;
  onOverride: (finding: Finding, reasonCode: string, note: string) => void;
}

export const PreFlightEditor: React.FC<PreFlightEditorProps> = ({
  auditResult,
  text,
  setText,
  title,
  setTitle,
  department,
  setDepartment,
  onRunAudit,
  isAuditing,
  onApplyEdit,
  onOverride
}) => {
  const [selectedFilter, setSelectedFilter] = useState<'ALL' | 'BLOCKER' | 'WARNING' | 'SUGGESTION'>('ALL');
  const [overrideFinding, setOverrideFinding] = useState<Finding | null>(null);

  const handleSelectPreset = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const draft = SAMPLE_DRAFTS.find(d => d.id === e.target.value);
    if (draft) {
      setTitle(draft.title);
      setDepartment(draft.department);
      setText(draft.text);
    }
  };

  const findings = auditResult?.findings || [];
  const filteredFindings = selectedFilter === 'ALL'
    ? findings
    : findings.filter(f => f.severity === selectedFilter);

  const summary = auditResult?.summary;
  const score = summary ? Math.round(summary.compliance_score) : 100;
  const tier = summary?.tier || 'GREEN';

  return (
    <div className="studio-grid">
      {/* Left Column: Authoring Draft Editor */}
      <div className="glass-panel editor-card">
        <div className="editor-card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flex: 1 }}>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Document Title"
              style={{
                background: 'transparent',
                border: 'none',
                color: '#fff',
                fontFamily: 'var(--font-heading)',
                fontSize: '16px',
                fontWeight: 700,
                outline: 'none',
                width: '100%',
                maxWidth: '380px'
              }}
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <select
              value=""
              onChange={handleSelectPreset}
              style={{
                padding: '6px 10px',
                background: 'rgba(255,255,255,0.06)',
                border: '1px solid var(--border-glass)',
                borderRadius: '6px',
                color: '#fff',
                fontSize: '12px'
              }}
            >
              <option value="" disabled>Load Enterprise Preset...</option>
              {SAMPLE_DRAFTS.map(d => (
                <option key={d.id} value={d.id}>{d.title}</option>
              ))}
            </select>

            <button
              className="btn btn-primary"
              onClick={onRunAudit}
              disabled={isAuditing}
            >
              <RefreshCw size={13} className={isAuditing ? 'animate-spin' : ''} />
              {isAuditing ? 'Auditing...' : 'Pre-Flight Inspect'}
            </button>
          </div>
        </div>

        <div className="editor-textarea-container">
          <textarea
            className="raw-editor"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Draft copy here or paste marketing press release..."
          />

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '14px', paddingTop: '10px', borderTop: '1px solid var(--border-glass)', fontSize: '11px', color: 'var(--text-muted)' }}>
            <div style={{ display: 'flex', gap: '16px' }}>
              <span>Words: {text.trim() ? text.trim().split(/\s+/).length : 0}</span>
              <span>Characters: {text.length}</span>
              {auditResult && auditResult.scrubbed_pii_count > 0 && (
                <span style={{ color: 'var(--teal-light)' }}>
                  <Lock size={11} style={{ display: 'inline', marginRight: '4px' }} />
                  {auditResult.scrubbed_pii_count} PII entity scrubbed in-flight
                </span>
              )}
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Compass size={12} color="var(--blue-accent)" />
              <span>Persona Alignment: {auditResult ? `${Math.round((1 - auditResult.persona_distance) * 100)}%` : '100%'}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Right Column: In-Context Sidecar Review Panel */}
      <div className="glass-panel sidecar-panel">
        <div className="sidecar-header">
          <div className="score-display-row">
            <div className="score-meter">
              <div className={`score-circle ${tier.toLowerCase()}`}>
                {score}
              </div>
              <div className="score-labels">
                <h3>Verity Compliance Score</h3>
                <p>
                  {tier === 'GREEN' && 'Ready for auto-publication'}
                  {tier === 'AMBER' && 'Brand Manager review required'}
                  {tier === 'RED' && 'Legal compliance blockers detected'}
                </p>
              </div>
            </div>

            <div className={`badge badge-${tier.toLowerCase()}`}>
              {tier} TIER
            </div>
          </div>

          <div className="finding-filters">
            <button
              className={`filter-chip ${selectedFilter === 'ALL' ? 'active' : ''}`}
              onClick={() => setSelectedFilter('ALL')}
            >
              All ({findings.length})
            </button>
            <button
              className={`filter-chip ${selectedFilter === 'BLOCKER' ? 'active' : ''}`}
              onClick={() => setSelectedFilter('BLOCKER')}
            >
              Blockers ({findings.filter(f => f.severity === 'BLOCKER').length})
            </button>
            <button
              className={`filter-chip ${selectedFilter === 'WARNING' ? 'active' : ''}`}
              onClick={() => setSelectedFilter('WARNING')}
            >
              Warnings ({findings.filter(f => f.severity === 'WARNING').length})
            </button>
            <button
              className={`filter-chip ${selectedFilter === 'SUGGESTION' ? 'active' : ''}`}
              onClick={() => setSelectedFilter('SUGGESTION')}
            >
              Tone ({findings.filter(f => f.severity === 'SUGGESTION').length})
            </button>
          </div>
        </div>

        <div className="findings-list">
          {filteredFindings.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
              <FileCheck2 size={44} color="var(--green-success)" style={{ margin: '0 auto 12px' }} />
              <h4 style={{ color: '#fff', fontSize: '15px', marginBottom: '6px' }}>Zero Active Violations</h4>
              <p style={{ fontSize: '12px' }}>This copy satisfies all active brand guidelines, factual records, and regulatory rules.</p>
            </div>
          ) : (
            filteredFindings.map((finding) => (
              <div key={finding.id} className={`finding-card ${finding.severity.toLowerCase()}`}>
                <div className="finding-card-header">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span className={`badge badge-${finding.severity === 'BLOCKER' ? 'red' : finding.severity === 'WARNING' ? 'amber' : 'blue'}`}>
                      {finding.category}
                    </span>
                    <span className="finding-title">{finding.title}</span>
                  </div>
                </div>

                <p className="finding-explanation">{finding.explanation}</p>

                <div className="finding-citation">
                  <ExternalLink size={12} />
                  <span>{finding.cited_source}</span>
                </div>

                {finding.suggested_edit && (
                  <div className="diff-box">
                    <span className="diff-del">{finding.flagged_text}</span>
                    <ArrowRight size={11} style={{ display: 'inline', margin: '0 4px', color: 'var(--text-muted)' }} />
                    <span className="diff-ins">{finding.suggested_edit}</span>
                  </div>
                )}

                <div className="finding-actions">
                  <button
                    className="btn btn-secondary"
                    style={{ padding: '4px 10px', fontSize: '11px' }}
                    onClick={() => setOverrideFinding(finding)}
                  >
                    Override
                  </button>
                  {finding.suggested_edit && (
                    <button
                      className="btn btn-primary"
                      style={{ padding: '4px 12px', fontSize: '11px' }}
                      onClick={() => onApplyEdit(finding.flagged_text, finding.suggested_edit)}
                    >
                      <Check size={12} />
                      1-Click Apply Diff
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {overrideFinding && (
        <OverrideModal
          finding={overrideFinding}
          onClose={() => setOverrideFinding(null)}
          onSubmit={(reason, note) => {
            onOverride(overrideFinding, reason, note);
            setOverrideFinding(null);
          }}
        />
      )}
    </div>
  );
};
