import json
import os
from typing import Any, Dict

from alibabacloud_dysmsapi20170525.client import Client as DysmsapiClient
from alibabacloud_dysmsapi20170525.models import SendSmsRequest
from alibabacloud_tea_openapi import models as open_api_models


def _create_client() -> DysmsapiClient:
    access_key_id = os.environ.get("ALIYUN_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIYUN_ACCESS_KEY_SECRET")
    region_id = os.environ.get("ALIYUN_REGION_ID", "cn-hangzhou")

    if not access_key_id or not access_key_secret:
        raise RuntimeError(
            "Missing ALIYUN_ACCESS_KEY_ID or ALIYUN_ACCESS_KEY_SECRET in environment."
        )

    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        region_id=region_id,
    )
    return DysmsapiClient(config)


def send_sms(payload: Dict[str, Any]) -> Dict[str, Any]:
    phone_numbers = payload.get("phone_numbers") or []
    if not isinstance(phone_numbers, list) or not phone_numbers:
        return {
            "ok": False,
            "request_id": None,
            "biz_id": None,
            "error": "Field 'phone_numbers' must be a non-empty list.",
        }

    sign_name = os.environ.get("ALIYUN_SMS_SIGN_NAME")
    template_code = os.environ.get("ALIYUN_SMS_TEMPLATE_CODE")
    if not sign_name or not template_code:
        return {
            "ok": False,
            "request_id": None,
            "biz_id": None,
            "error": "Missing ALIYUN_SMS_SIGN_NAME or ALIYUN_SMS_TEMPLATE_CODE in environment.",
        }

    template_params = payload.get("template_params") or {}
    template_param_json = json.dumps(template_params, ensure_ascii=False)

    try:
        client = _create_client()

        request = SendSmsRequest(
            phone_numbers=",".join(phone_numbers),
            sign_name=sign_name,
            template_code=template_code,
            template_param=template_param_json,
        )

        response = client.send_sms(request)
        body = response.body

        if body.code == "OK":
            return {
                "ok": True,
                "request_id": body.request_id,
                "biz_id": body.biz_id,
                "error": None,
            }

        return {
            "ok": False,
            "request_id": body.request_id,
            "biz_id": getattr(body, "biz_id", None),
            "error": f"{body.code}: {body.message}",
        }
    except Exception as exc:  # pragma: no cover - defensive
        return {
            "ok": False,
            "request_id": None,
            "biz_id": None,
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
                    "request_id": None,
                    "biz_id": None,
                    "error": f"Invalid JSON input: {type(exc).__name__}: {exc}",
                }
            )
        )
        return

    result = send_sms(payload)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    run_from_stdin()

