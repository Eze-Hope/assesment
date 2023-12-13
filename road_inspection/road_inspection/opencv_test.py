import rclpy
from rclpy.node import Node
from rclpy import qos
from cv2 import namedWindow, cvtColor, imshow, inRange, bitwise_and
from cv2 import destroyAllWindows, startWindowThread
from cv2 import COLOR_BGR2GRAY, waitKey
from cv2 import blur, Canny, resize, INTER_CUBIC
from numpy import mean
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from rclpy.qos import QoSProfile, QoSDurabilityPolicy

class ImageConverter(Node):

    def __init__(self):
        super().__init__('opencv_test')
        self.bridge = CvBridge()
        self.image_sub = self.create_subscription(Image,
                                                   "/limo/depth_camera_link/image_raw",
                                                   self.image_callback,
                                                   qos_profile=qos.qos_profile_sensor_data)

        # Create a publisher for the masked image
        self.masked_image_pub = self.create_publisher(Image, "/limo/masked_image", QoSProfile(
            depth=10, durability=QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL))

    def image_callback(self, data):
        namedWindow("Image window")
        namedWindow("masked")
        namedWindow("canny")

        # Convert ROS Image message to OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        cv_image = resize(cv_image, None, fx=0.2, fy=0.2, interpolation=INTER_CUBIC)

        # Define a range for green color in BGR format
        lower_green = (0, 150, 0)
        upper_green = (100, 255, 100)

        # Create a mask for green color
        mask = inRange(cv_image, lower_green, upper_green)

        # Apply the mask to the original image
        masked_image = bitwise_and(cv_image, cv_image, mask=mask)

        # Publish the masked image
        masked_image_msg = self.bridge.cv2_to_imgmsg(masked_image, "bgr8")
        self.masked_image_pub.publish(masked_image_msg)

        # Display the images
        imshow("Image window", cv_image)
        imshow("masked", masked_image)
        waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    image_converter = ImageConverter()
    rclpy.spin(image_converter)

    image_converter.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
