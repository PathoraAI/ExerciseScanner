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


class Chestpress(Exercise):
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
            # try:
            #     # shoulder - ankle - wrist
            #     if 12 in idx_to_coordinates and 28 in idx_to_coordinates and 16 in idx_to_coordinates:  # left side of body
            #         cv2.line(image, (idx_to_coordinates[12]), (idx_to_coordinates[28]), thickness=4,
            #                  color=(255, 0, 255))
            #         cv2.line(image, (idx_to_coordinates[28]), (idx_to_coordinates[16]), thickness=4,
            #                  color=(255, 0, 255))
            #         l1 = np.linspace(idx_to_coordinates[12], idx_to_coordinates[28], 100)
            #         l2 = np.linspace(idx_to_coordinates[28], idx_to_coordinates[16], 100)
            #         eang1 = ang((idx_to_coordinates[12], idx_to_coordinates[28]),
            #                     (idx_to_coordinates[28], idx_to_coordinates[16]))
            #         cv2.putText(image, str(round(eang1, 2)), (idx_to_coordinates[28]),
            #                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            #                     fontScale=0.6, color=(0, 255, 0), thickness=2)
            #         center, radius, start_angle, end_angle = convert_arc(l1[80], l2[20], sagitta=15)
            #         axes = (radius, radius)
            #         draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)
            #
            #     else:  # right side of body
            #         cv2.line(image, (idx_to_coordinates[11]), (idx_to_coordinates[27]), thickness=4,
            #                  color=(255, 0, 255))
            #         cv2.line(image, (idx_to_coordinates[27]), (idx_to_coordinates[15]), thickness=4,
            #                  color=(255, 0, 255))
            #         l1 = np.linspace(idx_to_coordinates[11], idx_to_coordinates[27], 100)
            #         l2 = np.linspace(idx_to_coordinates[27], idx_to_coordinates[16], 100)
            #         eang1 = ang((idx_to_coordinates[11], idx_to_coordinates[27]),
            #                     (idx_to_coordinates[27], idx_to_coordinates[15]))
            #         cv2.putText(image, str(round(eang1, 2)), (idx_to_coordinates[27]),
            #                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            #                     fontScale=0.6, color=(0, 255, 0), thickness=2)
            #         center, radius, start_angle, end_angle = convert_arc(l1[80], l2[20], sagitta=15)
            #         axes = (radius, radius)
            #         draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)
            # except:
            #     pass

            try:
                # shoulder - Elbow - wrist
                if 12 in idx_to_coordinates and 14 in idx_to_coordinates and 16 in idx_to_coordinates:  # right side of body

                    # Line rShoulder - rElbow
                    cv2.line(image, (idx_to_coordinates[12]), (idx_to_coordinates[14]), thickness=4,
                             color=(255, 0, 255))
                    l1 = np.linspace(idx_to_coordinates[12], idx_to_coordinates[14], 100)

                    # Line rElbow - rWrist
                    cv2.line(image, (idx_to_coordinates[14]), (idx_to_coordinates[16]), thickness=4,
                             color=(255, 0, 255))
                    l2 = np.linspace(idx_to_coordinates[14], idx_to_coordinates[16], 100)

                    # Angel upper - forearm
                    ang1 = ang((idx_to_coordinates[12], idx_to_coordinates[14]),
                               (idx_to_coordinates[14], idx_to_coordinates[16]))
                    # Text Angel upper - forearm
                    cv2.putText(image, "   " + str(round(ang1, 2)), (idx_to_coordinates[14]),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.6, color=(0, 255, 0), thickness=2)
                    center, radius, start_angle, end_angle = convert_arc(l1[80], l2[20], sagitta=15)
                    axes = (radius, radius)
                    draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)

                if 11 in idx_to_coordinates and 13 in idx_to_coordinates and 15 in idx_to_coordinates:  # left side of body
                    cv2.line(image, (idx_to_coordinates[11]), (idx_to_coordinates[13]), thickness=4,
                             color=(255, 0, 255))
                    cv2.line(image, (idx_to_coordinates[13]), (idx_to_coordinates[15]), thickness=4,
                             color=(255, 0, 255))
                    l1 = np.linspace(idx_to_coordinates[11], idx_to_coordinates[13], 100)
                    l2 = np.linspace(idx_to_coordinates[13], idx_to_coordinates[16], 100)
                    eang1 = ang((idx_to_coordinates[11], idx_to_coordinates[13]),
                                (idx_to_coordinates[13], idx_to_coordinates[15]))
                    cv2.putText(image, str(round(eang1, 2)), (idx_to_coordinates[13]),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.6, color=(0, 255, 0), thickness=2)
                    center, radius, start_angle, end_angle = convert_arc(l1[80], l2[20], sagitta=15)
                    axes = (radius, radius)
                    draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)

            except:
                pass

            # try:
            #     # elbow - wrist - horizontal ground
            #     if 14 in idx_to_coordinates and 16 in idx_to_coordinates:  # left side of body
            #         cv2.line(image, (idx_to_coordinates[14]), (idx_to_coordinates[16]), thickness=4,
            #                  color=(255, 0, 255))
            #         cv2.line(image, (idx_to_coordinates[16]),
            #                  (idx_to_coordinates[16][0] + 80, idx_to_coordinates[16][1]),
            #                  thickness=4, color=(255, 0, 255))
            #         l1 = np.linspace(idx_to_coordinates[14], idx_to_coordinates[16], 100)
            #         temp = (idx_to_coordinates[16][0] + 80, idx_to_coordinates[16][1])
            #         l2 = np.linspace(idx_to_coordinates[16], temp, 100)
            #         ang1 = ang((idx_to_coordinates[14], idx_to_coordinates[16]),
            #                    (idx_to_coordinates[16], temp))
            #         cv2.putText(image, "   " + str(round(ang1, 2)), (idx_to_coordinates[16]),
            #                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            #                     fontScale=0.6, color=(0, 255, 0), thickness=2)
            #         center, radius, start_angle, end_angle = convert_arc(l1[80], l2[20], sagitta=15)
            #         axes = (radius, radius)
            #         draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)
            #     else:  # right side of body
            #         cv2.line(image, (idx_to_coordinates[13]), (idx_to_coordinates[15]), thickness=4,
            #                  color=(255, 0, 255))
            #         cv2.line(image, (idx_to_coordinates[15]),
            #                  (idx_to_coordinates[15][0] + 80, idx_to_coordinates[15][1]),
            #                  thickness=4, color=(255, 0, 255))
            #         l1 = np.linspace(idx_to_coordinates[14], idx_to_coordinates[15], 100)
            #         temp = (idx_to_coordinates[15][0] + 80, idx_to_coordinates[15][1])
            #         l2 = np.linspace(idx_to_coordinates[15], temp, 100)
            #         ang1 = ang((idx_to_coordinates[14], idx_to_coordinates[15]),
            #                    (idx_to_coordinates[15], temp))
            #         cv2.putText(image, "   " + str(round(ang1, 2)), (idx_to_coordinates[15]),
            #                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            #                     fontScale=0.6, color=(0, 255, 0), thickness=2)
            #         center, radius, start_angle, end_angle = convert_arc(l1[80], l2[20], sagitta=15)
            #         axes = (radius, radius)
            #         draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)
            #
            # except:
            #     pass

            cv2.imshow('Image', rescale_frame(image, percent=100))
            if cv2.waitKey(5) & 0xFF == 27:
                break
        pose.close()
