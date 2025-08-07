FROM python:3.13.5-bullseye AS builder
LABEL authors="yuanz"
WORKDIR /build
RUN apk install --no-cache gcc musl-dev libffi-dev && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt
FROM python:3.13.5-bullseye
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*
COPY . .
USER appuser
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]