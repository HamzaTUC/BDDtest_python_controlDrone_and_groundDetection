from subprocess import call
import os
# os.chmod('/home/lowe/catkin_ws/src/arm_and_takeoff/src/cucumber/node_running_script.sh', 777
node_running_check= os.system('bash /home/lowe/catkin_ws/src/arm_and_takeoff/cucumber/features/steps/node_running_script.sh')
# rc = call("/home/lowe/catkin_ws/src/arm_and_takeoff/src/cucumber/node_running_script.sh", shell=True)

print("rc value: ",node_running_check)
if node_running_check==0:
    print("OK laser scan is in rostopic list")

elif node_running_check==1:
    print("NOK OK laser scan is NOT in rostopic list")    

else:
    print("Another exit value")    

