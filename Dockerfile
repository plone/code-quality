FROM python:3.10-slim

LABEL maintainer="kitconcept GmbH <info@kitconcept.com>" \
      org.label-schema.name="code-quality" \
      org.label-schema.description="Plone code quality tool" \
      org.label-schema.vendor="kitconcept GmbH" \
      org.label-schema.docker.cmd="docker run -rm -v "${PWD}":/github/workspace kitconcept/code-quality check black src"

COPY requirements.txt docker-entrypoint.py ./

RUN pip install -U pip && pip install -r requirements.txt

WORKDIR /github/workspace

ENTRYPOINT [ "/docker-entrypoint.py" ]
