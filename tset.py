import pyautogui 
import time

chestPositions = [(392, 650), (571, 653), (791, 666), (1086, 691), (1277, 683), (1552, 699), (1789, 692), (2053, 703), (2239, 712), (2486, 722), (2460, 913), (2244, 905), (2035, 922), (1792, 903), (1550, 884), (1297, 909), (1012, 917), (811, 900), (589, 926), (424, 922), (374, 1167), (549, 1143), (846, 1119), (1024, 1129), (1286, 1144), (1498, 1164), (1739, 1156), (1989, 1122), (2236, 1160), (2463, 1152)]
def clickChest(x,y):
    pyautogui.moveTo(x,y,0.6)
    pyautogui.click()
    time.sleep(1)
    pyautogui.click()
    time.sleep(2)

for positions in chestPositions:
    x,y = positions[0], positions[1]
    clickChest(x,y)