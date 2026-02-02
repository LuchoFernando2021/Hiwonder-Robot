[Readme!!!!!.txt](https://github.com/user-attachments/files/25020615/Readme.txt)
Log in via HDMI or MobaXterm:
user: ubuntu		//all lowercase
password: hiwonder	//all lowercase

For it to work correctly:
Activate camera: sudo systemctl restart start_app_node.service

To open the servo editor: python3 software/ainex_controller/main.py

Warning:
Working with PWM values for servomotors.

The Servos_O_PWM file in the New Pose sheet directly explains a list of IDs from 1 to 22 for each servomotor, and those captured positions represent how the robot will move.
