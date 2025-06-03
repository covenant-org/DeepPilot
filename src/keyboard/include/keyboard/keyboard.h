#ifndef KEYBOARD_H
#define KEYBOARD_H

#include <geometry_msgs/TwistStamped.h>
#include <ros/package.h>
#include <ros/ros.h>

#include "std_msgs/Bool.h"
#include "std_msgs/Empty.h"
#include <std_msgs/Int8.h>

#include <QWidget>
#include <QtGui>

#include <QApplication>
#include <QFont>
#include <QKeyEvent>
#include <QLabel>
#include <QVBoxLayout>

using namespace std;

class KeyPress : public QWidget {

public:
  KeyPress(QWidget *parent = 0); // constructor
  ~KeyPress();                   // destructor

protected:
  void keyPressEvent(QKeyEvent *e);

private:
  ros::NodeHandle nh_;

  ros::Publisher OvR;
  ros::Publisher pubLand1_;
  ros::Publisher pubTakeoff1_;
  ros::Publisher pubCommandPilot1_;
  ros::Publisher pubCommandCamera1_;
  ros::Publisher pubCommandRecord1_;

  geometry_msgs::Twist commandPilot;
  std_msgs::Empty msgLand;
  std_msgs::Empty msgTakeoff;
  std_msgs::Int8 override;
  std_msgs::Bool recordingMsg;

  geometry_msgs::Twist commandCam;

  QGridLayout *grid;
  QLabel *RecordingLabel;
  QLabel *RecordingStateLabel;
  QLabel *Command;

  QFont font;

  float speed;
  float altitude_speed;

  float pitch;
  float roll;
  float yaw;
  float altitude;
};

#endif
