import React from 'react';
import { Shield, Sparkles, FileText, Image, Database, BarChart3, Globe, BookOpen } from 'lucide-react';

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  status: 'ONLINE' | 'AUDITING' | 'SECURED';
  latestToken?: string;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  status,
  latestToken
}) => {
  return (
    <header className="top-navbar">
      <div className="brand-brand">
        <div className="brand-logo-icon">
          <Shield size={22} />
        </div>
        <div className="brand-text">
          <h1>
            AEGIS-Brand™ <span>v4.0 Defense</span>
          </h1>
          <p>Automated Enterprise Governance & Integrity Suite</p>
        </div>
      </div>

      <nav className="nav-tabs-bar">
        <button
          className={`nav-tab ${activeTab === 'editor' ? 'active' : ''}`}
          onClick={() => setActiveTab('editor')}
        >
          <FileText size={15} />
          Pre-Flight Studio
        </button>
        <button
          className={`nav-tab ${activeTab === 'visual' ? 'active' : ''}`}
          onClick={() => setActiveTab('visual')}
        >
          <Image size={15} />
          Multimodal CV & WCAG
        </button>
        <button
          className={`nav-tab ${activeTab === 'vault' ? 'active' : ''}`}
          onClick={() => setActiveTab('vault')}
        >
          <Database size={15} />
          Brand Vault & SSOT
        </button>
        <button
          className={`nav-tab ${activeTab === 'telemetry' ? 'active' : ''}`}
          onClick={() => setActiveTab('telemetry')}
        >
          <BarChart3 size={15} />
          Governance Telemetry
        </button>
        <button
          className={`nav-tab ${activeTab === 'cms' ? 'active' : ''}`}
          onClick={() => setActiveTab('cms')}
        >
          <Globe size={15} />
          CMS Gate & Slack Bots
        </button>
        <button
          className={`nav-tab ${activeTab === 'papers' ? 'active' : ''}`}
          onClick={() => setActiveTab('papers')}
        >
          <BookOpen size={15} />
          20-Paper Corpus
        </button>
      </nav>

      <div className="top-actions">
        {latestToken && (
          <div className="badge badge-green" title="Cryptographically stamped publish certificate">
            <Sparkles size={12} />
            {latestToken.slice(0, 16)}...
          </div>
        )}
        <div className="badge badge-teal">
          <span className="pulse-dot" />
          Air-Gapped ZDR
        </div>
      </div>
    </header>
  );
};
