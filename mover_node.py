import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
import math


class RectangleRobot(Node):

    def __init__(self):
        super().__init__('rectangle_robot')

        self.publisher_ = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.timer_callback
        )

        self.linear_speed = 0.5
        self.angular_speed = 0.7

        self.panjang = 2.0
        self.lebar = 1.0

        self.waktu_panjang = self.panjang / self.linear_speed
        self.waktu_lebar = self.lebar / self.linear_speed

        self.waktu_putar = (
            (math.pi / 2) / self.angular_speed
        )

        self.states = [
            ('MAJU', self.waktu_panjang),
            ('PUTAR', self.waktu_putar),
            ('MAJU', self.waktu_lebar),
            ('PUTAR', self.waktu_putar),
            ('MAJU', self.waktu_panjang),
            ('PUTAR', self.waktu_putar),
            ('MAJU', self.waktu_lebar),
            ('PUTAR', self.waktu_putar)
        ]

        self.current_state = 0
        self.state_start_time = time.time()

    def timer_callback(self):

        msg = Twist()

        if self.current_state >= len(self.states):

            msg.linear.x = 0.0
            msg.angular.z = 0.0

            self.publisher_.publish(msg)

            self.timer.cancel()

            return

        current_time = time.time()

        elapsed_time = (
            current_time - self.state_start_time
        )

        state_name, state_duration = (
            self.states[self.current_state]
        )

        if elapsed_time >= state_duration:

            self.current_state += 1
            self.state_start_time = current_time

            return

        if state_name == 'MAJU':

            msg.linear.x = self.linear_speed
            msg.angular.z = 0.0

        elif state_name == 'PUTAR':

            msg.linear.x = 0.0
            msg.angular.z = self.angular_speed

        self.publisher_.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = RectangleRobot()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:

        msg = Twist()

        msg.linear.x = 0.0
        msg.angular.z = 0.0

        node.publisher_.publish(msg)

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()