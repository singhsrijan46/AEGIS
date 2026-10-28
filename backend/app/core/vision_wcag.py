"""
Deterministic Multimodal Computer Vision & Accessibility Engine (Step 3 Deliverable)
Implements:
1. Deterministic CIELAB ΔE00 color distance against brand palette (threshold < 2.0).
2. WCAG 2.1 Mathematical Contrast Ratio (CR = (L1 + 0.05) / (L2 + 0.05)).
3. Logo exclusion zone clearance buffer (M >= 0.5 * H_logo) and aspect ratio distortion checks.
Synthesized from: LayoutLMv3 [13], DocOwl 1.5 [14], ScreenAI [15], OpenCV colorimetry.
"""

import math
from typing import List, Dict, Any, Tuple, Optional
from ..models.schemas import VisualAssetInput, VisualFinding


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    hex_clean = hex_str.lstrip('#')
    if len(hex_clean) == 3:
        hex_clean = "".join([c*2 for c in hex_clean])
    return int(hex_clean[0:2], 16), int(hex_clean[2:4], 16), int(hex_clean[4:6], 16)


def rgb_to_xyz(r: int, g: int, b: int) -> Tuple[float, float, float]:
    # Gamma expansion for sRGB
    def pivot(c: float) -> float:
        c = c / 255.0
        return ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92

    r_lin = pivot(r) * 100.0
    g_lin = pivot(g) * 100.0
    b_lin = pivot(b) * 100.0

    # sRGB to D65 XYZ matrix
    x = r_lin * 0.4124564 + g_lin * 0.3575761 + b_lin * 0.1804375
    y = r_lin * 0.2126729 + g_lin * 0.7151522 + b_lin * 0.0721750
    z = r_lin * 0.0193339 + g_lin * 0.1191920 + b_lin * 0.9503041
    return x, y, z


def xyz_to_lab(x: float, y: float, z: float) -> Tuple[float, float, float]:
    # D65 standard reference white
    xn, yn, zn = 95.047, 100.000, 108.883

    def f(t: float) -> float:
        return t ** (1.0 / 3.0) if t > 0.008856 else (7.787 * t) + (16.0 / 116.0)

    fx = f(x / xn)
    fy = f(y / yn)
    fz = f(z / zn)

    L = (116.0 * fy) - 16.0
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)
    return L, a, b


def hex_to_lab(hex_str: str) -> Tuple[float, float, float]:
    r, g, b = hex_to_rgb(hex_str)
    x, y, z = rgb_to_xyz(r, g, b)
    return xyz_to_lab(x, y, z)


def calculate_ciede2000(lab1: Tuple[float, float, float], lab2: Tuple[float, float, float]) -> float:
    """
    Standard CIEDE2000 (ΔE00) perceptual color difference formula.
    """
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2

    avg_L = (L1 + L2) / 2.0
    C1 = math.sqrt(a1**2 + b1**2)
    C2 = math.sqrt(a2**2 + b2**2)
    avg_C = (C1 + C2) / 2.0

    G = 0.5 * (1.0 - math.sqrt((avg_C**7) / (avg_C**7 + 25**7 + 1e-9)))
    a1_prime = (1.0 + G) * a1
    a2_prime = (1.0 + G) * a2

    C1_prime = math.sqrt(a1_prime**2 + b1**2)
    C2_prime = math.sqrt(a2_prime**2 + b2**2)
    avg_C_prime = (C1_prime + C2_prime) / 2.0

    h1_prime = math.atan2(b1, a1_prime) % (2 * math.pi)
    h2_prime = math.atan2(b2, a2_prime) % (2 * math.pi)

    if C1_prime == 0 or C2_prime == 0:
        avg_h_prime = h1_prime + h2_prime
    elif abs(h1_prime - h2_prime) <= math.pi:
        avg_h_prime = (h1_prime + h2_prime) / 2.0
    elif (h1_prime + h2_prime) < 2 * math.pi:
        avg_h_prime = (h1_prime + h2_prime + 2 * math.pi) / 2.0
    else:
        avg_h_prime = (h1_prime + h2_prime - 2 * math.pi) / 2.0

    T = (1.0 - 0.17 * math.cos(avg_h_prime - math.radians(30))
         + 0.24 * math.cos(2 * avg_h_prime)
         + 0.32 * math.cos(3 * avg_h_prime + math.radians(6))
         - 0.20 * math.cos(4 * avg_h_prime - math.radians(63)))

    delta_h_prime = h2_prime - h1_prime
    if abs(delta_h_prime) > math.pi:
        if h2_prime <= h1_prime:
            delta_h_prime += 2 * math.pi
        else:
            delta_h_prime -= 2 * math.pi

    delta_L_prime = L2 - L1
    delta_C_prime = C2_prime - C1_prime
    delta_H_prime = 2.0 * math.sqrt(C1_prime * C2_prime) * math.sin(delta_h_prime / 2.0)

    S_L = 1.0 + ((0.015 * (avg_L - 50.0)**2) / math.sqrt(20.0 + (avg_L - 50.0)**2))
    S_C = 1.0 + 0.045 * avg_C_prime
    S_H = 1.0 + 0.015 * avg_C_prime * T

    delta_theta = math.radians(30) * math.exp(-(((math.degrees(avg_h_prime) - 275) / 25.0)**2))
    R_C = 2.0 * math.sqrt((avg_C_prime**7) / (avg_C_prime**7 + 25**7 + 1e-9))
    R_T = -math.sin(2 * delta_theta) * R_C

    delta_e = math.sqrt(
        (delta_L_prime / S_L)**2 +
        (delta_C_prime / S_C)**2 +
        (delta_H_prime / S_H)**2 +
        R_T * (delta_C_prime / S_C) * (delta_H_prime / S_H)
    )
    return delta_e


