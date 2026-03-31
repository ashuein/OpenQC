<script setup>
</script>

<template>
  <div class="learn-content">
    <h1>Chapter 3: Six Sigma in the Laboratory</h1>
    <p class="chapter-subtitle">Using Sigma metrics to objectively measure assay quality and design optimal QC strategies.</p>

    <h2>What Six Sigma Means for Lab Quality</h2>
    <p>
      Six Sigma is a quality management methodology originally developed by Motorola in the 1980s and popularized by
      General Electric. In manufacturing, Six Sigma aims for no more than 3.4 defects per million opportunities. When
      applied to the clinical laboratory, it provides a universal metric for measuring how well an analytical method
      performs relative to its quality requirements.
    </p>
    <p>
      The core idea is simple: compare the <strong>allowable total error</strong> (how much error is acceptable) to the
      <strong>actual error</strong> (how much error the method actually produces). The ratio, expressed as a Sigma
      metric, tells you how many standard deviations of "safety margin" exist between your method's performance and the
      point at which it would produce clinically unacceptable results.
    </p>
    <p>
      A higher Sigma value means a more reliable method with a larger safety margin. A lower Sigma value means the
      method is operating close to its quality limit and requires more stringent QC to catch errors before they
      affect patient results.
    </p>

    <h2>The Sigma Metric Formula</h2>
    <p>
      The Sigma metric for a laboratory method is calculated as:
    </p>
    <pre class="diagram">
             TEa - |Bias|
      sigma = -----------
                 CV

  Where:
    TEa   = Total allowable error (%)
    Bias  = Systematic error / inaccuracy (%)
    CV    = Coefficient of variation / imprecision (%)
    </pre>

    <h3>Understanding Each Component</h3>
    <ul>
      <li>
        <strong>TEa (Total Allowable Error):</strong> The maximum amount of error that is acceptable for a given
        analyte without affecting clinical decision-making. TEa values are established by regulatory bodies, biological
        variation databases, and expert consensus. For example, if TEa for a SARS-CoV-2 Ct value is 15%, the method
        must produce results within 15% of the true value.
      </li>
      <li>
        <strong>Bias:</strong> The systematic error component — the consistent difference between the method's average
        result and the true (reference) value. Bias is typically estimated from proficiency testing (external QA),
        method comparison studies, or recovery experiments. It is expressed as a percentage.
      </li>
      <li>
        <strong>CV (Coefficient of Variation):</strong> The random error component — the imprecision of the method
        expressed as a percentage of the mean. CV is calculated from QC data as <code>(SD / mean) x 100</code>. It
        represents the run-to-run variability of the method.
      </li>
    </ul>

    <h2>Sigma Classification Bands</h2>
    <p>
      Sigma values are classified into performance bands that directly inform QC design decisions:
    </p>

    <table>
      <thead>
        <tr>
          <th>Sigma</th>
          <th>Classification</th>
          <th>Defect Rate</th>
          <th>QC Implications</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>&ge; 6</strong></td>
          <td style="color: #43A047;">World Class</td>
          <td>3.4 per million</td>
          <td>Minimal QC needed. Simple rules (1-3s) with N=2 controls suffice.</td>
        </tr>
        <tr>
          <td><strong>5 - 6</strong></td>
          <td style="color: #66BB6A;">Excellent</td>
          <td>233 per million</td>
          <td>Standard QC. Westgard multi-rules with N=2 controls.</td>
        </tr>
        <tr>
          <td><strong>4 - 5</strong></td>
          <td style="color: #F9A825;">Good</td>
          <td>6,210 per million</td>
          <td>Enhanced QC required. Multi-rules with N=4 controls recommended.</td>
        </tr>
        <tr>
          <td><strong>3 - 4</strong></td>
          <td style="color: #FF9800;">Marginal</td>
          <td>66,807 per million</td>
          <td>Maximum QC needed. Multi-rules with N=4 and tight limits. Consider method improvement.</td>
        </tr>
        <tr>
          <td><strong>2 - 3</strong></td>
          <td style="color: #E53935;">Poor</td>
          <td>308,538 per million</td>
          <td>Unacceptable for routine use without significant improvement. May need method change.</td>
        </tr>
        <tr>
          <td><strong>&lt; 2</strong></td>
          <td style="color: #B71C1C;">Unacceptable</td>
          <td>&gt;308,538 per million</td>
          <td>Method cannot meet quality requirements. Replace or fundamentally redesign.</td>
        </tr>
      </tbody>
    </table>

    <h2>The NMEDx (Normalized Method Decision) Chart</h2>
    <p>
      The NMEDx chart is a visual tool that plots a method's performance in a two-dimensional space with imprecision
      (CV as a fraction of TEa) on the x-axis and bias (as a fraction of TEa) on the y-axis. This normalization allows
      methods with different TEa values to be compared on the same chart.
    </p>
    <pre class="diagram">
  NMEDx Chart (Normalized Method Decision Chart)

  Bias/TEa
  1.0 |                                    Unacceptable
      |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
  0.8 |     .                                  .
      |        .     Poor (2-3 sigma)       .
  0.6 |           .                      .
      |              .  Marginal       .
  0.4 |                 . (3-4)     .
      |                    .     .    Good (4-5 sigma)
  0.2 |                       .
      |          Excellent  .     World Class (>=6)
  0.0 +---+---+---+---+---+---+---+---+---+--> CV/TEa
      0  0.05 0.10 0.15 0.20 0.25 0.30 0.35

  Lines represent constant Sigma values.
  Methods in the lower-left have better performance.
  Methods in the upper-right need improvement.
    </pre>

    <p>
      The NMEDx chart in OpenQC color-codes each plotted method according to its Sigma band, making it immediately
      clear which assays are performing well and which need attention.
    </p>

    <h2>How Sigma Score Drives QC Design</h2>
    <p>
      The practical power of the Sigma metric is that it directly determines which QC rules and how many controls are
      needed. High-Sigma methods need less QC because errors large enough to affect patients are extremely rare.
      Low-Sigma methods need aggressive QC because the method is operating close to its quality limit.
    </p>

    <table>
      <thead>
        <tr>
          <th>Sigma</th>
          <th>Recommended QC Rules</th>
          <th>Controls per Run</th>
          <th>Frequency</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>&ge; 6</strong></td>
          <td>1-3s only</td>
          <td>N = 2</td>
          <td>Standard (every run or daily)</td>
        </tr>
        <tr>
          <td><strong>5 - 6</strong></td>
          <td>1-3s / 2-2s / R-4s</td>
          <td>N = 2</td>
          <td>Standard</td>
        </tr>
        <tr>
          <td><strong>4 - 5</strong></td>
          <td>1-3s / 2-2s / R-4s / 4-1s</td>
          <td>N = 4</td>
          <td>Every run</td>
        </tr>
        <tr>
          <td><strong>3 - 4</strong></td>
          <td>Full Westgard multi-rules</td>
          <td>N = 4</td>
          <td>Every run, with repeat testing</td>
        </tr>
        <tr>
          <td><strong>&lt; 3</strong></td>
          <td>QC alone is insufficient</td>
          <td>N/A</td>
          <td>Method improvement required before QC design</td>
        </tr>
      </tbody>
    </table>

    <div class="info-box">
      <strong>Practical tip:</strong> When OpenQC calculates the Sigma metric for your assay, it automatically
      recommends the appropriate QC rules and control strategy based on the table above. Use the Sigma Analysis
      module to evaluate each assay in your laboratory.
    </div>

    <h2>TEa Sources</h2>
    <p>
      Selecting the appropriate TEa is critical — it defines the quality goal against which the Sigma metric is
      calculated. Common sources include:
    </p>
    <ul>
      <li>
        <strong>CLIA (Clinical Laboratory Improvement Amendments):</strong> The US federal program publishes fixed
        allowable error limits for regulated analytes. These are widely used as a baseline, though they may be
        broader than biologically derived goals.
      </li>
      <li>
        <strong>Biological Variation Databases:</strong> TEa can be derived from within-subject and between-subject
        biological variation using the formula <code>TEa = 1.65 * CV_i + 0.25 * (CV_i² + CV_g²)^0.5</code>, where
        CV_i is within-individual variation and CV_g is between-individual variation. The European Federation of
        Clinical Chemistry (EFLM) maintains a comprehensive biological variation database.
      </li>
      <li>
        <strong>CDSCO (Central Drugs Standard Control Organisation):</strong> India's regulatory body references
        ISO 15189 and manufacturer-specified performance requirements. For IVD devices marketed in India, the
        manufacturer's claimed performance specifications serve as the TEa benchmark.
      </li>
      <li>
        <strong>Clinical Decision Limits:</strong> For some analytes, TEa is derived from the clinical decision
        point — the concentration at which a diagnostic decision changes. The allowable error must be small enough
        that a result near the decision point is reliably classified.
      </li>
      <li>
        <strong>Expert Consensus (e.g., RCPA, RiliBaK):</strong> Professional organizations in various countries
        publish consensus-based quality goals. The Royal College of Pathologists of Australasia (RCPA) and the
        German Medical Association (RiliBaK) guidelines are commonly referenced.
      </li>
    </ul>

    <div class="warning-box">
      <strong>Important:</strong> Always document the source of your TEa values. During regulatory audits, you will
      need to justify why a particular TEa was chosen for each analyte. Using a recognized published source
      (CLIA, biological variation, or manufacturer claims) provides the strongest defensible position.
    </div>
  </div>
</template>
