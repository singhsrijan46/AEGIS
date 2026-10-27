import React from 'react';
import { BarChart3, AlertOctagon, TrendingUp, ShieldCheck, Flame, Users, Sparkles } from 'lucide-react';
import { CryptographicCertificate } from '../types';

interface GovernanceTelemetryProps {
  certificates: CryptographicCertificate[];
}

export const GovernanceTelemetry: React.FC<GovernanceTelemetryProps> = ({ certificates }) => {
  const departments = [
    { name: 'Content Marketing', score: 88.4, drafts: 142, blockerRate: '4.2%', trend: '+3.1%' },
    { name: 'Growth & Ads', score: 76.1, drafts: 98, blockerRate: '18.5%', trend: '-2.4%' },
    { name: 'Sales Outbound', score: 69.8, drafts: 210, blockerRate: '24.1%', trend: '-5.0%' },
    { name: 'External PR & Agencies', score: 71.3, drafts: 64, blockerRate: '21.0%', trend: '+1.5%' },
    { name: 'Autonomous AI Bots', score: 62.5, drafts: 320, blockerRate: '38.7%', trend: '-8.2%' }
  ];

  const frictionPoints = [
    {
      ruleId: 'RULE-LEX-001',
      ruleName: "Prohibited Vocabulary ('simple', 'cheap')",
      overrides: 14,
      severity: 'HIGH',
      clusterReason: 'Writers frequently override when drafting customer testimonial quotes or conversational social hooks.',
      recommendation: "Clarify policy: Exclude verbatim customer quotes in quotation marks from colloquial vocabulary linters."
    },
    {
      ruleId: 'RULE-VOICE-001',
      ruleName: '5D Persona Coordinate Compliance',
      overrides: 9,
      severity: 'MEDIUM',
      clusterReason: 'Social media growth managers override formal register for TikTok / Instagram caption drafts.',
      recommendation: "Introduce channel-specific persona vectors (e.g. B2B Whitepaper vs Social Video)."
    }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h2 style={{ fontSize: '20px' }}>Governance Telemetry & Guideline Ambiguity Engine</h2>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
          Continuous Learning Loop: Departmental Heatmaps, Creator Override Clustering & SHA-256 Ledger
        </p>
      </div>

      {/* Top Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
        <div className="glass-panel" style={{ padding: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', fontSize: '12px' }}>
            <span>Total Pre-Flight Checks</span>
            <BarChart3 size={16} color="var(--teal-primary)" />
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, marginTop: '8px', color: '#fff' }}>834</div>
          <div style={{ fontSize: '11px', color: 'var(--green-success)', marginTop: '4px' }}>+18% velocity this month</div>
        </div>

        <div className="glass-panel" style={{ padding: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', fontSize: '12px' }}>
            <span>Average Review Turnaround</span>
            <TrendingUp size={16} color="var(--blue-accent)" />
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, marginTop: '8px', color: '#fff' }}>3.2 hrs</div>
          <div style={{ fontSize: '11px', color: 'var(--teal-light)', marginTop: '4px' }}>Reduced from 4.5 days (75% faster)</div>
        </div>

        <div className="glass-panel" style={{ padding: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', fontSize: '12px' }}>
            <span>Factual Claim Precision</span>
            <ShieldCheck size={16} color="var(--green-success)" />
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, marginTop: '8px', color: '#fff' }}>99.4%</div>
          <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>Zero regulatory FTC fines</div>
        </div>

        <div className="glass-panel" style={{ padding: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', fontSize: '12px' }}>
            <span>Creator Override Rate</span>
            <AlertOctagon size={16} color="var(--amber-warning)" />
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, marginTop: '8px', color: '#fff' }}>5.1%</div>
          <div style={{ fontSize: '11px', color: 'var(--amber-warning)', marginTop: '4px' }}>Feeding ambiguity clustering</div>
        </div>
      </div>

      {/* Department Heatmap */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <Flame size={18} color="var(--amber-warning)" />
          <h3 style={{ fontSize: '15px' }}>Cross-Departmental Compliance & Risk Heatmap</h3>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {departments.map((dept) => (
            <div
              key={dept.name}
              style={{
                display: 'grid',
                gridTemplateColumns: '220px 1fr 100px 100px',
                alignItems: 'center',
                gap: '16px',
                padding: '10px 14px',
                background: 'rgba(0,0,0,0.25)',
                borderRadius: '8px',
                border: '1px solid var(--border-glass)'
              }}
            >
              <div style={{ fontWeight: 700, fontSize: '13px' }}>{dept.name}</div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', marginBottom: '4px', color: 'var(--text-secondary)' }}>
                  <span>Compliance Index</span>
                  <span style={{ fontWeight: 700, color: dept.score >= 80 ? 'var(--green-success)' : dept.score >= 70 ? 'var(--amber-warning)' : 'var(--red-blocker)' }}>
                    {dept.score} / 100
                  </span>
                </div>
                <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.08)', borderRadius: '3px' }}>
                  <div
                    style={{
                      width: `${dept.score}%`,
                      height: '100%',
                      background: dept.score >= 80 ? 'var(--green-success)' : dept.score >= 70 ? 'var(--amber-warning)' : 'var(--red-blocker)',
                      borderRadius: '3px'
                    }}
                  />
                </div>
              </div>

              <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                {dept.drafts} drafts
              </div>

              <div style={{ fontSize: '12px', fontWeight: 600, color: dept.score < 70 ? 'var(--red-blocker)' : 'var(--text-secondary)' }}>
                {dept.blockerRate} risk
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Ambiguity Clustering Recommendations */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <h3 style={{ fontSize: '15px', marginBottom: '14px' }}>Guideline Ambiguity Detector (HDBSCAN Clustering)</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          {frictionPoints.map((fp) => (
            <div key={fp.ruleId} style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-glass)', borderRadius: '10px', padding: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span className="badge badge-amber">{fp.ruleId}</span>
                <span style={{ fontSize: '11px', color: 'var(--amber-warning)' }}>{fp.overrides} Overrides Logged</span>
              </div>
              <h4 style={{ fontSize: '13px', color: '#fff', marginBottom: '6px' }}>{fp.ruleName}</h4>
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '12px', lineHeight: '1.5' }}>
                {fp.clusterReason}
              </p>
              <div style={{ background: 'rgba(0, 168, 150, 0.08)', border: '1px solid rgba(0, 168, 150, 0.2)', padding: '10px', borderRadius: '6px', fontSize: '11px', color: 'var(--teal-light)' }}>
                <strong>Recommended Rule Update:</strong> {fp.recommendation}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Cryptographic SHA-256 Audit Ledger */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
          <Sparkles size={16} color="var(--teal-light)" />
          <h3 style={{ fontSize: '15px' }}>Immutable Cryptographic Compliance Ledger</h3>
        </div>

        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '12px' }}>
          <thead>
            <tr style={{ background: 'rgba(0,0,0,0.3)', borderBottom: '1px solid var(--border-glass)', color: 'var(--text-muted)' }}>
              <th style={{ padding: '10px 14px' }}>Certificate Token</th>
              <th style={{ padding: '10px 14px' }}>Document ID</th>
              <th style={{ padding: '10px 14px' }}>SHA-256 Hash</th>
              <th style={{ padding: '10px 14px' }}>Score</th>
              <th style={{ padding: '10px 14px' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {certificates.length === 0 ? (
              <tr>
                <td colSpan={5} style={{ padding: '24px', textAlign: 'center', color: 'var(--text-muted)' }}>
                  Certificates are automatically stamped upon Green Tier audit passes.
                </td>
              </tr>
            ) : (
              certificates.map((cert) => (
                <tr key={cert.token} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <td style={{ padding: '10px 14px', fontFamily: 'var(--font-mono)', color: 'var(--teal-light)', fontWeight: 700 }}>
                    {cert.token}
                  </td>
                  <td style={{ padding: '10px 14px' }}>{cert.document_id}</td>
                  <td style={{ padding: '10px 14px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                    {cert.sha256_hash.slice(0, 20)}...
                  </td>
                  <td style={{ padding: '10px 14px' }}>
                    <span className="badge badge-green">{cert.compliance_score}</span>
                  </td>
                  <td style={{ padding: '10px 14px' }}>
                    <span className="badge badge-teal">{cert.status}</span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
