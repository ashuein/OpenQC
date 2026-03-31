# Regulatory Reference Documents

This folder is a placeholder for regulatory and standards documents relevant to IVD quality control and method validation in India and internationally. These documents are **not included** in the repository due to copyright restrictions but can be downloaded from the respective regulatory body websites.

---

## Recommended Documents

### CDSCO (Central Drugs Standard Control Organisation)

1. **MD-15: Medical Devices Rules, 2017 (as amended)**
   - Covers registration, manufacture, import, sale, and distribution of medical devices and IVDs in India.
   - Download from: https://cdsco.gov.in/opencms/opencms/en/Medical-Device-Diagnostics/Medical-Device-Diagnostics/

2. **CDSCO IVD Performance Evaluation Guidance**
   - Guidance for performance evaluation of in vitro diagnostic medical devices.
   - Download from: https://cdsco.gov.in/opencms/opencms/en/Medical-Device-Diagnostics/Medical-Device-Diagnostics/

### ICMR (Indian Council of Medical Research)

3. **ICMR Guidelines for Diagnostic Laboratory Validation**
   - Guidelines for validation and verification of diagnostic assays in Indian clinical laboratories.
   - Download from: https://www.icmr.gov.in/ or https://main.icmr.nic.in/

4. **ICMR National Guidelines for Quality Assurance in Public Health Laboratories**
   - Comprehensive QA framework for government and accredited laboratories.

### ISO / IEC Standards

5. **ISO 15189:2022 - Medical laboratories: Requirements for quality and competence**
   - The primary international standard for medical laboratory accreditation. Covers QC, method validation, measurement uncertainty, and competence requirements.
   - Purchase from: https://www.iso.org/standard/76677.html
   - Note: Summary/overview materials may be available from NABL (National Accreditation Board for Testing and Calibration Laboratories) at https://nabl-india.org/

6. **ISO 20914:2019 - Medical laboratories: Practical guidance for the estimation of measurement uncertainty**
   - Guidance specific to clinical laboratory measurement uncertainty estimation.
   - Purchase from: https://www.iso.org/standard/69445.html

### NABL (National Accreditation Board for Testing and Calibration Laboratories)

7. **NABL 112: Specific Criteria for Accreditation of Medical Laboratories**
   - Indian accreditation criteria aligned with ISO 15189, including QC and validation requirements.
   - Download from: https://nabl-india.org/

### CLSI (Clinical and Laboratory Standards Institute)

8. **EP05-A3: Evaluation of Precision of Quantitative Measurement Procedures**
   - Standard method for evaluating intra-run and inter-run precision.

9. **EP06-Ed2: Evaluation of Linearity of Quantitative Measurement Procedures**
   - Standard method for linearity and reportable range assessment.

10. **EP17-A2: Evaluation of Detection Capability for Clinical Laboratory Measurement Procedures**
    - Covers LOB, LOD, and LOQ determination.

11. **EP15-A3: User Verification of Quantitative Measurement Procedures**
    - Guidance for method verification in the user laboratory.

---

## How These Documents Relate to OpenQC Modules

| Document | OpenQC Module |
|----------|--------------|
| ISO 15189 (Section 7.3) | QC Monitor (IQC requirements) |
| CLSI EP17-A2 | Validation: LOD/LOQ studies |
| CLSI EP05-A3 | Validation: Precision studies |
| CLSI EP06-Ed2 | Validation: Linearity studies |
| CLSI EP15-A3 | Validation: Method verification |
| ISO 20914 | Measurement uncertainty estimation |
| CDSCO MD-15 | Regulatory compliance (India) |
| ICMR Guidelines | Lab accreditation (India) |
| NABL 112 | Accreditation criteria (India) |

---

## Usage

Place downloaded PDF files directly in this folder. The OpenQC application can reference these documents in generated validation reports and SOP cross-references.

Suggested file naming convention:
```
ISO_15189_2022_summary.pdf
CDSCO_MD15_2017_amended.pdf
ICMR_diagnostic_validation_guidelines.pdf
NABL_112_medical_labs.pdf
CLSI_EP17A2_detection_capability.pdf
```
