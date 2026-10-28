import React, { useState } from 'react';
import { Globe, ShieldAlert, CheckCircle2, MessageSquare, Terminal, Send, ArrowRight } from 'lucide-react';

interface CMSGateSimulatorProps {
  latestToken?: string;
  documentTitle: string;
}

export const CMSGateSimulator: React.FC<CMSGateSimulatorProps> = ({ latestToken, documentTitle }) => {
  const [selectedCMS, setSelectedCMS] = useState<'wordpress' | 'webflow' | 'contentful'>('wordpress');
  const [tokenInput, setTokenInput] = useState<string>(latestToken || '');
  const [publishLog, setPublishLog] = useState<any[]>([]);
  const [slackAction, setSlackAction] = useState<string | null>(null);

  const handlePublishAttempt = () => {
    const isSuccess = !!tokenInput && tokenInput.startsWith('VERITY-CERT-');
    const logEntry = {
      timestamp: new Date().toLocaleTimeString(),
      cms: selectedCMS,
      status: isSuccess ? 200 : 403,
      allowed: isSuccess,
      message: isSuccess
        ? `[HTTP 200 OK] Published to ${selectedCMS.toUpperCase()}. Verified with cryptographic token ${tokenInput}.`
        : `[HTTP 403 FORBIDDEN] Blocked by AEGIS-Brand™ pre-publish defense webhook. Draft lacks a valid Green-Tier certificate.`
    };
    setPublishLog([logEntry, ...publishLog]);
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 480px', gap: '24px' }}>
      {/* Left Column: CMS Publish Gate Simulator */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
          <Globe size={20} color="var(--teal-primary)" />
          <h2 style={{ fontSize: '18px' }}>Pre-Publish CMS Blocking Gateway Simulator</h2>
        </div>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '24px', lineHeight: '1.5' }}>
          In production, AEGIS-Brand™ webhooks intercept the publish transitions in WordPress, Webflow,
          and Contentful. Drafts without a verified Green Tier certificate are structurally blocked from public broadcast.
        </p>

        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '18px', borderRadius: '10px', border: '1px solid var(--border-glass)', marginBottom: '20px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '14px' }}>
            <div>
              <label style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>
                Publishing Destination
              </label>
              <select
                value={selectedCMS}
                onChange={(e) => setSelectedCMS(e.target.value as any)}
                style={{ width: '100%', padding: '8px 10px', background: 'rgba(255,255,255,0.06)', border: '1px solid var(--border-glass)', borderRadius: '6px', color: '#fff' }}
              >
                <option value="wordpress">WordPress REST API (/wp/v2/posts)</option>
                <option value="webflow">Webflow CMS Webhook</option>
                <option value="contentful">Contentful Delivery Filter</option>
              </select>
            </div>

            <div>
              <label style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>
                Cryptographic Token Input
              </label>
              <input
                type="text"
                value={tokenInput}
                onChange={(e) => setTokenInput(e.target.value)}
                placeholder="Paste VERITY-CERT-... or leave blank to test block"
                style={{ width: '100%', padding: '8px 10px', background: 'rgba(255,255,255,0.06)', border: '1px solid var(--border-glass)', borderRadius: '6px', color: '#fff', fontSize: '12px', fontFamily: 'var(--font-mono)' }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            {latestToken && (
              <button
                type="button"
                className="btn btn-secondary"
                style={{ fontSize: '11px' }}
                onClick={() => setTokenInput(latestToken)}
              >
                Auto-fill Latest Green Tier Token
              </button>
            )}

            <button className="btn btn-primary" onClick={handlePublishAttempt} style={{ marginLeft: 'auto' }}>
              <Send size={13} />
              Simulate CMS Publish Request
            </button>
          </div>
        </div>

        {/* Live Terminal Log */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px', fontSize: '12px', color: 'var(--text-muted)' }}>
            <Terminal size={14} />
            <span>Webhook Interceptor Live Audit Log</span>
          </div>

          <div
            style={{
              background: '#040810',
              border: '1px solid var(--border-glass)',
              borderRadius: '8px',
              padding: '14px',
              minHeight: '180px',
              maxHeight: '260px',
              overflowY: 'auto',
              fontFamily: 'var(--font-mono)',
              fontSize: '11px',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px'
            }}
          >
            {publishLog.length === 0 ? (
              <div style={{ color: 'var(--text-muted)' }}>
                [READY] Waiting for simulated publish webhook... Click 'Simulate CMS Publish Request'.
              </div>
            ) : (
              publishLog.map((log, i) => (
                <div key={i} style={{ color: log.allowed ? '#34D399' : '#F87171' }}>
                  <span style={{ color: 'var(--text-muted)' }}>[{log.timestamp}]</span> {log.message}
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Right Column: Slack Approval Bot Preview */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <MessageSquare size={18} color="var(--blue-accent)" />
          <h3 style={{ fontSize: '15px' }}>Slack & Teams Approval Bot Preview</h3>
        </div>

        <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '16px' }}>
          When content falls into the Amber tier (Score 70-89), Verity dispatches an interactive notification card to the Brand Stewardship channel.
        </p>

        {/* Slack Card Representation */}
        <div
          style={{
            background: '#1A1D21',
            borderRadius: '8px',
            border: '1px solid rgba(255,255,255,0.1)',
            padding: '16px',
            borderLeft: '4px solid var(--teal-primary)'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
            <div style={{ width: '20px', height: '20px', background: 'var(--teal-primary)', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: '10px', fontWeight: 900 }}>A</div>
            <strong style={{ fontSize: '12px', color: '#fff' }}>AEGIS Defense Sentinel Bot</strong>
            <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>APP 2:45 PM</span>
          </div>

          <div style={{ fontSize: '13px', fontWeight: 700, color: '#fff', marginBottom: '8px' }}>
            🛡️ AEGIS Audit Alert: {documentTitle}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '11px', color: 'var(--text-secondary)', background: 'rgba(0,0,0,0.2)', padding: '10px', borderRadius: '6px', marginBottom: '12px' }}>
            <div><strong>Author:</strong> Content Marketing</div>
            <div><strong>Status:</strong> AMBER TIER</div>
            <div><strong>Score:</strong> 78.4 / 100</div>
            <div><strong>Blockers:</strong> 0 active</div>
          </div>

          {slackAction ? (
            <div style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid rgba(16, 185, 129, 0.3)', padding: '8px', borderRadius: '6px', fontSize: '12px', color: '#34D399', textAlign: 'center' }}>
              ✅ Approved by Brand Director in Slack. Unlocked for CMS publication.
            </div>
          ) : (
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                className="btn btn-primary"
                style={{ flex: 1, fontSize: '11px', padding: '6px' }}
                onClick={() => setSlackAction('approved')}
              >
                ✅ 1-Click Approve
              </button>
              <button
                className="btn btn-secondary"
                style={{ flex: 1, fontSize: '11px', padding: '6px' }}
                onClick={() => alert('Opening diff inspection modal...')}
              >
                🔍 Inspect Diffs
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
