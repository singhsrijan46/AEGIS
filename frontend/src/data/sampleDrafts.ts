export interface SampleDraft {
  id: string;
  title: string;
  author: string;
  department: string;
  text: string;
  description: string;
}

export const SAMPLE_DRAFTS: SampleDraft[] = [
  {
    id: "draft-press-release",
    title: "Q4 Enterprise SaaS Launch Press Release",
    author: "Dave Morrison (Growth Marketing)",
    department: "Content Marketing",
    description: "Contains multiple failure modes: banned 'cheap', missing ™ trademark, 99.999% SLA hallucination, false FedRAMP High security clearance, and arithmetic conversion error.",
    text: `Inkloom Verity is cheap and simple to deploy across distributed teams. It is the only platform delivering guaranteed 10X ROI and FedRAMP High certification with an unprecedented 99.999% uptime guarantee.

Early customer benchmarks show we increased conversions by 310% from 2.1% to 6.5% within 30 days. For pricing details on our $49/month tier or Project Titan deployment, contact enterprise@inkloom.internal.`
  },
  {
    id: "draft-outbound-campaign",
    title: "Outbound Growth Campaign & LinkedIn Ad",
    author: "Jessica Reed (Agency Contractor)",
    department: "External Creative Agencies",
    description: "Promotional hype with colloquial buzzwords ('ninja', 'game changer'), outdated $49 pricing, and unsubstantiated absolute superlatives ('the only').",
    text: `Looking for a rockstar solution to scale your content? Inkloom Verity is a game changer for modern growth marketers. 

Our ninja engineering team built the only brand protection tool that guarantees flawless copy for under $49/month. Join thousands of high-velocity teams who refuse to let outdated governance slow them down.`
  },
  {
    id: "draft-compliant-casestudy",
    title: "Enterprise Brand Governance Benchmark Report",
    author: "Elena Rostova (Head of Brand & Legal)",
    department: "Brand & Legal Stewardship",
    description: "Fully compliant draft aligning with official Brand Constitution, active SOC 2 Type II attestation, and audited 99.95% SLA. Achieves GREEN TIER with SHA-256 certificate.",
    text: `Inkloom Verity™ delivers cost-effective enterprise brand governance with an audited 99.95% contractual uptime SLA. 

Operating within an air-gapped, zero-data-retention VPC architecture, our SOC 2 Type II certified platform empowers distributed marketing departments to accelerate pre-publication reviews from days to under four hours. Audited enterprise case studies demonstrate an average 31% conversion uplift across active customer deployments.`
  }
];
