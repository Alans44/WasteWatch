# WasteWatch
 HackPrinceton 24' 

WasteWatch is a computer vision-powered waste detection application that classifies and tracks recyclable, non-recyclable, and hazardous waste in real-time using satellite and CCTV imagery. Built with YOLO, this project aims to monitor pollution and aid in targeted waste management efforts.

## Features
- **Real-Time Waste Detection**: Detects and classifies waste items as recyclable, non-recyclable, or hazardous.
- **Full-Screen Webcam Feed**: Displays a full-screen feed for live monitoring.
- **Detection Log**: Logs detected items in a collapsible sidebar for easy tracking.
- **Customizable UI**: Sleek, full-screen design with color-coded detection categories.

## Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/alans44/WasteWatch.git
2. Install dependencies
3. configure your model in a settings.py
4. streamlit run app.py

Technologies
Streamlit: For building an interactive and web-based UI.
YOLO: Model used for real-time object detection and classification.
OpenCV: For handling image and video streams.