# Complete System Design: Shoplifting Detection with Live CCTV & Mobile App

## YES, THIS IS 100% POSSIBLE! ✅

Here's a comprehensive system design for production deployment.

---

## 1. SYSTEM ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                         HARDWARE LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  CCTV Cam 1  │  │  CCTV Cam 2  │  │  CCTV Cam N  │          │
│  │ (RTSP/HTTP)  │  │ (RTSP/HTTP)  │  │ (RTSP/HTTP)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│                    NETWORK LAYER (LAN/WAN)                      │
│                    (WiFi/Ethernet/4G/5G)                        │
└───────────────────────────┼─────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│                    SERVER/CLOUD LAYER                           │
├───────────────────────────┼─────────────────────────────────────┤
│                           │                                     │
│     ┌─────────────────────▼──────────────────────┐             │
│     │  Flask/Python Detection Server             │             │
│     │  (app.py)                                  │             │
│     │                                            │             │
│     │  • YOLO v8 Pose Detection                  │             │
│     │  • XGBoost Classification                  │             │
│     │  • Frame Processing (Multi-threaded)       │             │
│     │  • Alert Management                        │             │
│     └─────────────────────┬──────────────────────┘             │
│                           │                                     │
│         ┌─────────────────┼─────────────────┐                  │
│         │                 │                 │                  │
│    ┌────▼────┐       ┌───▼────┐       ┌───▼────┐             │
│    │REST API │       │WebSocket│       │Database│             │
│    │Endpoints│       │Real-time│       │SQLite/ │             │
│    │         │       │Streams  │       │PostgreSQL            │
│    └────┬────┘       └───┬────┘       └───┬────┘             │
│         │                 │                 │                  │
└─────────┼─────────────────┼─────────────────┼──────────────────┘
          │                 │                 │
┌─────────┼─────────────────┼─────────────────┼──────────────────┐
│          │                 │                 │   CLIENT LAYER   │
├──────────┼─────────────────┼─────────────────┼──────────────────┤
│          │                 │                 │                  │
│  ┌───────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐           │
│  │ Mobile App   │  │  Web Browser │  │  Admin Panel│           │
│  │ (iOS/Android)│  │ (Dashboard)  │  │ (Desktop)   │           │
│  │              │  │              │  │             │           │
│  │ • React Nat. │  │ • React/Vue  │  │ • React     │           │
│  │   or Flutter │  │   or Angular │  │              │           │
│  │ • Real-time  │  │ • Real-time  │  │ • Analytics │           │
│  │   alerts     │  │   monitoring │  │ • Reports   │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. DETAILED COMPONENT BREAKDOWN

### 2.1 HARDWARE COMPONENTS

```
CCTV Cameras
├── IP Cameras (Recommended)
│   ├── RTSP Stream Support
│   │   └── Example: rtsp://192.168.1.100:554/stream
│   ├── HTTP MJPEG Stream
│   │   └── Example: http://192.168.1.100:8080/video
│   └── Common Brands: Hikvision, Dahua, Reolink, Ubiquiti
│
├── USB Cameras
│   └── Direct connection to server
│
└── Server Hardware
    ├── CPU: Intel i7/i9 or AMD Ryzen 5/7
    ├── GPU: NVIDIA RTX 3060/3080 (for faster inference)
    ├── RAM: 16GB+ recommended
    ├── Storage: 500GB SSD (for alerts + recordings)
    └── Network: Gigabit Ethernet preferred
```

### 2.2 SOFTWARE STACK

```
Backend (Server)
├── Framework: Flask + Flask-SocketIO
├── Detection Models:
│   ├── YOLOv8 (Pose Detection)
│   └── XGBoost (Activity Classification)
├── Video Processing: OpenCV
├── Database: PostgreSQL (for production)
├── Message Queue: Redis (for scaling)
└── Deployment: Docker + Docker-Compose

Frontend (Mobile)
├── React Native (Single codebase for iOS/Android)
│   or
├── Flutter (Google's framework)

Frontend (Web Dashboard)
├── React.js or Vue.js
├── Real-time: Socket.io Client
└── UI Framework: Material-UI or Tailwind CSS
```

