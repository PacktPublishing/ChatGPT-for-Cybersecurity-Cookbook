# Sample Scenario 1: Suspicious Network Activity

## Context:

You are a cybersecurity analyst at CyberGuard Inc., and you have noticed some suspicious network activity that seems to be bypassing the current detection rules. After analyzing the network logs, you discover a recurring pattern where an unknown external IP is making multiple failed SSH login attempts on one of your critical servers.

## Findings:

1. **External IP Address: `192.168.1.101`** (Note: This is a placeholder IP for the purpose of this scenario)
2. **Targeted Server: `Server-XYZ`**
3. **SSH Port: `22`**
4. **Frequency:** High (multiple failed attempts in short intervals)
5. **Pattern:** All attempts are using the username `admin`

## Objectives:

- You want to create a custom YARA rule that will alert you whenever this specific pattern of failed SSH attempts occurs.
- This rule should be specific enough to not trigger alerts for legitimate SSH traffic or random failed attempts.

This sample scenario can be used as a basis for drafting a YARA rule using ChatGPT, testing it, refining it, and finally deploying it in a threat detection system.