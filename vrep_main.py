import vrep
import sys
import math
import time
import random

vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP 5 last param is 200 hz

if clientID != -1:
    print("Connected to remote API server")

else:
    print("Connection not succesful")
    sys.exit("Could not connect")

error_code, camera_motor_handle = vrep.simxGetObjectHandle(clientID,"snake_joint_cam",vrep.simx_opmode_oneshot_wait)
horizontal_joint_handles = []
verticle_joint_handles = []
h_starts = []
v_starts = []
error_code, snek_handle = vrep.simxGetObjectHandle(clientID,"snake",vrep.simx_opmode_oneshot_wait)
error_code, start_pos = vrep.simxGetObjectPosition(clientID,snek_handle,-1, vrep.simx_opmode_streaming)
for x in range(1,5):
    h_handle = "snake_joint_h{}".format(x)
    v_handle = "snake_joint_v{}".format(x)
    error_code, temp_h_handle = vrep.simxGetObjectHandle(clientID, h_handle,
                                                               vrep.simx_opmode_oneshot_wait)
    error_code, temp_v_handle = vrep.simxGetObjectHandle(clientID, v_handle,
                                                               vrep.simx_opmode_oneshot_wait)

    horizontal_joint_handles.append(temp_h_handle)
    verticle_joint_handles.append(temp_v_handle)

error_code, gps_handle = vrep.simxGetObjectHandle(clientID, "GPS", vrep.simx_opmode_oneshot_wait)
# print(gps_handle)
#
# print(horizontal_joint_handles)
# print(verticle_joint_handles)

time_step = 0

speed = 5
ampitude_h = 0
ampitude_v = 20
phase_v = 120
phase_h = 160
phase_cam = 180
encodings = [speed, ampitude_h, ampitude_v, phase_v, phase_h]

A_H= ampitude_h*math.pi/180
A_V= ampitude_v*math.pi/180
P_V= phase_v*math.pi/180
P_H=phase_h*math.pi/180
P_C=phase_cam*math.pi/180
inputs = [A_H, A_V, P_V, P_H, P_C]
while True:
    time_step += 1



    for x in range(1,5):
        error_code = vrep.simxSetJointTargetPosition(clientID,
                                                     verticle_joint_handles[x-1],
                                                     (A_V)*math.sin(time_step*(speed)+x*(P_V)),
                                                     vrep.simx_opmode_oneshot)
        error_code = vrep.simxSetJointTargetPosition(clientID,
                                                     horizontal_joint_handles[x-1],
                                                     (A_H)*math.cos(time_step*(speed)+x*(P_H)),
                                                     vrep.simx_opmode_oneshot)

    error_code = vrep.simxSetJointTargetPosition(clientID,
                                                 camera_motor_handle,
                                                 (A_V)/2*math.sin(time_step*(speed)+(P_V)+(P_C)),
                                                 vrep.simx_opmode_oneshot)
    if time_step % 200 == 0:
        error_code, position = vrep.simxGetObjectPosition(clientID, camera_motor_handle, -1, vrep.simx_opmode_blocking)
        print(position[:2])
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
        time.sleep(1)
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

    time.sleep(.05)
    if error_code != 0 and error_code != 1:
        print(error_code)
        sys.exit()


print("end")