---

## 3. DATA FLOW ARCHITECTURE

```
DETECTION PIPELINE
──────────────────

Frame Input
    │
    ▼
Frame Queue (Buffer)
    │
    ▼
YOLOv8 Inference
    │ (Detects human poses)
    │
    ├─ No Humans → Discard
    │
    └─ Humans Found → Extract Keypoints
        │
        ▼
    XGBoost Classification
        │ (Classify as Suspicious/Normal)
        │
        ├─ Normal (prob > 0.5) → Draw Green Box
        │
        └─ Suspicious (prob < 0.5) → Draw Red Box
            │
            ▼
        Confidence Check (>= 0.85?)
            │
            ├─ Yes → Generate Alert
            │        │
            │        ├─ Emit via WebSocket (Real-time)
            │        ├─ Store in Database
            │        ├─ Log to File (alerts.txt)
            │        └─ Send Notification (Push)
            │
            └─ No → Continue monitoring


OUTPUT CHANNELS
───────────────

                    ┌──────────────────────────┐
                    │   Alert Generated        │
                    └──────────┬───────────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
            ┌───▼────┐    ┌────▼────┐   ┌────▼────┐
            │WebSocket│    │Database │   │Log File │
            │Broadcast│    │Store    │   │Alert Log│
            └───┬────┘    └────┬────┘   └────┬────┘
                │              │             │
        ┌───────┼──────────────┼─────────────┘
        │       │              │
        │   ┌───▼──────┐  ┌────▼─────┐
        │   │Mobile App│  │Analytics │
        │   │Real-time │  │Dashboard │
        │   └──────────┘  └──────────┘
        │
    ┌───▼──────────────────────┐
    │Push Notification         │
    │(Optional)                │
    │ • Firebase Cloud         │
    │ • APNs (iOS)             │
    │ • FCM (Android)          │
    └──────────────────────────┘
```

---

## 4. SERVER ARCHITECTURE (Multi-threaded)