def calculate_relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """
    WCAG 2.1 Relative Luminance formula.
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    """
    def channel_lum(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4

    r_lum = channel_lum(rgb[0])
    g_lum = channel_lum(rgb[1])
    b_lum = channel_lum(rgb[2])
    return 0.2126 * r_lum + 0.7152 * g_lum + 0.0722 * b_lum


def calculate_wcag_contrast_ratio(hex1: str, hex2: str) -> float:
    """
    WCAG 2.1 Contrast Ratio = (L1 + 0.05) / (L2 + 0.05) where L1 is lighter.
    """
    lum1 = calculate_relative_luminance(hex_to_rgb(hex1))
    lum2 = calculate_relative_luminance(hex_to_rgb(hex2))

    l_lighter = max(lum1, lum2)
    l_darker = min(lum1, lum2)

    return (l_lighter + 0.05) / (l_darker + 0.05)


class MultimodalVisualAuditor:
    def __init__(self, official_palette: Dict[str, str], logo_constraints: Dict[str, Any]):
        self.official_palette = official_palette
        self.logo_constraints = logo_constraints

    def audit_asset(self, asset: VisualAssetInput) -> List[VisualFinding]:
        findings = []

        # 1. CIELAB ΔE00 Color Verification for Dominant Hexes
        for hex_code in asset.dominant_hexes:
            lab_test = hex_to_lab(hex_code)
            min_delta_e = float('inf')
            closest_brand_swatch = None

            for swatch_name, swatch_hex in self.official_palette.items():
                lab_swatch = hex_to_lab(swatch_hex)
                delta_e = calculate_ciede2000(lab_test, lab_swatch)
                if delta_e < min_delta_e:
                    min_delta_e = delta_e
                    closest_brand_swatch = (swatch_name, swatch_hex)

            # Check if this color attempted to be a brand color but drifted
            # If 2.0 < ΔE < 12.0, it's an unauthorized variation of an official brand color
            if 2.0 < min_delta_e < 12.0 and closest_brand_swatch:
                findings.append(VisualFinding(
                    asset_id=asset.id,
                    check_type="COLOR_DELTA_E",
                    severity="WARNING",
                    title=f"Brand Color Drift: Hex '{hex_code}' (ΔE = {min_delta_e:.2f})",
                    explanation=(
                        f"Detected color '{hex_code}' deviates from official {closest_brand_swatch[0]} "
                        f"('{closest_brand_swatch[1]}') with a CIELAB perceptual distance of ΔE00 = {min_delta_e:.2f}. "
                        f"Corporate brand standard requires ΔE00 < 2.0 for visually imperceptible fidelity."
                    ),
                    measured_value=round(min_delta_e, 2),
                    threshold_value=2.0,
                    passed=False,
                    citation="AEGIS Design System & Token Specifications, Section 1.2: Brand Colors, Page 8",
                    suggestion=f"Snap to official brand hex: {closest_brand_swatch[1]}"
                ))

        # 2. WCAG 2.1 Contrast Ratio Audit
        if asset.text_color_hex and asset.background_color_hex:
            contrast_ratio = calculate_wcag_contrast_ratio(asset.text_color_hex, asset.background_color_hex)
            min_required = 4.5  # WCAG AA for normal body text
            if contrast_ratio < min_required:
                findings.append(VisualFinding(
                    asset_id=asset.id,
                    check_type="WCAG_CONTRAST",
                    severity="BLOCKER",
                    title=f"WCAG 2.1 AA Contrast Failure ({contrast_ratio:.2f}:1 < 4.5:1)",
                    explanation=(
                        f"Text overlay '{asset.text_color_hex}' against background '{asset.background_color_hex}' "
                        f"yields a contrast ratio of {contrast_ratio:.2f}:1, failing the mandatory WCAG 2.1 AA "
                        f"minimum threshold of 4.5:1. This exposes the organization to ADA Title III litigation."
                    ),
                    measured_value=round(contrast_ratio, 2),
                    threshold_value=min_required,
                    passed=False,
                    citation="Digital Accessibility Guidelines (ADA Title III & WCAG 2.1), Section 2, Page 12",
                    suggestion="Darken background or brighten text to exceed 4.5:1 contrast."
                ))

        # 3. Logo Exclusion Safe-Zone Buffer and Aspect Ratio Check
        if asset.has_logo and asset.logo_bbox:
            # bbox: [x, y, w, h]
            lx, ly, lw, lh = asset.logo_bbox
            # Clear space margin M = 0.5 * lh
            m = 0.5 * lh
            target_ar = self.logo_constraints.get("allowed_aspect_ratio", 3.2)
            actual_ar = lw / max(1, lh)
            ar_drift = abs(actual_ar - target_ar) / target_ar

            # Aspect Ratio distortion
            if ar_drift > self.logo_constraints.get("max_aspect_ratio_drift", 0.05):
                findings.append(VisualFinding(
                    asset_id=asset.id,
                    check_type="LOGO_ASPECT_RATIO",
                    severity="BLOCKER",
                    title=f"Logo Aspect Ratio Distortion ({actual_ar:.2f} vs {target_ar:.2f})",
                    explanation=(
                        f"The logo width-to-height aspect ratio is distorted by {ar_drift*100:.1f}%. "
                        f"Official brand logo aspect ratio must strictly be maintained at {target_ar:.2f}:1 "
                        f"without horizontal or vertical stretching."
                    ),
                    measured_value=round(actual_ar, 2),
                    threshold_value=target_ar,
                    passed=False,
                    citation="AEGIS-Brand™ Global Governance & Defense Standard v4.0, Section 1.4: Logo Geometry, Page 14",
                    suggestion=f"Constrain logo scaling proportions to {target_ar:.2f}:1.",
                    bounding_box=asset.logo_bbox
                ))

            # Buffer Clearance check: Ensure logo isn't placed within margin M of asset edge
            if lx < m or ly < m or (lx + lw + m) > asset.width or (ly + lh + m) > asset.height:
                findings.append(VisualFinding(
                    asset_id=asset.id,
                    check_type="LOGO_SAFE_ZONE",
                    severity="WARNING",
                    title="Logo Clear-Space Margin Encroachment",
                    explanation=(
                        f"The logo bounding box [{lx}, {ly}, {lw}, {lh}] violates the 0.5H ({m:.1f}px) "
                        f"mandatory exclusion buffer from the asset boundaries. No text or border may encroach."
                    ),
                    measured_value=round(min(lx, ly, asset.width - (lx + lw), asset.height - (ly + lh)), 1),
                    threshold_value=round(m, 1),
                    passed=False,
                    citation="AEGIS-Brand™ Global Governance & Defense Standard v4.0, Section 1.5: Logo Protection Clear Space, Page 15",
                    suggestion=f"Provide at least {m:.1f}px margin around all 4 sides of the logo.",
                    bounding_box=[int(lx - m), int(ly - m), int(lw + 2*m), int(lh + 2*m)]
                ))

        # 4. Alt-Text Accessibility Audit
        if not asset.has_alt_text or len(asset.alt_text.strip()) < 10:
            suggested_alt = (
                f"Marketing graphic for AEGIS-Brand showing automated enterprise governance and "
                f"multimodal content verification features."
            )
            findings.append(VisualFinding(
                asset_id=asset.id,
                check_type="ALT_TEXT",
                severity="BLOCKER",
                title="Missing / Inadequate Image Alt-Text",
                explanation=(
                    "Asset is missing screen-reader accessible alt-text or has an inadequate placeholder. "
                    "WCAG 2.1 Guideline 1.1.1 requires descriptive non-text content alternatives."
                ),
                measured_value=float(len(asset.alt_text.strip())),
                threshold_value=10.0,
                passed=False,
                citation="Digital Accessibility Guidelines (WCAG 2.1 Guideline 1.1.1: Non-Text Content)",
                suggestion=f"Insert screen-reader alt text: '{suggested_alt}'"
            ))

        return findings
