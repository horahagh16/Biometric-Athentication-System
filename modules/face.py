from deepface import DeepFace
# Face Processing Function
def face_analyzer(img):
    # Load image and analyze
    objs = DeepFace.analyze(
        img_path=img,
        actions=("emotion", "gender", "race"),
        enforce_detection=False,
        detector_backend="retinaface",
    )

    # Extract relevant information
    dominant_emotion = objs[0]['dominant_emotion']
    dominant_gender = objs[0]['dominant_gender']
    dominant_race = objs[0]['dominant_race']

    # Concatenate into a single string
    result = f"{dominant_emotion}{dominant_gender}{dominant_race}"

    return result