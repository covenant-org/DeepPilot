import sys
import cv2
import rospy
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge


class Recorder:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/bebop2/camera_base/image_raw',
                                          Image, self.callback, queue_size=1,
                                          buff_size=2**24)
        self.odom_sub = rospy.Subscriber(
            '/bebop/cmd_vel', Twist, self.odom_callback, queue_size=1
        )

    def odom_callback(self, data):
        print(data)

    def callback(self, data):
        frame = self.bridge.imgmsg_to_cv2(data, "bgr8")
        frame = cv2.resize(frame, (640, 360))
        cv2.imshow('frame', frame)
        cv2.waitKey(1)


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
