import React, { useState } from 'react';
import { BrandRule, TemporalFact } from '../types';
import { Database, Plus, ShieldCheck, Clock, CheckCircle2, AlertCircle, FileText } from 'lucide-react';

interface BrandVaultManagerProps {
  rules: BrandRule[];
  facts: TemporalFact[];
  onAddFact: (fact: TemporalFact) => void;
}

export const BrandVaultManager: React.FC<BrandVaultManagerProps> = ({ rules, facts, onAddFact }) => {
  const [activeTab, setActiveTab] = useState<'rules' | 'facts' | 'tokens'>('facts');
  const [showAddModal, setShowAddModal] = useState(false);

  // New fact form state
  const [newEntity, setNewEntity] = useState('Inkloom Verity');
  const [newAttribute, setNewAttribute] = useState('');
  const [newValue, setNewValue] = useState('');
  const [validFrom, setValidFrom] = useState('2026-01-01');
  const [validTo, setValidTo] = useState('2027-12-31');
  const [sourceDoc, setSourceDoc] = useState('Executive Board Minutes Q4 2026');

  const handleAddSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const fact: TemporalFact = {
      id: `FACT-USER-${Date.now().toString().slice(-4)}`,
      entity: newEntity,
      attribute: newAttribute,
      value: newValue,
      valid_from: validFrom,
      valid_to: validTo,
      source_document: sourceDoc,
      section: 'Section 1.1',
      page: 1,
      status: 'ACTIVE'
    };
    onAddFact(fact);
    setShowAddModal(false);
    setNewAttribute('');
    setNewValue('');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '20px' }}>Enterprise Brand Vault & Temporal SSOT</h2>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            Codified Brand Constitution, Design Tokens, and Time-Bounded Knowledge Graph
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <div className="nav-tabs-bar" style={{ background: 'rgba(255,255,255,0.04)' }}>
            <button
              className={`nav-tab ${activeTab === 'facts' ? 'active' : ''}`}
              onClick={() => setActiveTab('facts')}
            >
              Temporal SSOT ({facts.length})
            </button>
            <button
              className={`nav-tab ${activeTab === 'rules' ? 'active' : ''}`}
              onClick={() => setActiveTab('rules')}
            >
              Brand Constitution DAG ({rules.length})
            </button>
            <button
              className={`nav-tab ${activeTab === 'tokens' ? 'active' : ''}`}
              onClick={() => setActiveTab('tokens')}
            >
              Design Tokens & Persona
            </button>
          </div>

          {activeTab === 'facts' && (
            <button className="btn btn-primary" onClick={() => setShowAddModal(true)}>
              <Plus size={14} />
              Register Enterprise Fact
            </button>
          )}
        </div>
      </div>

      {/* Tab 1: Temporal Knowledge Graph Facts */}
      {activeTab === 'facts' && (
        <div className="glass-panel" style={{ overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '13px' }}>
            <thead>
              <tr style={{ background: 'rgba(0,0,0,0.3)', borderBottom: '1px solid var(--border-glass)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '14px 18px', fontWeight: 600 }}>Entity & Attribute</th>
                <th style={{ padding: '14px 18px', fontWeight: 600 }}>Verified Fact Value</th>
                <th style={{ padding: '14px 18px', fontWeight: 600 }}>Temporal Validity</th>
                <th style={{ padding: '14px 18px', fontWeight: 600 }}>Status</th>
                <th style={{ padding: '14px 18px', fontWeight: 600 }}>Authoritative Provenance</th>
              </tr>
            </thead>
            <tbody>
              {facts.map((f, i) => (
                <tr key={f.id || i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', background: i % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.01)' }}>
                  <td style={{ padding: '14px 18px' }}>
                    <div style={{ fontWeight: 700, color: '#fff' }}>{f.attribute}</div>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{f.entity}</div>
                  </td>
                  <td style={{ padding: '14px 18px', color: 'var(--text-primary)', maxWidth: '320px' }}>
                    <strong>{f.value}</strong>
                  </td>
                  <td style={{ padding: '14px 18px', fontFamily: 'var(--font-mono)', fontSize: '12px' }}>
                    <span style={{ color: 'var(--teal-light)' }}>{f.valid_from}</span>
                    <span style={{ color: 'var(--text-muted)', margin: '0 6px' }}>➔</span>
                    <span style={{ color: f.status === 'DEPRECATED' ? 'var(--red-blocker)' : 'var(--teal-light)' }}>
                      {f.valid_to}
                    </span>
                  </td>
                  <td style={{ padding: '14px 18px' }}>
                    <span className={`badge ${f.status === 'ACTIVE' ? 'badge-green' : 'badge-red'}`}>
                      {f.status}
                    </span>
                  </td>
                  <td style={{ padding: '14px 18px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                    <div>{f.source_document}</div>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{f.section}, Page {f.page}</div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab 2: Brand Constitution Rules DAG */}
      {activeTab === 'rules' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '16px' }}>
          {rules.map((r) => (
            <div key={r.id} className="glass-panel" style={{ padding: '18px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span className="badge badge-teal">{r.category}</span>
                  <span className={`badge badge-${r.severity === 'BLOCKER' ? 'red' : r.severity === 'WARNING' ? 'amber' : 'blue'}`}>
                    {r.severity}
                  </span>
                </div>
                <h4 style={{ fontSize: '14px', marginBottom: '6px', color: '#fff' }}>{r.name}</h4>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.5', marginBottom: '12px' }}>
                  {r.description}
                </p>
              </div>

              <div style={{ fontSize: '11px', color: 'var(--text-muted)', borderTop: '1px solid var(--border-glass)', paddingTop: '10px' }}>
                <span style={{ color: 'var(--teal-light)' }}>{r.source_document}</span> ({r.section}, p.{r.page})
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tab 3: Design Tokens & Persona Vector */}
      {activeTab === 'tokens' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div className="glass-panel" style={{ padding: '20px' }}>
            <h3 style={{ fontSize: '15px', marginBottom: '16px' }}>Official Color Tokens (CIELAB Reference)</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ width: '32px', height: '32px', background: '#00A896', borderRadius: '6px' }} />
                <div>
                  <div style={{ fontWeight: 700, fontSize: '12px' }}>PRIMARY_TEAL</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>#00A896</div>
                </div>
              </div>

              <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ width: '32px', height: '32px', background: '#0F2537', borderRadius: '6px' }} />
                <div>
                  <div style={{ fontWeight: 700, fontSize: '12px' }}>NAVY_DARK</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>#0F2537</div>
                </div>
              </div>

              <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ width: '32px', height: '32px', background: '#2563EB', borderRadius: '6px' }} />
                <div>
                  <div style={{ fontWeight: 700, fontSize: '12px' }}>ACCENT_BLUE</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>#2563EB</div>
                </div>
              </div>

              <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ width: '32px', height: '32px', background: '#10B981', borderRadius: '6px' }} />
                <div>
                  <div style={{ fontWeight: 700, fontSize: '12px' }}>EMERALD_GREEN</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>#10B981</div>
                </div>
              </div>
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '20px' }}>
            <h3 style={{ fontSize: '15px', marginBottom: '16px' }}>Target 5D Persona Vector Coordinates</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                  <span>Formality</span>
                  <strong>+0.65 (Executive)</strong>
                </div>
                <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px' }}>
                  <div style={{ width: '82%', height: '100%', background: 'var(--teal-primary)', borderRadius: '3px' }} />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                  <span>Authority</span>
                  <strong>+0.85 (Authoritative)</strong>
                </div>
                <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px' }}>
                  <div style={{ width: '92%', height: '100%', background: 'var(--blue-accent)', borderRadius: '3px' }} />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                  <span>Directness</span>
                  <strong>+0.75 (Concise)</strong>
                </div>
                <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px' }}>
                  <div style={{ width: '87%', height: '100%', background: 'var(--green-success)', borderRadius: '3px' }} />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Add Fact Modal */}
      {showAddModal && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h3 style={{ fontSize: '16px', marginBottom: '14px' }}>Register Enterprise Truth to Temporal SSOT</h3>
            <form onSubmit={handleAddSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div>
                <label style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Entity</label>
                <input
                  type="text"
                  value={newEntity}
                  onChange={(e) => setNewEntity(e.target.value)}
                  required
                  style={{ width: '100%', padding: '8px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-glass)', borderRadius: '6px', color: '#fff' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Attribute (e.g. FedRAMP High Authorization)</label>
                <input
                  type="text"
                  value={newAttribute}
                  onChange={(e) => setNewAttribute(e.target.value)}
                  required
                  placeholder="e.g. Q1 2027 Price Sheet"
                  style={{ width: '100%', padding: '8px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-glass)', borderRadius: '6px', color: '#fff' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Verified Value</label>
                <input
                  type="text"
                  value={newValue}
                  onChange={(e) => setNewValue(e.target.value)}
                  required
                  placeholder="e.g. $129/seat/month"
                  style={{ width: '100%', padding: '8px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-glass)', borderRadius: '6px', color: '#fff' }}
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <div>
                  <label style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Valid From (YYYY-MM-DD)</label>
                  <input
                    type="date"
                    value={validFrom}
                    onChange={(e) => setValidFrom(e.target.value)}
                    required
                    style={{ width: '100%', padding: '8px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-glass)', borderRadius: '6px', color: '#fff' }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Valid To (YYYY-MM-DD)</label>
                  <input
                    type="date"
                    value={validTo}
                    onChange={(e) => setValidTo(e.target.value)}
                    required
                    style={{ width: '100%', padding: '8px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-glass)', borderRadius: '6px', color: '#fff' }}
                  />
                </div>
              </div>

              <div>
                <label style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Source Provenance Document</label>
                <input
                  type="text"
                  value={sourceDoc}
                  onChange={(e) => setSourceDoc(e.target.value)}
                  required
                  style={{ width: '100%', padding: '8px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-glass)', borderRadius: '6px', color: '#fff' }}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '10px' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowAddModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Save to Knowledge Graph
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
