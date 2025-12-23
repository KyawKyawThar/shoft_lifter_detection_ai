# System Components Summary

## What Gets Created

### Files in Your Project:
```
shop_lifter/
├── README.md                    ← START HERE
├── QUICK_START.md              ← 30-minute setup
├── SYSTEM_DESIGN.md            ← Full architecture (14 sections)
├── MOBILE_APP_SETUP.md         ← iOS/Android code
├── app.py                      ← NEW: Flask server
├── detection.py                ← Original code (still works)
├── best.pt                     ← YOLOv8 model
├── model_weights.json          ← XGBoost model
└── alerts.txt                  ← Generated alerts log
```

---

## Technology Stack

```
┌─────────────────────────────────────────────┐
│          PRODUCTION STACK                   │
├─────────────────────────────────────────────┤
│                                             │
│  BACKEND                                   │
│  ├─ Language: Python 3.9+                  │
│  ├─ Framework: Flask (lightweight)         │
│  ├─ Real-time: Socket.IO (WebSocket)      │
│  ├─ ML: YOLOv8 + XGBoost                  │
│  ├─ Database: PostgreSQL (optional)        │
│  ├─ Cache: Redis (optional)                │
│  └─ Hosting: AWS/DigitalOcean/On-prem    │
│                                             │
│  FRONTEND (MOBILE)                         │
│  ├─ Option 1: React Native (JavaScript)   │
│  │  └─ Cross-platform (iOS + Android)     │
│  ├─ Option 2: Flutter (Dart)              │
│  │  └─ Alternative cross-platform         │
│  └─ UI Framework: Material Design          │
│                                             │
│  FRONTEND (WEB)                            │
│  ├─ Dashboard: React.js or Vue.js         │
│  ├─ Real-time: Socket.io-client            │
│  └─ Styling: Tailwind CSS or Material-UI  │
│                                             │
│  DEPLOYMENT                                │
│  ├─ Containerization: Docker               │
│  ├─ Orchestration: Docker Compose          │
│  ├─ CI/CD: GitHub Actions                  │
│  └─ Monitoring: Prometheus + Grafana       │
│                                             │
└─────────────────────────────────────────────┘
```

---

## System Flow Diagram

```
DETECTION CYCLE (Every Frame)
────────────────────────────

┌──────────────┐
│ Read Frame   │  ←─ Camera input (30-60ms)
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ YOLOv8           │  ← Detect poses (30-50ms)
│ Inference        │
└──────┬───────────┘
       │
       ├─ No humans → Skip
       │
       └─ Humans found
          │
          ▼
     ┌────────────────────┐
     │ Extract             │  ← Get keypoints
     │ Keypoints           │    from skeleton
     └────┬───────────────┘
          │
          ▼
     ┌──────────────────┐
     │ XGBoost          │  ← Classify behavior
     │ Classification   │    (5-8ms)
     └────┬─────────────┘
          │
          ├─ Normal (>0.5) → Green box
          │
          └─ Suspicious (<0.5) → Red box
             │
             ├─ Low confidence → Draw only
             │
             └─ High conf (>0.85) → ALERT!
                │
                ├─ WebSocket → All clients
                ├─ Database → Store alert
                ├─ Log file → alerts.txt
                └─ Push → Mobile notification


TOTAL TIME: 40-75ms per frame = 13-25 FPS minimum
```

---

## Real-Time Communication

```
WEBSOCKET FLOW
──────────────

Server                                    Client (Mobile/Web)
├─ Establish connection                  ← connect
│  └─ Emit "message"         ───────────────────→
│                                         └─ Show "Connected"
│
├─ Every 33ms:
│  └─ Emit frame data        ───────────────────→
│                                         └─ Update video
│
├─ On alert:
│  └─ Emit alert object      ───────────────────→
│                                         ├─ Show popup
│                                         ├─ Play sound
│                                         └─ Add to list
│
└─ On disconnect            ←─────────────────
   └─ Cleanup               (Server detects)
```

