import json
import os
import smtplib
from email.message import EmailMessage
from typing import Any, Dict, List


def _build_message(
    subject: str,
    body: str,
    body_type: str,
    from_addr: str,
    to_addrs: List[str],
) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)

    body_type = (body_type or "plain").lower()
    if body_type not in {"plain", "html"}:
        body_type = "plain"

    msg.set_content(body, subtype=body_type)
    return msg


def send_email(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core email sending logic.

    Expected keys in payload:
      - smtp_host (str, required)
      - smtp_port (int, required)
      - use_ssl (bool, optional, default False)
      - username (str, required)
      - password (str, required)
      - from_addr (str, optional – falls back to EMAIL_DEFAULT_FROM)
      - to_addrs (List[str], required)
      - subject (str, required)
      - body (str, required)
      - body_type (str, optional: 'plain' or 'html', default 'plain')
    """
    smtp_host = payload.get("smtp_host")
    smtp_port = payload.get("smtp_port")
    username = payload.get("username")
    password = payload.get("password")
    use_ssl = bool(payload.get("use_ssl", False))

    if not smtp_host or not smtp_port or not username or not password:
        return {
            "ok": False,
            "message_id": None,
            "error": "Missing required SMTP configuration (smtp_host, smtp_port, username, password).",
        }

    to_addrs = payload.get("to_addrs") or []
    if not isinstance(to_addrs, list) or not to_addrs:
        return {
            "ok": False,
            "message_id": None,
            "error": "Field 'to_addrs' must be a non-empty list of recipient addresses.",
        }

    default_from = os.environ.get("EMAIL_DEFAULT_FROM")
    from_addr = payload.get("from_addr") or default_from or username

    subject = payload.get("subject") or ""
    body = payload.get("body") or ""
    body_type = payload.get("body_type") or "plain"

    msg = _build_message(subject, body, body_type, from_addr, to_addrs)

    try:
        if use_ssl:
            server: smtplib.SMTP | smtplib.SMTP_SSL = smtplib.SMTP_SSL(
                smtp_host, int(smtp_port)
            )
        else:
            server = smtplib.SMTP(smtp_host, int(smtp_port))
            server.starttls()

        with server:
            server.login(username, password)
            response = server.send_message(msg)

        if response:
            return {
                "ok": False,
                "message_id": None,
                "error": f"Failed recipients: {response}",
            }

        return {
            "ok": True,
            "message_id": msg.get("Message-Id"),
            "error": None,
        }
    except Exception as exc:  # pragma: no cover - defensive
        return {
            "ok": False,
            "message_id": None,
            "error": f"{type(exc).__name__}: {exc}",
        }


def run_from_stdin() -> None:
    """
    CLI entrypoint: read one JSON object from stdin and write one JSON object to stdout.
    """
    try:
        raw = input()
        payload = json.loads(raw)
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "message_id": None,
                    "error": f"Invalid JSON input: {type(exc).__name__}: {exc}",
                }
            )
        )
        return

    result = send_email(payload)
    print(json.dumps(result))


if __name__ == "__main__":
    run_from_stdin()

