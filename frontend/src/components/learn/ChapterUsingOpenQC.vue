<script setup>
</script>

<template>
  <div class="learn-content">
    <h1>Chapter 6: Using OpenQC — Step by Step</h1>
    <p class="chapter-subtitle">Detailed walkthroughs for every module in the application.</p>

    <h2>QC Monitor Walkthrough</h2>
    <p>
      The QC Monitor is the core module of OpenQC. It accepts raw QC data files, performs Westgard rule evaluation,
      generates Levey-Jennings charts, and produces QC reports.
    </p>

    <h3>Step 1: Upload an Excel File</h3>
    <p>
      Navigate to <strong>QC Monitor</strong> from the sidebar. You will see a file upload area at the top of the page.
    </p>
    <ul>
      <li>Click the upload area or drag and drop a file onto it.</li>
      <li><strong>Supported formats:</strong> <code>.xlsx</code> (Excel) files exported from PCR instruments such as QuantStudio, Bio-Rad CFX, Roche LightCycler, or similar platforms.</li>
      <li>The file must contain columns for sample identifiers and Ct values. OpenQC automatically detects common column naming conventions.</li>
      <li><strong>Example file to use:</strong> <code>sample_qc_quantstudio.xlsx</code> from the sample data directory.</li>
    </ul>

    <h3>Step 2: Fill in Metadata</h3>
    <p>
      After selecting a file, fill in the metadata fields:
    </p>
    <ul>
      <li><strong>Instrument:</strong> The PCR instrument used (e.g., "QuantStudio 5", "CFX96"). This is recorded in the audit trail and helps filter runs later.</li>
      <li><strong>Assay:</strong> The name of the PCR assay (e.g., "SARS-CoV-2 RT-PCR", "HIV-1 Viral Load").</li>
      <li><strong>Channel:</strong> The fluorescence channel / reporter dye (e.g., "FAM", "VIC", "ROX").</li>
      <li><strong>Reagent Lot ID:</strong> The lot number of the PCR reagent kit. Critical for tracking lot-to-lot variation.</li>
      <li><strong>Control Lot ID:</strong> The lot number of the QC control material.</li>
    </ul>

    <div class="info-box">
      <strong>Tip:</strong> Metadata fields are optional but strongly recommended. They enable filtering and grouping
      in the Dashboard and are included in QC reports and the audit trail.
    </div>

    <h3>Step 3: Click Upload and Analyze</h3>
    <p>
      Click the upload button to submit the file. OpenQC will:
    </p>
    <ol>
      <li>Parse the Excel file and extract Ct values for each control level.</li>
      <li>Calculate summary statistics (mean, SD, CV) from the data.</li>
      <li>Evaluate all six Westgard rules against the data points.</li>
      <li>Generate the Levey-Jennings chart.</li>
      <li>Record the upload and analysis in the audit trail.</li>
    </ol>
    <p>
      The analysis typically completes within a few seconds. A progress indicator shows the current status.
    </p>

    <h3>Step 4: Read the Levey-Jennings Chart</h3>
    <p>
      After analysis, the Levey-Jennings chart is displayed below the upload area. The chart shows:
    </p>
    <ul>
      <li><strong>Data points:</strong> Each dot represents a QC measurement plotted against the run number (x-axis) and Ct value (y-axis).</li>
      <li><strong>Center line:</strong> The established mean Ct value.</li>
      <li><strong>SD lines:</strong> Horizontal lines at +/-1SD, +/-2SD, and +/-3SD from the mean.</li>
      <li><strong>Color coding:</strong> Points within acceptable limits are shown in the default color. Points triggering warnings or violations are highlighted.</li>
    </ul>

    <h3>Step 5: Interpret Violations</h3>
    <p>
      Below the chart, the Violations Table lists any Westgard rule violations detected:
    </p>
    <ul>
      <li>Each row shows the rule violated, the data point(s) involved, the control level, and the severity (warning or reject).</li>
      <li>Warning violations (1-2s) indicate points to monitor but do not require rejection.</li>
      <li>Reject violations (1-3s, 2-2s, R-4s, 4-1s, 10x) indicate the run should not be reported without investigation.</li>
    </ul>
    <p>
      <strong>Expected results with sample file:</strong> Using <code>sample_qc_quantstudio.xlsx</code>, you should
      see a set of QC data points with summary statistics calculated. The data is designed to demonstrate a clean
      dataset with all points within acceptable limits.
    </p>
    <p>
      To see violations in action, use <code>sample_qc_violations.xlsx</code>, which contains intentional outliers
      that trigger various Westgard rules.
    </p>

    <h3>Step 6: Export QC Report</h3>
    <p>
      Click the Export button in the page header to generate a QC report. The report includes:
    </p>
    <ul>
      <li>Summary statistics (mean, SD, CV) for each control level.</li>
      <li>The Levey-Jennings chart.</li>
      <li>A list of all Westgard violations.</li>
      <li>Run metadata (instrument, assay, lot numbers).</li>
      <li>Timestamp and audit trail reference.</li>
    </ul>

    <h2>Sigma Analysis Walkthrough</h2>
    <p>
      The Sigma Analysis module calculates the Sigma metric for your assays and recommends appropriate QC strategies.
    </p>

    <h3>Step 1: Enter Assay Parameters</h3>
    <p>
      Navigate to <strong>Sigma Analysis</strong> from the sidebar. Enter the following values for each assay:
    </p>
    <ul>
      <li><strong>TEa (Total Allowable Error):</strong> The quality requirement for the analyte, expressed as a percentage. Source this from CLIA, biological variation databases, or manufacturer claims.</li>
      <li><strong>Bias:</strong> The systematic error of the method, expressed as a percentage. Obtain from proficiency testing or method comparison studies.</li>
      <li><strong>CV (Coefficient of Variation):</strong> The imprecision of the method, expressed as a percentage. Calculate from your QC data (at least 20 data points).</li>
    </ul>

    <div class="info-box">
      <strong>Example values to try:</strong> TEa = 15%, Bias = 2.5%, CV = 3.0%. This should yield a Sigma of
      approximately 4.2 (Good performance).
    </div>

    <h3>Step 2: Click Calculate</h3>
    <p>
      Click the Calculate button. OpenQC applies the Sigma formula: <code>sigma = (TEa - |Bias|) / CV</code>.
    </p>

    <h3>Step 3: Read the Results Table</h3>
    <p>
      The results table displays:
    </p>
    <ul>
      <li>The calculated Sigma value.</li>
      <li>The performance classification (World Class, Excellent, Good, Marginal, Poor, or Unacceptable).</li>
      <li>The recommended QC rules and number of controls based on the Sigma level.</li>
    </ul>

    <h3>Step 4: Interpret the NMEDx Chart</h3>
    <p>
      The NMEDx (Normalized Method Decision) chart plots your assay's performance:
    </p>
    <ul>
      <li>The x-axis represents imprecision (CV) normalized to TEa.</li>
      <li>The y-axis represents bias normalized to TEa.</li>
      <li>Colored bands show the Sigma zones (World Class through Unacceptable).</li>
      <li>Your assay appears as a point on the chart — its position tells you immediately how much safety margin exists.</li>
    </ul>

    <h3>Step 5: Follow Recommended QC Rules</h3>
    <p>
      Based on the calculated Sigma value, OpenQC recommends a QC strategy:
    </p>
    <ul>
      <li>Which Westgard rules to apply.</li>
      <li>How many controls to run per batch (N=2 or N=4).</li>
      <li>Whether the current method performance is adequate or needs improvement.</li>
    </ul>

    <h2>Validation Walkthrough</h2>
    <p>
      The Validation module guides you through assay validation studies with statistical analysis and reporting.
    </p>

    <h3>Step 1: Select Validation Type</h3>
    <p>
      Navigate to <strong>Validation</strong> from the sidebar. Choose the type of validation study:
    </p>
    <ul>
      <li><strong>LOD (Limit of Detection):</strong> For determining the lowest detectable concentration.</li>
      <li><strong>Precision:</strong> For assessing intra-run and inter-run variability.</li>
      <li><strong>Linearity:</strong> For verifying the reportable range and amplification efficiency.</li>
    </ul>

    <h3>Step 2: Upload Dataset</h3>
    <p>
      Upload an Excel file containing your validation data:
    </p>
    <ul>
      <li><strong>For LOD:</strong> Use <code>sample_validation_lod.xlsx</code>. The file should contain replicate measurements at multiple low concentrations.</li>
      <li><strong>For Linearity:</strong> Use <code>sample_validation_linearity.xlsx</code>. The file should contain measurements across a serial dilution series.</li>
    </ul>

    <h3>Step 3: Define Acceptance Criteria</h3>
    <p>
      Set the acceptance criteria for your study:
    </p>
    <ul>
      <li>For LOD: detection rate threshold (typically 95%).</li>
      <li>For Precision: maximum acceptable CV (typically 5% intra-run, 10% inter-run).</li>
      <li>For Linearity: minimum R<sup>2</sup> (typically 0.99) and acceptable slope range.</li>
    </ul>

    <h3>Step 4: Run Validation</h3>
    <p>
      Click the validate button. OpenQC performs the appropriate statistical analysis based on the selected study type.
    </p>

    <h3>Step 5: Interpret Results</h3>
    <p>
      The results section displays:
    </p>
    <ul>
      <li>Calculated statistics (LOD value, CV values, R<sup>2</sup>, slope, etc.).</li>
      <li>Pass/fail determination against your acceptance criteria.</li>
      <li>Visualizations (scatter plots for linearity, distribution plots for precision).</li>
      <li>A downloadable validation report.</li>
    </ul>

    <h2>Lot Registry Walkthrough</h2>
    <p>
      The Lot Registry tracks reagent and control material lots, enabling traceability and lot-to-lot comparison.
    </p>
    <ol>
      <li>Navigate to <strong>Lot Registry</strong> from the sidebar.</li>
      <li>Click to add a new lot entry.</li>
      <li>Enter the lot details: lot number, material type (reagent or control), manufacturer, expiration date, and any notes.</li>
      <li>Save the entry. It will appear in the registry table.</li>
      <li>When uploading QC data, reference the lot ID to link runs to specific lots.</li>
      <li>Use the registry to track when lots change and correlate lot transitions with QC performance shifts.</li>
    </ol>

    <h2>Audit Trail Walkthrough</h2>
    <p>
      The Audit Trail provides a tamper-evident record of all system activities.
    </p>
    <ol>
      <li>Navigate to <strong>Audit Trail</strong> from the sidebar.</li>
      <li>The main view shows a chronological list of all actions (uploads, analyses, exports, configuration changes).</li>
      <li>Each entry shows the timestamp, user, action type, and details.</li>
      <li>Use the filter options to narrow by date range, action type, or user.</li>
      <li>Click <strong>Verify Integrity</strong> to run the hash chain verification. The system will confirm whether the entire audit trail is intact or identify any broken links.</li>
      <li>Use the export function to generate audit trail reports for regulatory review.</li>
    </ol>

    <div class="warning-box">
      <strong>Note:</strong> The audit trail is append-only. Entries cannot be edited or deleted through the
      application interface. This is by design — regulatory requirements mandate that audit records be immutable.
    </div>

    <h2>Regulatory Assistant Walkthrough</h2>
    <p>
      The Regulatory Assistant uses AI to help answer regulatory and compliance questions relevant to clinical
      laboratory QC.
    </p>

    <h3>Prerequisites</h3>
    <ul>
      <li>An API key must be configured in <strong>Settings</strong> before the Regulatory Assistant can be used.</li>
      <li>Navigate to Settings, find the API key configuration section, and enter your key.</li>
    </ul>

    <h3>Using the Assistant</h3>
    <ol>
      <li>Navigate to <strong>Regulatory</strong> from the sidebar.</li>
      <li>Type your question in the input area. Examples:
        <ul>
          <li>"What are the QC requirements under ISO 15189:2022?"</li>
          <li>"How often should QC be run according to CLIA?"</li>
          <li>"What documentation is needed for CDSCO IVD registration?"</li>
        </ul>
      </li>
      <li>The assistant provides responses grounded in regulatory standards and laboratory best practices.</li>
      <li>Use the responses as a starting point for your compliance documentation — always verify against the primary regulatory text.</li>
    </ol>

    <div class="info-box">
      <strong>Disclaimer:</strong> The Regulatory Assistant is a reference tool, not a substitute for professional
      regulatory consultation. Always verify critical compliance decisions with your quality manager and regulatory
      affairs team.
    </div>
  </div>
</template>
