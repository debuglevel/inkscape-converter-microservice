# Inkscape Converter Microservice

Microservice to convert whatever formats Inkscape reads to whatever formats Inkscape writes (using
the `--export-filename` argument).

## Example usage

### Convert a SVG to PDF

POST a conversion job:

```bash
$ curl --location --request POST 'http://localhost:8080/images/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "inputFormat": "svg",
    "outputFormat": "pdf",
    "base64": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjxzdmcKICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICB4bWxuczpjYz0iaHR0cDovL2NyZWF0aXZlY29tbW9ucy5vcmcvbnMjIgogICB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIKICAgeG1sbnM6c29kaXBvZGk9Imh0dHA6Ly9zb2RpcG9kaS5zb3VyY2Vmb3JnZS5uZXQvRFREL3NvZGlwb2RpLTAuZHRkIgogICB4bWxuczppbmtzY2FwZT0iaHR0cDovL3d3dy5pbmtzY2FwZS5vcmcvbmFtZXNwYWNlcy9pbmtzY2FwZSIKICAgd2lkdGg9IjIxMG1tIgogICBoZWlnaHQ9IjI5N21tIgogICB2aWV3Qm94PSIwIDAgMjEwIDI5NyIKICAgdmVyc2lvbj0iMS4xIgogICBpZD0ic3ZnOCIKICAgaW5rc2NhcGU6dmVyc2lvbj0iMS4wLjItMiAoZTg2Yzg3MDg3OSwgMjAyMS0wMS0xNSkiCiAgIHNvZGlwb2RpOmRvY25hbWU9InRlc3Quc3ZnIj4KICA8ZGVmcwogICAgIGlkPSJkZWZzMiIgLz4KICA8c29kaXBvZGk6bmFtZWR2aWV3CiAgICAgaWQ9ImJhc2UiCiAgICAgcGFnZWNvbG9yPSIjZmZmZmZmIgogICAgIGJvcmRlcmNvbG9yPSIjNjY2NjY2IgogICAgIGJvcmRlcm9wYWNpdHk9IjEuMCIKICAgICBpbmtzY2FwZTpwYWdlb3BhY2l0eT0iMC4wIgogICAgIGlua3NjYXBlOnBhZ2VzaGFkb3c9IjIiCiAgICAgaW5rc2NhcGU6em9vbT0iMC4zNSIKICAgICBpbmtzY2FwZTpjeD0iNDAwIgogICAgIGlua3NjYXBlOmN5PSI1NjAiCiAgICAgaW5rc2NhcGU6ZG9jdW1lbnQtdW5pdHM9Im1tIgogICAgIGlua3NjYXBlOmN1cnJlbnQtbGF5ZXI9ImxheWVyMSIKICAgICBpbmtzY2FwZTpkb2N1bWVudC1yb3RhdGlvbj0iMCIKICAgICBzaG93Z3JpZD0iZmFsc2UiCiAgICAgaW5rc2NhcGU6d2luZG93LXdpZHRoPSIxMjgwIgogICAgIGlua3NjYXBlOndpbmRvdy1oZWlnaHQ9Ijk2MSIKICAgICBpbmtzY2FwZTp3aW5kb3cteD0iMTM1OCIKICAgICBpbmtzY2FwZTp3aW5kb3cteT0iLTgiCiAgICAgaW5rc2NhcGU6d2luZG93LW1heGltaXplZD0iMSIgLz4KICA8bWV0YWRhdGEKICAgICBpZD0ibWV0YWRhdGE1Ij4KICAgIDxyZGY6UkRGPgogICAgICA8Y2M6V29yawogICAgICAgICByZGY6YWJvdXQ9IiI+CiAgICAgICAgPGRjOmZvcm1hdD5pbWFnZS9zdmcreG1sPC9kYzpmb3JtYXQ+CiAgICAgICAgPGRjOnR5cGUKICAgICAgICAgICByZGY6cmVzb3VyY2U9Imh0dHA6Ly9wdXJsLm9yZy9kYy9kY21pdHlwZS9TdGlsbEltYWdlIiAvPgogICAgICAgIDxkYzp0aXRsZT48L2RjOnRpdGxlPgogICAgICA8L2NjOldvcms+CiAgICA8L3JkZjpSREY+CiAgPC9tZXRhZGF0YT4KICA8ZwogICAgIGlua3NjYXBlOmxhYmVsPSJFYmVuZSAxIgogICAgIGlua3NjYXBlOmdyb3VwbW9kZT0ibGF5ZXIiCiAgICAgaWQ9ImxheWVyMSI+CiAgICA8cmVjdAogICAgICAgc3R5bGU9ImZpbGw6IzgwMDAwMDtzdHJva2Utd2lkdGg6MC4yNjQ1ODMiCiAgICAgICBpZD0icmVjdDEwIgogICAgICAgd2lkdGg9IjE5OC4wNTk1MiIKICAgICAgIGhlaWdodD0iMjg1Ljc1IgogICAgICAgeD0iNi4wNDc2MTkzIgogICAgICAgeT0iNi4wNDc2MTg5IiAvPgogICAgPGVsbGlwc2UKICAgICAgIHN0eWxlPSJmaWxsOiMwMDgwMDA7c3Ryb2tlLXdpZHRoOjAuMjY0NTgzIgogICAgICAgaWQ9InBhdGgxMiIKICAgICAgIGN4PSIxMDQuNjk5NDEiCiAgICAgICBjeT0iMTQ2LjY1NDc1IgogICAgICAgcng9IjY1LjM4OTg3NyIKICAgICAgIHJ5PSI2NC4yNTU5NTEiIC8+CiAgPC9nPgo8L3N2Zz4K"
}'

{"id":"7ae282c1-cec3-48d7-b1f9-93ed53114c18","inputFormat":"svg","outputFormat":"pdf","createdOn":"2021-08-01 13:54:06"}
```

