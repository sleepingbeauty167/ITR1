#!/usr/bin/env python

#import rospy, which is a python library fro ROS
import rospy, sys
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

start = True
PI = 3.1415926535897
location = None

#callback function which accepts the pos as a parameter
def callback(msg):
    global location, start
    location = msg.x, msg.y
    if start:
         # print Turtle's location
        print("Turtle's initial location:", location)
        start = False

def reset_values(twist_msg):
    twist_msg.linear.x = 0
    twist_msg.linear.y = 0
    twist_msg.linear.z = 0
    twist_msg.angular.x = 0
    twist_msg.angular.y = 0
    twist_msg.angular.z = 0

def start_turtle():
    global location
    # angles in radians
    angular_speed = 40 * PI / 180
    goal_angle = 45 * PI / 180
    speed = 0.2
    goal_distance = 1

    #declares that your node is publishing to the cmd_vel topic
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    #Create a subscriber object that will listen to the 'pose' topic and will call the callback 
    #function each time it reads something from the topic
    sub = rospy.Subscriber("/turtle1/pose", Pose, callback)

    #the topic /cmd_vel topic should have the message type Twist
    twist_msg = Twist()

    #we are moving just in x-axis, so reser other values
    reset_values(twist_msg)
    twist_msg.linear.x = speed

    # Get current time
    t0 = rospy.Time.now().to_sec()
    cure_distance = 0

    # Loop as long as the turtle did not pass one meter
    while (cure_distance < goal_distance):
        # Publish the velocity
        pub.publish(twist_msg)
        #  Get current time
        t1 = rospy.Time.now().to_sec()
        #compute for how long the turtle is moving
        delta_t = t1 - t0
        # Calculates current distance
        cure_distance = speed * delta_t
    
    print("Turtle's final location:", location)
    # After the loop, stops the turtle
    twist_msg.linear.x = 0
    # Force the turtle to stop
    pub.publish(twist_msg)

    #ROTATE PART - rotate the turtle 45 degrees and then stop

    # no need for linear components
    reset_values(twist_msg)
    twist_msg.angular.z = angular_speed
    #  Get current time
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    # Loop as long as the turtle did not complete to rotate 45 degrees
    while (current_angle < goal_angle):
        pub.publish(twist_msg)
        #  Get current time
        t1 = rospy.Time.now().to_sec()
        delta_t = t1 - t0
        current_angle = angular_speed * delta_t

    # Force the turtle to stop
    twist_msg.angular.z = 0
    pub.publish(twist_msg)
    rospy.spin()


if __name__ == '__main__':
    
    #initiate a node called my_turtle
    rospy.init_node("my_turtle")
    try:
        start_turtle()
    except rospy.ROSInterruptException:
        pass
