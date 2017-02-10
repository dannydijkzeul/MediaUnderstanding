import dlib
import openface
from skimage import io 



def makeAffine(img):

	face_detector = dlib.get_frontal_face_detector()
	predictor_model = "shape_predictor_68_face_landmarks.dat"

	face_detector = dlib.get_frontal_face_detector()
	face_pose_predictor = dlib.shape_predictor(predictor_model)
	face_aligner = openface.AlignDlib(predictor_model)

	detected_faces = face_detector(img, 1)
	for i, face_rect in enumerate(detected_faces):
		pose_landmarks = face_pose_predictor(img, face_rect)
		alignedFace = face_aligner.align(64, img, face_rect, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
	if len(detected_faces) == 0:
		return None
	else:
		return alignedFace

