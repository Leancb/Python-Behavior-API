import json
import re
from jsonschema import validate
from pathlib import Path
from behave import given, when, then
from features.support import http_client

ROOT = Path(__file__).resolve().parents[1]

@given("the API base url")
def step_base_url(context):
    # Apenas marcador. BASE_URL vem do .env
    pass

@given('the request body')
@given('the request body:')
def step_body(context):
    context.request_body = json.loads(context.text)

@when('I send a {method} request to "{path}"')
def step_send(context, method, path):
    body = getattr(context, "request_body", None)
    context.last_response = http_client.request(method, path, body=body)
    if hasattr(context, "request_body"):
        delattr(context, "request_body")

@then('the response status code should be {code:d}')
def step_status(context, code):
    assert context.last_response.response.status_code == code, (
        f"Esperado {code}, obtido {context.last_response.response.status_code}"
    )

@then('the response time should be less than {ms:d} ms')
def step_time(context, ms):
    assert context.last_response.elapsed_ms < ms, (
        f"Demorou {context.last_response.elapsed_ms} ms (limite {ms} ms)"
    )

@then('the response header "{name}" should contain "{partial}"')
def step_header_contains(context, name, partial):
    value = context.last_response.response.headers.get(name)
    assert value and partial in value, f'Header {name}="{value}" não contém "{partial}"'

@then('the response should contain text "{snippet}"')
def step_contains_text(context, snippet):
    text = context.last_response.response.text
    assert snippet in text, f'Trecho "{snippet}" não encontrado na resposta.'

@then('the json path "{path}" should equal "{expected}"')
def step_json_equals(context, path, expected):
    val = _json_path(context, path)
    assert str(val) == expected, f'Path {path} = {val}, esperado {expected}'

@then('the json path "{path}" should not be empty')
def step_json_not_empty(context, path):
    val = _json_path(context, path)
    assert val not in ("", None, [], {}), f'Path {path} está vazio: {val}'

@then('the json path "{path}" should be an integer')
def step_json_int(context, path):
    val = _json_path(context, path)
    assert isinstance(val, int), f'Path {path} não é int: {type(val)} => {val}'

@then('the json path "{path}" should be an array')
def step_json_array(context, path):
    val = _json_path(context, path)
    assert isinstance(val, list), f'Path {path} não é array: {type(val)}'

@then('the json path "{path}" should contain "@"')
def step_json_contains_at(context, path):
    val = _json_path(context, path)
    assert isinstance(val, str) and "@" in val, f'Path {path} não contém "@" => {val}'

@then('the response body should match schema "{schema_path}"')
def step_match_schema(context, schema_path):
    schema_file = (ROOT / schema_path).resolve()
    payload = context.last_response.response.json()
    with open(schema_file, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate(instance=payload, schema=schema)

def _json_path(context, path):
    """Suporte simples a JSONPath mínimo: $.a.b[0].c"""
    data = context.last_response.response.json()
    assert path.startswith("$."), f"JSONPath deve iniciar com '$.': {path}"
    current = data
    tokens = re.findall(r'\.([A-Za-z0-9_]+)|\[(\d+)\]', path[1:])
    for key, idx in tokens:
        if key:
            current = current[key]
        else:
            current = current[int(idx)]
    return current
