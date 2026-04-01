/**
 * Print the current page as a PDF report.
 * Temporarily injects a print header with report metadata,
 * triggers window.print(), then cleans up.
 */
export function printReport({ title, subtitle, generatedAt } = {}) {
  const header = document.createElement('div')
  header.className = 'print-report-header'
  header.innerHTML = `
    <div class="print-report-header__logo">OpenQC Report</div>
    <h1 class="print-report-header__title">${title || document.title}</h1>
    ${subtitle ? `<p class="print-report-header__subtitle">${subtitle}</p>` : ''}
    <p class="print-report-header__meta">Generated: ${generatedAt || new Date().toLocaleString()} | OpenQC Laboratory QC Platform</p>
    <hr class="print-report-header__divider" />
  `
  document.body.prepend(header)

  window.print()

  // Clean up after print dialog closes
  setTimeout(() => header.remove(), 500)
}