```python
┌─────────────────────────────────────────────────────────┐
│              Flask Application                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Main Thread (Event Loop)                              │
│  └─ HTTP Request Handler                               │
│     ├─ GET  /api/status → Return system status        │
│     ├─ POST /api/start/<source> → Start detection    │
│     ├─ POST /api/stop → Stop detection               │
│     └─ GET  /api/alerts → Fetch pending alerts       │
│                                                         │
│  WebSocket Thread                                       │
│  └─ Real-time Communication                            │
│     ├─ Emit frames every 33ms (30 FPS)                │
│     ├─ Broadcast alerts to all clients                │
│     └─ Handle client connections/disconnections       │
│                                                         │
│  Detection Thread (Background)                          │
│  └─ Video Processing Loop                              │
│     ├─ Read frame from camera                         │
│     ├─ YOLOv8 inference (30-60ms)                     │
│     ├─ XGBoost prediction (5-10ms)                    │
│     ├─ Frame annotation                                │
│     ├─ Alert generation                                │
│     └─ Queue management                                │
│                                                         │
│  Alert Processing Thread (Queue Worker)                │
│  └─ Process queued alerts                              │
│     ├─ Save to database                               │
│     ├─ Log to file                                    │
│     └─ Send notifications                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 5. MOBILE APP ARCHITECTURE (React Native Example)

```
┌────────────────────────────────────────┐
│     React Native Application            │
├────────────────────────────────────────┤
│                                         │
│  Navigation Stack                       │
│  ├─ HomeScreen                          │
│  │  └─ Camera feed display              │
│  │  └─ Start/Stop controls              │
│  │  └─ Live video preview               │
│  │                                      │
│  ├─ AlertsScreen                        │
│  │  └─ Real-time alerts list            │
│  │  └─ Alert details                    │
│  │  └─ Timestamp + confidence           │
│  │                                      │
│  ├─ SettingsScreen                      │
│  │  └─ Server IP configuration          │
│  │  └─ Camera source selection           │
│  │  └─ Alert preferences                │
│  │                                      │
│  └─ StatsScreen                         │
│     └─ Detection statistics             │
│     └─ Charts & graphs                  │
│                                          │
│  State Management (Redux/Context)       │
│  ├─ connectionStatus                    │
│  ├─ detectionActive                     │
│  ├─ alerts: [...Alert[]]                │
│  ├─ currentFrame: ImageData              │
│  └─ statistics: {...}                   │
│                                          │
│  Services Layer                          │
│  ├─ SocketService                       │
│  │  └─ socket.io-client connection      │
│  │                                      │
│  ├─ APIService                          │
│  │  └─ axios HTTP requests              │
│  │                                      │
│  └─ NotificationService                 │
│     └─ react-native-push-notification   │
│                                          │
│  Native Modules (Optional)               │
│  └─ Camera access permissions           │
│  └─ Storage permissions                 │
│  └─ Network status monitoring           │
│                                          │
└────────────────────────────────────────┘
```

---

## 6. DATABASE SCHEMA (PostgreSQL)

```sql
-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(20), -- admin, supervisor, viewer
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Cameras Table
CREATE TABLE cameras (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    source_url VARCHAR(255),
    location VARCHAR(255),
    type VARCHAR(50), -- RTSP, HTTP, USB, FILE
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Detection Sessions
CREATE TABLE detection_sessions (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER REFERENCES cameras(id),
    start_time TIMESTAMP DEFAULT NOW(),
    end_time TIMESTAMP,
    total_frames INTEGER DEFAULT 0,
    alerts_count INTEGER DEFAULT 0,
    status VARCHAR(20) -- running, completed, error
);

-- Alerts Table (Main)
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES detection_sessions(id),
    frame_number INTEGER,
    confidence FLOAT,
    timestamp TIMESTAMP DEFAULT NOW(),
    alert_type VARCHAR(50), -- suspicious, unusual, etc
    image_path VARCHAR(255), -- path to saved frame
    is_reviewed BOOLEAN DEFAULT false,
    notes TEXT
);

-- Alert Images (Store frames for review)
CREATE TABLE alert_images (
    id SERIAL PRIMARY KEY,
    alert_id INTEGER REFERENCES alerts(id),
    image_data BYTEA,
    created_at TIMESTAMP DEFAULT NOW()
);

