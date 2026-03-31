<script setup>
</script>

<template>
  <div class="learn-content">
    <h1>Chapter 2: Westgard Rules Explained</h1>
    <p class="chapter-subtitle">The statistical rules that determine whether a QC run should be accepted or rejected.</p>

    <h2>History: Who Is James Westgard?</h2>
    <p>
      Dr. James O. Westgard is an American clinical chemist who, along with colleagues, published the foundational
      paper on multi-rule QC in 1981. Before Westgard's work, laboratories relied on simple control limits (typically
      mean +/- 2SD or +/- 3SD) to accept or reject analytical runs. These single-rule approaches had significant
      limitations: a 2SD rule rejected too many runs that were actually acceptable (high false rejection rate), while
      a 3SD rule missed too many runs that had genuine errors (poor error detection).
    </p>
    <p>
      Westgard's insight was to combine multiple rules in a sequential evaluation. By using different rules to detect
      different types of errors — random error, systematic error, and trends — the multi-rule approach achieves both
      low false rejection rates and high error detection. This "Westgard multi-rule" system has become the worldwide
      standard for clinical laboratory QC.
    </p>

    <h2>The Levey-Jennings Chart</h2>
    <p>
      The Levey-Jennings (L-J) chart is the primary visual tool for QC monitoring. It plots control values over time
      against statistical limits derived from the control material's established mean and standard deviation (SD).
    </p>

    <div class="diagram">
  Levey-Jennings Chart Structure

  Ct
  value
    |
  +3SD -------.------.-------.------- Reject zone (1-3s rule)
    |         |      |       |
  +2SD -------.------.-------.------- Warning zone (1-2s rule)
    |         |      |       |
  +1SD -------.------.-------.-------
    |         |      |       |
  Mean =======#======#=======#======= Central line
    |         |      |       |
  -1SD -------.------.-------.-------
    |         |      |       |
  -2SD -------.------.-------.------- Warning zone (1-2s rule)
    |         |      |       |
  -3SD -------.------.-------.------- Reject zone (1-3s rule)
    |
    +----1----2----3----4----5----6-- Run number (time)

  Each data point (.) represents a single QC measurement.
  Points within +/-2SD are considered acceptable.
  Points between +/-2SD and +/-3SD trigger warnings.
  Points beyond +/-3SD trigger rejection.
    </div>

    <h3>How to Read the Chart</h3>
    <ul>
      <li><strong>The center line</strong> represents the established mean Ct value for the control material, calculated from at least 20 data points during the validation period.</li>
      <li><strong>The SD lines</strong> (at +/-1SD, +/-2SD, +/-3SD) divide the chart into zones. Approximately 68% of values should fall within +/-1SD, 95% within +/-2SD, and 99.7% within +/-3SD.</li>
      <li><strong>The trend over time</strong> is as important as individual points. A gradual drift toward one side of the mean, even if no single point exceeds 2SD, may indicate a developing systematic error.</li>
    </ul>

    <h2>Mean, SD, and z-Scores in QC Context</h2>
    <p>
      Before applying Westgard rules, the laboratory must establish the statistical parameters for each control level:
    </p>
    <ul>
      <li><strong>Mean:</strong> The average Ct value from the validation dataset (minimum 20 runs, ideally performed over 20 different days to capture inter-day variation).</li>
      <li><strong>Standard Deviation (SD):</strong> A measure of the spread of Ct values around the mean. A smaller SD indicates higher precision.</li>
      <li><strong>z-score:</strong> The number of standard deviations a data point is from the mean. Calculated as: <code>z = (observed - mean) / SD</code>. A z-score of +2.0 means the value is exactly 2 SD above the mean.</li>
    </ul>
    <p>
      Westgard rules are fundamentally based on z-scores, though they are often expressed in terms of SD units for clarity.
    </p>

    <h2>The Six Westgard Rules</h2>
    <p>
      OpenQC evaluates the following six rules in the order shown. The first rule (<strong>1-2s</strong>) is a warning
      that triggers evaluation of the remaining rejection rules.
    </p>

    <h3>1-2s Rule (Warning)</h3>
    <p>
      <strong>Definition:</strong> A single control observation exceeds the mean +/- 2SD.
    </p>
    <p>
      <strong>Interpretation:</strong> This is a <em>warning rule only</em> — it does not by itself cause rejection.
      When a 1-2s violation is detected, the remaining rejection rules must be evaluated. Approximately 1 in 20 (5%)
      of all QC values will exceed +/-2SD by chance alone in a normally distributed dataset, so this rule serves as a
      screening trigger.
    </p>
    <div class="diagram">
  1-2s Rule: Warning — one point beyond +/-2SD

  +3SD  --------------------------------
  +2SD  --------------------------------
  +1SD  ------*----*---------*----------
  Mean  ==*==========*===*==============
  -1SD  ------------------*-------------
  -2SD  -------=---------=--------------
  -3SD  --------------------------------
              Run:  1  2  3  4  5  6  7

  Example: Point at run 3 is above +2SD.
  Action:  Trigger warning, evaluate rejection rules.
    </div>

    <h3>1-3s Rule (Reject)</h3>
    <p>
      <strong>Definition:</strong> A single control observation exceeds the mean +/- 3SD.
    </p>
    <p>
      <strong>Interpretation:</strong> This indicates a large random error or the start of a major systematic error.
      Statistically, only about 0.3% of values should fall beyond +/-3SD. When this occurs, the run must be rejected.
      Common causes include sample mix-up, pipetting error, reagent failure, or instrument malfunction.
    </p>
    <div class="diagram">
  1-3s Rule: Reject — one point beyond +/-3SD

  +3SD  --------.--X--------------------  X = violation
  +2SD  --------.--.--------------------
  +1SD  ---*----.--.-------*------------
  Mean  ===========.===*================
  -1SD  --------.---.------------------
  -2SD  --------.--.--------------------
  -3SD  --------.---.-------------------
              Run:  1  2  3  4  5  6  7

  Example: Point at run 2 exceeds +3SD.
  Action:  Reject the run immediately.
    </div>

    <h3>2-2s Rule (Reject)</h3>
    <p>
      <strong>Definition:</strong> Two consecutive control observations exceed the mean + 2SD or both exceed the mean - 2SD
      (i.e., two consecutive points on the <em>same side</em> beyond +/-2SD).
    </p>
    <p>
      <strong>Interpretation:</strong> This rule detects systematic error — a consistent shift or bias in one
      direction. It can apply within a single run (if multiple controls are measured) or across consecutive runs.
      Common causes include calibration drift, deteriorating reagent lot, or changes in environmental conditions.
    </p>
    <div class="diagram">
  2-2s Rule: Reject — two consecutive beyond +/-2SD (same side)

  +3SD  --------------------------------
  +2SD  ------X---X---------------------  X = violations
  +1SD  --*---------*----*--------------
  Mean  ================================
  -1SD  --------------------*-----------
  -2SD  --------------------------------
  -3SD  --------------------------------
            Run:  1  2  3  4  5  6  7

  Example: Runs 2 and 3 both exceed +2SD.
  Action:  Reject — systematic error detected.
    </div>

    <h3>R-4s Rule (Reject)</h3>
    <p>
      <strong>Definition:</strong> The range between two control observations within a single run exceeds 4SD (one
      control exceeds +2SD while the other is below -2SD, or vice versa).
    </p>
    <p>
      <strong>Interpretation:</strong> This rule detects large random error within a single analytical run. It only
      applies when two different control levels (e.g., L1 and L2) are measured in the same run. If one is high and the
      other is low, the total spread (range) indicates poor precision. Common causes include a pipetting error on one
      of the controls, a bubble in the optical path, or well-to-well variability.
    </p>
    <div class="diagram">
  R-4s Rule: Reject — within-run range exceeds 4SD

  +3SD  --------X (L1)------------------  X = violation
  +2SD  --------------------------------
  +1SD  --------------------------------
  Mean  ================================
  -1SD  --------------------------------
  -2SD  --------------------------------
  -3SD  --------X (L2)------------------  X = violation
                 |
                 |-- Range = 6SD (exceeds 4SD)
                 |
            Within single run

  Example: L1 at +3SD, L2 at -3SD in the same run.
  Action:  Reject — large random error.
    </div>

    <h3>4-1s Rule (Reject)</h3>
    <p>
      <strong>Definition:</strong> Four consecutive control observations exceed the mean + 1SD or all four exceed the
      mean - 1SD (i.e., four consecutive on the <em>same side</em> beyond +/-1SD).
    </p>
    <p>
      <strong>Interpretation:</strong> This rule detects a small but persistent systematic error. Each individual point
      may appear acceptable, but the pattern of four consecutive points all shifted in the same direction is statistically
      unlikely (probability ~6% under normal conditions) and indicates a real bias. Common causes include gradual
      reagent deterioration, subtle instrument drift, or a new lot of control material with a slightly different
      target value.
    </p>
    <div class="diagram">
  4-1s Rule: Reject — four consecutive beyond +/-1SD (same side)

  +3SD  --------------------------------
  +2SD  --------------------------------
  +1SD  ------X---X---X---X-------------  X = violations
  Mean  ================================
  -1SD  --*-------------------*---------
  -2SD  --------------------------------
  -3SD  --------------------------------
            Run:  1  2  3  4  5  6  7

  Example: Runs 2-5 are all above +1SD.
  Action:  Reject — systematic shift detected.
    </div>

    <h3>10x Rule (Reject)</h3>
    <p>
      <strong>Definition:</strong> Ten consecutive control observations fall on the same side of the mean (regardless
      of how far from the mean they are).
    </p>
    <p>
      <strong>Interpretation:</strong> This rule detects a very small but sustained systematic error or bias. Each
      individual point may be well within acceptable limits, but the probability of ten consecutive points all falling
      on the same side of the mean by chance is approximately 0.1% (2<sup>-10</sup>). This pattern is a strong
      indicator of a real shift in the analytical system. Common causes include a slow change in reagent concentration
      over weeks, environmental drift, or a subtle change in instrument calibration.
    </p>
    <div class="diagram">
  10x Rule: Reject — ten consecutive on same side of mean

  +3SD  --------------------------------
  +2SD  --------------------------------
  +1SD  --*---*-------*-----*---*-------
  Mean  ================================
  -1SD  -------=--*-----*--------=--*---
  -2SD  --------------------------------
  -3SD  --------------------------------
            Run:  1  2  3  4  5  6  7  8  9 10 11 12

  Example: Runs 1-10 are all above the mean.
  Some are barely above, some are near +1SD,
  but ALL are on the same side.
  Action:  Reject — sustained bias detected.
    </div>

    <h2>Summary of Westgard Rules</h2>

    <table>
      <thead>
        <tr>
          <th>Rule</th>
          <th>Type</th>
          <th>Condition</th>
          <th>Error Detected</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>1-2s</strong></td>
          <td>Warning</td>
          <td>1 point beyond +/-2SD</td>
          <td>Screening trigger</td>
          <td>Evaluate other rules</td>
        </tr>
        <tr>
          <td><strong>1-3s</strong></td>
          <td>Reject</td>
          <td>1 point beyond +/-3SD</td>
          <td>Large random error</td>
          <td>Reject run</td>
        </tr>
        <tr>
          <td><strong>2-2s</strong></td>
          <td>Reject</td>
          <td>2 consecutive beyond +/-2SD, same side</td>
          <td>Systematic error</td>
          <td>Reject run</td>
        </tr>
        <tr>
          <td><strong>R-4s</strong></td>
          <td>Reject</td>
          <td>Within-run range exceeds 4SD</td>
          <td>Large random error</td>
          <td>Reject run</td>
        </tr>
        <tr>
          <td><strong>4-1s</strong></td>
          <td>Reject</td>
          <td>4 consecutive beyond +/-1SD, same side</td>
          <td>Systematic error</td>
          <td>Reject run</td>
        </tr>
        <tr>
          <td><strong>10x</strong></td>
          <td>Reject</td>
          <td>10 consecutive on same side of mean</td>
          <td>Small sustained bias</td>
          <td>Reject run</td>
        </tr>
      </tbody>
    </table>

    <h2>Rule Evaluation Order and the Multi-Rule Approach</h2>
    <p>
      The Westgard multi-rule system is designed to be evaluated in a specific order:
    </p>
    <ol>
      <li>Check the current data point against the <strong>1-2s</strong> rule. If the point is within +/-2SD, the run passes — no further evaluation is needed.</li>
      <li>If 1-2s is triggered (warning), check <strong>1-3s</strong>. If the point exceeds +/-3SD, reject immediately.</li>
      <li>If 1-3s is not triggered, check <strong>2-2s</strong> using the current and previous data points.</li>
      <li>Check <strong>R-4s</strong> if multiple control levels were measured in the same run.</li>
      <li>Check <strong>4-1s</strong> using the current and preceding three data points.</li>
      <li>Check <strong>10x</strong> using the current and preceding nine data points.</li>
    </ol>
    <p>
      This sequential approach minimizes false rejections while maintaining high sensitivity to real analytical errors.
      OpenQC implements this exact evaluation order automatically when analyzing uploaded QC data.
    </p>

    <h2>When to Reject a Run vs. Investigate</h2>
    <p>
      Not all rule violations require the same response:
    </p>
    <ul>
      <li><strong>1-2s warning only:</strong> Do not reject. Document and monitor. If the next run is normal, the single outlier was likely random variation.</li>
      <li><strong>1-3s violation:</strong> Reject the run. Repeat with fresh controls. If the repeat passes, the original failure was likely a random event (pipetting error, bubble). If the repeat also fails, investigate deeper (reagent lot, instrument calibration).</li>
      <li><strong>2-2s or 4-1s violation:</strong> Indicates systematic error. Check recent changes: new reagent lot? New control lot? Instrument maintenance? Operator change? Environmental change (temperature, humidity)?</li>
      <li><strong>R-4s violation:</strong> Check for within-run problems: pipetting technique, sample integrity, well position effects.</li>
      <li><strong>10x violation:</strong> Review the trend over the past several runs. This often signals a gradual shift that needs recalibration or new baseline establishment.</li>
    </ul>

    <div class="warning-box">
      <strong>Important:</strong> Never suppress or ignore a Westgard violation. Every violation must be documented,
      investigated, and resolved. Regulatory auditors will review your QC records and expect to see evidence of
      corrective action for every out-of-control event.
    </div>
  </div>
</template>
