#!/usr/bin/env python
# === OPENCV ====
import rospy
import cv2
# import video
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
# === TWIST ====
from geometry_msgs.msg import Twist
# === override ===
# ----------------------------------------------
from time import time
# =============Library for DeepPilot==========================
import numpy as np
import collections


class DeepPilot:

    def __init__(self):
        # ====== ROS
        self.data = open(
            "deeppilot-datasets/2025-05-27-20-55-46-03551/speeds.txt")
        self.bridge = CvBridge()
        self.imag1 = rospy.Subscriber(
            '/bebop2/camera_base/image_raw', Image, self.callback, queue_size=1, buff_size=2**24)
        self.override = 1
        self.pub_cmd_vel_Estimation = rospy.Publisher(
            '/bebop/cmd_vel', Twist, queue_size=10)
        self.vel_msg = Twist()

        self.q = collections.deque()

        self.frame_cont = 0
        self.cont = 0
        self.index = 0

        self.override = 0

        self.pitch = 0.0
        self.roll = 0.0
        self.altitude = 0.0
        self.yaw = 0.0

        self.elapse = 0.0
        self.lap_time = 0.0
        self.tic = 0.0
        self.toc = 0.0

        self.alpha = 0.1
        print("Loaded model from disk")

        print('===============  READY ================================')

    def callback(self, data):

        frame = self.bridge.imgmsg_to_cv2(data, "bgr8")
        frame = cv2.resize(frame, (640, 360))
        self.flag = 0

        self.frame_cont = self.frame_cont + 1

        if len(self.q) < 6 and self.frame_cont == 5:

            if len(self.q) == 5:
                self.q.popleft()

            self.q.append(frame.copy())
            self.frame_cont = 0

        if len(self.q) == 5:
            self.flag = 1

            self.outputImage = np.zeros((720, 1920, 3), dtype="uint8")

            self.outputImage[0:360, 0:640] = self.q[0]
            self.outputImage[0:360, 640:1280] = self.q[1]
            self.outputImage[0:360, 1280:1920] = self.q[2]

            self.outputImage[360:720, 0:640] = self.q[3]
            self.outputImage[360:720, 640:1280] = self.q[4]
            self.outputImage[360:720, 1280:1920] = frame

            if self.flag == 1:
                scale = cv2.resize(self.outputImage, (640, 360))
                cv2.imshow('Temporal view', scale)
                cv2.waitKey(1)

            start = time()
            line = self.data.readline()
            if not line:
                return
            print(line)
            _, roll, pitch, yaw, altitude = line.split()

            self.elapse = time() - start

            self.pred_roll = round(float(roll), 2)
            self.pred_pitch = round(float(pitch), 2)
            self.pred_altitude = round(float(altitude), 2)
            self.pred_yaw = round(float(yaw), 2)

            self.pitch = round(self.alpha * self.pitch +
                               (1 - self.alpha) * self.pred_pitch, 2)
            self.roll = round(self.alpha * self.roll +
                              (1 - self.alpha) * self.pred_roll, 2)
            self.altitude = round(
                self.alpha * self.altitude + (1 - self.alpha) * self.pred_altitude, 2)
            self.yaw = round(self.alpha * self.yaw +
                             (1 - self.alpha) * self.pred_yaw, 2)

            self.vel_msg.linear.x = self.pitch
            self.vel_msg.linear.y = self.roll
            self.vel_msg.linear.z = self.altitude
            self.vel_msg.angular.x = 0.0
            self.vel_msg.angular.y = 0.0
            self.vel_msg.angular.z = self.yaw

            self.pub_cmd_vel_Estimation.publish(self.vel_msg)


def main():
    rospy.init_node('DeepPilot', anonymous=True)
    print("init_node DeepPilot")
    pred = DeepPilot()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        pred.data.close()
        cv2.destroyAllWindows()
        sys.exit()


if __name__ == '__main__':
    main()
