openclaw-addons
================

A curated collection of plugins, skills, and utilities for OpenClaw.

This repository currently provides:

- **Email skill** (`email-sender`): send emails via common global and Chinese providers (Gmail, QQ, 163, and any SMTP-compatible provider).
- **Aliyun SMS skill** (`aliyun-sms`): send SMS messages using Alibaba Cloud SMS service.

### Project layout

- **`skills/email-sender/SKILL.md`**: Anthropic Agent Skill descriptor for the email skill.
- **`skills/email-sender/scripts/email_sender.py`**: CLI implementation used by the skill.
- **`skills/aliyun-sms/SKILL.md`**: Anthropic Agent Skill descriptor for the Aliyun SMS skill.
- **`skills/aliyun-sms/scripts/aliyun_sms.py`**: CLI implementation used by the skill.
- **`requirements.txt`**: Python dependencies for the skills.

### Prerequisites

- **Python**: 3.9+ recommended.
- **Dependencies**: installed via `pip install -r requirements.txt`.
- **Network access** from the environment where OpenClaw runs to:
  - SMTP servers of your mail providers (e.g. Gmail, QQ, 163).
  - Aliyun SMS endpoint.

### Installing dependencies

```bash
pip install -r requirements.txt
```

### Email skill (`skills/email_sender`)

The email skill is implemented as a small Python module that can be invoked by OpenClaw (or any orchestrator) as a subprocess or library call.

**Environment variables**

- `EMAIL_DEFAULT_FROM` (optional): default sender address if not provided in the request.

For provider-specific SMTP configuration you can either:

- Pass connection details in the skill request payload, or
- Configure them in your own wrapper around this skill.

Typical SMTP values:

- **Gmail**: `smtp.gmail.com:587` (TLS)
- **QQ Mail**: `smtp.qq.com:465` (SSL) or `smtp.qq.com:587` (TLS)
- **163 Mail**: `smtp.163.com:465` (SSL) or `smtp.163.com:25/587` (TLS)

**Request payload (JSON)**

```json
{
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
}
```

The script will read this JSON from stdin and print a JSON response to stdout.

### Aliyun SMS skill (`skills/aliyun_sms`)

The Aliyun SMS skill uses the official Alibaba Cloud SDK.

**Environment variables**

- `ALIYUN_ACCESS_KEY_ID`
- `ALIYUN_ACCESS_KEY_SECRET`
- `ALIYUN_REGION_ID` (e.g. `cn-hangzhou`)
- `ALIYUN_SMS_SIGN_NAME`
- `ALIYUN_SMS_TEMPLATE_CODE`

**Request payload (JSON)**

```json
{
  "phone_numbers": ["13800000000"],
  "template_params": {
    "code": "123456"
  }
}
```

As with the email skill, the request is read from stdin and a JSON result is written to stdout.

### Chinese README

For a Chinese version of this README, see `README.zh-CN.md`.
