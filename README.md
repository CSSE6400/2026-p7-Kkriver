[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=23551354)
# CSSE6400 Week 7 Practical

Using Celery with Redis and SQS, and deploying container images using these to AWS ECR.

Please see the [instructions](https://csse6400.uqcloud.net/practicals/week07) for more details.

## Local Redis workflow

Build and start the local development stack:

```bash
docker compose build app worker
docker compose up -d
```

Create a todo and generate an iCal file:

```bash
curl -sS -X POST http://localhost:6400/api/v1/todos \
  -H 'Content-Type: application/json' \
  -d '{"title":"Week07 Demo","description":"Generate iCal","deadline_at":"2026-04-20T10:00:00"}'

curl -sS -X POST http://localhost:6400/api/v1/todos/ical
```

## AWS SQS workflow

1. Copy `aws.env.example` to `aws.env` and paste in your Learner Lab credentials.
2. Create a `credentials` file for Terraform in the same directory.
3. Provision the queue with Terraform:

```bash
terraform init
terraform apply
```

4. Start the app and worker using the SQS override:

```bash
docker compose -f docker-compose.yaml -f docker-compose.sqs.yaml up -d --build
```

This keeps PostgreSQL as the Celery result backend while using AWS SQS as the broker.

