"""Report generation engine -- renders HTML templates to PDF via WeasyPrint."""
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "utils" / "pdf_templates"
_jinja_env = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)), autoescape=True)

try:
    from weasyprint import HTML as WeasyHTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False


def render_html(template_name: str, context: dict) -> str:
    """Render an HTML template with the given context."""
    template = _jinja_env.get_template(template_name)
    context.setdefault("generated_at", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
    return template.render(**context)


def render_pdf(template_name: str, context: dict) -> bytes:
    """Render an HTML template to PDF bytes.

    Raises ImportError if WeasyPrint is not installed.
    """
    if not WEASYPRINT_AVAILABLE:
        raise ImportError(
            "WeasyPrint is required for PDF generation. Install with: pip install weasyprint"
        )
    html_str = render_html(template_name, context)
    return WeasyHTML(string=html_str).write_pdf()


def generate_qc_report(run_data: dict, analysis_data: dict) -> bytes:
    """Generate QC run report PDF.

    Args:
        run_data: dict with run metadata (id, assay, instrument, file_name, file_hash, etc.)
        analysis_data: dict with run_status, first_reject_rule, violations, summary_stats,
                       evaluated_points
    """
    context = {
        "run_id": run_data.get("id", ""),
        "assay": run_data.get("assay", ""),
        "instrument": run_data.get("instrument", ""),
        "uploaded_at": run_data.get("uploaded_at", ""),
        "reagent_lot_id": run_data.get("reagent_lot_id"),
        "control_lot_id": run_data.get("control_lot_id"),
        "file_name": run_data.get("file_name", ""),
        "file_hash": run_data.get("file_hash", ""),
        "run_status": analysis_data.get("run_status", "pass"),
        "first_reject_rule": analysis_data.get("first_reject_rule"),
        "violations": analysis_data.get("violations", []),
        "summary_stats": analysis_data.get("summary_stats", {}),
        "data_points": analysis_data.get("evaluated_points", []),
    }
    return render_pdf("qc_report.html", context)


def generate_validation_report(validation_data: dict) -> bytes:
    """Generate validation report PDF."""
    return render_pdf("validation_report.html", validation_data)


def generate_sigma_report(sigma_results: list[dict]) -> bytes:
    """Generate Sigma report PDF."""
    context = {
        "results": sigma_results,
        "assay_count": len(sigma_results),
    }
    return render_pdf("sigma_report.html", context)


def generate_audit_report(entries: list[dict], chain_verification: dict) -> bytes:
    """Generate audit trail report PDF."""
    context = {
        "entries": entries,
        "total_entries": len(entries),
        "chain_verification": chain_verification,
    }
    return render_pdf("audit_report.html", context)
