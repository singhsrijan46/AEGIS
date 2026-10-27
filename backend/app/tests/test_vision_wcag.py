import pytest
from backend.app.core.vision_wcag import (
    hex_to_rgb,
    calculate_wcag_contrast_ratio,
    calculate_ciede2000,
    hex_to_lab,
    MultimodalVisualAuditor
)
from backend.app.models.schemas import VisualAssetInput
from backend.app.core.brand_vault import BrandVault


def test_wcag_contrast_ratio():
    # White on Black: (1.0 + 0.05) / (0.0 + 0.05) = 21:1
    white = "#FFFFFF"
    black = "#000000"
    ratio = calculate_wcag_contrast_ratio(white, black)
    assert ratio >= 20.9

    # Poor contrast: Light gray (#AAAAAA) on White (#FFFFFF)
    poor_ratio = calculate_wcag_contrast_ratio("#AAAAAA", "#FFFFFF")
    assert poor_ratio < 4.5  # Fails WCAG AA


def test_cielab_color_difference():
    # Exact same color has ΔE = 0
    teal = "#00A896"
    lab1 = hex_to_lab(teal)
    lab2 = hex_to_lab(teal)
    assert calculate_ciede2000(lab1, lab2) == 0.0

    # Slight drift (#00B5A2)
    lab_drift = hex_to_lab("#00B5A2")
    delta_e = calculate_ciede2000(lab1, lab_drift)
    assert delta_e > 0.0


def test_visual_auditor_flags():
    vault = BrandVault()
    auditor = MultimodalVisualAuditor(vault.official_palette, vault.logo_constraints)

    bad_asset = VisualAssetInput(
        filename="promo_banner.png",
        width=1200,
        height=630,
        dominant_hexes=["#00B8A5"],  # Drifted teal (~3-4 ΔE)
        has_logo=True,
        logo_bbox=[10, 10, 320, 100],  # Violates 0.5H (50px) margin from edge (10px < 50px)
        has_alt_text=False,
        alt_text="",
        text_color_hex="#888888",
        background_color_hex="#999999"  # Low contrast
    )

    findings = auditor.audit_asset(bad_asset)
    types = {f.check_type for f in findings}
    assert "COLOR_DELTA_E" in types
    assert "WCAG_CONTRAST" in types
    assert "LOGO_SAFE_ZONE" in types
    assert "ALT_TEXT" in types
