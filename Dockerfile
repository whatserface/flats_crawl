# syntax=docker/dockerfile:1
FROM python:3.10.6

WORKDIR /python
ENV HOST=postgres
ENV DATABASE=sreality
ENV USER=postgres
ENV PASSWORD=opaq3195
ENV PORT=5432

ENV PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
WORKDIR /python/scraper
CMD python ../server/web_server.py