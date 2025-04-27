import json
import importlib.util
from pathlib import Path
import os

spec = importlib.util.spec_from_file_location("handler", "lambda/index.py")
handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler)

class DummyContext:
    invoked_function_arn = (
        "arn:aws:lambda:ap-northeast-1:123456789012:function:test-fn"
    )

event = {
    "body": json.dumps({
        "message": "こんにちは！AIについて100文字で教えてください",
        "conversationHistory": []
    }),
    "requestContext": {}
}

def test_lambda_local_call():
    resp = handler.lambda_handler(event, context=DummyContext())

    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert body["success"] is True
    assert "response" in body

    # デバッグ用に表示
    print("Model reply:", body)