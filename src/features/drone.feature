

Feature: Precision altimeter with TerraRanger One

Scenario: Lower than 0.2 meters AGL
Given TerraRanger One ROS node is running
When The drone is at an altitude less than 0.2 meters above ground level
Then Range Message of TerraRanger One ROS node is minus infinity.


Scenario: Lower than 14 meters and higher than 0.2 meters AGL
Given TerraRanger One ROS node is running
When The drone is flying lower than 14 meters and higher than 0.2 meters above ground level
Then The difference between the drone's altitude above ground level and Range Message of TerraRanger One ROS node is less then 0.30 meters. 


Scenario: Higher than 14 meters AGL
Given TerraRanger One ROS node is running
When The drone is flying higher than 14 meters above ground level
Then Range Message of TerraRanger One ROS node is plus infinity.  



