## Deep Pilot network

La arquitectura de la red neuronal está definida en el README.md en la raíz del
proyecto.

El objetivo de este documento es realizar una breve descripción del código fuente
de este proyecto.

El proyecto utiliza ROS Noetic como plataforma de desarrollo y siguiendo la 
filosofía de ROS, se utilizan nodos para desacoplar cada parte del proyecto.

El nodo principal es la clase DeepPilot, que se encarga de realizar el control 
del vehículo siguiendo la salida del modelo. Este nodo escucha los mensajes del
tópico `/bebop2/camera_base/image_raw` en el que se publican los frames de la
cámara del drone y del tópico `/keyboard/override` en el que se indica el deseo
del pilot por volar de forma autónoma. DeepPilot a su vez publica los comandos
de control en el tópico `/bebop2/cmd_vel`.