---

## Cost Breakdown (Monthly)

```
CLOUD DEPLOYMENT (AWS)
──────────────────────

Hardware:
  EC2 Server (t3.xlarge)        $80
  Database (RDS PostgreSQL)     $30
  Cache (Redis)                 $15
  Storage (S3)                  $5-20
  Data Transfer                 $10-30
  ─────────────────────────────────
  TOTAL:                        $140-175/month


ON-PREMISES DEPLOYMENT
──────────────────────

Hardware (note):
  This project is offered as a software-only subscription. Hardware (servers, cameras,
  PoE switches, NVR/DVRs, encoders, etc.) is NOT included and must be provided/installed
  by the customer or their integrator.

Recommended minimal on-site hardware (customer-provided):
  - Small/home setups: Raspberry Pi 4 + Coral USB or a light NUC (no GPU required)
  - SMB setups: Refurbished server or small NUC with an external accelerator (Jetson/Coral/USB-NCS)
  - High-throughput: Server with discrete GPU (RTX/GTX) for many streams

Operating (monthly) — software subscription (example pricing):
  Personal (1–2 cameras):        $9/month
  Standard (up to 6 cameras):    $29/month
  Business (up to 20 cameras):   $99/month
  Enterprise (custom / 20+):      Custom pricing

Optional paid services:
  - Cloud storage / long retention
  - Priority support & SLA
  - Managed provisioning for installers

Notes:
  - Customers who prefer full turn-key installs can partner with local installers for hardware supply and installation.
  - The above subscription prices are example starting points — adjust by market and support costs.
  
See the subscription one-pager for full pricing, onboarding and reseller details:

- [SUBSCRIPTION_PLANS.md](SUBSCRIPTION_PLANS.md)
```

---

## Timeline to Production

```
DEVELOPMENT TIMELINE
─────────────────────

Week 1: Backend & Server Setup
├─ Day 1: Flask app + WebSocket setup
├─ Day 2-3: Integration with detection models
├─ Day 4: Testing & optimization
└─ Day 5: Documentation

Week 2: Mobile App Development
├─ Day 1: Project setup (React Native)
├─ Day 2-3: UI components + API integration
├─ Day 4: Testing on emulator
└─ Day 5: Refinements

Week 3: Testing & Integration
├─ Day 1-2: End-to-end testing
├─ Day 3: Bug fixes & optimization
├─ Day 4: Security review
└─ Day 5: Documentation

Week 4: Deployment
├─ Day 1-2: Cloud setup (AWS/DigitalOcean)
├─ Day 3: CI/CD pipeline
├─ Day 4: Production deployment
└─ Day 5: Monitoring & support


TOTAL: 4 weeks to MVP (minimum viable product)
TOTAL: 8 weeks to production-ready
```

---

## Comparison: Before vs After

```
BEFORE (Current State)
──────────────────────
✅ Offline video processing (single file)
✅ Detects suspicious activity
✅ Outputs annotated video
❌ No real-time monitoring
❌ No mobile app
❌ No live camera support
❌ No alerts/notifications
❌ Manual file processing only


AFTER (With This System)
────────────────────────
✅ Offline video processing (single file)
✅ Detects suspicious activity
✅ Outputs annotated video
✅ REAL-TIME monitoring (live cameras)
✅ iOS + Android mobile app
✅ LIVE camera support (RTSP/HTTP)
✅ INSTANT alerts + notifications
✅ Automatic continuous processing
✅ Multi-camera support
✅ Alert history + database
✅ Web dashboard
✅ User authentication
✅ Scalable to 100+ cameras
```

---

## Key Metrics You'll Track

