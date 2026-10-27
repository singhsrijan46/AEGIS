import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { PreFlightEditor } from './components/PreFlightEditor';
import { VisualAssetInspector } from './components/VisualAssetInspector';
import { BrandVaultManager } from './components/BrandVaultManager';
import { GovernanceTelemetry } from './components/GovernanceTelemetry';
import { CMSGateSimulator } from './components/CMSGateSimulator';
import { ResearchCorpusExplorer } from './components/ResearchCorpusExplorer';

import {
  DocumentAuditResponse,
  Finding,
  BrandRule,
  TemporalFact,
  CryptographicCertificate
} from './types';
import { SAMPLE_DRAFTS } from './data/sampleDrafts';
import {
  auditDocumentAPI,
  getBrandRulesAPI,
  getTemporalFactsAPI,
  addTemporalFactAPI,
  recordOverrideAPI
} from './api/client';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('editor');
  const [draftTitle, setDraftTitle] = useState<string>(SAMPLE_DRAFTS[0].title);
  const [department, setDepartment] = useState<string>(SAMPLE_DRAFTS[0].department);
  const [draftText, setDraftText] = useState<string>(SAMPLE_DRAFTS[0].text);

  const [auditResult, setAuditResult] = useState<DocumentAuditResponse | null>(null);
  const [isAuditing, setIsAuditing] = useState<boolean>(false);

  const [rules, setRules] = useState<BrandRule[]>([]);
  const [facts, setFacts] = useState<TemporalFact[]>([]);
  const [certificates, setCertificates] = useState<CryptographicCertificate[]>([]);

  // Initial load
  useEffect(() => {
    loadMetadata();
    runAudit(draftText, draftTitle, department);
  }, []);

  const loadMetadata = async () => {
    const fetchedRules = await getBrandRulesAPI();
    if (fetchedRules && fetchedRules.length > 0) {
      setRules(fetchedRules);
    }
    const fetchedFacts = await getTemporalFactsAPI();
    if (fetchedFacts && fetchedFacts.length > 0) {
      setFacts(fetchedFacts);
    }
  };

  const runAudit = async (textToAudit: string, titleToAudit: string, deptToAudit: string) => {
    setIsAuditing(true);
    try {
      const res = await auditDocumentAPI(textToAudit, titleToAudit, deptToAudit);
      setAuditResult(res);

      if (res.summary.cryptographic_token) {
        setCertificates(prev => [
          {
            token: res.summary.cryptographic_token!,
            document_id: res.document_id,
            sha256_hash: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
            timestamp: Date.now() / 1000,
            compliance_score: res.summary.compliance_score,
            tier: res.summary.tier,
            status: res.summary.publishing_status,
            issuer: 'Inkloom Verity Engine v2.4'
          },
          ...prev
        ]);
      }
    } finally {
      setIsAuditing(false);
    }
  };

  // 1-Click apply diff handler: updates text in-place and re-audits
  const handleApplyEdit = (originalSpan: string, replacement: string) => {
    const updated = draftText.replace(originalSpan, replacement);
    setDraftText(updated);
    runAudit(updated, draftTitle, department);
  };

  // Override handler
  const handleOverride = async (finding: Finding, reasonCode: string, note: string) => {
    await recordOverrideAPI({
      finding_id: finding.id,
      document_id: auditResult?.document_id || 'doc-1',
      rule_id: finding.rule_id,
      reason_code: reasonCode,
      justification_note: note,
      author: 'Frontline Creator'
    });

    // Remove the overridden finding from local view
    if (auditResult) {
      const remainingFindings = auditResult.findings.filter(f => f.id !== finding.id);
      const blockers = remainingFindings.filter(f => f.severity === 'BLOCKER').length;
      const warnings = remainingFindings.filter(f => f.severity === 'WARNING').length;
      const score = Math.max(0, 100 - blockers * 25 - warnings * 10);
      const tier = blockers === 0 && score >= 90 ? 'GREEN' : blockers === 0 && score >= 70 ? 'AMBER' : 'RED';

      setAuditResult({
        ...auditResult,
        summary: {
          ...auditResult.summary,
          total_findings: remainingFindings.length,
          blockers,
          warnings,
          compliance_score: score,
          tier: tier as any
        },
        findings: remainingFindings
      });
    }
  };

  const handleAddFact = async (fact: TemporalFact) => {
    await addTemporalFactAPI(fact);
    setFacts(prev => [fact, ...prev]);
  };

  return (
    <div className="app-container">
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        status={isAuditing ? 'AUDITING' : 'ONLINE'}
        latestToken={auditResult?.summary.cryptographic_token}
      />

      <main className="main-content">
        {activeTab === 'editor' && (
          <PreFlightEditor
            auditResult={auditResult}
            text={draftText}
            setText={setDraftText}
            title={draftTitle}
            setTitle={setDraftTitle}
            department={department}
            setDepartment={setDepartment}
            onRunAudit={() => runAudit(draftText, draftTitle, department)}
            isAuditing={isAuditing}
            onApplyEdit={handleApplyEdit}
            onOverride={handleOverride}
          />
        )}

        {activeTab === 'visual' && (
          <VisualAssetInspector />
        )}

        {activeTab === 'vault' && (
          <BrandVaultManager
            rules={rules}
            facts={facts}
            onAddFact={handleAddFact}
          />
        )}

        {activeTab === 'telemetry' && (
          <GovernanceTelemetry
            certificates={certificates}
          />
        )}

        {activeTab === 'cms' && (
          <CMSGateSimulator
            latestToken={auditResult?.summary.cryptographic_token}
            documentTitle={draftTitle}
          />
        )}

        {activeTab === 'papers' && (
          <ResearchCorpusExplorer />
        )}
      </main>
    </div>
  );
}

export default App;
