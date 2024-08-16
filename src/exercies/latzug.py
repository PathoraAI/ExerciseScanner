import mediapipe as mp
from src.ThreadedCamera import ThreadedCamera
from src.exercies.Exercise import Exercise

from src.utils import *

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose_landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=2, color=(0, 0, 255)) # color circles
pose_connection_drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0)) # color lines
PRESENCE_THRESHOLD = 0.5
VISIBILITY_THRESHOLD = 0.5
performedRep = False


class Latzug(Exercise):
    def __init__(self):
        pass

    def exercise(self, source):
        threaded_camera = ThreadedCamera(source)
        scount = 0
        while True:
            success, image = threaded_camera.show_frame()
            if not success or image is None:
                continue
            image = cv2.flip(image, 1)
            image_orig = cv2.flip(image, 1)
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=pose_landmark_drawing_spec,
                connection_drawing_spec=pose_connection_drawing_spec)
            idx_to_coordinates = get_idx_to_coordinates(image, results)

            try:
                # shoulder - hip - knee
                if 12 in idx_to_coordinates and 24 in idx_to_coordinates and 26 in idx_to_coordinates:  # right side of body

                    cv2.line(image, (idx_to_coordinates[12]), (idx_to_coordinates[24]), thickness=4,
                             color=(255, 0, 255))
                    l1 = np.linspace(idx_to_coordinates[12], idx_to_coordinates[24], 100)

                    cv2.line(image, (idx_to_coordinates[24]), (idx_to_coordinates[26]), thickness=4,
                             color=(255, 0, 255))
                    l2 = np.linspace(idx_to_coordinates[24], idx_to_coordinates[26], 100)

                    # Angel
                    ang1 = ang((idx_to_coordinates[12], idx_to_coordinates[24]),
                               (idx_to_coordinates[24], idx_to_coordinates[26]))

                    # Text Angel upper - forearm
                    cv2.putText(image, "   " + str(round(ang1, 2)), (idx_to_coordinates[24]),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.6, color=(0, 255, 0), thickness=2)
                    if round(ang1) > 80 or round(ang1) < 110:
                        print("Setz dich mit einem Rechten Winkel in den Knie hin" + ang1)

                    center, radius, start_angle, end_angle = convert_arc(l1[80], l2[24], sagitta=15)
                    axes = (radius, radius)
                    draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)

                if 11 in idx_to_coordinates and 23 in idx_to_coordinates and 25 in idx_to_coordinates:  # left side of body

                    cv2.line(image, (idx_to_coordinates[11]), (idx_to_coordinates[23]), thickness=4,
                             color=(255, 0, 255))
                    l1 = np.linspace(idx_to_coordinates[11], idx_to_coordinates[23], 100)

                    cv2.line(image, (idx_to_coordinates[23]), (idx_to_coordinates[25]), thickness=4,
                             color=(255, 0, 255))
                    l2 = np.linspace(idx_to_coordinates[23], idx_to_coordinates[25], 100)

                    ang2 = ang((idx_to_coordinates[11], idx_to_coordinates[23]),
                                (idx_to_coordinates[23], idx_to_coordinates[25]))

                    cv2.putText(image, str(round(ang2, 2)), (idx_to_coordinates[23]),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.6, color=(0, 255, 0), thickness=2)
                    print(ang2)
                    if ang2 > 110:
                        print("Setz dich mit einem Rechten Winkel in den Knie hin" + ang2)

                    center, radius, start_angle, end_angle = convert_arc(l1[80], l2[20], sagitta=15)
                    axes = (radius, radius)
                    draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)

            except:
                pass


            try:
                # hip - knee - heel
                if 26 in idx_to_coordinates and 30 in idx_to_coordinates and 24 in idx_to_coordinates:  # right side of body

                    # Line rhip - rknie
                    cv2.line(image, (idx_to_coordinates[24]), (idx_to_coordinates[26]), thickness=4,
                             color=(255, 0, 255))
                    l1 = np.linspace(idx_to_coordinates[24], idx_to_coordinates[26], 100)

                    # Line rheel - rfood.index
                    cv2.line(image, (idx_to_coordinates[26]), (idx_to_coordinates[30]), thickness=4,
                             color=(255, 0, 255))
                    l2 = np.linspace(idx_to_coordinates[26], idx_to_coordinates[30], 100)

                    # Angel rfemur - rfoot
                    angel = round(ang((idx_to_coordinates[24], idx_to_coordinates[26]),
                               (idx_to_coordinates[26], idx_to_coordinates[30])))
                    # Text Angel rfemur - rfoot
                    cv2.putText(image, "   " + str(round(angel, 2)), (idx_to_coordinates[26]),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.6, color=(0, 255, 0), thickness=2)

                    if angel < 70 or angel > 120:
                        print("Falsch R")

                    center, radius, start_angle, end_angle = convert_arc(l1[80], l2[20], sagitta=15)
                    axes = (radius, radius)
                    draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)

                # lhip - lknee - lheel
                if 23 in idx_to_coordinates and 25 in idx_to_coordinates and 29 in idx_to_coordinates:

                    # Line rhip - rknie
                    cv2.line(image, (idx_to_coordinates[23]), (idx_to_coordinates[25]), thickness=4,
                             color=(255, 0, 255))
                    l1 = np.linspace(idx_to_coordinates[23], idx_to_coordinates[25], 100)

                    # Line rheel - rfood.index
                    cv2.line(image, (idx_to_coordinates[25]), (idx_to_coordinates[29]), thickness=4,
                             color=(255, 0, 255))
                    l2 = np.linspace(idx_to_coordinates[25], idx_to_coordinates[29], 100)

                    # Angel rfemur - rfoot
                    angel_lfemur_lfoot = round(ang((idx_to_coordinates[23], idx_to_coordinates[25]),
                               (idx_to_coordinates[25], idx_to_coordinates[29])))
                    # Text Angel rfemur - rfoot
                    cv2.putText(image, "   " + str(round(angel, 2)), (idx_to_coordinates[25]),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.6, color=(0, 255, 0), thickness=2)

                    if angel_lfemur_lfoot < 70 or angel > 120:
                        print("Falsch L Femur")

                    center, radius, start_angle, end_angle = convert_arc(l1[80], l2[20], sagitta=15)
                    axes = (radius, radius)
                    draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)
            except:
                pass

            cv2.imshow('Image', rescale_frame(image, percent=100))
            if cv2.waitKey(5) & 0xFF == 27:
                break

        pose.close()