```
OPERATIONAL METRICS
───────────────────

Performance:
  ├─ Frames per second (FPS): Target 25+
  ├─ Inference time: Target <75ms
  ├─ Alert latency: Target <500ms
  └─ API response time: Target <100ms

Reliability:
  ├─ System uptime: Target 99.9%
  ├─ Mean time to recovery: Target <5 min
  ├─ Error rate: Target <0.1%
  └─ False positive rate: Track for tuning

Business:
  ├─ Alerts per day: Varies by location
  ├─ Detection accuracy: % correct
  ├─ User engagement: App opens/day
  └─ ROI: Losses prevented vs cost
```

---

## Security Checklist

```
IMPLEMENTATION CHECKLIST
────────────────────────

□ Network Security
  □ HTTPS/TLS 1.3
  □ Firewall (only 80, 443, 22)
  □ DDoS protection

□ Authentication
  □ JWT tokens (API)
  □ Secure sessions (Web)
  □ Multi-factor authentication (optional)

□ Authorization
  □ Role-based access control
  □ Camera-level permissions
  □ Audit logging

□ Data Protection
  □ Database encryption (AES-256)
  □ Password hashing (bcrypt)
  □ API key rotation (90 days)

□ API Security
  □ Rate limiting (100 req/min)
  □ Input validation
  □ CORS configuration
  □ SQL injection prevention

□ Monitoring
  □ Security event logging
  □ Intrusion detection (fail2ban)
  □ Real-time alerts
```

---

## Getting Started Checklist

```
RIGHT NOW (Today)
─────────────────
□ Read README.md (you are here!)
□ Skim SYSTEM_DESIGN.md (20 min read)
□ Skim QUICK_START.md

THIS WEEK
──────────
□ Try QUICK_START.md locally
□ Test with webcam
□ Send test alert

NEXT WEEK
──────────
□ Deploy to cloud or local server
□ Setup mobile app development
□ Create basic dashboard

THIS MONTH
──────────
□ Mobile app working
□ Database setup
□ User authentication
□ Production deployment

ONGOING
────────
□ Monitor system performance
□ Collect user feedback
□ Improve accuracy
□ Add new features
```

---

## Questions to Ask Yourself

```
PLANNING QUESTIONS
──────────────────

Q: Where will the server run?
   → Cloud: AWS, DigitalOcean, Azure, GCP
   → Local: Office server, NAS, Raspberry Pi (slower)

Q: How many cameras?
   → 1-2: Single server sufficient
   → 5-10: Single cloud server (t3.xlarge)
   → 50+: Multiple servers with load balancer

Q: What database?
   → Starting: SQLite (local)
   → Production: PostgreSQL or MySQL

Q: Which mobile platform first?
   → React Native: Same code for iOS + Android
   → Flutter: Also cross-platform, newer
   → Native: Faster but 2x development time

Q: What's the budget?
   → Cheap: Local server + free cloud tier ($0-50/mo)
   → Medium: AWS EC2 ($150-300/mo)
   → Enterprise: Dedicated infrastructure ($500+/mo)

Q: Timeline?
   → MVP (4 weeks): Get basic system running
   → Beta (8 weeks): Add mobile app + database
   → Production (12 weeks): Full security + scaling
```

---

## Success Criteria

```
How to Know You've Succeeded:
────────────────────────────

✅ Server runs without errors
✅ Can detect objects in video streams
✅ Mobile app connects to server
✅ Alerts arrive in <500ms
✅ System handles 5+ cameras
✅ Uptime > 99.5% over 24 hours
✅ No false positives in test scenarios
✅ Mobile app works on iOS AND Android
✅ Database stores alerts correctly
✅ Users report high satisfaction

Bonus:
✅ System handles 20+ cameras
✅ Analytics dashboard working
✅ Third-party integrations
✅ <100ms alert latency
```

---

**🎉 YOU'RE READY TO BUILD!**

Start with: **README.md** → **QUICK_START.md** → **SYSTEM_DESIGN.md**

Questions? Check the FAQ in each document or reach out to the community.

Good luck! 🚀
