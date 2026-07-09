

import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st


from database.db import get_all_students

print("FACE PIPELINE LOADED")
# -----------------------------
# Load Dlib Models (Only Once)
# -----------------------------
@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    shape_predictor = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    face_rec_model = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, shape_predictor, face_rec_model


# -----------------------------
# Generate Face Embeddings
# -----------------------------
def get_face_embeddings(image_np):

    detector, sp, facerec = load_dlib_models()

    st.write("Image shape:", image_np.shape)
    st.write("Image dtype:", image_np.dtype)

    faces = detector(image_np, 1)

    st.write("Detector found:", len(faces))

    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        descriptor = facerec.compute_face_descriptor(image_np, shape)
        encodings.append(np.array(descriptor))

    return np.array(encodings)


# -----------------------------
# Train Face Classifier
# -----------------------------
@st.cache_resource
def get_trained_model():

    x_train = []
    y_train = []

    students = get_all_students()

    if not students:
        return None

    for student in students:
        embedding = student.get("face_embedding")

        if embedding is not None:
            x_train.append(np.array(embedding))
            y_train.append(student["student_id"])

    if len(x_train) == 0:
        return None

    # Sirf 1 student hai
    if len(set(y_train)) < 2:
        return {
            "clf": None,
            "x": x_train,
            "y": y_train
        }

    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    try:
        clf.fit(x_train, y_train)
    except ValueError:
        return None

    return {
        "clf": clf,
        "x": x_train,
        "y": y_train
    }
# -----------------------------
# Refresh Cached Classifier
# -----------------------------
def train_classifier():

    st.cache_resource.clear()

    model = get_trained_model()

    return bool(model)


# -----------------------------
# Predict Student
# -----------------------------
def predict_attendance(image_np):
    print("FUNCTION STARTED")
    print(__file__)

    encodings = get_face_embeddings(image_np)

    
    print("Encodings:", encodings)
    print("Encodings shape:", encodings.shape)
    print("Length:", len(encodings))

    detected_students = {}

    model = get_trained_model()

    print("MODEL =", model)

    if model is None:
        print("MODEL IS NONE")
        return {}, [], len(encodings)

    print("MODEL IS NOT NONE")

    clf = model["clf"]
    x_train = model["x"]
    y_train = model["y"]

    all_student_ids = sorted(set(y_train))
    st.write("Before for loop")

    for encoding in encodings:
        st.write("Inside loop")

        if clf is not None:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_student_ids[0])

        st.write("Predicted:", predicted_id)

        student_embedding = x_train[y_train.index(predicted_id)]

        distance = np.linalg.norm(student_embedding - encoding)

        st.write("Distance:", distance)

        threshold = 0.60

        st.write("Distance <= Threshold ?", distance <= threshold)

        if distance <= threshold:
            st.write("ADDING STUDENT")
            detected_students[predicted_id] = distance

    st.write("Detected Students:", detected_students)

    return detected_students, all_student_ids, len(encodings)