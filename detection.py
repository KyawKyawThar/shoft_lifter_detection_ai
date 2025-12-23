import os
from ultralytics import YOLO
import cv2
import xgboost as xgb
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
import time

# Global cooldown to prevent email spam
last_email_time = 0
email_cooldown = 5  # Minimum seconds between emails

def send_email_alert(frame_number, confidence, video_path, frame):
    """Send email alert asynchronously without blocking detection"""
    global last_email_time
    
    # Check cooldown period
    current_time = time.time()
    if current_time - last_email_time < email_cooldown:
        return
    
    last_email_time = current_time
    
    # For now, log to file instead of email (Gmail rate-limited)
    try:
        with open('alerts.txt', 'a') as f:
            f.write(f"[ALERT] Frame {frame_number}: Suspicious activity detected (Confidence: {confidence:.2f})\n")
        print(f"✓ Alert logged to file for frame {frame_number}")
    except Exception as e:
        print(f"✗ Error logging alert: {e}")
    
    # Uncomment below after 1-2 hours (after Gmail rate-limit resets)
    # email_thread = threading.Thread(
    #     target=_send_email_background,
    #     args=(frame_number, confidence, video_path, frame),
    #     daemon=True
    # )
    # email_thread.start()

def _send_email_background(frame_number, confidence, video_path, frame):
    """Background thread for sending emails"""
    try:
        # Define the SMTP server credentials
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = "kyawkyaw.thar84@gmail.com"
        sender_password = "uvgzlmaaxbjdcoxw"  # Gmail App Password
        sender_name = "shoft_lifting_detection"
        recipient_email = 'kyawkyaw.thar14@gmail.com'
        
        # Create the email content (without image attachment for reliability)
        subject = "🚨 Shoplifting Alert - " + sender_name
        body = f" ⚠ Alert! Suspicious activity detected in video.\nFrame: {frame_number}\nConfidence: {confidence:.2f}\n\nDetection System: {sender_name}"
        
        # Set up the MIME
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{sender_name} <{sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to the SMTP server and send the email
        print(f"📧 Connecting to {smtp_server}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(0)  # Set to 1 for debug info
        
        print(f"🔒 Starting TLS...")
        server.starttls()
        
        print(f"🔑 Logging in as {sender_email}...")
        server.login(sender_email, sender_password)
        
        print(f"✉️  Sending email...")
        server.send_message(msg)
        server.quit()
        
        print(f"✓ Email alert sent successfully for frame {frame_number}")
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"✗ Authentication Failed: {str(e)}")
        print(f"  → Check if App Password is correct")
        print(f"  → Go to: https://myaccount.google.com/apppasswords")
        
    except smtplib.SMTPServerDisconnected as e:
        print(f"✗ Server disconnected: {str(e)}")
        print(f"  → Usually caused by auth failure or invalid credentials")
        
    except smtplib.SMTPException as e:
        print(f"✗ SMTP Error: {str(e)[:100]}")
        
    except Exception as e:
        print(f"✗ Unexpected Error: {type(e).__name__}: {str(e)[:100]}")


def detect_shoplifting(video_path):
    model_yolo = YOLO(r"./best.pt")
    model = xgb.Booster()
    model.load_model(r"./model_weights.json")

    cap = cv2.VideoCapture(video_path)

    print('Total Frame', cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc('F', 'M', 'P', '4')
    
    # Generate a unique output path
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = fr"./{video_name}_output.mp4"
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_tot = 0

    while cap.isOpened():
        success, frame = cap.read()

        if success:
            results = model_yolo(frame, verbose=False)

            # Visualize the results on the frame
            annotated_frame = results[0].plot(boxes=False)

            for r in results:
                bound_box = r.boxes.xyxy
                conf = r.boxes.conf.tolist()
                keypoints = r.keypoints.xyn.tolist()

                print(f'Frame {frame_tot}: Detected {len(bound_box)} bounding boxes')

                for index, box in enumerate(bound_box):
                    if conf[index] > 0.75:
                        x1, y1, x2, y2 = box.tolist()
                        data = {}

                        # Initialize the x and y lists for each possible key
                        for j in range(len(keypoints[index])):
                            data[f'x{j}'] = keypoints[index][j][0]
                            data[f'y{j}'] = keypoints[index][j][1]

                        # print(f'Bounding Box {index}: {data}')
                        df = pd.DataFrame(data, index=[0])
                        dmatrix = xgb.DMatrix(df)
                        cut = model.predict(dmatrix)
                        binary_predictions = (cut > 0.5).astype(int)[0]
                        print(f'Prediction: {binary_predictions}')

                        if binary_predictions == 0:  # Suspicious activity
                            conf_text = f'Suspicious ({conf[index]:.2f})'
                            cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 7, 58), 2)
                            cv2.putText(annotated_frame, conf_text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 7, 58), 2)
                            # Send email alert if confidence is high
                            if conf[index] >= 0.85:
                                send_email_alert(frame_tot, conf[index], video_path, annotated_frame)
                        elif binary_predictions == 1:  # Normal activity
                            conf_text = f'Normal ({conf[index]:.2f})'
                            cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (57, 255, 20), 2)
                            cv2.putText(annotated_frame, conf_text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_DUPLEX, 1.0, (57, 255, 20), 2)


            cv2.imshow('Frame', annotated_frame)

            out.write(annotated_frame)
            frame_tot += 1
            print('Processed Frame:', frame_tot)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Example usage:
video_path = r"./gettyimages-1995820194-640_adpp.mp4"
detect_shoplifting(video_path)
