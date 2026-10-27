"""
Cryptographic Audit Ledger (Step 5 Deliverable)
Produces immutable SHA-256 compliance verification certificates for FTC / SEC audit defensibility.
"""

import hashlib
import time
from typing import List, Dict, Any, Optional
from ..models.schemas import CryptographicCertificate


class CryptographicAuditLedger:
    def __init__(self):
        self.certificates: List[CryptographicCertificate] = []

    def issue_certificate(self, document_id: str, text: str, score: float, tier: str, status: str) -> CryptographicCertificate:
        """
        Computes SHA-256 fingerprint over document content + audit metadata.
        """
        ts = time.time()
        raw_payload = f"{document_id}:{ts}:{score}:{tier}:{text}"
        sha256_hash = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()
        token = f"VERITY-CERT-{sha256_hash[:16].upper()}"

        cert = CryptographicCertificate(
            token=token,
            document_id=document_id,
            sha256_hash=sha256_hash,
            timestamp=ts,
            compliance_score=score,
            tier=tier,
            status=status
        )
        self.certificates.append(cert)
        return cert

    def verify_token(self, token: str) -> Optional[CryptographicCertificate]:
        for cert in self.certificates:
            if cert.token == token:
                return cert
        return None

    def get_all_certificates(self) -> List[CryptographicCertificate]:
        return self.certificates
