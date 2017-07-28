import pyautogui
import time
import pygame

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
class varHolder():
    color = GREEN
    runMacro = False

def runMacro():
    try:
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("0")
        pyautogui.typewrite('45', .03)
        pyautogui.typewrite(['down'])
        pyautogui.typewrite('82', .03)
        pyautogui.typewrite(['down'])
        pyautogui.typewrite('130', .03)
        pyautogui.typewrite(['down'])
        pyautogui.typewrite('150', .03)
        pyautogui.typewrite(['down'])
        pyautogui.typewrite('174', .03)
        pyautogui.typewrite(['down'])
        pyautogui.typewrite('180', .03)
        pyautogui.typewrite(['down'])
        pyautogui.typewrite('163', .03)
        pyautogui.typewrite(['down'])
        pyautogui.typewrite('161', .03)
        pyautogui.typewrite(['down'])
        pyautogui.typewrite('127', .03)
        pyautogui.typewrite(['down'])
        pyautogui.typewrite('82', .03)
        pyautogui.typewrite(['down'])
        pyautogui.typewrite('81', .03)
        pyautogui.typewrite(['down'])
        pyautogui.typewrite('78', .03)
        pyautogui.typewrite(['enter'])
        print("\nDone.")
    except KeybaordInterrupt:
        print("\nDone. --KI--")

var = varHolder()
var.color = GREEN
var.runMacro = False
pygame.init()
screen = pygame.display.set_mode([200,200])
pygame.display.set_caption("Cocalc Macro")
clock = pygame.time.Clock()
done = False
while not done:
    var.runMacro = False
    var.color = GREEN
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done = True
            if event.key == pygame.K_RETURN:
                var.color = RED
                var.runMacro = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            var.color = RED
            var.runMacro = True

    screen.fill(var.color)
    pygame.display.flip()

    if var.runMacro == True:
        runMacro()

    clock.tick(60)

pygame.quit()
