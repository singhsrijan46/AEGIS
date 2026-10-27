import React, { useState } from 'react';
import { RESEARCH_PAPERS } from '../data/papersData';
import { AcademicPaper } from '../types';
import { BookOpen, Search, FileText, ArrowUpRight, CheckCircle2, ShieldAlert } from 'lucide-react';

export const ResearchCorpusExplorer: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredPapers = RESEARCH_PAPERS.filter(p =>
    p.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.citation.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.core_mechanism.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '20px' }}>Academic Research Review & 20-Paper Synthesis Matrix</h2>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            Foundational Literature Deconstruction: Mechanisms Extracted vs Enterprise Vulnerabilities Resolved
          </p>
        </div>

        <div style={{ position: 'relative', width: '320px' }}>
          <Search size={15} style={{ position: 'absolute', left: '12px', top: '10px', color: 'var(--text-muted)' }} />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search papers, citations, concepts..."
            style={{
              width: '100%',
              padding: '8px 12px 8px 36px',
              background: 'rgba(255,255,255,0.06)',
              border: '1px solid var(--border-glass)',
              borderRadius: '20px',
              color: '#fff',
              fontSize: '12px'
            }}
          />
        </div>
      </div>

      {/* Grid of 20 Research Papers */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(460px, 1fr))', gap: '16px' }}>
        {filteredPapers.map((paper) => (
          <div
            key={paper.id}
            className="glass-panel"
            style={{
              padding: '20px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between'
            }}
          >
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                <span className="badge badge-teal">Paper #{paper.id}</span>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                  {paper.filename}
                </span>
              </div>

              <h3 style={{ fontSize: '15px', color: '#fff', marginBottom: '4px' }}>{paper.title}</h3>
              <div style={{ fontSize: '12px', color: 'var(--blue-accent)', marginBottom: '12px', fontWeight: 600 }}>
                {paper.citation}
              </div>

              <div style={{ background: 'rgba(0,0,0,0.25)', padding: '10px', borderRadius: '8px', fontSize: '12px', marginBottom: '12px', lineHeight: '1.5' }}>
                <strong style={{ color: 'var(--text-secondary)' }}>Core Mechanism: </strong>
                <span style={{ color: '#fff' }}>{paper.core_mechanism}</span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '14px' }}>
                <div style={{ background: 'rgba(16, 185, 129, 0.08)', border: '1px solid rgba(16, 185, 129, 0.2)', padding: '10px', borderRadius: '6px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', fontWeight: 700, color: 'var(--green-success)', marginBottom: '4px' }}>
                    <CheckCircle2 size={13} />
                    WHAT WE EXTRACT
                  </div>
                  <p style={{ fontSize: '11px', color: 'var(--text-primary)', lineHeight: '1.4' }}>
                    {paper.what_we_extract}
                  </p>
                </div>

                <div style={{ background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.2)', padding: '10px', borderRadius: '6px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', fontWeight: 700, color: '#F87171', marginBottom: '4px' }}>
                    <ShieldAlert size={13} />
                    WHAT WE FIX
                  </div>
                  <p style={{ fontSize: '11px', color: 'var(--text-primary)', lineHeight: '1.4' }}>
                    {paper.what_we_fix}
                  </p>
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border-glass)', paddingTop: '10px', fontSize: '11px', color: 'var(--text-muted)' }}>
              <span>Archived in <code>research_papers/</code></span>
              <span style={{ color: 'var(--teal-light)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                Full PDF Available <ArrowUpRight size={12} />
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
