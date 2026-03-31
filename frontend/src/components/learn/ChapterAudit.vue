<script setup>
</script>

<template>
  <div class="learn-content">
    <h1>Chapter 5: Audit Trail and Regulatory Compliance</h1>
    <p class="chapter-subtitle">How OpenQC ensures data integrity through cryptographic audit trails.</p>

    <h2>Why Audit Trails Matter</h2>
    <p>
      An audit trail is a chronological record of all activities that affect data within a system. In clinical
      laboratories, audit trails serve two critical purposes: they enable <strong>accountability</strong> (who did
      what, and when) and they enable <strong>integrity verification</strong> (has any data been altered after the fact).
    </p>
    <p>
      Regulatory frameworks worldwide require robust audit trails for any system that generates, processes, or stores
      data used for clinical decision-making:
    </p>

    <table>
      <thead>
        <tr>
          <th>Standard</th>
          <th>Audit Trail Requirements</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>ISO 15189:2022</strong></td>
          <td>Section 7.11.3 requires the laboratory to maintain records of all changes to controlled documents and data, including who made the change and when.</td>
        </tr>
        <tr>
          <td><strong>CE-IVD / IVDR</strong></td>
          <td>Annex I, Section 16 requires traceability of all data and processes. Software used for IVD purposes must maintain audit trails.</td>
        </tr>
        <tr>
          <td><strong>CDSCO</strong></td>
          <td>Medical Device Rules 2017 (India) require maintenance of records demonstrating compliance with quality management system requirements, aligned with ISO 13485.</td>
        </tr>
        <tr>
          <td><strong>21 CFR Part 11 (FDA)</strong></td>
          <td>US FDA regulation for electronic records requires computer-generated, time-stamped audit trails that record the date, time, operator, and nature of changes.</td>
        </tr>
        <tr>
          <td><strong>CAP</strong></td>
          <td>Accreditation checklists require documentation of all corrective actions, instrument maintenance, and QC decisions.</td>
        </tr>
      </tbody>
    </table>

    <h2>SHA-256 File Hashing Explained</h2>
    <p>
      OpenQC uses <strong>SHA-256</strong> (Secure Hash Algorithm, 256-bit) to create a unique digital fingerprint
      of every audit trail entry. SHA-256 is a cryptographic hash function that takes any input data and produces a
      fixed-length, 256-bit (64 hexadecimal character) output.
    </p>

    <h3>Key Properties</h3>
    <ul>
      <li>
        <strong>Deterministic:</strong> The same input always produces the same hash. If you hash the same audit
        trail entry twice, you get the same result.
      </li>
      <li>
        <strong>Avalanche effect:</strong> Even a tiny change to the input (a single character) produces a
        completely different hash. This makes tampering immediately detectable.
      </li>
      <li>
        <strong>One-way function:</strong> You cannot reverse-engineer the original data from the hash. The hash
        proves what the data was, without exposing the data itself.
      </li>
      <li>
        <strong>Collision resistant:</strong> It is computationally infeasible to find two different inputs that
        produce the same hash.
      </li>
    </ul>

    <div class="diagram">
  SHA-256 Hashing Example:

  Input: "QC run uploaded: run_id=42, file=sample_qc.xlsx, user=labtech1"

  SHA-256 Hash:
  a7f3b2c1d4e5f6a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2

  Now change ONE character ("run_id=43" instead of "run_id=42"):

  Input: "QC run uploaded: run_id=43, file=sample_qc.xlsx, user=labtech1"

  SHA-256 Hash:
  e1d2c3b4a5f6e7d8c9b0a1f2e3d4c5b6a7f8e9d0c1b2a3f4e5d6c7b8a9f0e1d2

  Completely different hash — tampering is immediately evident.
    </div>

    <h2>Hash Chain Integrity</h2>
    <p>
      OpenQC does not just hash individual entries — it creates a <strong>hash chain</strong> where each entry's
      hash includes the hash of the previous entry. This creates an unbreakable chronological chain similar to
      blockchain technology.
    </p>

    <div class="diagram">
  Hash Chain Structure:

  Entry 1                    Entry 2                    Entry 3
  +---------------------+   +---------------------+   +---------------------+
  | Action: Upload       |   | Action: Analyze      |   | Action: Export       |
  | Timestamp: 10:00:01  |   | Timestamp: 10:00:05  |   | Timestamp: 10:00:12  |
  | User: labtech1       |   | User: labtech1       |   | User: labtech1       |
  | Previous: 000000     |   | Previous: a7f3b2...  |   | Previous: e1d2c3...  |
  |                      |   |                      |   |                      |
  | Hash: a7f3b2...      |-->| Hash: e1d2c3...      |-->| Hash: b4c5d6...      |
  +---------------------+   +---------------------+   +---------------------+

  Each entry's hash is computed from:
    - The entry's own data (action, timestamp, user, details)
    - The hash of the PREVIOUS entry

  This means modifying ANY entry invalidates ALL subsequent hashes.
    </div>

    <h3>Why This Matters</h3>
    <p>
      Suppose someone attempts to modify Entry 2 (e.g., changing an analysis result). The modification would change
      Entry 2's hash. But Entry 3's hash was computed using Entry 2's original hash. Now Entry 3's recorded hash
      no longer matches what you would compute from the current data — the chain is broken. The tampering is
      detected automatically.
    </p>
    <p>
      To successfully tamper with the audit trail, an attacker would need to recompute the hashes of the modified
      entry and <em>every subsequent entry</em> in the chain. OpenQC's verification process detects this by
      recomputing the entire chain from scratch and comparing against the stored hashes.
    </p>

    <h2>Tamper Detection</h2>
    <p>
      OpenQC provides built-in tamper detection that can be run at any time:
    </p>
    <ol>
      <li>The system retrieves all audit trail entries in chronological order.</li>
      <li>Starting from the first entry, it recomputes the SHA-256 hash using the entry's data and the previous entry's hash.</li>
      <li>The recomputed hash is compared against the stored hash for each entry.</li>
      <li>If any hash does not match, the system identifies the exact entry where the chain was broken and flags it as potentially tampered.</li>
    </ol>

    <div class="warning-box">
      <strong>What happens when tampering is detected:</strong> OpenQC displays a clear warning identifying
      which entry in the chain has been compromised. The laboratory should immediately investigate, document the
      finding, and report it to the quality manager. Any patient results associated with the tampered period should
      be reviewed.
    </div>

    <h2>Regulatory Export</h2>
    <p>
      During regulatory audits and accreditation inspections, auditors need access to complete, verifiable audit
      trails. OpenQC supports exporting audit trail data in formats suitable for regulatory review:
    </p>
    <ul>
      <li>
        <strong>Complete chronological record:</strong> Every action performed in the system — uploads, analyses,
        exports, configuration changes — with timestamps, user identification, and details.
      </li>
      <li>
        <strong>Hash verification report:</strong> A summary showing the integrity status of the entire audit chain,
        confirming that no entries have been modified.
      </li>
      <li>
        <strong>Filtered views:</strong> The ability to filter by date range, user, action type, or specific
        assay/instrument — so auditors can focus on the relevant time period.
      </li>
      <li>
        <strong>Export formats:</strong> Data can be exported as structured files (CSV, JSON) that auditors can
        independently verify.
      </li>
    </ul>

    <div class="info-box">
      <strong>Best practice:</strong> Run the audit trail integrity check regularly (at least monthly) and before
      any regulatory inspection. Document the verification results as part of your quality management system.
      This proactive approach demonstrates to auditors that your laboratory takes data integrity seriously.
    </div>
  </div>
</template>
