import sys
import cv2
import rospy
import collections
import numpy as np
from random import randint
from datetime import datetime
from os import path, makedirs, getcwd
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge

default_dir = path.join(
    getcwd(),
    "deeppilot-datasets",
    f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}-{str(randint(0, 10000)).rjust(5, "0")}')


class Recorder:
    def __init__(self, output_dir=default_dir):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/bebop2/camera_base/image_raw',
                                          Image, self.callback, queue_size=1,
                                          buff_size=2**24)
        self.odom_sub = rospy.Subscriber(
            '/bebop/cmd_vel', Twist, self.odom_callback, queue_size=1
        )
        self.q = collections.deque()
        self.last_odom = Twist()
        self.frame_cont = 0
        self.output_dir = output_dir
        self.entry = 0
        makedirs(output_dir, exist_ok=True)

    def odom_callback(self, data):
        self.last_odom = data

    def callback(self, data):
        frame = self.bridge.imgmsg_to_cv2(data, "bgr8")
        frame = cv2.resize(frame, (640, 360))
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

        self.frame_cont += 1
        if self.frame_cont < 5:
            return

        self.frame_cont = 0

        if len(self.q) == 6:
            self.q.popleft()

        self.q.append(frame.copy())

        if len(self.q) == 6:
            outputImage = np.zeros((720, 1920, 3), dtype="uint8")

            outputImage[0:360, 0:640] = self.q[0]
            outputImage[0:360, 640:1280] = self.q[1]
            outputImage[0:360, 1280:1920] = self.q[2]

            outputImage[360:720, 0:640] = self.q[3]
            outputImage[360:720, 640:1280] = self.q[4]

            outputImage[360:720, 1280:1920] = frame
            scaled_moisac = cv2.resize(outputImage, (640, 380))
            self.entry += 1
            imgname = f"{str(self.entry).rjust(6, '0')}.jpg"
            img_path = path.join(self.output_dir, f"{imgname}")
            cv2.imwrite(str(img_path), scaled_moisac)

            labels_path = path.join(self.output_dir, "speeds.txt")
            with open(labels_path, "a") as f:
                f.write(
                    f"{imgname} {self.last_odom.linear.x} {self.last_odom.linear.y} {self.last_odom.linear.z} {self.last_odom.angular.x} {self.last_odom.angular.y} {self.last_odom.angular.z}\n"
                )


def main():
    rospy.init_node('Recorder', anonymous=True)
    print("init_node recorder")
    node = Recorder()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyAllWindows()
        sys.exit()


if __name__ == '__main__':
    main()
