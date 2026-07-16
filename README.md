# AI Observability & Alerting System

A lightweight, production-inspired observability and alerting system designed to detect, aggregate, and notify failures from third-party AI integrations in real time.

---

##  Overview

Modern AI systems rely heavily on third-party providers (LLMs, APIs, external services). When these integrations fail, the most common outcome is **silent downtime**—errors are logged, but no action is taken until users report issues.

This project solves that problem by introducing a **self-aware system** that:

* Detects failures as they happen
* Aggregates errors intelligently
* Sends actionable alerts to Slack
* Reduces downtime and improves reliability

---

##  Problem Statement

In production systems:

* Third-party APIs can fail unpredictably (timeouts, rate limits, outages, or even potential downtimes)
* Errors are often **logged but ignored**
* Engineers only react **after users complain** or customer support raises concern
* This leads to:

  * Poor user experience
  * Revenue loss due to system downtime
  * Delayed incident response

---

## Solution

This system introduces a **structured observability + alerting layer** on top of AI integrations. It extends beyond just logging error for discrete events and instead introduces a reactive approach. Typically;
```text
Failure happens → system detects → system alerts → human reacts
```

Instead of reacting to individual errors, it:

```text
Captures → Aggregates → Evaluates → Alerts
```

---

##  Architecture

```text
API Request
   ↓
AI Service Layer
   ↓
Third-Party Integration (Fireworks / Together)
   ↓
Error Occurs
   ↓
ErrorCollector (structured capture)
   ↓
AlertManager (aggregation + threshold logic)
   ↓
SlackNotifier
   ↓
 Alert Sent
```

---

##  Integrations

This project uses real AI providers via their SDKs:

* Fireworks AI
* Together AI

Failures from these services are intentionally captured and monitored.

---

##  Core Components

### 1. Service Layer

Wraps all third-party calls and captures failures.

```text
Responsible for:
- Intercepting errors
- Sending structured events to ErrorCollector
```

---

### 2. ErrorCollector

Central in-memory store for all captured failures.

```text
Stores:
- event type
- provider
- error type
- timestamp
- metadata
```

---

### 3. AlertManager

The “brain” of the system.

```text
Handles:
- Time-window filtering
- Error aggregation
- Threshold-based alerting
- Deduplication (prevents spam)
```

---

### 4. SlackNotifier

Delivers alerts to a Slack channel via webhook.

---

##  Features

* -  Real-time failure detection
* - Error aggregation (no alert spam)
* - Sliding time-window monitoring
* - Threshold-based alerting
* - Deduplicated alerts
* - Third-party integration monitoring
* - Async-safe architecture

---

##  Demo

### Trigger a failure

```bash
curl http://localhost:8000/fireworks
```

### What happens

```text
1. API call fails (e.g. invalid key / timeout)
2. Error is captured by ErrorCollector
3. AlertManager aggregates failures
4. Slack receives a single alert
```

---

##  Example Alert

```text
🚨 CRITICAL: Fireworks Failure

Provider: fireworks  
Error: TimeoutError  
Failures: 57 (last 2 mins)  
Status: Ongoing  
```

---

##  Key Design Decisions

### 1. Aggregation over raw alerts

Avoids alert fatigue by sending **one alert per failure pattern**, not per error.

---

### 2. Separation of concerns

| Component      | Responsibility       |
| -------------- | -------------------- |
| Service Layer  | Capture errors       |
| ErrorCollector | Store errors         |
| AlertManager   | Decide when to alert |
| SlackNotifier  | Send alerts          |

---

### 3. In-memory buffer (intentional)

Used for:

* fast aggregation
* simplicity

Trade-offs:

* not persistent
* not distributed

---

##  Lessons & Insights

* Logs alone are not observability
* Alerts must represent **patterns**, not events
* Third-party failures are the most common production risk
* Aggregation is essential for signal clarity
* External systems can fail silently

---

##  Future Improvements

*  Redis for shared, persistent error storage
*  Celery for reliable background scheduling
*  Sentry for deep error tracking and stack traces
*  A self-healing system → Automatic fallback between providers
*  Metrics dashboard (error rate, latency, uptime)
*  Distributed tracing (OpenTelemetry)

---

##  Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-observability-system.git
cd ai-observability-system
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure environment variables

```env
FIREWORKS_API_KEY=your_key
TOGETHER_API_KEY=your_key
SLACK_ACCESS_TOKEN=your_slack_access_token_with_chat:write_access
```

---

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

---

##  Architectural Diagram
```

                          ┌──────────────────────────┐
                          │        Client/User       │
                          └────────────┬─────────────┘
                                       │
                                       ▼
                          ┌──────────────────────────┐
                          │       FastAPI API        │
                          │   (/fireworks, /together)│
                          └────────────┬─────────────┘
                                       │
                                       ▼
                          ┌──────────────────────────┐
                          │       AI Service Layer   │
                          │  (Failure Capture Point) │
                          └───────┬────────┬─────────┘
                                  │        │
                ┌─────────────────┘        └─────────────────┐
                ▼                                            ▼
   ┌──────────────────────────┐              ┌──────────────────────────┐
   │   Fireworks Integration  │              │   Together Integration   │
   │     (SDK Client)         │              │     (SDK Client)         │
   └────────────┬─────────────┘              └────────────┬─────────────┘
                │                                            │
                ▼                                            ▼
        ❌ Failure Occurs                            ❌ Failure Occurs
                │                                            │
                └──────────────┬─────────────────────────────┘
                               ▼
                 ┌──────────────────────────┐
                 │     ErrorCollector       │
                 │ (Structured Error Store) │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │     AlertManager         │
                 │                          │
                 │  • Time Window Filter    │
                 │  • Threshold Check       │
                 │  • Deduplication         │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │     SlackNotifier        │
                 │   (Webhook Delivery)     │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │     Slack Channel        │
                 │   #ai_model_alarms       │
                 └──────────────────────────┘
                
```

---
```text
1. A request hits the API endpoint
2. The AI Service calls a third-party provider (Fireworks / Together)
3. If the provider fails, the error is captured
4. Errors are stored temporarily in ErrorCollector
5. AlertManager evaluates errors over a time window
6. If a threshold is exceeded, a single alert is triggered
7. SlackNotifier sends a structured alert to Slack
```

##  Author

Built as a practical exploration of **observability, monitoring, and alerting systems** in AI-driven applications.

---

##  Final Note

This project demonstrates a key shift in engineering mindset:

> From *“logging errors”* → to *“understanding and reacting to system failures in real time”*

---

