# Behave environment hooks (Allure, anexos úteis)
import json
from allure_commons.types import AttachmentType
import allure

def after_step(context, step):
    # anexa última resposta se existir
    resp = getattr(context, "last_response", None)
    if resp:
        try:
            body_repr = resp.response.json()
        except Exception:
            body_repr = resp.response.text

        allure.attach(
            json.dumps({
                "status_code": resp.response.status_code,
                "elapsed_ms": resp.elapsed_ms,
                "headers": dict(resp.response.headers),
                "body": body_repr
            }, ensure_ascii=False, indent=2),
            name="HTTP Response",
            attachment_type=AttachmentType.JSON
        )
