# Mobile App Setup Guide for iOS and Android

## Option 1: React Native (Recommended for Cross-Platform)

### Installation
```bash
npx react-native init ShopliftingDetectionApp
cd ShopliftingDetectionApp
npm install socket.io-client axios
```

### App.js Configuration
```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, ScrollView, Alert, Image } from 'react-native';
import io from 'socket.io-client';
import axios from 'axios';

const API_URL = 'http://YOUR_SERVER_IP:5000'; // Change to your server IP
const SOCKET = io(API_URL);

export default function App() {
  const [cameraSource, setCameraSource] = useState('0');
  const [isRunning, setIsRunning] = useState(false);
  const [alerts, setAlerts] = useState([]);
  const [frameData, setFrameData] = useState(null);

  useEffect(() => {
    // Connect to WebSocket
    SOCKET.on('connect', () => {
      console.log('Connected to server');
    });

    SOCKET.on('alert', (data) => {
      Alert.alert('🚨 ALERT', `Suspicious activity detected!\nConfidence: ${data.confidence.toFixed(2)}`);
      setAlerts([data, ...alerts]);
    });

    SOCKET.on('frame', (data) => {
      setFrameData(data.data);
    });

    return () => SOCKET.off();
  }, [alerts]);

  const startDetection = async () => {
    try {
      const response = await axios.post(`${API_URL}/api/start/${cameraSource}`);
      setIsRunning(true);
      Alert.alert('Success', response.data.message);
    } catch (error) {
      Alert.alert('Error', 'Failed to start detection');
    }
  };

  const stopDetection = async () => {
    try {
      const response = await axios.post(`${API_URL}/api/stop`);
      setIsRunning(false);
      Alert.alert('Success', response.data.message);
    } catch (error) {
      Alert.alert('Error', 'Failed to stop detection');
    }
  };

  return (
    <ScrollView style={{ flex: 1, padding: 20, backgroundColor: '#f5f5f5' }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 20 }}>
        🛒 Shoplifting Detection
      </Text>

      {/* Video Stream Display */}
      {frameData && (
        <Image
          source={{ uri: `data:image/jpg;base64,${frameData}` }}
          style={{ width: '100%', height: 300, marginBottom: 20, borderRadius: 10 }}
        />
      )}

      {/* Camera Source Input */}
      <Text style={{ fontSize: 16, marginBottom: 10 }}>Camera Source:</Text>
      <TextInput
        placeholder="0 (webcam) or RTSP URL"
        value={cameraSource}
        onChangeText={setCameraSource}
        style={{
          borderWidth: 1,
          borderColor: '#ddd',
          padding: 10,
          marginBottom: 20,
          borderRadius: 5,
        }}
      />

      {/* Control Buttons */}
      <TouchableOpacity
        onPress={startDetection}
        disabled={isRunning}
        style={{
          backgroundColor: isRunning ? '#ccc' : '#4CAF50',
          padding: 15,
          borderRadius: 10,
          marginBottom: 10,
        }}
      >
        <Text style={{ color: 'white', fontSize: 16, textAlign: 'center', fontWeight: 'bold' }}>
          ▶ Start Detection
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        onPress={stopDetection}
        disabled={!isRunning}
        style={{
          backgroundColor: isRunning ? '#f44336' : '#ccc',
          padding: 15,
          borderRadius: 10,
          marginBottom: 20,
        }}
      >
        <Text style={{ color: 'white', fontSize: 16, textAlign: 'center', fontWeight: 'bold' }}>
          ⏹ Stop Detection
        </Text>
      </TouchableOpacity>

      {/* Alerts History */}
      <Text style={{ fontSize: 16, fontWeight: 'bold', marginBottom: 10 }}>
        Alerts ({alerts.length})
      </Text>
      {alerts.map((alert, index) => (
        <View
          key={index}
          style={{
            backgroundColor: 'white',
            padding: 15,
            marginBottom: 10,
            borderRadius: 5,
            borderLeftWidth: 4,
            borderLeftColor: '#f44336',
          }}
        >
          <Text style={{ fontWeight: 'bold' }}>Frame: {alert.frame}</Text>
          <Text>Confidence: {(alert.confidence * 100).toFixed(2)}%</Text>
          <Text style={{ fontSize: 12, color: '#666' }}>{new Date(alert.timestamp).toLocaleTimeString()}</Text>
        </View>
      ))}
    </ScrollView>
  );
}
```

## Option 2: Flutter (Alternative)

### Installation
```bash
flutter create shoplifting_detection
cd shoplifting_detection
flutter pub add socket_io_client http
```

