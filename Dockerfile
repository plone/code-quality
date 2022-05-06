FROM python:3.10-slim

LABEL maintainer="Plone Community <dev@plone.org>"  \
      org.label-schema.name="code-quality" \
      org.label-schema.description="Plone code quality tool" \
      org.label-schema.vendor="Plone Foundation" \
      org.label-schema.docker.cmd="docker run -rm -v "${PWD}":/github/workspace plone/code-quality check black src"

COPY requirements.txt pyproject.toml docker-entrypoint.py ./

RUN pip install -U pip && pip install -r requirements.txt

WORKDIR /github/workspace

ENTRYPOINT [ "/docker-entrypoint.py" ]
