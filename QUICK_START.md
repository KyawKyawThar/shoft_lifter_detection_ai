# Quick Start Guide: Deploy Your System in 30 Minutes

## PART 1: Start the Backend Server (5 minutes)

### Install Dependencies
```bash
cd /Users/kkt/Desktop/shop_lifter
pip install flask flask-cors flask-socketio
```

### Run the Server
```bash
python app.py
```

Expected output:
```
🚀 Shoplifting Detection Server
📱 REST API: http://localhost:5000/api/
🔌 WebSocket: ws://localhost:5000/socket.io/
```

Server is now running! 🎉

---

## PART 2: Test the API (Using cURL or Postman)

### Start Detection (Webcam)
```bash
curl -X POST http://localhost:5000/api/start/0
```

Response:
```json
{"message": "Detection started", "source": "0"}
```

### Start Detection (IP Camera - RTSP)
```bash
curl -X POST http://localhost:5000/api/start/rtsp://192.168.1.100:554/stream
```

### Get System Status
```bash
curl http://localhost:5000/api/status
```

### Get Pending Alerts
```bash
curl http://localhost:5000/api/alerts
```

### Stop Detection
```bash
curl -X POST http://localhost:5000/api/stop
```

---

## PART 3: Create Simple Web Dashboard (Quick Test)

Create file: `dashboard.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Shoplifting Detection Dashboard</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f0f0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: #333; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .controls { display: flex; gap: 10px; margin-bottom: 20px; }
        button { padding: 10px 20px; font-size: 16px; cursor: pointer; border: none; border-radius: 5px; }
        .btn-start { background: #4CAF50; color: white; }
        .btn-stop { background: #f44336; color: white; }
        .status { padding: 15px; background: white; border-radius: 5px; margin-bottom: 20px; }
        .alerts-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }
        .alert-card { background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #f44336; }
        .alert-card h3 { color: #f44336; }
        .feed { width: 100%; border: 2px solid #333; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛒 Shoplifting Detection System</h1>
            <p>Real-time monitoring dashboard</p>
        </div>

        <div class="controls">
            <input type="text" id="cameraSource" placeholder="0 (webcam) or RTSP URL" value="0" style="padding: 10px; flex: 1; border: 1px solid #ddd; border-radius: 5px;">
            <button class="btn-start" onclick="startDetection()">▶ Start</button>
            <button class="btn-stop" onclick="stopDetection()">⏹ Stop</button>
        </div>

        <div class="status">
            <h3>System Status</h3>
            <p>Status: <span id="status">Disconnected</span></p>
            <p>Camera: <span id="camera">None</span></p>
            <p>Alerts: <span id="alertCount">0</span></p>
        </div>

        <div>
            <h2>Live Stream</h2>
            <img id="videoFeed" src="" alt="No feed" class="feed" style="display:none;">
            <p id="noFeed">Waiting for detection to start...</p>
        </div>

        <div>
            <h2>Recent Alerts</h2>
            <div class="alerts-container" id="alertsContainer">
                <p>No alerts yet</p>
            </div>
        </div>
    </div>

    <script>
        const socket = io('http://localhost:5000');
        let alerts = [];

        socket.on('connect', () => {
            document.getElementById('status').textContent = 'Connected';
            console.log('Connected to server');
        });

        socket.on('alert', (data) => {
            alerts.unshift(data);
            updateAlerts();
            showNotification(`🚨 Alert! Frame ${data.frame} - Confidence: ${(data.confidence*100).toFixed(2)}%`);
        });

        socket.on('frame', (data) => {
            if (data.data) {
                const img = document.getElementById('videoFeed');
                img.src = 'data:image/jpeg;base64,' + btoa(String.fromCharCode(...new Uint8Array(data.data)));
                img.style.display = 'block';
                document.getElementById('noFeed').style.display = 'none';
            }
        });

        async function startDetection() {
            const source = document.getElementById('cameraSource').value || '0';
            try {
                const response = await fetch(`http://localhost:5000/api/start/${source}`, { method: 'POST' });
                const data = await response.json();
                document.getElementById('camera').textContent = source;
                showNotification('✅ Detection started: ' + source);
            } catch (e) {
                showNotification('❌ Error: ' + e.message);
            }
        }

        async function stopDetection() {
            try {
                const response = await fetch('http://localhost:5000/api/stop', { method: 'POST' });
                const data = await response.json();
                document.getElementById('camera').textContent = 'Stopped';
                document.getElementById('noFeed').style.display = 'block';
                document.getElementById('videoFeed').style.display = 'none';
                showNotification('⏹ Detection stopped');
            } catch (e) {
                showNotification('❌ Error: ' + e.message);
            }
        }

        function updateAlerts() {
            const container = document.getElementById('alertsContainer');
            document.getElementById('alertCount').textContent = alerts.length;
            
            if (alerts.length === 0) {
                container.innerHTML = '<p>No alerts yet</p>';
                return;
            }

            container.innerHTML = alerts.slice(0, 10).map(alert => `
                <div class="alert-card">
                    <h3>Frame ${alert.frame}</h3>
                    <p>Confidence: ${(alert.confidence*100).toFixed(2)}%</p>
                    <p>Type: ${alert.type}</p>
                    <p style="font-size: 12px; color: #666;">
                        ${new Date(alert.timestamp).toLocaleTimeString()}
                    </p>
                </div>
            `).join('');
        }

        function showNotification(message) {
            console.log(message);
            alert(message); // Replace with toast notification library for production
        }
    </script>