-- System Logs
CREATE TABLE system_logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(20), -- INFO, WARNING, ERROR
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create Indexes for Performance
CREATE INDEX idx_alerts_timestamp ON alerts(timestamp);
CREATE INDEX idx_alerts_session_id ON alerts(session_id);
CREATE INDEX idx_sessions_camera_id ON detection_sessions(camera_id);
```

---

## 7. DEPLOYMENT ARCHITECTURE

### Option A: Single Server (Small-Medium Business)
```
┌─────────────────────────────────────┐
│      Ubuntu Server / AWS EC2        │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐   │
│  │ Docker Container             │   │
│  │                              │   │
│  │ ├─ Flask App (Port 5000)    │   │
│  │ ├─ PostgreSQL (Port 5432)   │   │
│  │ ├─ Redis (Port 6379)        │   │
│  │ └─ Nginx Reverse Proxy      │   │
│  │    (Port 80, 443)           │   │
│  │                              │   │
│  └──────────────────────────────┘   │
│                                     │
│  Storage: SSD 500GB                │
│  RAM: 16GB                         │
│  CPU: 8 cores                      │
│                                     │
└─────────────────────────────────────┘
```

### Option B: Scalable Architecture (Large Enterprise)
```
┌────────────────────────────────────────────────────────┐
│                  AWS/Cloud Infrastructure              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────┐                                      │
│  │Load Balancer │  (AWS ALB / Nginx)                  │
│  │(Port 80,443) │                                      │
│  └──────┬───────┘                                      │
│         │                                              │
│  ┌──────┴─────────────────────┐                       │
│  │                             │                       │
│  ▼                             ▼                       │
│ ┌─────────────┐         ┌─────────────┐              │
│ │EC2 Instance │         │EC2 Instance │              │
│ │(Detection 1)│         │(Detection 2)│              │
│ │Port 5000    │         │Port 5000    │              │
│ └──────┬──────┘         └──────┬──────┘              │
│        │                       │                       │
│        └───────────┬───────────┘                       │
│                    │                                   │
│            ┌───────▼────────┐                         │
│            │  RDS PostgreSQL│                         │
│            │  (Multi-AZ)    │                         │
│            └───────┬────────┘                         │
│                    │                                   │
│      ┌─────────────┴─────────────┐                   │
│      │                           │                    │
│      ▼                           ▼                    │
│  ┌────────┐              ┌────────────┐             │
│  │ Redis  │              │  S3 Bucket │             │
│  │ Cache  │              │(Alert Imgs)│             │
│  └────────┘              └────────────┘             │
│                                                       │
│  ┌──────────────────────────────────────┐           │
│  │CloudWatch (Monitoring & Logging)     │           │
│  │Prometheus + Grafana (Metrics)        │           │
│  └──────────────────────────────────────┘           │
│                                                       │
│  ┌──────────────────────────────────────┐           │
│  │Mobile Apps                           │           │
│  │├─ iOS (App Store)                   │           │
│  │├─ Android (Play Store)               │           │
│  │└─ Web Dashboard (CloudFront CDN)    │           │
│  └──────────────────────────────────────┘           │
│                                                       │
└────────────────────────────────────────────────────────┘
```

---

## 8. SECURITY ARCHITECTURE

```
┌────────────────────────────────────────────────┐
│          SECURITY LAYERS                       │
├────────────────────────────────────────────────┤
│                                                │
│  Layer 1: Network Security                    │
│  ├─ HTTPS/SSL (TLS 1.3)                      │
│  ├─ VPN for admin access                      │
│  ├─ Firewall (UFW/iptables)                  │
│  │  └─ Allow only:                            │
│  │     ├─ Port 80 (HTTP redirect)             │
│  │     ├─ Port 443 (HTTPS)                    │
│  │     └─ Port 22 (SSH admin only)           │
│  └─ DDoS Protection (Cloudflare)              │
│                                                │
│  Layer 2: Authentication                      │
│  ├─ JWT Tokens (for API)                      │
│  ├─ Session Management (HttpOnly cookies)    │
│  ├─ Multi-factor Authentication (MFA)        │
│  ├─ OAuth 2.0 (Social login option)          │
│  └─ API Key rotation (every 90 days)         │
│                                                │
│  Layer 3: Authorization                       │
│  ├─ Role-based Access Control (RBAC)         │
│  │  ├─ Admin (Full access)                    │
│  │  ├─ Supervisor (View + Review)             │
│  │  └─ Viewer (Read-only)                     │
│  └─ Camera-level permissions                  │
│                                                │
│  Layer 4: Data Protection                     │
│  ├─ Database Encryption (AES-256)             │
│  ├─ Password Hashing (bcrypt)                 │
│  ├─ Sensitive data masking                    │
│  └─ GDPR compliance (data retention)          │
│                                                │
│  Layer 5: API Security                        │
│  ├─ Rate Limiting (100 req/min per IP)       │
│  ├─ Input Validation & Sanitization          │
│  ├─ CORS Configuration                        │
│  ├─ SQL Injection Prevention (ORM)            │
│  └─ CSRF Protection (tokens)                  │
│                                                │
│  Layer 6: Monitoring & Logging                │
│  ├─ Security event logging                    │
│  ├─ Intrusion detection (fail2ban)           │
│  ├─ Audit trails (who did what, when)       │
│  └─ Real-time alerts for suspicious activity │
│                                                │
└────────────────────────────────────────────────┘
```

---

## 9. SCALING STRATEGY

### Problem: Single Server Can't Handle Multiple Camera Streams

```
Solution 1: Horizontal Scaling (Add More Servers)
──────────────────────────────────────────────────

                    ┌─────────────────┐
                    │ Load Balancer   │
                    │ (Nginx/HAProxy) │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
      ┌────▼──┐         ┌────▼──┐         ┌────▼──┐
      │Server1│         │Server2│         │Server3│
      │(Cam1) │         │(Cam2) │         │(Cam3) │
      └────┬──┘         └────┬──┘         └────┬──┘
           │                 │                 │
           └─────────────────┼─────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Shared DB      │
                    │  PostgreSQL     │
                    │  + Redis Cache  │
                    └─────────────────┘


