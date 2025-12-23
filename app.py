"""
Shoplifting Detection Server with Live CCTV Support
Supports REST API and WebSocket for real-time alerts
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading
import cv2
import json
from datetime import datetime
from ultralytics import YOLO
import xgboost as xgb
import pandas as pd
import queue

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Detection configuration
detection_active = False
camera_stream = None
alerts_queue = queue.Queue()
last_alert_time = 0
alert_cooldown = 5  # seconds

# Load models
model_yolo = YOLO("./best.pt")
model_xgb = xgb.Booster()
model_xgb.load_model("./model_weights.json")

class CCTVDetector:
    def __init__(self, source):
        """
        source: IP camera URL (RTSP), file path, or 0 for webcam
        Example: "rtsp://192.168.1.100:554/stream"
                "http://192.168.1.100:8080/video"
                "./video.mp4"
                0 (for webcam)
        """
        self.source = source
        self.cap = None
        self.running = False
        self.frame_count = 0
        
    def start(self):
        """Open camera/stream connection"""
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            return False
        self.running = True
        return True
    
    def stop(self):
        """Close camera connection"""
        self.running = False
        if self.cap:
            self.cap.release()
    
    def get_frame(self):
        """Get next frame from camera"""
        if not self.cap:
            return None
        success, frame = self.cap.read()
        return frame if success else None
    
    def process_frame(self, frame):
        """Process frame with YOLOv8 and XGBoost"""
        results = model_yolo(frame, verbose=False)
        annotated_frame = results[0].plot(boxes=False)
        
        alerts = []
        
        for r in results:
            bound_box = r.boxes.xyxy
            conf = r.boxes.conf.tolist()
            keypoints = r.keypoints.xyn.tolist()
            
            for index, box in enumerate(bound_box):
                if conf[index] > 0.75 and len(keypoints) > index:
                    x1, y1, x2, y2 = box.tolist()
                    data = {}
                    
                    for j in range(len(keypoints[index])):
                        data[f'x{j}'] = keypoints[index][j][0]
                        data[f'y{j}'] = keypoints[index][j][1]
                    
                    try:
                        df = pd.DataFrame(data, index=[0])
                        dmatrix = xgb.DMatrix(df)
                        prediction = model_xgb.predict(dmatrix)
                        binary_pred = (prediction > 0.5).astype(int)[0]
                        
                        if binary_pred == 0:  # Suspicious
                            conf_text = f'Suspicious ({conf[index]:.2f})'
                            color = (255, 7, 58)  # Red
                            
                            if conf[index] >= 0.85:
                                alerts.append({
                                    'frame': self.frame_count,
                                    'confidence': float(conf[index]),
                                    'type': 'suspicious',
                                    'timestamp': datetime.now().isoformat()
                                })
                        else:  # Normal
                            conf_text = f'Normal ({conf[index]:.2f})'
                            color = (57, 255, 20)  # Green
                        
                        cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                        cv2.putText(annotated_frame, conf_text, (int(x1), int(y1) - 10), 
                                   cv2.FONT_HERSHEY_DUPLEX, 1.0, color, 2)
                    except:
                        pass
        
        self.frame_count += 1
        return annotated_frame, alerts

def detection_loop():
    """Main detection loop running in background thread"""
    global last_alert_time
    
    detector = CCTVDetector(camera_stream)
    if not detector.start():
        socketio.emit('error', {'message': 'Failed to open camera stream'})
        return
    
    try:
        while detection_active:
            frame = detector.get_frame()
            if frame is None:
                break
            
            annotated_frame, alerts = detector.process_frame(frame)
            
            # Handle alerts
            for alert in alerts:
                current_time = datetime.now().timestamp()
                if current_time - last_alert_time >= alert_cooldown:
                    alerts_queue.put(alert)
                    socketio.emit('alert', alert, broadcast=True)
                    
                    # Log alert
                    with open('alerts.txt', 'a') as f:
                        f.write(json.dumps(alert) + '\n')
                    
                    last_alert_time = current_time
            
            # Emit frame to connected clients
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_data = buffer.tobytes()
            socketio.emit('frame', {'data': frame_data}, broadcast=True)
    
    finally:
        detector.stop()

# REST API Endpoints

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get detection system status"""
    return jsonify({
        'status': 'active' if detection_active else 'inactive',
        'camera_source': camera_stream,
        'alerts_pending': alerts_queue.qsize()
    })

@app.route('/api/start/<path:source>', methods=['POST'])
def start_detection(source):
    """Start detection with given camera source"""
    global camera_stream, detection_active
    
    camera_stream = source
    detection_active = True
    
    # Start detection in background thread
    thread = threading.Thread(target=detection_loop, daemon=True)
    thread.start()
    
    return jsonify({'message': 'Detection started', 'source': source})

@app.route('/api/stop', methods=['POST'])
def stop_detection():
    """Stop detection"""
    global detection_active
    detection_active = False
    return jsonify({'message': 'Detection stopped'})

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get pending alerts"""
    alerts = []
    while not alerts_queue.empty():
        alerts.append(alerts_queue.get())
    return jsonify({'alerts': alerts})

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update detection configuration"""
    # Placeholder for future config updates
    return jsonify({'message': 'Configuration updated'})

# WebSocket Events

@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected to detection server'})
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('start_stream')
def handle_start_stream(data):
    """Start detection stream from mobile app"""
    global camera_stream, detection_active
    
    camera_source = data.get('source', '0')
    camera_stream = camera_source
    detection_active = True
    
    thread = threading.Thread(target=detection_loop, daemon=True)
    thread.start()
    
    emit('message', {'data': 'Stream started'}, broadcast=True)

@socketio.on('stop_stream')
def handle_stop_stream():
    """Stop detection stream"""
    global detection_active
    detection_active = False
    emit('message', {'data': 'Stream stopped'}, broadcast=True)

if __name__ == '__main__':
    print("🚀 Shoplifting Detection Server")
    print("📱 REST API: http://localhost:5000/api/")
    print("🔌 WebSocket: ws://localhost:5000/socket.io/")
    print("\nCamera sources:")
    print("  - Webcam: 0")
    print("  - RTSP: rtsp://192.168.1.100:554/stream")
    print("  - HTTP: http://192.168.1.100:8080/video")
    print("  - File: ./video.mp4")
    print("\nStart detection: POST /api/start/<source>")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
