import React, { useState } from 'react';
import { VisualAssetInput, VisualFinding } from '../types';
import {
  Image,
  Eye,
  Sliders,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  Maximize2,
  Palette
} from 'lucide-react';

export const VisualAssetInspector: React.FC = () => {
  const [activeAsset, setActiveAsset] = useState<string>('banner-1');
  const [logoMargin, setLogoMargin] = useState<number>(20); // px from edge (less than 50px creates violation)
  const [textColor, setTextColor] = useState<string>('#94A3B8'); // Low contrast against dark
  const [bgColor, setBgColor] = useState<string>('#0B1526');
  const [testHex, setTestHex] = useState<string>('#00B8A5'); // Drifted teal
  const [altText, setAltText] = useState<string>('');

  // 1. CIELAB ΔE calculation mock
  const isTealDrift = testHex.toUpperCase() !== '#00A896';
  const deltaE = isTealDrift ? 3.42 : 0.0;

  // 2. WCAG Contrast Calculation
  const isContrastFailing = textColor === '#94A3B8' || textColor === '#64748B';
  const contrastRatio = isContrastFailing ? 3.12 : 7.85;

  // 3. Logo Clear Space Buffer (0.5H = 40px required)
  const isSafeZoneViolated = logoMargin < 40;

  // 4. Alt Text status
  const isAltMissing = altText.trim().length < 10;

  const handleFixAll = () => {
    setLogoMargin(50);
    setTextColor('#F8FAFC');
    setTestHex('#00A896');
    setAltText('Official promotional banner for Inkloom Verity pre-publication brand governance platform.');
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 420px', gap: '24px' }}>
      {/* Left Column: Visual Canvas & Overlays */}
      <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div>
            <h2 style={{ fontSize: '18px' }}>Multimodal Visual Asset Inspector</h2>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Deterministic OpenCV CIELAB ΔE00, WCAG 2.1 Contrast & LayoutLMv3 Logo Buffer Audit
            </p>
          </div>

          <button className="btn btn-primary" onClick={handleFixAll}>
            <Sparkles size={14} />
            1-Click Resolve Visual Guardrails
          </button>
        </div>

        {/* Interactive Asset Canvas Mockup */}
        <div
          style={{
            flex: 1,
            minHeight: '440px',
            background: bgColor,
            borderRadius: '12px',
            border: '2px solid var(--border-glass)',
            position: 'relative',
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            padding: '30px',
            boxShadow: 'inset 0 0 40px rgba(0,0,0,0.6)'
          }}
        >
          {/* Top Bar with Logo & Safe Zone Buffer Box */}
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
            <div
              style={{
                position: 'relative',
                border: isSafeZoneViolated ? '2px dashed var(--red-blocker)' : '1px dashed var(--teal-primary)',
                background: isSafeZoneViolated ? 'rgba(239, 68, 68, 0.1)' : 'rgba(0, 168, 150, 0.05)',
                padding: '12px 20px',
                borderRadius: '8px',
                transition: 'all 0.2s ease',
                marginLeft: `${logoMargin}px`,
                marginTop: `${Math.max(10, logoMargin - 10)}px`
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{ width: '28px', height: '28px', background: testHex, borderRadius: '6px' }} />
                <span style={{ fontWeight: 800, fontSize: '16px', letterSpacing: '0.5px' }}>INKLOOM VERITY</span>
              </div>

              {isSafeZoneViolated && (
                <div
                  style={{
                    position: 'absolute',
                    top: '-12px',
                    right: '-12px',
                    background: 'var(--red-blocker)',
                    color: '#fff',
                    borderRadius: '50%',
                    padding: '3px'
                  }}
                  title="0.5H Clear Space Margin Encroached"
                >
                  <AlertTriangle size={14} />
                </div>
              )}
            </div>

            <div className="badge badge-teal">
              4K Display Resolution
            </div>
          </div>

          {/* Center Text Overlay with WCAG Contrast Meter */}
          <div style={{ textAlign: 'center', margin: '40px 0' }}>
            <h1
              style={{
                color: textColor,
                fontSize: '32px',
                fontWeight: 900,
                letterSpacing: '-0.02em',
                marginBottom: '10px',
                transition: 'color 0.2s ease'
              }}
            >
              Enterprise Brand Integrity Guaranteed
            </h1>
            <p style={{ color: textColor, opacity: 0.85, fontSize: '16px', maxWidth: '600px', margin: '0 auto' }}>
              Decompose marketing assertions into verifiable atomic units before public release.
            </p>
          </div>

          {/* Bottom Palette Swatch Bar */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Palette:</span>
              <div style={{ width: '22px', height: '22px', background: testHex, borderRadius: '4px', border: '1px solid #fff' }} title={testHex} />
              <div style={{ width: '22px', height: '22px', background: '#0F2537', borderRadius: '4px' }} title="#0F2537" />
              <div style={{ width: '22px', height: '22px', background: '#2563EB', borderRadius: '4px' }} title="#2563EB" />
            </div>

            <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
              Alt Text: {isAltMissing ? <span style={{ color: 'var(--red-blocker)' }}>Missing</span> : <span style={{ color: 'var(--green-success)' }}>Attached</span>}
            </div>
          </div>
        </div>
      </div>

      {/* Right Column: Visual Findings & Controls */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {/* Metric 1: CIELAB Color Distance */}
        <div className="glass-panel" style={{ padding: '18px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Palette size={16} color={deltaE > 2.0 ? 'var(--amber-warning)' : 'var(--green-success)'} />
              <h4 style={{ fontSize: '13px' }}>CIELAB ΔE00 Colorimetry</h4>
            </div>
            <span className={`badge ${deltaE > 2.0 ? 'badge-amber' : 'badge-green'}`}>
              ΔE = {deltaE.toFixed(2)}
            </span>
          </div>

          <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '12px' }}>
            Official Primary Teal is <code>#00A896</code>. Tolerance ceiling is ΔE00 &lt; 2.0.
          </p>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              className="btn btn-secondary"
              style={{ flex: 1, fontSize: '11px' }}
              onClick={() => setTestHex('#00B8A5')}
            >
              Simulate Drift (#00B8A5)
            </button>
            <button
              className="btn btn-primary"
              style={{ flex: 1, fontSize: '11px' }}
              onClick={() => setTestHex('#00A896')}
            >
              Snap Official (#00A896)
            </button>
          </div>
        </div>

        {/* Metric 2: WCAG 2.1 Contrast Ratio */}
        <div className="glass-panel" style={{ padding: '18px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Eye size={16} color={contrastRatio < 4.5 ? 'var(--red-blocker)' : 'var(--green-success)'} />
              <h4 style={{ fontSize: '13px' }}>WCAG 2.1 AA Contrast Ratio</h4>
            </div>
            <span className={`badge ${contrastRatio < 4.5 ? 'badge-red' : 'badge-green'}`}>
              {contrastRatio.toFixed(2)}:1
            </span>
          </div>

          <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '12px' }}>
            WCAG 2.1 AA mandates at least 4.5:1 contrast for standard body text and 3.0:1 for headers.
          </p>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              className="btn btn-secondary"
              style={{ flex: 1, fontSize: '11px' }}
              onClick={() => setTextColor('#94A3B8')}
            >
              Low Contrast Text
            </button>
            <button
              className="btn btn-primary"
              style={{ flex: 1, fontSize: '11px' }}
              onClick={() => setTextColor('#F8FAFC')}
            >
              Compliant (#F8FAFC)
            </button>
          </div>
        </div>

        {/* Metric 3: Logo Safe Zone Boundary */}
        <div className="glass-panel" style={{ padding: '18px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Maximize2 size={16} color={isSafeZoneViolated ? 'var(--red-blocker)' : 'var(--green-success)'} />
              <h4 style={{ fontSize: '13px' }}>Logo Clear Space (0.5H Buffer)</h4>
            </div>
            <span className={`badge ${isSafeZoneViolated ? 'badge-red' : 'badge-green'}`}>
              {isSafeZoneViolated ? 'Violated' : 'Passed'}
            </span>
          </div>

          <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '12px' }}>
            LayoutLMv3 detects edge distance. Buffer must exceed 40px (0.5 × logo height).
          </p>

          <input
            type="range"
            min={10}
            max={70}
            value={logoMargin}
            onChange={(e) => setLogoMargin(Number(e.target.value))}
            style={{ width: '100%', accentColor: 'var(--teal-primary)' }}
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
            <span>10px (Encroachment)</span>
            <span>Current: {logoMargin}px</span>
            <span>70px (Compliant)</span>
          </div>
        </div>

        {/* Metric 4: Alt Text Auditor */}
        <div className="glass-panel" style={{ padding: '18px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
            <h4 style={{ fontSize: '13px' }}>ScreenAI Alt-Text Auditor</h4>
            <span className={`badge ${isAltMissing ? 'badge-red' : 'badge-green'}`}>
              {isAltMissing ? 'Missing' : 'Passed'}
            </span>
          </div>

          <textarea
            rows={2}
            value={altText}
            onChange={(e) => setAltText(e.target.value)}
            placeholder="No alt-text defined for screen-readers..."
            style={{
              width: '100%',
              padding: '8px 10px',
              background: 'rgba(0,0,0,0.3)',
              border: '1px solid var(--border-glass)',
              borderRadius: '6px',
              color: '#fff',
              fontSize: '12px',
              marginBottom: '10px',
              resize: 'none'
            }}
          />

          <button
            className="btn btn-secondary"
            style={{ width: '100%', fontSize: '11px' }}
            onClick={() => setAltText('Inkloom Verity enterprise marketing banner with verified compliance metrics.')}
          >
            <Sparkles size={12} />
            Generate ScreenAI Alt-Text
          </button>
        </div>
      </div>
    </div>
  );
};
