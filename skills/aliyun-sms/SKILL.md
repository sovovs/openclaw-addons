---
name: aliyun-sms
description: >
  Send SMS messages using Alibaba Cloud (Aliyun) SMS service, typically for
  verification codes and notification messages to Chinese phone numbers.
license: MIT
compatibility:
  language: python
  minimum_python: "3.9"
metadata:
  implementation:
    type: cli
    command: python skills/aliyun-sms/scripts/aliyun_sms.py
  io:
    transport: stdin-stdout-or-direct-call
    request_format: json
    response_format: json
resources:
  - path: ../../README.md
    purpose: reference
---

## Purpose

This skill sends SMS messages via the Aliyun SMS service. It is intended for
agents (e.g., OpenClaw, Claude Code, or other Anthropic-compatible runtimes)
that need to deliver verification codes or notifications to one or more phone
numbers.

## When to use this skill

Use this skill when:

- You need to send verification codes (e.g., 2FA, login codes) to a phone number.
- You need to send short notification messages via Aliyun SMS.
- The user has provided or approved a phone number and message purpose.

Do **not** use this skill for:

- Bulk marketing campaigns (often subject to additional compliance rules).
- Sending to numbers without proper user consent.

## Invocation (CLI / subprocess)

This skill is implemented as a CLI tool that reads a single JSON object from
stdin and writes a single JSON object to stdout.

For runtimes that prefer subprocess tools, run the command declared in
`metadata.implementation.command` and pass a single JSON request via stdin:

```bash
echo '{
  "phone_numbers": ["13800000000"],
  "template_params": { "code": "123456" }
}' | python skills/aliyun-sms/scripts/aliyun_sms.py
```

The script will print a single JSON object on stdout in this structure:

- `ok` (bool): whether the SMS send request was accepted.
- `request_id` (str | null): Aliyun request ID if available.
- `biz_id` (str | null): Aliyun business ID if available.
- `error` (str | null): error message or Aliyun error code/message when failed.

## Configuration

### Environment variables

The underlying implementation uses these environment variables:

- `ALIYUN_ACCESS_KEY_ID` (required)
- `ALIYUN_ACCESS_KEY_SECRET` (required)
- `ALIYUN_REGION_ID` (optional, default `cn-hangzhou`)
- `ALIYUN_SMS_SIGN_NAME` (required)
- `ALIYUN_SMS_TEMPLATE_CODE` (required)

The `template_params` field of the request will be converted to a JSON string
and passed to Aliyun as template parameters, so its keys must match the
placeholders defined in your Aliyun SMS template.

## Request format

The expected JSON payload schema:

- `phone_numbers` (list of string, required): one or more E.164 or local-format
  numbers that Aliyun accepts; internally joined by commas.
- `template_params` (object, optional): template variables to substitute into
  the configured template.

## Safety & permissions

- Only send SMS messages to numbers that the user controls or has consented to.
- Avoid including highly sensitive data in SMS (e.g., full passwords); use
  short-lived codes instead.
- Respect local regulations and Aliyun SMS policies regarding message content
  and frequency.

