import threading
import DobotDllType as dType
import json


CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll and get the CDLL object
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "COM4", 115200)[0]
print("Connect status:",CON_STR[state])

def BasicDemo():
    if (state == dType.DobotConnect.DobotConnect_NoError):
        
        #清空队列
        #Clean Command Queued
        dType.SetQueuedCmdClear(api)

        #Async Motion Params Setting (DONT USE / CHANGE VALUE UNLESS FOR CALIBRATING)
        #dType.SetHOMEParams(api, 250, 0, 0, 0, isQueued = 1)
        #dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
        #dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

        #Async Home
        lastIndex = dType.SetHOMECmd(api, temp = 0, isQueued = 1)[0]
        
        #Async Move PTP
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 210, 10, 10, 10, isQueued = 1)[0]
       # lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 200, 0, 0, 0, isQueued = 1)[0]
       # lastIndex = dType.SetEndEffectorSuctionCup(api, True, True, isQueued = 1)[0]
        # lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 210, 10, 10, 10, isQueued = 1)[0]
        #lastIndex = dType.SetEndEffectorSuctionCup(api, True, False, isQueued = 1)[0]
        
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 235.13, 105.28, -48.73 + 20, 0, isQueued = 1)[0]

        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 119.15, 233.22, -58.18, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 250, 0, 0, 0, isQueued = 1)[0]

        # 235.31118774414062, 105.28866577148438, -48.73237609863281, 24.105859756469727
# [119.15263366699219, 233.22808837890625, -58.18601989746094, 62.93821334838867]

        #Start to Execute Command Queue
        dType.SetQueuedCmdStartExec(api)

        #Wait for Executing Last Command 
        while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
            dType.dSleep(500)
            print("last index : ")
            print(lastIndex)
            print("current Index : ")
            print(dType.GetQueuedCmdCurrentIndex(api)[0])

        #Stop to Execute Command Queued
        dType.SetQueuedCmdStopExec(api)

        #Disconnect Dobot
        dType.DisconnectDobot(api)


def getPose2():

    if state == dType.DobotConnect.DobotConnect_NoError:
        # Start executing queued commands
        # dType.SetQueuedCmdClear(api)
        respond = dType.GetPose(api)[:4]
        
    # dType.SetQueuedCmdStartExec(api)

    # Wait for getting pose
    dType.dSleep(500)

    #Stop to Execute Command Queued
    #dType.SetQueuedCmdStopExec(api)
    
    #Disconnect Dobot
    #dType.DisconnectDobot(api)

    return respond





def RobotExecute2(response):
    xc, yc, zc, rc = getPose2()
    lastIndex = 0
    if state == dType.DobotConnect.DobotConnect_NoError:
        # Start executing queued commands
        dType.SetQueuedCmdClear(api)

        # Retrieve current pose
        # xc, yc, zc, rc = getPose2()
        # print("Current pose:")
        # print(xc, yc, zc, rc)

        # Accessing single command
        command = response.get('command', '')

        if command == 'move':
            direction = response.get('parameters', '').get('direction', '')
            if direction == 'up':
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xc, yc, zc + 80, rc, isQueued=1)[0]
                print("Move command: up")
            elif direction == 'down':
                print("Move command: down")
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xc, yc, zc - 80, rc, isQueued=1)[0]
            elif direction == 'left':
                print("Move command: left")
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xc, yc + 50, zc, rc, isQueued=1)[0]
            elif direction == 'right':
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xc, yc - 50, zc, rc, isQueued=1)[0]
                print("Move command: right")
            elif direction == 'forward':
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xc + 20, yc-30, zc, rc, isQueued=1)[0]
                print("Move command: right")
            else:
                print("Invalid direction for move command.")
                print(direction)
        elif command == 'move_to':
            parameters = response.get('parameters', '')
            x = parameters.get('x', '')
            y = parameters.get('y', '')
            z = parameters.get('z', '')
            print(f"Move to command: x={x}, y={y}, z={z}")
            lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, x, y, z, 0, isQueued=1)[0]
        elif command == 'suction_cup':
            action_status = response.get('parameters', '').get('action', '')
            if action_status == 'on':
                print(f"Suction cup command: {action_status}")
                lastIndex = dType.SetEndEffectorSuctionCup(api, True, True, isQueued=1)[0]
                #lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xc, yc, zc+50, 0, isQueued=1)[0]
            elif action_status == 'off':
                print(f"Suction cup command: {action_status}")
                lastIndex = dType.SetEndEffectorSuctionCup(api, False, False, isQueued=1)[0]
                #lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xc, yc, zc+50, 0, isQueued=1)[0]
            else:
                print("Invalid action status for suction cup command.")
        else:
            print("Invalid command.")

        # Start executing queued commands
        dType.SetQueuedCmdStartExec(api)

        # Wait for executing last command
        while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
            dType.dSleep(500)

        # Stop executing command queued
        dType.SetQueuedCmdStopExec(api)

        dType.SetQueuedCmdClear(api)

 


#Example data
json_content = """{"actions": [{"command": "suction_cup", "parameters": {"action": "on"}}, {"command": "move_to", "parameters": {"x": 266.05, "y": 8.32, "z": -53.46}}, {"command": "move", "parameters": {"direction": "forward"}}, {"command": "suction_cup", "parameters": {"action": "off"}}]}"""

json_content3 = """{"actions": [{"command": "suction_cup", "parameters": {"action": "off"}}]}"""

json_content5 = """{"actions": [{"command": "suction_cup", "parameters": {"action": "on"}}, {"command": "move_to", "parameters": {"x": 76.8, "y": -191, "z": -48.3}}, {"command": "move", "parameters": {"direction": "up"}}, {"command": "suction_cup", "parameters": {"action": "off"}},{"command": "move_to", "parameters": {"x": 195.5, "y": 155.8, "z": 0.00}}]}"""


json_content4 = """{"actions": [{"command": "suction_cup", "parameters": {"action": "on"}}, {"command": "move_to", "parameters": {"x": 192.4, "y": -206.1, "z": -48.3}}, {"command": "move", "parameters": {"direction": "forward"}}, {"command": "suction_cup", "parameters": {"action": "off"}},{"command": "move_to", "parameters": {"x": 195.5, "y": 155.8, "z": 0.00}}]}"""



json_content2 = """{"actions": [{"command": "suction_cup", "parameters": {"action": "on"}}, {"command": "move_to", "parameters": {"x": 184.30, "y": -93.6, "z": -48.5}}, {"command": "move_to", "parameters": {"x": 192.4, "y": -206.1, "z": -18.5}}, {"command": "suction_cup", "parameters": {"action": "off"}},{"command": "move_to", "parameters": {"x": 195.5, "y": 155.8, "z": 0.00}}]}"""

data = json.loads(json_content5)['actions']



#Use function

# BasicDemo()

print(getPose2())

for action in data:
   print(action)
   RobotExecute2(action)