GET conversion job information:

```bash
$ curl 'http://localhost:8080/images/7ae282c1-cec3-48d7-b1f9-93ed53114c18'

{"id":"7ae282c1-cec3-48d7-b1f9-93ed53114c18","inputFormat":"svg","outputFormat":"pdf","createdOn":"2021-08-01 13:54:06"}
```

GET conversion output:

```bash
$ curl -o test.pdf 'http://localhost:8080/images/7ae282c1-cec3-48d7-b1f9-93ed53114c18/download'
```

DELETE conversion:

```bash
$ curl --request DELETE 'http://localhost:8080/images/7ae282c1-cec3-48d7-b1f9-93ed53114c18'
```

## Development

### Environment

#### Initialize virtual environment (using venv)

```sh
python3 -m venv venv
```

#### Activate virtual environment

```sh
source ./venv/Scripts/activate
```

```powershell
.\venv\Scripts\Activate.ps1
```

### Dependencies

#### Install dependencies

```sh
pip install -r requirements-dev.txt
```

#### Dependency updates

`pip list --outdated` shows outdated (transitive) dependencies.

#### Formatting / Linting

##### black

`black` is used for formatting, because `black` does not ask about your opinion about how Python code should be
formatted.

```bash
black .
```

##### mypy

mypy checks the type annotations:

```sh
mypy app tests
```

### Testing

#### Run tests

```sh
pytest
```

#### Run tests on every file change

```sh
pytest-watch -c # -c clears terminal before pytest runs
```

#### Run test against different environments

```sh
tox
```

### Documentation

#### OpenAPI documentation

* Open [Swagger UI](http://localhost:8000/docs) or [ReDoc](http://localhost:8000/redoc)
* OpenAPI specs are available (as JSON) at http://localhost:8080/openapi.json
* Update `openapi.json` via `python update-openapi.py`

### All-in-one

`tox.ini` is also configured to run some additional commands (like a Makefile):

* `black .` for formatting
* `python update-openapi.py` to update `openapi.yaml`
* `pytest` for testing

### Deployment

#### Development (with auto reloading changed files)

```sh
uvicorn app.rest.main:fastapi --port=8080 --reload --log-config=app/logging-config.yaml
```

#### Production

This should be quite okay:

```sh
uvicorn app.rest.main:fastapi --port=8080 --log-config=app/logging-config.yaml
```

But some docs mention that `gunicorn` can be used as a manager.

#### Production (via docker compose)

```sh
docker compose up --build
```


