<script setup>
</script>

<template>
  <div class="learn-content">
    <h1>Chapter 4: Assay Validation Fundamentals</h1>
    <p class="chapter-subtitle">The essential validation studies every PCR assay must pass before clinical use.</p>

    <h2>Why Validation Is Required</h2>
    <p>
      Assay validation is the process of demonstrating, through documented evidence, that an analytical method
      consistently produces results that meet predetermined acceptance criteria. No PCR assay should be used for
      patient testing until it has been validated in the laboratory where it will be used.
    </p>
    <p>
      Even commercially available IVD kits require verification (a subset of validation) when implemented in a new
      laboratory. This is because performance can be affected by local conditions: the specific instrument model,
      environmental factors, operator technique, water quality, and sample types encountered in that particular setting.
    </p>
    <p>
      Regulatory standards — ISO 15189:2022 (Section 7.3), CLIA, CE-IVD (IVDR), and CDSCO — all require documented
      validation or verification before clinical use. Failure to validate is one of the most common citations in
      laboratory accreditation inspections.
    </p>

    <h2>Limit of Detection (LOD)</h2>
    <p>
      The <strong>Limit of Detection (LOD)</strong> is the lowest amount of target analyte that can be reliably
      distinguished from a blank (no-target) sample. "Reliably" typically means detected in at least 95% of
      replicates at that concentration.
    </p>

    <h3>How LOD Is Calculated</h3>
    <p>
      The classical approach for calculating LOD involves measuring blank or near-blank samples:
    </p>
    <div class="diagram">
  LOD Calculation:

  LOD = Mean_blank + 3 * SD_blank

  Where:
    Mean_blank = Average Ct (or signal) of blank samples
    SD_blank   = Standard deviation of blank measurements
    3          = Multiplier for 99.7% confidence

  Alternative (probit analysis):
    Test serial dilutions near the expected LOD.
    At each concentration, run 20+ replicates.
    LOD = concentration detected in 95% of replicates
    (determined by probit regression).
    </div>

    <p>
      For qualitative PCR assays (detected/not detected), LOD is often expressed as copies/mL or IU/mL. For
      quantitative assays, LOD represents the lowest reliably quantifiable concentration, though LOQ (below) is
      more appropriate for quantification.
    </p>

    <h3>Practical Considerations</h3>
    <ul>
      <li>Use at least 20 replicate measurements of blank samples to calculate Mean_blank and SD_blank.</li>
      <li>If the assay does not produce a Ct value for blank samples (undetermined), use a probit-based approach with serial dilutions instead.</li>
      <li>The LOD should be established in the sample matrix (e.g., extracted nucleic acid from clinical specimens), not in water.</li>
      <li>Report LOD in clinically meaningful units (copies/mL, IU/mL) rather than Ct values.</li>
    </ul>

    <h2>Limit of Quantification (LOQ)</h2>
    <p>
      The <strong>Limit of Quantification (LOQ)</strong> is the lowest concentration at which the analyte can be
      reliably quantified with acceptable precision. While LOD tells you "can I detect it?", LOQ tells you
      "can I measure it accurately enough to report a number?"
    </p>
    <p>
      LOQ is determined using a CV threshold approach:
    </p>
    <div class="diagram">
  LOQ Determination (CV Threshold Method):

  CV (%)
    50 |  *
    40 |     *
    30 |        *
    20 |           *  - - - - - - - - - - CV threshold (e.g., 20%)
    15 |              *
    10 |                 *     *     *
     5 |                          *
       +------+------+------+------+----> Concentration
       LOD          LOQ

  1. Prepare serial dilutions spanning the low end of the range.
  2. Measure each dilution in at least 10 replicates.
  3. Calculate CV at each concentration.
  4. LOQ = lowest concentration where CV is below the threshold.

  Common CV thresholds:
    - 20% for most molecular assays
    - 15% for high-precision requirements
    - 25% for screening assays
    </div>

    <div class="info-box">
      <strong>Note:</strong> LOQ is always equal to or higher than LOD. You can detect an analyte at concentrations
      below LOQ, but you cannot reliably quantify it — results below LOQ should be reported as "detected, below
      the limit of quantification."
    </div>

    <h2>Precision</h2>
    <p>
      <strong>Precision</strong> measures the closeness of agreement between independent measurements obtained under
      stipulated conditions. In PCR validation, precision is assessed at two levels:
    </p>

    <h3>Intra-Run Precision (Repeatability)</h3>
    <p>
      Repeatability measures the variation when the same sample is tested multiple times within a single analytical
      run, by the same operator, on the same instrument, using the same reagents.
    </p>
    <ul>
      <li>Test at least 2-3 concentration levels (low, medium, high).</li>
      <li>Run a minimum of 10 replicates at each level within a single run.</li>
      <li>Calculate mean, SD, and CV for each level.</li>
      <li>Typical acceptance: CV &lt; 5% for quantitative PCR assays (Ct values).</li>
    </ul>

    <h3>Inter-Run Precision (Reproducibility)</h3>
    <p>
      Reproducibility measures variation across different runs, days, operators, and potentially different instruments
      or reagent lots. It captures the total variation that affects patient results in routine practice.
    </p>
    <ul>
      <li>Test the same concentration levels used for repeatability.</li>
      <li>Run at least 20 measurements at each level, spread across at least 10 different days.</li>
      <li>Vary conditions: different operators, different aliquots of reagents, different times of day.</li>
      <li>Calculate mean, SD, and CV for each level across all runs.</li>
      <li>Typical acceptance: CV &lt; 10% for quantitative PCR assays (Ct values).</li>
    </ul>

    <table>
      <thead>
        <tr>
          <th>Parameter</th>
          <th>Intra-Run (Repeatability)</th>
          <th>Inter-Run (Reproducibility)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Conditions</td>
          <td>Same run, operator, reagents, day</td>
          <td>Different runs, days, operators</td>
        </tr>
        <tr>
          <td>Minimum replicates</td>
          <td>10 per level</td>
          <td>20 per level (across 10+ days)</td>
        </tr>
        <tr>
          <td>Typical CV acceptance</td>
          <td>&lt; 5%</td>
          <td>&lt; 10%</td>
        </tr>
        <tr>
          <td>What it measures</td>
          <td>Instrument and pipetting precision</td>
          <td>Total method variation in routine use</td>
        </tr>
      </tbody>
    </table>

    <h2>Linearity</h2>
    <p>
      <strong>Linearity</strong> is the ability of the assay to produce results that are directly proportional to the
      concentration of the analyte across the reportable range. For quantitative PCR, a linear assay produces Ct
      values that decrease by a consistent amount for each log-unit increase in target concentration.
    </p>

    <h3>How to Assess Linearity</h3>
    <ol>
      <li>Prepare a serial dilution series spanning the expected reportable range (e.g., 10<sup>1</sup> to 10<sup>8</sup> copies/mL).</li>
      <li>Measure each dilution in triplicate (minimum).</li>
      <li>Plot observed values (Ct or log copies) against expected values (known concentrations).</li>
      <li>Perform linear regression analysis.</li>
    </ol>

    <h3>Key Statistics</h3>
    <div class="diagram">
  Linearity Assessment:

  Ct value
    35 |  *
    30 |     *
    25 |        *
    20 |           *          Regression line:
    15 |              *       y = mx + b
    10 |                 *
       +----|----|----|----|----|-----> Log concentration
       1    2    3    4    5    6

  Key metrics:
    R² (coefficient of determination)
      - Measures how well data fits the regression line
      - R² >= 0.99 is typically required
      - R² >= 0.995 is ideal

    Slope
      - For a perfect PCR assay: slope = -3.32
        (corresponds to 100% amplification efficiency)
      - Acceptable range: -3.1 to -3.6
        (corresponds to 90-110% efficiency)

    y-intercept
      - Theoretical Ct at 1 copy of target
      - Used to calculate amplification efficiency:
        E = (10^(-1/slope) - 1) * 100%
    </div>

    <h3>What "Good Linearity" Looks Like</h3>
    <ul>
      <li><strong>R<sup>2</sup> &ge; 0.99:</strong> Data points closely follow the regression line with minimal scatter.</li>
      <li><strong>Slope between -3.1 and -3.6:</strong> Amplification efficiency is between 90% and 110%.</li>
      <li><strong>No systematic deviation:</strong> Residuals (differences between observed and predicted values) should be randomly distributed, not showing a pattern (which would indicate non-linearity).</li>
      <li><strong>Consistent across the range:</strong> Precision should not degrade significantly at the extremes of the range.</li>
    </ul>

    <h2>Defining Acceptance Criteria</h2>
    <p>
      Before running validation experiments, you must define acceptance criteria. These should be:
    </p>
    <ul>
      <li><strong>Pre-defined:</strong> Written before testing begins, not adjusted after seeing results.</li>
      <li><strong>Scientifically justified:</strong> Based on clinical requirements, manufacturer claims, or published guidelines.</li>
      <li><strong>Documented:</strong> Recorded in the validation protocol before experiments start.</li>
    </ul>

    <table>
      <thead>
        <tr>
          <th>Validation Study</th>
          <th>Typical Acceptance Criteria</th>
          <th>Source</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>LOD</td>
          <td>&ge; 95% detection at claimed concentration</td>
          <td>CLSI EP17-A2, manufacturer claim</td>
        </tr>
        <tr>
          <td>LOQ</td>
          <td>CV &lt; 20% at claimed concentration</td>
          <td>Laboratory-defined based on clinical need</td>
        </tr>
        <tr>
          <td>Repeatability</td>
          <td>CV &lt; 5% (Ct values)</td>
          <td>Manufacturer claim or CLSI EP05-A3</td>
        </tr>
        <tr>
          <td>Reproducibility</td>
          <td>CV &lt; 10% (Ct values)</td>
          <td>Manufacturer claim or CLSI EP05-A3</td>
        </tr>
        <tr>
          <td>Linearity</td>
          <td>R<sup>2</sup> &ge; 0.99, slope -3.1 to -3.6</td>
          <td>CLSI EP06-A, PCR efficiency standards</td>
        </tr>
      </tbody>
    </table>

    <div class="info-box">
      <strong>OpenQC tip:</strong> The Validation module allows you to select the type of study (LOD, Precision,
      Linearity), upload your dataset, and define custom acceptance criteria. OpenQC performs the statistical
      analysis and generates a validation report that can be included directly in your assay validation documentation.
    </div>
  </div>
</template>
