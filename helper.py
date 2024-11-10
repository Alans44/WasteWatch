from ultralytics import YOLO
import time
import streamlit as st
import cv2
import settings
import threading

def sleep_and_clear_success():
    time.sleep(3)
    st.session_state['recyclable_placeholder'].empty()
    st.session_state['non_recyclable_placeholder'].empty()
    st.session_state['hazardous_placeholder'].empty()

def load_model(model_path):
    model = YOLO(model_path)
    return model

def classify_waste_type(detected_items):
    recyclable_items = set(detected_items) & set(settings.RECYCLABLE)
    non_recyclable_items = set(detected_items) & set(settings.NON_RECYCLABLE)
    hazardous_items = set(detected_items) & set(settings.HAZARDOUS)
    return recyclable_items, non_recyclable_items, hazardous_items

def remove_dash_from_class_name(class_name):
    return class_name.replace("_", " ")

def _display_detected_frames(model, st_frame, image):
    if 'unique_classes' not in st.session_state:
        st.session_state['unique_classes'] = set()
    res = model.predict(image, conf=0.6)
    names = model.names
    detected_items = set()
    for result in res:
        new_classes = set([names[int(c)] for c in result.boxes.cls])
        if new_classes != st.session_state['unique_classes']:
            st.session_state['unique_classes'] = new_classes
            st.session_state['recyclable_placeholder'].markdown('')
            st.session_state['non_recyclable_placeholder'].markdown('')
            st.session_state['hazardous_placeholder'].markdown('')
            detected_items.update(st.session_state['unique_classes'])
            recyclable_items, non_recyclable_items, hazardous_items = classify_waste_type(detected_items)
            if recyclable_items:
                detected_items_str = "\n- ".join(remove_dash_from_class_name(item) for item in recyclable_items)
                st.session_state['recyclable_placeholder'].markdown(
                    f"<div class='stRecyclable'><strong>Recyclable items:</strong>\n\n- {detected_items_str}</div>",
                    unsafe_allow_html=True
                )
            if non_recyclable_items:
                detected_items_str = "\n- ".join(remove_dash_from_class_name(item) for item in non_recyclable_items)
                st.session_state['non_recyclable_placeholder'].markdown(
                    f"<div class='stNonRecyclable'><strong>Non-Recyclable items:</strong>\n\n- {detected_items_str}</div>",
                    unsafe_allow_html=True
                )
            if hazardous_items:
                detected_items_str = "\n- ".join(remove_dash_from_class_name(item) for item in hazardous_items)
                st.session_state['hazardous_placeholder'].markdown(
                    f"<div class='stHazardous'><strong>Hazardous items:</strong>\n\n- {detected_items_str}</div>",
                    unsafe_allow_html=True
                )
            threading.Thread(target=sleep_and_clear_success).start()
    res_plotted = res[0].plot()
    st_frame.image(res_plotted, channels="BGR", use_column_width=True, output_format='auto')

def play_webcam(model, st_frame):
    source_webcam = settings.WEBCAM_PATH
    try:
        vid_cap = cv2.VideoCapture(source_webcam)
        while vid_cap.isOpened():
            success, image = vid_cap.read()
            if success:
                _display_detected_frames(model, st_frame, image)
            else:
                vid_cap.release()
                break
    except Exception as e:
        st.error("Error loading video: " + str(e))