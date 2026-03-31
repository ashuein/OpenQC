<script setup>
</script>

<template>
  <div class="learn-content">
    <h1>Chapter 8: Designing Experiments &amp; Generating Reports</h1>
    <p class="chapter-subtitle">A practical guide for laboratory scientists using OpenQC.</p>

    <!-- ============================================================ -->
    <!-- Section 1: Planning Your QC Program                          -->
    <!-- ============================================================ -->
    <h2>1. Planning Your QC Program</h2>
    <p>
      A well-designed QC program begins before the first control is measured. The decisions you make during the
      planning phase determine whether your QC system will reliably detect clinically significant errors or
      generate noise that obscures real problems.
    </p>

    <h3>How Many Control Levels Do You Need?</h3>
    <p>
      At a minimum, run <strong>two control levels</strong> per analytical run: a low positive and a high positive.
      Two levels allow you to apply multi-rule Westgard evaluation (including the R-4s rule, which requires two
      levels). A third mid-range level improves error detection across the full reportable range and is recommended
      for quantitative assays.
    </p>
    <table>
      <thead>
        <tr>
          <th>Control Levels</th>
          <th>Use Case</th>
          <th>Westgard Rules Available</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1 level</td>
          <td>Qualitative assays only</td>
          <td>1-2s, 1-3s only</td>
        </tr>
        <tr>
          <td>2 levels (recommended minimum)</td>
          <td>Quantitative assays</td>
          <td>All six rules (1-2s, 1-3s, 2-2s, R-4s, 4-1s, 10x)</td>
        </tr>
        <tr>
          <td>3 levels</td>
          <td>High-volume quantitative assays</td>
          <td>All rules with improved sensitivity across the range</td>
        </tr>
      </tbody>
    </table>

    <h3>How Often to Run Controls</h3>
    <ul>
      <li><strong>Every run:</strong> Required when each analytical run produces patient results independently (e.g., PCR batches).</li>
      <li><strong>Every shift:</strong> Appropriate for continuous analyzers running 24/7 (clinical chemistry, hematology).</li>
      <li><strong>Per batch:</strong> When patient samples are grouped into discrete batches with shared reagents and calibration.</li>
    </ul>

    <div class="info-box">
      <strong>Rule of thumb:</strong> If in doubt, run controls with every analytical run. The cost of a QC control
      is negligible compared to the cost of reporting erroneous patient results.
    </div>

    <h3>Establishing Mean and SD</h3>
    <p>
      Before applying Westgard rules, you must establish reliable estimates of the mean and standard deviation for
      each control level. This requires collecting a <strong>minimum of 20 data points</strong> under routine operating
      conditions, spread across at least 10 different runs or days.
    </p>
    <ul>
      <li>Run controls alongside patient samples under normal conditions &mdash; do not use dedicated "setup" runs.</li>
      <li>Exclude obvious outliers (e.g., failed extractions) but document every exclusion.</li>
      <li>Recalculate mean and SD periodically (every 6 months or after a reagent lot change).</li>
    </ul>

    <div class="warning-box">
      <strong>Important:</strong> Do not apply Westgard rules until you have at least 20 data points. Rules applied
      to fewer data points produce unreliable mean/SD estimates and generate excessive false rejections.
    </div>

    <h3>Choosing TEa Values</h3>
    <p>
      Total Allowable Error (TEa) defines the maximum error acceptable for a given analyte. Select TEa from
      authoritative sources:
    </p>
    <table>
      <thead>
        <tr>
          <th>Source</th>
          <th>Region / Scope</th>
          <th>Notes</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>CLIA</td>
          <td>United States</td>
          <td>Published proficiency testing criteria for regulated analytes</td>
        </tr>
        <tr>
          <td>Biological Variation Database</td>
          <td>International</td>
          <td>Desirable TEa derived from within- and between-individual variation</td>
        </tr>
        <tr>
          <td>RILIBAK</td>
          <td>Germany</td>
          <td>Maximum allowable deviation from target value</td>
        </tr>
        <tr>
          <td>CDSCO / NABL</td>
          <td>India</td>
          <td>Aligned with ISO 15189 and manufacturer specifications</td>
        </tr>
        <tr>
          <td>Manufacturer claims</td>
          <td>Global</td>
          <td>Package insert performance specifications (use as minimum baseline)</td>
        </tr>
      </tbody>
    </table>

    <h3>Documentation Requirements for Regulatory Audit</h3>
    <p>
      Your QC program documentation should include:
    </p>
    <ul>
      <li>QC policy: which rules are applied, how many levels, how often controls are run.</li>
      <li>Source and justification for mean, SD, and TEa values.</li>
      <li>Lot change records and parallel testing data.</li>
      <li>Corrective action records for all QC failures.</li>
      <li>Periodic QC review summaries (monthly or quarterly).</li>
    </ul>

    <!-- ============================================================ -->
    <!-- Section 2: Preparing QC Data Files                           -->
    <!-- ============================================================ -->
    <h2>2. Preparing QC Data Files</h2>
    <p>
      OpenQC accepts Excel (<code>.xlsx</code>) files exported from PCR instruments and clinical analyzers. The
      system supports three file format profiles:
    </p>

    <h3>Supported Formats</h3>
    <table>
      <thead>
        <tr>
          <th>Format</th>
          <th>Instrument</th>
          <th>Required Columns</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>QuantStudio</td>
          <td>Applied Biosystems QuantStudio</td>
          <td><code>Sample Name</code>, <code>Target Name</code>, <code>CT</code>, <code>Ct Mean</code>, <code>Ct SD</code></td>
        </tr>
        <tr>
          <td>Bio-Rad CFX</td>
          <td>Bio-Rad CFX96 / CFX384</td>
          <td><code>Sample</code>, <code>Target</code>, <code>Cq</code>, <code>Cq Mean</code>, <code>Cq Std. Dev</code></td>
        </tr>
        <tr>
          <td>Generic</td>
          <td>Any instrument</td>
          <td>User-defined column mapping (sample, target, value columns)</td>
        </tr>
      </tbody>
    </table>

    <h3>How to Export Data from Common Instruments</h3>

    <p><strong>Applied Biosystems QuantStudio:</strong></p>
    <ol>
      <li>Open the experiment in QuantStudio Design &amp; Analysis software.</li>
      <li>Go to <strong>Export</strong> &gt; <strong>Results</strong>.</li>
      <li>Select <code>.xlsx</code> format and save.</li>
      <li>The exported file is directly compatible with the QuantStudio format in OpenQC.</li>
    </ol>

    <p><strong>Bio-Rad CFX Manager:</strong></p>
    <ol>
      <li>Open the run in CFX Manager.</li>
      <li>Go to <strong>Export</strong> &gt; <strong>Quantification Cq Results</strong>.</li>
      <li>Save as <code>.xlsx</code>.</li>
      <li>Use the Bio-Rad CFX format in OpenQC.</li>
    </ol>

    <p><strong>Roche LightCycler:</strong></p>
    <ol>
      <li>Export the analysis results as <code>.xlsx</code> from the LightCycler software.</li>
      <li>Use the <strong>Generic format</strong> in OpenQC and map the columns manually (sample name, target, Ct/Cp value).</li>
    </ol>

    <p><strong>Clinical Chemistry Analyzers:</strong></p>
    <ol>
      <li>Export the daily QC report as <code>.xlsx</code> from the analyzer software or LIS.</li>
      <li>Ensure the file includes sample identifier, analyte name, and measured value columns.</li>
      <li>Use the Generic format with appropriate column mapping.</li>
    </ol>

    <p><strong>Hematology Analyzers:</strong></p>
    <ol>
      <li>Export QC data as <code>.xlsx</code> from the analyzer software.</li>
      <li>Ensure the file includes control level, parameter name, and measured value columns.</li>
      <li>Use the Generic format with column mapping.</li>
    </ol>

    <h3>Column Mapping for Generic Format</h3>
    <p>
      When using the Generic format, you specify which columns in your file correspond to the required fields.
      OpenQC reads your column headers and allows you to map them:
    </p>
    <ul>
      <li><strong>Sample column:</strong> The column containing sample or control identifiers.</li>
      <li><strong>Target column:</strong> The column containing the analyte or target name.</li>
      <li><strong>Value column:</strong> The column containing the measured value (Ct, concentration, count, etc.).</li>
    </ul>

    <h3>Best Practices for Data Files</h3>
    <ul>
      <li><strong>Consistent naming:</strong> Use the same sample names and target names across all files (e.g., always "QC-Low" not sometimes "QC Low" or "qc_low").</li>
      <li><strong>Include lot numbers:</strong> Record reagent and control lot numbers in the metadata fields during upload.</li>
      <li><strong>Record dates:</strong> Ensure the exported file includes run date information, or enter the date during upload.</li>
      <li><strong>Do not modify exported files:</strong> Upload the file exactly as exported from the instrument. Manual edits can introduce errors and compromise audit trail integrity.</li>
    </ul>

    <div class="info-box">
      <strong>Tip:</strong> Use the example datasets in the <code>example_sets/</code> directory to familiarize
      yourself with the expected file formats before uploading your own data. Files like
      <code>sample_qc_quantstudio.xlsx</code> and <code>sample_qc_biorad.xlsx</code> demonstrate the correct
      column structure.
    </div>

    <!-- ============================================================ -->
    <!-- Section 3: Setting Up Lot Tracking                           -->
    <!-- ============================================================ -->
    <h2>3. Setting Up Lot Tracking</h2>
    <p>
      Reagent and control material lots are a major source of variation in laboratory measurements. A new lot of
      control material may have a different target value (mean) and dispersion (SD) compared to the previous lot,
      even if both are from the same manufacturer and catalog number.
    </p>

    <h3>Why Lot Tracking Matters</h3>
    <ul>
      <li>A new lot may shift the mean Ct or concentration, causing false Westgard violations if the old mean/SD are still applied.</li>
      <li>Regulatory standards require traceability of results to specific reagent and control lots.</li>
      <li>Lot tracking enables root cause analysis when QC failures occur &mdash; was it a lot change or a genuine analytical error?</li>
    </ul>

    <h3>When to Register a New Lot</h3>
    <p>
      Register a new lot in the <strong>Lot Registry</strong> whenever you receive a new shipment of control material
      or reagent kit with a different lot number. Do this <em>before</em> you use the new lot for the first time.
    </p>

    <h3>How to Handle Lot Transitions</h3>
    <ol>
      <li><strong>Register the new lot</strong> in the Lot Registry with the lot number, manufacturer, material type, and expiration date.</li>
      <li><strong>Run the new lot in parallel</strong> with the old lot for at least 5 runs (ideally 20 for full mean/SD establishment).</li>
      <li><strong>Establish new mean and SD</strong> from the parallel data for the new lot.</li>
      <li><strong>Switch over</strong> to the new lot and mark the lot change in OpenQC.</li>
      <li><strong>Document the transition</strong> including parallel testing results and the date of switch.</li>
    </ol>

    <div class="info-box">
      <strong>OpenQC behavior:</strong> OpenQC automatically resets Westgard rule evaluation history at lot
      boundaries. This prevents carryover violations from the previous lot's data influencing the new lot's
      evaluation. Historical data for the old lot is preserved for review.
    </div>

    <!-- ============================================================ -->
    <!-- Section 4: Running QC Analysis — Step by Step                -->
    <!-- ============================================================ -->
    <h2>4. Running QC Analysis &mdash; Step by Step</h2>

    <h3>For RT-PCR / Molecular Assays</h3>
    <ol>
      <li>Export QC data from your instrument software (QuantStudio, CFX Manager, or other) as <code>.xlsx</code>.</li>
      <li>Open <strong>QC Monitor</strong> in OpenQC.</li>
      <li>Upload the file by clicking the upload area or dragging the file onto it.</li>
      <li>Enter the metadata: instrument name, assay name, fluorescence channel, reagent lot ID, and control lot ID.</li>
      <li>Click <strong>Upload and Analyze</strong>.</li>
      <li>Review the Levey-Jennings chart &mdash; look for trends, shifts, and outliers.</li>
      <li>Check the violation table for any Westgard rule violations.</li>
      <li>Make a decision: accept the run and report patient results, or investigate the violation before releasing results.</li>
    </ol>

    <h3>For Clinical Chemistry</h3>
    <p>
      The workflow is identical to the RT-PCR flow above. Note that in OpenQC, the value field (labeled "Ct Value"
      in the interface) holds the measured concentration or activity value for clinical chemistry analytes. The
      Westgard evaluation and Levey-Jennings charting work the same way regardless of whether the value represents
      a Ct, a concentration in mg/dL, or an enzyme activity in U/L.
    </p>

    <h3>For Hematology</h3>
    <p>
      The same workflow applies. Export your QC data from the hematology analyzer, upload it using the Generic format,
      and map the columns to your CBC parameters (WBC, RBC, Hgb, Hct, PLT, etc.). Each parameter is tracked as a
      separate control level.
    </p>

    <div class="warning-box">
      <strong>Remember:</strong> Always review the Levey-Jennings chart visually in addition to checking rule
      violations. Statistical rules can miss subtle trends that an experienced eye can catch, and visual inspection
      provides context that numbers alone cannot.
    </div>

    <!-- ============================================================ -->
    <!-- Section 5: Performing Sigma Analysis                         -->
    <!-- ============================================================ -->
    <h2>5. Performing Sigma Analysis</h2>
    <p>
      Sigma analysis quantifies the quality of your analytical method by combining allowable error (TEa),
      systematic error (bias), and random error (imprecision/CV) into a single metric. A higher Sigma value
      indicates a more robust method with greater margin for error.
    </p>

    <h3>Where to Find TEa Values</h3>
    <table>
      <thead>
        <tr>
          <th>Source</th>
          <th>Applicability</th>
          <th>How to Access</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>CLIA</td>
          <td>US laboratories</td>
          <td>Published in 42 CFR 493, Subpart I &mdash; Proficiency Testing Programs</td>
        </tr>
        <tr>
          <td>RILIBAK</td>
          <td>German laboratories</td>
          <td>Published by the German Medical Association (Bundesarztekammer)</td>
        </tr>
        <tr>
          <td>Biological Variation Database</td>
          <td>International (desirable TEa)</td>
          <td>EFLM Biological Variation Database (biologicalvariation.eu)</td>
        </tr>
        <tr>
          <td>CDSCO / NABL</td>
          <td>Indian laboratories</td>
          <td>NABL guidelines aligned with ISO 15189</td>
        </tr>
        <tr>
          <td>Manufacturer's package insert</td>
          <td>Global (as baseline)</td>
          <td>Performance specifications section of the IVD kit insert</td>
        </tr>
      </tbody>
    </table>

    <h3>How to Calculate Bias</h3>
    <p>
      Bias is the systematic difference between your method's results and the true (or accepted reference) value.
      There are several approaches:
    </p>
    <ul>
      <li>
        <strong>From EQA/PT program results:</strong> Compare your laboratory's results to the peer group mean
        in External Quality Assessment or Proficiency Testing programs. Bias = (Your mean &minus; Peer group mean)
        / Peer group mean &times; 100%.
      </li>
      <li>
        <strong>From peer group comparison:</strong> If your instrument participates in a manufacturer peer group,
        use the difference between your results and the group consensus.
      </li>
      <li>
        <strong>From recovery experiments:</strong> Spike a known quantity of analyte into a sample matrix and
        measure the recovered amount. Bias = (Recovered &minus; Expected) / Expected &times; 100%.
      </li>
    </ul>

    <h3>How to Calculate CV</h3>
    <p>
      CV (coefficient of variation) quantifies your method's imprecision:
    </p>
    <ul>
      <li>
        <strong>From your own QC data:</strong> Use a minimum of 20 data points from routine QC runs.
        CV = (SD / Mean) &times; 100%. Use inter-run (reproducibility) CV for Sigma calculations, as this
        reflects total method variation.
      </li>
      <li>
        <strong>Using the Precision module in OpenQC:</strong> Upload your precision study data and OpenQC will
        calculate intra-run and inter-run CV automatically.
      </li>
    </ul>

    <h3>Entering Values and Interpreting the NMEDx Chart</h3>
    <p>
      In the <strong>Sigma Analysis</strong> module, enter TEa, Bias, and CV for each assay. After clicking
      Calculate, review:
    </p>
    <ul>
      <li>The <strong>Sigma value</strong>: computed as (TEa &minus; |Bias|) / CV.</li>
      <li>The <strong>performance classification</strong>: World Class (&ge;6), Excellent (5&ndash;6), Good (4&ndash;5), Marginal (3&ndash;4), Poor (2&ndash;3), or Unacceptable (&lt;2).</li>
      <li>The <strong>NMEDx chart</strong>: your assay is plotted with bias on the y-axis and imprecision on the x-axis, both normalized to TEa. The colored zones show how much safety margin your method has.</li>
    </ul>

    <div class="info-box">
      <strong>Interpretation:</strong> An assay plotted in the green/blue zones of the NMEDx chart has sufficient
      margin &mdash; simple QC rules with two controls are adequate. An assay in the yellow or red zones requires
      more stringent QC rules, more controls per run, or method improvement.
    </div>

    <!-- ============================================================ -->
    <!-- Section 6: Method Validation Workflow                        -->
    <!-- ============================================================ -->
    <h2>6. Method Validation Workflow</h2>
    <p>
      Method validation is required whenever you introduce a new method, commission a new instrument, or switch to
      a new reagent formulation. The goal is to demonstrate that the method performs acceptably in your laboratory
      under your routine operating conditions.
    </p>

    <h3>LOD Study Design</h3>
    <ul>
      <li>Prepare <strong>20 replicates of a blank sample</strong> (no target analyte).</li>
      <li>Prepare <strong>20 replicates at 3&ndash;5 concentrations</strong> near the expected LOD.</li>
      <li>Run all replicates on the same day, under the same conditions.</li>
      <li>Record: concentration, replicate number, measured value (Ct or signal).</li>
    </ul>
    <pre class="diagram">
  LOD Study Layout:

  Concentration    Replicates    Expected Outcome
  -------------------------------------------------------
  Blank (0)        20            No detection (baseline)
  0.5x LOD         20            Partial detection
  1x LOD           20            >= 95% detection
  2x LOD           20            ~100% detection
  5x LOD           20            100% detection

  LOD = lowest concentration detected in >= 95% of replicates
    </pre>

    <h3>LOQ Study Design</h3>
    <ul>
      <li>Prepare <strong>10 replicates at 5&ndash;7 concentrations</strong>.</li>
      <li>Concentrations should span from LOD to approximately 10&times; LOD.</li>
      <li>Calculate CV at each concentration level.</li>
      <li>LOQ = the lowest concentration where CV &le; the threshold (typically 20%).</li>
    </ul>
    <pre class="diagram">
  LOQ Study Layout:

  Concentration    Replicates    CV Calculated    Pass?
  -----------------------------------------------------------
  1x LOD           10            35%              No
  2x LOD           10            25%              No
  3x LOD           10            18%              Yes (LOQ)
  5x LOD           10            12%              Yes
  7x LOD           10            8%               Yes
  10x LOD          10            5%               Yes

  LOQ = 3x LOD in this example (first level with CV <= 20%)
    </pre>

    <h3>Precision Study Design</h3>
    <p>
      Precision is assessed at two levels:
    </p>
    <ul>
      <li>
        <strong>Intra-run (repeatability):</strong> Run 20 replicates of the same sample in a single analytical
        run. Use at least 2 concentration levels (low and high).
      </li>
      <li>
        <strong>Inter-run (reproducibility):</strong> Run a minimum of 3 runs over 3 different days, with at
        least 2&ndash;3 replicates per run per concentration level.
      </li>
      <li>Record: run date, run ID, replicate number, measured value.</li>
    </ul>
    <pre class="diagram">
  Precision Study Layout:

  Intra-Run (single run, same day):
  Level     Replicates    Calculate
  ----------------------------------
  Low       20            Mean, SD, CV
  High      20            Mean, SD, CV

  Inter-Run (across days):
  Level     Runs    Days    Replicates/Run    Calculate
  -------------------------------------------------------
  Low       >= 3    >= 3    2-3               Mean, SD, CV (total)
  High      >= 3    >= 3    2-3               Mean, SD, CV (total)
    </pre>

    <h3>Linearity Study Design</h3>
    <ul>
      <li>Prepare <strong>5&ndash;7 concentration levels</strong> spanning the reportable range.</li>
      <li>Run a minimum of <strong>3 replicates per level</strong>.</li>
      <li>Include the lowest and highest values in your expected measurement range.</li>
      <li>Record: expected concentration, measured value, replicate number.</li>
    </ul>
    <pre class="diagram">
  Linearity Study Layout:

  Level    Expected Conc.    Replicates    Measured Values
  ---------------------------------------------------------
  1        10 copies/mL      3             Ct1, Ct2, Ct3
  2        100 copies/mL     3             Ct1, Ct2, Ct3
  3        1,000 copies/mL   3             Ct1, Ct2, Ct3
  4        10,000 copies/mL  3             Ct1, Ct2, Ct3
  5        100,000 copies/mL 3             Ct1, Ct2, Ct3
  6        1,000,000 c/mL    3             Ct1, Ct2, Ct3

  Evaluate: R2 >= 0.99, slope between -3.1 and -3.6
    </pre>

    <div class="info-box">
      <strong>OpenQC tip:</strong> Upload your validation study data to the <strong>Validation</strong> module.
      Select the study type (LOD, Precision, or Linearity), define your acceptance criteria, and OpenQC will
      perform the statistical analysis and generate a validation report suitable for regulatory submission.
    </div>

    <!-- ============================================================ -->
    <!-- Section 7: Generating Reports                                -->
    <!-- ============================================================ -->
    <h2>7. Generating Reports</h2>
    <p>
      OpenQC provides several report types to support routine QC review, management oversight, and regulatory
      compliance.
    </p>

    <h3>QC Run Report</h3>
    <p>
      Generated after each QC analysis in the QC Monitor. Contains:
    </p>
    <ul>
      <li>Summary statistics (mean, SD, CV) for each control level.</li>
      <li>The Levey-Jennings chart with all data points and SD lines.</li>
      <li>A complete list of Westgard rule violations with severity classification.</li>
      <li>Run metadata: instrument, assay, channel, reagent lot, control lot, date/time.</li>
      <li>Audit trail reference (hash and timestamp).</li>
    </ul>
    <p>
      <strong>When to generate:</strong> After every QC run, especially when violations are detected. Archive the
      report alongside the raw data file.
    </p>

    <h3>Sigma Report</h3>
    <p>
      Generated from the Sigma Analysis module. Contains:
    </p>
    <ul>
      <li>TEa, bias, and CV values for each assay.</li>
      <li>Calculated Sigma values and performance classifications.</li>
      <li>NMEDx chart visualization.</li>
      <li>Recommended QC rules and number of controls.</li>
    </ul>
    <p>
      <strong>When to generate:</strong> During QC planning sessions, management reviews, and when evaluating
      whether to change QC strategies.
    </p>

    <h3>Validation Report</h3>
    <p>
      Generated from the Validation module after completing a validation study. Contains:
    </p>
    <ul>
      <li>Study type, acceptance criteria, and study design parameters.</li>
      <li>Raw data summary and calculated statistics (LOD, CV, R<sup>2</sup>, slope).</li>
      <li>Pass/fail determination for each acceptance criterion.</li>
      <li>Visualizations (scatter plots, distribution plots).</li>
    </ul>
    <p>
      <strong>When to generate:</strong> At the conclusion of each validation study, for inclusion in your
      method validation documentation package for regulatory submission.
    </p>

    <h3>Audit Trail Export</h3>
    <p>
      Generated from the Audit Trail view. Contains:
    </p>
    <ul>
      <li>Chronological record of all system actions (uploads, analyses, exports, lot changes, configuration changes).</li>
      <li>Timestamps, user identifiers, and action details for each entry.</li>
      <li>Hash chain integrity status.</li>
    </ul>
    <p>
      <strong>When to generate:</strong> Before regulatory inspections, during accreditation audits, and as a
      monthly backup practice.
    </p>

    <h3>Report Best Practices</h3>
    <ul>
      <li><strong>Generate reports immediately after analysis.</strong> Do not delay &mdash; the data is freshest and the context is clearest right after the run.</li>
      <li><strong>Archive PDF reports alongside raw data.</strong> Store both the original <code>.xlsx</code> file and the generated report in the same directory or document management system.</li>
      <li><strong>Export the audit trail monthly</strong> for backup. This provides an independent copy in case of system failure.</li>
      <li><strong>Include lot change documentation in reports.</strong> When a lot transition occurs, attach the parallel testing data and new mean/SD calculations to the QC report.</li>
    </ul>

    <!-- ============================================================ -->
    <!-- Section 8: Maintaining Audit Trail Integrity                 -->
    <!-- ============================================================ -->
    <h2>8. Maintaining Audit Trail Integrity</h2>
    <p>
      The audit trail is your laboratory's proof that data has not been altered after the fact. OpenQC uses a
      SHA-256 hash chain to ensure that every action is recorded immutably and in sequence.
    </p>

    <h3>What Gets Logged Automatically</h3>
    <ul>
      <li>File uploads (including file name, file hash, and file size).</li>
      <li>QC analyses (parameters used, results calculated).</li>
      <li>Report exports (type of report, format, timestamp).</li>
      <li>Lot changes (old lot, new lot, effective date).</li>
      <li>Configuration changes (settings modified, old value, new value).</li>
    </ul>

    <h3>How Chain Integrity Works</h3>
    <p>
      Each audit entry is hashed using SHA-256, and each hash incorporates the hash of the previous entry. This
      creates an unbreakable chain: modifying any single entry invalidates all subsequent hashes, making tampering
      immediately detectable.
    </p>

    <h3>How to Verify Chain Integrity</h3>
    <ol>
      <li>Navigate to the <strong>Audit Trail</strong> view.</li>
      <li>Click <strong>Verify Chain</strong> (or "Verify Integrity").</li>
      <li>OpenQC recomputes every hash in the chain from scratch and compares against stored hashes.</li>
      <li>A green confirmation indicates the chain is intact. A red warning identifies the exact entry where the chain was broken.</li>
    </ol>

    <h3>What to Do If Tamper Is Detected</h3>
    <ol>
      <li>Document the finding immediately, including the entry number, timestamp, and nature of the discrepancy.</li>
      <li>Notify your quality manager and IT administrator.</li>
      <li>Investigate the root cause: was it intentional tampering, a software bug, or data corruption?</li>
      <li>Review all patient results associated with the affected time period.</li>
      <li>Record the investigation findings and corrective actions in your quality management system.</li>
    </ol>

    <div class="warning-box">
      <strong>Regulatory obligation:</strong> Under ISO 15189, 21 CFR Part 11, and equivalent standards, any
      detected data integrity failure must be investigated and documented. Failure to act on a tamper detection
      finding is itself a compliance violation.
    </div>

    <h3>Audit Trail Best Practices</h3>
    <ul>
      <li><strong>Never modify uploaded Excel files after upload.</strong> If a correction is needed, upload a new corrected file &mdash; both the original and correction will be logged.</li>
      <li><strong>Use the Lot Registry for all lot changes.</strong> Changes made through the registry are automatically logged in the audit trail.</li>
      <li><strong>Export the audit trail before system maintenance.</strong> This preserves a baseline in case the maintenance process affects data.</li>
      <li><strong>Keep file hashes for external verification.</strong> Record the SHA-256 hash of uploaded files in an independent system (e.g., a lab notebook or LIMS) for cross-verification.</li>
    </ul>

    <!-- ============================================================ -->
    <!-- Section 9: Troubleshooting Common Issues                     -->
    <!-- ============================================================ -->
    <h2>9. Troubleshooting Common Issues</h2>

    <table>
      <thead>
        <tr>
          <th>Problem</th>
          <th>Likely Cause</th>
          <th>Solution</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>"No mean/SD" error</td>
          <td>The uploaded file does not include Ct Mean/SD columns, or no control lot is assigned with established values.</td>
          <td>Ensure your exported file includes the mean and SD columns, or assign a control lot in the Lot Registry that has established mean/SD values from at least 20 data points.</td>
        </tr>
        <tr>
          <td>Westgard violations on first few runs</td>
          <td>Not enough historical data points to establish a reliable mean and SD.</td>
          <td>Collect at least 20 data points before applying Westgard rules. Use the initial runs to establish baseline statistics only.</td>
        </tr>
        <tr>
          <td>R-4s triggering unexpectedly</td>
          <td>Both control levels may not be included in the same run, or there is a genuine divergence between levels.</td>
          <td>Verify that both control levels (L1 and L2) are present in each uploaded file. If the divergence is real, investigate the analytical process.</td>
        </tr>
        <tr>
          <td>Validation LOD seems too high</td>
          <td>Blank contamination or insufficient replicates are inflating the baseline.</td>
          <td>Check for contamination in blank samples. Increase the number of replicates (use 20 or more). Ensure the sample matrix is representative.</td>
        </tr>
        <tr>
          <td>Sigma score is "Unacceptable"</td>
          <td>The method's bias and/or imprecision exceed what the TEa allows.</td>
          <td>Review method bias (consider recalibration or a different calibrator). Review precision (check maintenance, reagent quality). If the method fundamentally cannot meet the TEa, consider switching to a better-performing method or platform.</td>
        </tr>
      </tbody>
    </table>

    <div class="info-box">
      <strong>General troubleshooting tip:</strong> When encountering unexpected results, always check the basics
      first: correct file format, correct column names, sufficient data points, and correct lot assignment. Most
      issues are caused by data preparation errors rather than analytical problems.
    </div>
  </div>
</template>
