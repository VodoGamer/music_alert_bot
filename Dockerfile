FROM python:3.11-slim

ENV TZ Europe/Moscow

ARG PROJECT_NAME
WORKDIR /$PROJECT_NAME

RUN pip install poetry

COPY poetry.loc[k] pyproject.toml README.md .env ./
RUN poetry install --only main

COPY . ./

RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT [ "./docker-entrypoint.sh" ]

CMD [ "python", "-m", "src" ]
