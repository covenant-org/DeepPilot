/***********************************************************************
 * Derechos reservados                                                 *
 * Autores: Leticia Oyuki Rojas Perez, Jose Martinez Carranza          *
 * Versión: 1.0                                                        *
 * Última actualización:  05/06/2018                                   *
 *                                                                     *
 * Ejemplo de Interfaz de control manual                               *
 *                                                                     *
 ***********************************************************************/

#include "keyboard.h"
#include <QKeyEvent>

KeyPress::KeyPress(QWidget *parent) : nh_("~"), QWidget(parent) {
  ROS_INFO("Init Keyboard Controller");

  pubTakeoff1_ = nh_.advertise<std_msgs::Empty>("/bebop/takeoff", 3);
  pubLand1_ = nh_.advertise<std_msgs::Empty>("/bebop/land", 3);
  pubCommandPilot1_ = nh_.advertise<geometry_msgs::Twist>("/bebop/cmd_vel", 3);
  pubCommandRecord1_ = nh_.advertise<std_msgs::Bool>("/bebop/record", 3);
  this->recordingMsg.data = false;
  speed = 0.3;
  altitude_speed = 1.0;
  pitch = 0;
  roll = 0;
  yaw = 0;
  altitude = 0;

  OvR = nh_.advertise<std_msgs::Int8>("/keyboard/override", 3);

  override.data = 0;

  RecordingLabel = new QLabel("Recording: ", this);
  RecordingStateLabel = new QLabel("No", this);

  Command = new QLabel(" ", this);

  font = Command->font();
  font.setPointSize(20);
  font.setBold(true);
  Command->setFont(font);

  grid = new QGridLayout(this);

  grid->addWidget(RecordingLabel, 1, 0);
  grid->addWidget(RecordingStateLabel, 1, 1);

  grid->addWidget(Command, 5, 0);

  setLayout(grid);
}

KeyPress::~KeyPress() {}

void KeyPress::keyPressEvent(QKeyEvent *event) {
  bool send_command = true;

  commandPilot.linear.x = 0.0;
  commandPilot.linear.y = 0.0;
  commandPilot.linear.z = 0.0;
  commandPilot.angular.z = 0.0;

  pitch = 0;
  roll = 0;
  altitude = 0;
  yaw = 0;

  if (event->key() == Qt::Key_H) {
    pitch = 0.0;
    roll = 0.0;
    altitude = 0.0;
    yaw = 0.0;
    Command->setText("HOVERING");
    setLayout(grid);
  } else if (event->key() == Qt::Key_T) {

    pubTakeoff1_.publish(msgTakeoff);
    Command->setText("TAKE OFF");
    setLayout(grid);

  } else if (event->key() == Qt::Key_Space) {

    pubLand1_.publish(msgLand);
    Command->setText("LANDING");
    this->recordingMsg.data = false;
    this->pubCommandRecord1_.publish(this->recordingMsg);
    RecordingStateLabel->setText("No");
    setLayout(grid);

  } else if (event->key() == Qt::Key_X) {
    override.data = 6;
    OvR.publish(override);
    send_command = false;
    Command->setText("AUTONOMOUS MODE");
    setLayout(grid);

  } else if (event->key() == Qt::Key_C) {
    override.data = 10;
    OvR.publish(override);
    send_command = false;
    Command->setText("<font color=red>CANCEL CONTROLLER</font></h2>");
    setLayout(grid);

  } else if (event->key() == Qt::Key_Q) {
    yaw += speed;
    Command->setText("YAW LEFT");
    setLayout(grid);
  } else if (event->key() == Qt::Key_E) {
    yaw -= speed;
    Command->setText("YAW RIGHT");
    setLayout(grid);
  } else if (event->key() == Qt::Key_W) {
    pitch += speed;
    Command->setText("FORWARD");
    setLayout(grid);
  } else if (event->key() == Qt::Key_S) {
    pitch -= speed;
    Command->setText("BACKWARD");
    setLayout(grid);
  } else if (event->key() == Qt::Key_A) {
    roll += speed;
    Command->setText("LEFT");
    setLayout(grid);
  } else if (event->key() == Qt::Key_D) {
    roll -= speed;
    Command->setText("RIGHT");
    setLayout(grid);
  } else if (event->key() == Qt::Key_Up) {
    altitude += speed;
    Command->setText("UP");
    setLayout(grid);
  } else if (event->key() == Qt::Key_Down) {
    altitude -= speed;
    Command->setText("DOWN");
    setLayout(grid);
  } else if (event->key() == Qt::Key_Left) {
    speed -= .1;
    if (speed < .1)
      speed = .1;
  } else if (event->key() == Qt::Key_Right) {
    speed += .1;
    if (speed > 1)
      speed = 1;
  } else if (event->key() == Qt::Key_R) {
    this->recordingMsg.data = !this->recordingMsg.data;
    if (!this->recordingMsg.data)
      RecordingStateLabel->setText("No");
    else
      RecordingStateLabel->setText("Yes");
    this->pubCommandRecord1_.publish(this->recordingMsg);
  }

  if (event->key() == Qt::Key_Escape) {
    qApp->quit();
  }

  commandPilot.linear.x = pitch;
  commandPilot.linear.y = roll;
  commandPilot.linear.z = altitude;
  commandPilot.angular.z = yaw;

  pubCommandPilot1_.publish(commandPilot);
}
