# Sample Scenario 2: Malware Infection via Email Attachment

## Context:

You're a cybersecurity analyst for a financial institution. Your organization has been receiving phishing emails that contain a malicious PDF attachment. Generic detection rules haven't been effective in catching this particular threat.

## Findings:

1. **Email Subject:** "Invoice Details - Urgent"
2. **Sender Email:** Varies, but always from a free email service like Gmail or Yahoo.
3. **Attachment:** A PDF file named `Invoice_details.pdf`
4. **Malicious Behavior:** Once opened, the PDF tries to execute a script that writes a small `.txt` file to the `C:\Windows\Temp directory`.
5. **Text File Content:** The text file contains an encoded script designed to download additional payloads.

## Objectives:

- Your goal is to create a custom YARA rule that identifies emails with this specific pattern of behavior.
- The rule should catch the email based on its subject, sender's domain, and the behavior of the attached PDF.

Having two scenarios will allow readers to gain a more comprehensive understanding of how to create custom YARA rules for different types of threats.