Solution 2: Message Queue (For High Volume)
────────────────────────────────────────────

Camera Stream → Frame Queue → Worker Pool → Database
                   (Celery/RabbitMQ)
                   
  ┌─────┐ ┌─────┐ ┌─────┐
  │Work1│ │Work2│ │Work3│ (Process in parallel)
  └─────┘ └─────┘ └─────┘
```

### Performance Targets

```
Single Server Capacity:
├─ 1-2 streams @ 30 FPS (max quality)
├─ 4-6 streams @ 15 FPS (medium)
└─ 10+ streams @ 5 FPS (low latency mode)

With Horizontal Scaling (3 servers):
├─ 6-8 streams @ 30 FPS
├─ 12-18 streams @ 15 FPS
└─ 30+ streams @ 5 FPS

GPU Acceleration (NVIDIA RTX 3080):
├─ Reduces inference time from 60ms → 15ms
├─ Allows 2-3x more concurrent streams
└─ Cost: ~$1200-1500 one-time investment
```

---

## 10. DEVELOPMENT TIMELINE

```
Phase 1: Development (2-3 weeks)
├─ Server setup & API development
├─ Database schema & implementation
├─ Mobile app basic UI
└─ Integration testing

Phase 2: Beta Testing (1-2 weeks)
├─ Real environment testing
├─ Bug fixes & optimization
└─ Security audit

Phase 3: Production Deployment (1 week)
├─ Server provisioning (AWS/DigitalOcean)
├─ CI/CD pipeline setup
├─ SSL certificates & security
└─ Monitoring setup

Phase 4: Post-Launch (Ongoing)
├─ User support
├─ Performance monitoring
├─ Model fine-tuning
└─ Feature updates
```

---

## 11. COST ESTIMATION (Monthly)

```
Cloud Hosting (AWS)
├─ EC2 (t3.xlarge) × 2 servers       $80/month
├─ RDS PostgreSQL (db.t3.small)      $30/month
├─ ElastiCache Redis                 $15/month
├─ S3 Storage (alerts + images)      $5-20/month
└─ Data Transfer & Monitoring        $10-30/month
────────────────────────────────────
CLOUD TOTAL:                         $140-175/month


On-Premises (Self-Hosted)
├─ Server (one-time)                 $1500-3000
├─ Camera hardware                   $200-1000 per camera
├─ Internet bandwidth                $50-200/month
├─ Maintenance                       $200/month
────────────────────────────────────
MONTHLY OPERATIONAL:                 $250-400/month