</body>
</html>
```

Open in browser: `http://localhost:5000/dashboard.html` (or save locally and open)

---

## PART 4: Mobile App Quick Test

### Option A: Use Expo (Easiest - No Build Required)

```bash
# Install Expo CLI
npm install -g expo-cli

# Create new React Native app
expo init ShopliftingDetectionApp --template
cd ShopliftingDetectionApp

# Install dependencies
npm install socket.io-client axios
npm install react-native-screens react-native-safe-area-context

# Create App.js (see MOBILE_APP_SETUP.md for full code)

# Run on iOS simulator
expo start --ios

# Or Android emulator
expo start --android

# Or scan QR code with Expo Go app on your phone
expo start
```

### Option B: React Native CLI (Production)

```bash
npx react-native init ShopliftingDetectionApp
cd ShopliftingDetectionApp
npm install socket.io-client axios

# For iOS
cd ios && pod install && cd ..
npx react-native run-ios

# For Android
npx react-native run-android
```

---

## PART 5: Connect Everything

### Update API_URL in your app:

**Find your computer's IP address:**
```bash
# macOS
ifconfig | grep inet

# Linux
ip addr

# Windows
ipconfig
```

Look for `192.168.x.x` or `10.x.x.x` (not localhost!)

**Example: 192.168.1.100**

Then update in your mobile app code:
```javascript
const API_URL = 'http://192.168.1.100:5000';
```

---

## TESTING CHECKLIST ✅

```
☐ Backend Server Running
  └─ Test: curl http://localhost:5000/api/status

☐ Camera Connection
  └─ Start: curl -X POST http://localhost:5000/api/start/0
  
☐ WebSocket Connection
  └─ Dashboard loads & connects
  
☐ Frame Streaming
  └─ Live video appears in browser/app
  
☐ Alert Generation
  └─ Person detected in frame → Alert shown
  
☐ Mobile App
  └─ Connects to server
  └─ Shows live stream
  └─ Receives alerts in real-time
```

---

## TROUBLESHOOTING

### Problem: "Connection refused"
**Solution:** 
- Make sure Flask server is running: `python app.py`
- Check IP address is correct (not localhost from mobile)
- Check firewall allows port 5000

### Problem: "No frames showing"
**Solution:**
- Check camera source is valid (0 for webcam)
- For IP cameras: verify RTSP URL is correct
- Check logs for inference errors

### Problem: "Too slow / Laggy"
**Solution:**
- Reduce FPS: Lower resolution in camera settings
- Add GPU: Install NVIDIA GPU for CUDA acceleration
- Reduce confidence threshold to skip frames

### Problem: "Out of memory"
**Solution:**
- Reduce frame queue size
- Limit number of concurrent connections
- Use garbage collection optimization

---

## NEXT STEPS

1. ✅ Backend running locally → Test with `curl`
2. ✅ Browser dashboard working → See live feed
3. ✅ Mobile app connected → Receive alerts
4. ⬜ Deploy to cloud → AWS/DigitalOcean
5. ⬜ Add authentication → JWT tokens
6. ⬜ Add database → PostgreSQL
7. ⬜ Production optimizations → Caching, compression
8. ⬜ Publish apps → App Store & Play Store

---

## QUICK REFERENCE: API ENDPOINTS

```
Start Detection
POST /api/start/<source>
  source: "0" (webcam) or "rtsp://..." or "http://..."
  Response: {message, source}

Stop Detection
POST /api/stop
  Response: {message}

Get Status
GET /api/status
  Response: {status, camera_source, alerts_pending}

Get Alerts
GET /api/alerts
  Response: {alerts: [...]}

WebSocket Events
  "alert" - New suspicious activity
  "frame" - Video frame data
  "message" - System messages
```

---

## ESTIMATED TIME TO PRODUCTION

| Task | Time |
|------|------|
| Backend setup | 2-3 days |
| Mobile app UI | 3-5 days |
| Testing & debugging | 2-3 days |
| Deployment | 1-2 days |
| **Total** | **1-2 weeks** |

You've already done the hard part (detection models)!
The rest is just plumbing 🔧

Good luck! 🚀
