---
name: email-sender
description: >
  Send emails via common global and Chinese SMTP providers (Gmail, QQ Mail, 163, etc.)
  on behalf of the user or calling agent. Use this skill whenever you need to deliver
  transactional or notification emails from within an agent workflow.
license: MIT
compatibility:
  language: python
  minimum_python: "3.9"
metadata:
  implementation:
    type: cli
    command: python skills/email-sender/scripts/email_sender.py
  io:
    transport: stdin-stdout-or-direct-call
    request_format: json
    response_format: json
resources:
  - path: ../../README.md
    purpose: reference
---

## Purpose

This skill sends emails using SMTP. It is designed for use by agents such as
OpenClaw, Claude Code, or other tooling that supports Anthropic Agent Skills.

It supports:

- International providers like Gmail.
- Chinese providers like QQ Mail and 163 Mail.
- Any other SMTP-compatible mail service, as long as credentials and host/port are provided.

## When to use this skill

Use this skill when:

- You need to send a notification, verification code, or report via email.
- The user has asked you to email content to one or more recipients.
- You are implementing workflow steps that must send email through specific providers.

Do **not** use this skill for:

- Long-term email inbox management.
- POP/IMAP retrieval or complex threading logic (these are out of scope).

## Invocation (CLI / subprocess)

This skill is implemented as a CLI tool that reads a single JSON object from
stdin and writes a single JSON object to stdout.

When used from an agent runtime that prefers subprocess-based tools, run the
command declared in `metadata.implementation.command`:

```bash
echo '{
  "smtp_host": "smtp.qq.com",
  "smtp_port": 465,
  "use_ssl": true,
  "username": "your_account@qq.com",
  "password": "your_smtp_or_app_password",
  "from_addr": "your_account@qq.com",
  "to_addrs": ["target@example.com"],
  "subject": "Hello from OpenClaw",
  "body": "This is a test email from the OpenClaw email skill.",
  "body_type": "plain"
}' | python skills/email-sender/scripts/email_sender.py
```

The script reads a single line of JSON from stdin and prints a single line of
JSON to stdout with this structure:

- `ok` (bool): whether sending was successful.
- `message_id` (str | null): SMTP message-id if available.
- `error` (str | null): error message if any.

## Configuration

### Environment variables

- `EMAIL_DEFAULT_FROM` (optional): default sender address if `from_addr`
  is not provided in the payload. If this is also missing, the SMTP
  username will be used as the sender address.

### SMTP provider examples

These are common SMTP endpoints; always confirm with provider documentation:

- Gmail: `smtp.gmail.com:587` (TLS)
- QQ Mail: `smtp.qq.com:465` (SSL) or `smtp.qq.com:587` (TLS)
- 163 Mail: `smtp.163.com:465` (SSL) or `smtp.163.com:25/587` (TLS)

## Safety & permissions

- Never hard-code credentials; consume them from secure configuration
  management or secrets storage.
- Be explicit about who should receive emails and why.
- Avoid sending sensitive information in cleartext email bodies unless
  the user explicitly requests it and understands the risk.

