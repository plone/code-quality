FROM python:3.10-slim as base
FROM base as builder

RUN pip install -U pip wheel \
    && mkdir /app /wheelhouse

COPY requirements.txt /app/
COPY src /app/src

RUN cd /app/ && pip wheel -r requirements.txt --wheel-dir=/wheelhouse

FROM base

LABEL maintainer="Plone Community <dev@plone.org>"  \
      org.label-schema.name="code-quality" \
      org.label-schema.description="Plone code quality tool" \
      org.label-schema.vendor="Plone Foundation" \
      org.label-schema.docker.cmd="docker run -rm -v "${PWD}":/github/workspace plone/code-quality check black src"

COPY docker-entrypoint.py /
COPY --from=builder /wheelhouse /wheelhouse
RUN pip install --force-reinstall --no-index --no-deps /wheelhouse/*

WORKDIR /github/workspace

ENTRYPOINT [ "/docker-entrypoint.py" ]