### Main Dart Code
```dart
import 'package:flutter/material.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Shoplifting Detection',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const DetectionScreen(),
    );
  }
}

class DetectionScreen extends StatefulWidget {
  const DetectionScreen({Key? key}) : super(key: key);

  @override
  State<DetectionScreen> createState() => _DetectionScreenState();
}

class _DetectionScreenState extends State<DetectionScreen> {
  late IO.Socket socket;
  bool isRunning = false;
  List<Map<String, dynamic>> alerts = [];
  TextEditingController cameraSourceController = TextEditingController(text: '0');
  
  static const String serverUrl = 'http://YOUR_SERVER_IP:5000';

  @override
  void initState() {
    super.initState();
    _connectToServer();
  }

  void _connectToServer() {
    socket = IO.io(serverUrl, IO.OptionBuilder().build());
    
    socket.on('connect', (_) {
      print('Connected to server');
    });

    socket.on('alert', (data) {
      setState(() {
        alerts.insert(0, data);
      });
      _showAlert('🚨 Alert', 'Suspicious activity detected!\nConfidence: ${(data['confidence'] * 100).toStringAsFixed(2)}%');
    });

    socket.on('disconnect', (_) {
      print('Disconnected from server');
    });
  }

  void _showAlert(String title, String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) => AlertDialog(
        title: Text(title),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  Future<void> _startDetection() async {
    try {
      final response = await http.post(
        Uri.parse('$serverUrl/api/start/${cameraSourceController.text}'),
      );
      
      if (response.statusCode == 200) {
        setState(() => isRunning = true);
        _showAlert('Success', 'Detection started');
      }
    } catch (e) {
      _showAlert('Error', 'Failed to start detection: $e');
    }
  }

  Future<void> _stopDetection() async {
    try {
      final response = await http.post(Uri.parse('$serverUrl/api/stop'));
      
      if (response.statusCode == 200) {
        setState(() => isRunning = false);
        _showAlert('Success', 'Detection stopped');
      }
    } catch (e) {
      _showAlert('Error', 'Failed to stop detection: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🛒 Shoplifting Detection')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          TextField(
            controller: cameraSourceController,
            decoration: InputDecoration(
              labelText: 'Camera Source',
              hintText: '0 (webcam) or RTSP URL',
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
            ),
          ),
          const SizedBox(height: 20),
          ElevatedButton.icon(
            onPressed: isRunning ? null : _startDetection,
            icon: const Icon(Icons.play_arrow),
            label: const Text('Start Detection'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.green,
              padding: const EdgeInsets.symmetric(vertical: 15),
            ),
          ),
          const SizedBox(height: 10),
          ElevatedButton.icon(
            onPressed: isRunning ? _stopDetection : null,
            icon: const Icon(Icons.stop),
            label: const Text('Stop Detection'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              padding: const EdgeInsets.symmetric(vertical: 15),
            ),
          ),
          const SizedBox(height: 30),
          Text(
            'Alerts (${alerts.length})',
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          ...alerts.map((alert) => Card(
            child: ListTile(
              leading: const Icon(Icons.warning, color: Colors.red),
              title: Text('Frame: ${alert['frame']}'),
              subtitle: Text('Confidence: ${(alert['confidence'] * 100).toStringAsFixed(2)}%'),
              trailing: Text(DateTime.parse(alert['timestamp']).toString().split('.')[0]),
            ),
          )),
        ],
      ),
    );
  }

  @override
  void dispose() {
    socket.disconnect();
    cameraSourceController.dispose();
    super.dispose();
  }
}
```

## Installation Instructions

### For React Native:
```bash
# iOS
cd ios && pod install && cd ..
npx react-native run-ios

# Android
npx react-native run-android
```

### For Flutter:
```bash
# iOS
flutter run -d iphone

# Android
flutter run -d android
```

## Server Setup

### 1. Install dependencies:
```bash
pip install flask flask-cors flask-socketio python-socketio python-engineio
```

### 2. Run the server:
```bash
python app.py
```

The server will be available at:
- REST API: `http://YOUR_IP:5000/api/`
- WebSocket: `ws://YOUR_IP:5000/socket.io/`

## Camera Sources Examples

| Source | Example |
|--------|---------|
| Webcam | `0` |
| Local video | `./video.mp4` |
| IP Camera (RTSP) | `rtsp://192.168.1.100:554/stream` |
| IP Camera (HTTP) | `http://192.168.1.100:8080/video` |

## API Endpoints

### Start Detection
```
POST /api/start/<source>
Response: {"message": "Detection started", "source": "..."}
```

### Stop Detection
```
POST /api/stop
Response: {"message": "Detection stopped"}
```

### Get Status
```
GET /api/status
Response: {"status": "active/inactive", "camera_source": "...", "alerts_pending": 0}
```

### Get Alerts
```
GET /api/alerts
Response: {"alerts": [...]}
```

## Network Configuration

Make sure:
1. Server IP is accessible from mobile device (same WiFi network)
2. Port 5000 is not blocked by firewall
3. Update `API_URL` in mobile app with your server IP
