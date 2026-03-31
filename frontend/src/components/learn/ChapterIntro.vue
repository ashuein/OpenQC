<script setup>
</script>

<template>
  <div class="learn-content">
    <h1>Chapter 1: Introduction to Quality Control in PCR Labs</h1>
    <p class="chapter-subtitle">Understanding why QC matters and how controls protect patient outcomes.</p>

    <h2>What Is Quality Control?</h2>
    <p>
      Quality Control (QC) in clinical laboratories is a set of systematic procedures designed to monitor and evaluate
      the analytical processes that produce patient results. In PCR-based molecular diagnostics, QC ensures that every
      test run produces results that are accurate, precise, and clinically meaningful.
    </p>
    <p>
      Without rigorous QC, a laboratory cannot distinguish between a genuine patient result and one caused by reagent
      degradation, instrument drift, operator error, or environmental fluctuation. QC is not optional — it is a
      fundamental requirement of every accredited diagnostic laboratory worldwide.
    </p>

    <h2>Why QC Matters in Diagnostic Labs</h2>
    <p>
      Diagnostic PCR assays directly inform clinical decisions: whether a patient has an infectious disease, whether a
      transplant recipient is experiencing rejection, or whether a cancer biomarker is rising. A false negative can
      delay life-saving treatment. A false positive can lead to unnecessary interventions, patient anxiety, and wasted
      healthcare resources.
    </p>
    <p>
      QC acts as the safety net between the analytical instrument and the patient report. By running known control
      materials alongside patient samples, the laboratory can verify that the entire analytical system — from nucleic
      acid extraction through amplification and detection — is performing within acceptable limits.
    </p>

    <div class="info-box">
      <strong>Key principle:</strong> A QC failure means the analytical system cannot be trusted. Patient results from
      that run should not be reported until the root cause is identified and resolved.
    </div>

    <h2>The Role of Controls: L1, L2, and L3</h2>
    <p>
      In quantitative PCR QC, laboratories typically run multiple levels of control materials to assess performance
      across the clinically relevant measurement range:
    </p>
    <ul>
      <li>
        <strong>Level 1 (L1) — Low positive control:</strong> Contains a low concentration of the target analyte,
        near the clinical decision point. This control is most sensitive to changes in assay sensitivity and is
        critical for detecting shifts that could cause false negatives.
      </li>
      <li>
        <strong>Level 2 (L2) — Mid-range control:</strong> Contains a moderate concentration of target, representing
        the middle of the reportable range. L2 monitors overall assay stability and is the most commonly used single
        control level.
      </li>
      <li>
        <strong>Level 3 (L3) — High positive control:</strong> Contains a high concentration of target, near the upper
        end of the linear range. L3 helps detect issues with amplification efficiency at high template loads and
        monitors linearity.
      </li>
    </ul>
    <p>
      Running multiple levels provides a more complete picture of assay performance than any single control can offer.
      A shift detected only at L1 but not L2 or L3 suggests a sensitivity problem, while a shift across all levels
      suggests a systematic error such as calibration drift.
    </p>

    <h2>What Ct Values Represent</h2>
    <p>
      The <strong>Ct value</strong> (cycle threshold, also written as Cq for quantification cycle) is the PCR cycle
      number at which the fluorescence signal crosses a defined threshold. It is the primary quantitative output of
      real-time PCR.
    </p>
    <p>
      Ct values are inversely proportional to the amount of target nucleic acid in the sample:
    </p>
    <ul>
      <li>A <strong>low Ct</strong> (e.g., 15-20) indicates a high concentration of target — the signal rises early.</li>
      <li>A <strong>high Ct</strong> (e.g., 35-40) indicates a low concentration — more amplification cycles are needed before the signal is detectable.</li>
      <li>An <strong>undetermined Ct</strong> means the fluorescence never crossed the threshold within the allotted cycles, suggesting the target is absent or below the limit of detection.</li>
    </ul>
    <p>
      In QC, we track the Ct values of control materials over time. Because the controls have a known, fixed
      concentration, their Ct values should remain stable from run to run. When they drift or jump, something in the
      analytical system has changed.
    </p>

    <div class="diagram">
Ct value vs. Target concentration:

  Ct
  40 |  *
  35 |     *
  30 |        *
  25 |           *
  20 |              *
  15 |                 *
     +-------------------------
       Low              High
         Target concentration

  Note: Relationship is inversely logarithmic.
  A 1-Ct shift represents approximately a 2-fold
  change in target quantity.
    </div>

    <h2>How QC Ensures Patient Safety</h2>
    <p>
      QC operates on a simple but powerful principle: <strong>if the controls fail, the patient results cannot be
      trusted.</strong> This is implemented through a daily workflow:
    </p>
    <ol>
      <li>Before or alongside patient testing, the laboratory processes control materials of known concentration.</li>
      <li>The resulting Ct values are plotted on a Levey-Jennings chart and evaluated against statistical rules (Westgard rules).</li>
      <li>If all controls pass, the run is accepted and patient results can be reported.</li>
      <li>If any control triggers a rejection rule, the run is flagged, patient results are held, and the laboratory investigates the root cause.</li>
      <li>Corrective action is documented, the issue is resolved, and the run is repeated before results are released.</li>
    </ol>

    <h2>Regulatory Requirements</h2>
    <p>
      QC is not just good practice — it is mandated by every major regulatory framework:
    </p>

    <table>
      <thead>
        <tr>
          <th>Standard</th>
          <th>Requirement</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>ISO 15189:2022</td>
          <td>Section 7.7.1 requires laboratories to implement QC procedures that verify the attainment of intended quality of results.</td>
        </tr>
        <tr>
          <td>CLIA (US)</td>
          <td>42 CFR 493.1256 mandates that laboratories follow manufacturers' QC instructions and run controls at frequencies sufficient to detect clinically relevant errors.</td>
        </tr>
        <tr>
          <td>CE-IVD (EU)</td>
          <td>IVDR 2017/746 requires manufacturers to specify QC procedures, and laboratories must implement them.</td>
        </tr>
        <tr>
          <td>CDSCO (India)</td>
          <td>MD/IVD rules require compliance with ISO 15189 for clinical laboratories.</td>
        </tr>
        <tr>
          <td>CAP (US)</td>
          <td>College of American Pathologists checklists require documented QC with evidence of corrective action for failures.</td>
        </tr>
      </tbody>
    </table>

    <div class="info-box">
      <strong>Bottom line:</strong> QC is the bridge between analytical measurement and clinical trust. OpenQC
      automates the statistical evaluation, charting, and documentation so that laboratory professionals can focus
      on interpretation and patient care.
    </div>
  </div>
</template>
