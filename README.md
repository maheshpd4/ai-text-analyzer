# AI Text Analyzer - FastAPI + Kafka + Kubernetes

## Architecture

```text
Swagger / Client
        ↓
FastAPI REST API
        ↓
Kafka Topic (text-events)
        ↓
Kafka Consumer
        ↓
Sentiment Processing
        ↓
SQLite Database
        ↓
Docker Containerization
        ↓
Docker Hub Registry
        ↓
Kubernetes Deployment + Services
```

---

## Project Overview

This project demonstrates an end-to-end event-driven microservice pipeline using Python, Kafka, Docker, and Kubernetes.

A user submits text through Swagger UI.

The FastAPI application receives the request and publishes the message to Kafka.

A Kafka consumer reads the message, performs sentiment analysis, and stores the processed result in SQLite.

This project demonstrates real-world concepts such as asynchronous messaging, containerization, service communication, and Kubernetes deployment.

---

## Technology Stack

- Python
- FastAPI
- Kafka
- Confluent Kafka Python Client
- SQLite
- Docker
- Docker Hub
- Kubernetes
- Swagger UI

---

## End-to-End Architecture Flow

```text
User
 ↓
Swagger UI
 ↓
FastAPI API
 ↓
Kafka Producer
 ↓
Kafka Topic (text-events)
 ↓
Kafka Consumer
 ↓
Sentiment Analysis Logic
 ↓
SQLite Database
```

---

## API Endpoints

### 1. Health Check

Endpoint:

```http
GET /
```

Response:

```json
{
  "message": "AI Text Analyzer API Running"
}
```

---

### 2. Analyze Text

Endpoint:

```http
POST /analyze
```

Sample Request:

```json
{
  "text": "Kubernetes and Kafka integration is awesome"
}
```

Sample Response:

```json
{
  "status": "SUCCESS",
  "message": "Text published to Kafka topic",
  "payload": {
    "text": "Kubernetes and Kafka integration is awesome"
  }
}
```

---

### 3. Get Results

Endpoint:

```http
GET /results
```

Returns processed sentiment records.

---

## Docker Images

### API Image

```text
maheshpd4/ai-text-analyzer-api:v3
```

### Consumer Image

```text
maheshpd4/text-analyzer-consumer:v5
```

---

## Kubernetes Components

```text
text-analyzer-api
text-analyzer-consumer
kafka
zookeeper
kafka-service
zookeeper-service
text-analyzer-api-service
```

---

## Folder Structure

```text
ai_text_analyzer/
│
├── api_app.py
├── consumer.py
├── requirements.txt
├── Dockerfile
├── Dockerfile.consumer
├── docker-compose.yml
├── consumer-deployment.yaml
├── README.md
│
└── k8s/
    └── deployment.yaml
```

---

## Docker Commands

### Build API Image

```bash
docker build --no-cache -t maheshpd4/ai-text-analyzer-api:v3 .
```

### Push API Image

```bash
docker push maheshpd4/ai-text-analyzer-api:v3
```

### Build Consumer Image

```bash
docker build --no-cache -f Dockerfile.consumer -t maheshpd4/text-analyzer-consumer:v5 .
```

### Push Consumer Image

```bash
docker push maheshpd4/text-analyzer-consumer:v5
```

---

## Kubernetes Commands

### Check Pods

```bash
kubectl get pods
```

### Check Services

```bash
kubectl get svc
```

### Deploy API

```bash
kubectl delete deployment text-analyzer-api
kubectl apply -f k8s/deployment.yaml
```

### Deploy Consumer

```bash
kubectl delete deployment text-analyzer-consumer
kubectl apply -f consumer-deployment.yaml
```

### Check API Logs

```bash
kubectl logs <api-pod-name>
```

Example:

```bash
kubectl logs text-analyzer-api-7c696dd8bc-88kqc
```

### Check Consumer Logs

```bash
kubectl logs -f <consumer-pod-name>
```

Example:

```bash
kubectl logs -f text-analyzer-consumer-5986fb69fd-fc48c
```

---

## Swagger Testing

### Start Port Forwarding

```bash
kubectl port-forward service/text-analyzer-api-service 8090:8000
```

Open browser:

```text
http://127.0.0.1:8090/docs
```

---

## Sample Test Request

Use POST `/analyze`

```json
{
  "text": "Final end to end validation is awesome"
}
```

Expected response:

```json
{
  "status": "SUCCESS",
  "message": "Text published to Kafka topic"
}
```

---

## Consumer Expected Output

```text
Waiting for Kafka messages...
Processed Kafka Message:
{
  'input_text': 'Final end to end validation is awesome',
  'word_count': 6,
  'character_count': 36,
  'positive_words': 1,
  'negative_words': 0,
  'sentiment': 'Positive'
}
Result stored in database
```

---

## Problems Solved During Implementation

### 1. Kafka localhost issue

Problem:

```text
localhost:9092 connection refused
```

Root cause:

Inside Kubernetes, localhost refers to the same pod, not Kafka service.

Fix:

```python
"bootstrap.servers": "kafka-service:9092"
```

---

### 2. Stale Docker image issue

Problem:

Updated code was not reflecting in Kubernetes.

Root cause:

Kubernetes reused cached local Docker images.

Fix:

Use Docker Hub images with versioning:

```text
v3
v4
v5
```

Deployment:

```yaml
imagePullPolicy: Always
```

---

### 3. SQLite table missing

Problem:

```text
sqlite3.OperationalError: no such table: sentiment_results
```

Root cause:

Container starts with fresh filesystem.

Fix:

```sql
CREATE TABLE IF NOT EXISTS sentiment_results
```

---

### 4. Consumer logs not visible

Problem:

No logs shown via kubectl logs.

Root cause:

Python stdout buffering inside containers.

Fix:

```python
print(..., flush=True)
```

---

### 5. Kafka DNS resolution failure after restart

Problem:

```text
Failed to resolve kafka-service
```

Root cause:

Consumer started before cluster DNS stabilized.

Fix:

Restart pod:

```bash
kubectl delete pod <consumer-pod>
```

---

## Learning Outcomes

This project provided hands-on understanding of:

- FastAPI REST APIs
- Kafka Producer/Consumer architecture
- Event-driven microservices
- SQLite persistence
- Docker image creation
- Docker Hub registry publishing
- Kubernetes deployments
- Kubernetes services
- Pod networking
- Cluster DNS
- Logging/debugging
- Production troubleshooting
- Microservice communication

---

## Git Commands

### Check Status

```bash
git status
```

### Add Files

```bash
git add .
```

### Commit

```bash
git commit -m "Final AI text analyzer Kafka Kubernetes project"
```

### Push

```bash
git push origin main
```

---

## Future Enhancements

- Replace SQLite with PostgreSQL
- Add Redis caching
- Add Prometheus monitoring
- Add Grafana dashboards
- Add CI/CD using GitHub Actions
- Deploy to GKE / AKS / EKS
- Add authentication
- Add ML-based sentiment analysis
- Add UI dashboard
- Add persistent volume storage

---

## Final Achievement

Built a complete end-to-end cloud-native event-driven application using:

```text
FastAPI + Kafka + Docker + Docker Hub + Kubernetes
```

This is portfolio-grade project experience.