Mobile App Distribution
├─ iOS App Store Developer           $99/year
├─ Google Play Store Developer       $25 (one-time)
└─ Certificate renewal (annual)      $99/year
────────────────────────────────────
TOTAL APP DISTRIBUTION:              $100-200/year
```

---

## 12. IMPLEMENTATION CHECKLIST

```
☐ Phase 1: Backend Setup
  ☐ Create Flask app structure
  ☐ Implement REST API endpoints
  ☐ Setup WebSocket for real-time data
  ☐ Create database models (SQLAlchemy)
  ☐ Implement user authentication
  ☐ Add logging and error handling

☐ Phase 2: Detection Engine
  ☐ Load YOLOv8 model
  ☐ Load XGBoost model
  ☐ Implement frame processing pipeline
  ☐ Test with sample videos
  ☐ Optimize inference speed
  ☐ Add frame buffering/queuing

☐ Phase 3: Mobile App (React Native)
  ☐ Setup React Native project
  ☐ Create main navigation structure
  ☐ Implement WebSocket connection
  ☐ Build alert display UI
  ☐ Add camera controls
  ☐ Implement local notifications
  ☐ Add settings/configuration screen
  ☐ Build for iOS and Android

☐ Phase 4: Database & Storage
  ☐ Setup PostgreSQL
  ☐ Create migration scripts
  ☐ Setup backup strategy
  ☐ Configure S3 for image storage
  ☐ Implement cleanup jobs (old alerts)

☐ Phase 5: Security & Testing
  ☐ Add JWT authentication
  ☐ Implement rate limiting
  ☐ Setup HTTPS/SSL
  ☐ Security penetration testing
  ☐ Load testing (>100 concurrent users)
  ☐ Integration testing

☐ Phase 6: Deployment
  ☐ Containerize with Docker
  ☐ Setup Docker Compose
  ☐ Deploy to cloud (AWS/DigitalOcean)
  ☐ Configure CI/CD pipeline (GitHub Actions)
  ☐ Setup monitoring (Prometheus/Grafana)
  ☐ Configure alerting for system failures

☐ Phase 7: Documentation & Support
  ☐ API documentation (Swagger)
  ☐ User manual
  ☐ Admin guide
  ☐ Troubleshooting guide
  ☐ Training videos
```

---

## 13. KEY STATISTICS & METRICS

```
Performance Metrics to Monitor:
├─ Frame Processing Time
│  ├─ YOLOv8 inference: 30-60ms
│  ├─ XGBoost prediction: 5-10ms
│  └─ Total: 40-75ms per frame
│
├─ Throughput
│  ├─ Frames per second (FPS)
│  ├─ Alerts per minute
│  └─ API response time (<100ms)
│
├─ Reliability
│  ├─ System uptime (99.9%)
│  ├─ Mean time to recovery (< 5 min)
│  └─ Error rate (< 0.1%)
│
└─ Resource Usage
   ├─ CPU: 60-80%
   ├─ RAM: 4-8GB
   ├─ Bandwidth: 5-20 Mbps per stream
   └─ Storage: 10GB per 1000 alerts
```

---

## 14. CONCLUSION

✅ **YES, THIS IS COMPLETELY FEASIBLE!**

**Why this system is practical:**

1. **Proven Technologies** - All components are production-proven
2. **Scalable** - Can grow from 1 camera to 100+
3. **Cost-Effective** - ~$150-400/month for cloud hosting
4. **Cross-Platform** - Works on iOS, Android, and Web
5. **Real-time** - WebSocket ensures <100ms latency
6. **Secure** - Multiple security layers
7. **Maintainable** - Modern, well-documented code

**Start Simple:**
1. Deploy single server with 1-2 cameras
2. Test and optimize
3. Scale to multiple cameras/servers as needed
4. Add advanced features (analytics, ML improvements, etc.)

**Timeline to Production:** 4-6 weeks for basic implementation

---

**Ready to proceed? Next steps:**
1. Finalize server choice (AWS, DigitalOcean, or on-premise)
2. Start backend development with Flask + Flask-SocketIO
3. Parallelize mobile app development
4. Begin integration testing
5. Deploy to production
