#!/bin/bash

VAR1=$(rostopic list | grep /spur/laser/scan )
VAR2="/spur/laser/scan"

if [ "$VAR1" = "$VAR2" ]
then
        exit 0
else
        exit 1
fi


