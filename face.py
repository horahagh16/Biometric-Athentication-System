from deepface import DeepFace
# Face Processing Function
def face_analyzer(img):
    """Analyze the face image for emotion, gender, and race."""
    objs = DeepFace.analyze(img_path=img, actions=("emotion", "gender", "race"), enforce_detection=False, detector_backend="retinaface")
    return f"{objs[0]['dominant_emotion']}{objs[0]['dominant_gender']}{objs[0]['dominant_race']}"
