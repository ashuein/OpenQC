<script setup>
</script>

<template>
  <div class="learn-content">
    <h1>Chapter 7: Example Datasets Reference</h1>
    <p class="chapter-subtitle">A complete guide to the sample files included with OpenQC and what to expect from each.</p>

    <h2>Overview</h2>
    <p>
      OpenQC ships with a set of example datasets in the <code>backend/data/samples/</code> directory. These files
      are designed to help you test every module of the application and verify that it is functioning correctly. Each
      file is crafted to demonstrate specific features and produce predictable, verifiable results.
    </p>
    <p>
      Use these files when first setting up OpenQC, after upgrades, or for training new laboratory staff on the system.
    </p>

    <h2>Sample Files</h2>

    <table>
      <thead>
        <tr>
          <th>File Name</th>
          <th>Module</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>sample_qc_quantstudio.xlsx</code></td>
          <td>QC Monitor</td>
          <td>Standard QC dataset in QuantStudio export format with Ct values for multiple control levels.</td>
        </tr>
        <tr>
          <td><code>sample_qc_violations.xlsx</code></td>
          <td>QC Monitor</td>
          <td>QC dataset with intentional outliers designed to trigger Westgard rule violations.</td>
        </tr>
        <tr>
          <td><code>sample_sigma_inputs.xlsx</code></td>
          <td>Sigma Analysis</td>
          <td>Pre-calculated TEa, Bias, and CV values for multiple assays for Sigma metric calculation.</td>
        </tr>
        <tr>
          <td><code>sample_validation_lod.xlsx</code></td>
          <td>Validation (LOD)</td>
          <td>Replicate measurements at serial dilutions near the limit of detection.</td>
        </tr>
        <tr>
          <td><code>sample_validation_linearity.xlsx</code></td>
          <td>Validation (Linearity)</td>
          <td>Serial dilution series spanning a wide concentration range for linearity assessment.</td>
        </tr>
      </tbody>
    </table>

    <h2>Detailed File Descriptions and Expected Results</h2>

    <h3>sample_qc_quantstudio.xlsx</h3>
    <p>
      <strong>Module:</strong> QC Monitor<br>
      <strong>Format:</strong> Simulated QuantStudio export with sample identifiers and Ct values<br>
      <strong>Contents:</strong> QC data for control levels with Ct values distributed around established means
    </p>
    <p><strong>How to use:</strong></p>
    <ol>
      <li>Navigate to QC Monitor.</li>
      <li>Upload the file and optionally fill in metadata (instrument: "QuantStudio 5", assay: "SARS-CoV-2").</li>
      <li>Click Upload and Analyze.</li>
    </ol>
    <p><strong>Expected results:</strong></p>
    <ul>
      <li>Summary statistics should be calculated for the control data.</li>
      <li>The Levey-Jennings chart should display data points distributed around the mean with most points within +/-2SD.</li>
      <li>This is a clean dataset — you should see no rejection-level violations, though individual points near +/-2SD may trigger 1-2s warnings.</li>
      <li>The overall run status should be PASS.</li>
    </ul>

    <div class="info-box">
      <strong>Verification check:</strong> After upload, confirm that the Levey-Jennings chart renders correctly with
      clearly labeled SD lines and that the summary statistics table shows reasonable values for mean, SD, and CV.
    </div>

    <h3>sample_qc_violations.xlsx</h3>
    <p>
      <strong>Module:</strong> QC Monitor<br>
      <strong>Format:</strong> Same structure as the QuantStudio file<br>
      <strong>Contents:</strong> QC data with deliberately placed outlier values to trigger Westgard rule violations
    </p>
    <p><strong>How to use:</strong></p>
    <ol>
      <li>Navigate to QC Monitor.</li>
      <li>Upload the file.</li>
      <li>Click Upload and Analyze.</li>
    </ol>
    <p><strong>Expected results:</strong></p>
    <ul>
      <li>The Levey-Jennings chart should show one or more data points clearly outside the +/-2SD or +/-3SD lines.</li>
      <li>The Violations Table should list specific Westgard rule violations with the affected data points identified.</li>
      <li>Expect to see violations such as 1-3s (points beyond +/-3SD) and potentially 2-2s (consecutive points on the same side beyond +/-2SD).</li>
      <li>The overall run status should be FAIL due to rejection-level violations.</li>
    </ul>

    <div class="warning-box">
      <strong>Training exercise:</strong> Use this file to practice the corrective action workflow. When violations
      are detected, document the investigation steps you would take in a real laboratory scenario: check the data
      points, identify the rule violated, determine potential root causes, and describe the corrective action.
    </div>

    <h3>sample_sigma_inputs.xlsx</h3>
    <p>
      <strong>Module:</strong> Sigma Analysis<br>
      <strong>Format:</strong> Tabular data with columns for assay name, TEa, Bias, and CV<br>
      <strong>Contents:</strong> Pre-calculated quality parameters for multiple hypothetical assays
    </p>
    <p><strong>How to use:</strong></p>
    <ol>
      <li>Navigate to Sigma Analysis.</li>
      <li>You can enter values manually from this file, or use it as a reference for the expected input format.</li>
      <li>Enter TEa, Bias, and CV values for an assay.</li>
      <li>Click Calculate.</li>
    </ol>
    <p><strong>Expected results:</strong></p>
    <ul>
      <li>The Sigma metric should be calculated correctly using the formula <code>sigma = (TEa - |Bias|) / CV</code>.</li>
      <li>The classification should match the Sigma bands (e.g., Sigma &ge; 6 = World Class, 5-6 = Excellent, etc.).</li>
      <li>The NMEDx chart should plot the assay in the correct zone.</li>
      <li>QC recommendations should be appropriate for the calculated Sigma level.</li>
    </ul>

    <h3>sample_validation_lod.xlsx</h3>
    <p>
      <strong>Module:</strong> Validation (LOD study)<br>
      <strong>Format:</strong> Replicate Ct values at multiple low concentration levels<br>
      <strong>Contents:</strong> Measurements at serial dilutions near the expected limit of detection
    </p>
    <p><strong>How to use:</strong></p>
    <ol>
      <li>Navigate to Validation.</li>
      <li>Select LOD as the validation type.</li>
      <li>Upload the file.</li>
      <li>Set the detection rate threshold (use 95% as default).</li>
      <li>Run the validation.</li>
    </ol>
    <p><strong>Expected results:</strong></p>
    <ul>
      <li>The LOD should be calculated based on the lowest concentration where the detection rate meets or exceeds the threshold.</li>
      <li>Higher concentration levels should show 100% detection rates.</li>
      <li>Lower concentration levels should show decreasing detection rates.</li>
      <li>The result should include a clear statement of the determined LOD value.</li>
    </ul>

    <h3>sample_validation_linearity.xlsx</h3>
    <p>
      <strong>Module:</strong> Validation (Linearity study)<br>
      <strong>Format:</strong> Ct values measured across a serial dilution series<br>
      <strong>Contents:</strong> Data spanning a wide concentration range to assess linearity
    </p>
    <p><strong>How to use:</strong></p>
    <ol>
      <li>Navigate to Validation.</li>
      <li>Select Linearity as the validation type.</li>
      <li>Upload the file.</li>
      <li>Set acceptance criteria (R<sup>2</sup> &ge; 0.99, slope -3.1 to -3.6).</li>
      <li>Run the validation.</li>
    </ol>
    <p><strong>Expected results:</strong></p>
    <ul>
      <li>The regression analysis should produce an R<sup>2</sup> value close to or exceeding 0.99.</li>
      <li>The slope should fall within the acceptable range for PCR efficiency.</li>
      <li>The scatter plot should show data points closely following the regression line.</li>
      <li>The validation result should be PASS if the acceptance criteria are met.</li>
    </ul>

    <h2>Quick Reference Table</h2>
    <p>
      Use this table as a quick lookup when testing OpenQC modules:
    </p>

    <table>
      <thead>
        <tr>
          <th>File</th>
          <th>Module</th>
          <th>Expected Outcome</th>
          <th>Key Verification</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>sample_qc_quantstudio.xlsx</code></td>
          <td>QC Monitor</td>
          <td>PASS — all points within limits</td>
          <td>L-J chart renders, stats calculated</td>
        </tr>
        <tr>
          <td><code>sample_qc_violations.xlsx</code></td>
          <td>QC Monitor</td>
          <td>FAIL — Westgard violations detected</td>
          <td>Violations table populated, chart highlights outliers</td>
        </tr>
        <tr>
          <td><code>sample_sigma_inputs.xlsx</code></td>
          <td>Sigma Analysis</td>
          <td>Sigma metrics calculated per assay</td>
          <td>NMEDx chart plotted, QC recommendations shown</td>
        </tr>
        <tr>
          <td><code>sample_validation_lod.xlsx</code></td>
          <td>Validation</td>
          <td>LOD determined at correct concentration</td>
          <td>Detection rates calculated per level</td>
        </tr>
        <tr>
          <td><code>sample_validation_linearity.xlsx</code></td>
          <td>Validation</td>
          <td>PASS — R<sup>2</sup> &ge; 0.99</td>
          <td>Regression line plotted, slope and R<sup>2</sup> displayed</td>
        </tr>
      </tbody>
    </table>

    <div class="info-box">
      <strong>Tip:</strong> Keep these sample files accessible for new staff onboarding. Walking through each file
      with a new team member is an effective way to train them on both the software and the underlying QC concepts.
    </div>
  </div>
</template>
