import pygame, sys
from button import Button
import cv2
import mediapipe as mp
import numpy as np
import math

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
cap = cv2.VideoCapture(0)

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Exercise Menu")
BG = pygame.image.load("assets/Background.png")
clock = pygame.time.Clock()

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

font = pygame.font.Font(None, 36)
def workout(choice):
    while True:
        SCREEN.blit(BG, (0, 0))
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}

            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                points[id] = (cx, cy)

            if choice == "squats":
                # if the left foot x pos is less than the left shoulder
                # circle the left foot & tell them to move it on the screen
                if points[27][0] < points[11][0]:
                    correct_prompt = font.render("Left feet needs to be", True, (255, 255, 255))
                    correct_prompt2 = font.render("around your left shoulder width :)", True,
                                                 (255, 255, 255))
                    SCREEN.blit(correct_prompt, (810, 180))
                    SCREEN.blit(correct_prompt2, (730, 200))
                    cv2.circle(img, points[27], 15, (0, 0, 255), cv2.FILLED)

                # if the right foot x pos is greater than the right shoulder
                # circle the right foot & tell them to move it on the screen
                if points[28][0] > points[12][0]:
                    correct_prompt = font.render("Right feet needs to be", True, (255, 255, 255))
                    correct_prompt2 = font.render("around your right shoulder width :)", True,
                                                  (255, 255, 255))
                    SCREEN.blit(correct_prompt, (810, 220))
                    SCREEN.blit(correct_prompt2, (730, 240))
                    cv2.circle(img, points[28], 15, (0, 0, 255), cv2.FILLED)

        pygame_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pygame_frame = np.rot90(pygame_frame)
        pygame_frame = pygame.surfarray.make_surface(pygame_frame)
        SCREEN.blit(pygame_frame, (0, 0))

        pygame.display.flip()

        # Handle events or conditions to break out of the loop if needed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()

        clock.tick(30)

# creating the workout screens
def workout_menu():
    while True:
        # update the screen
        SCREEN.blit(BG, (0,0))

        # find the position of the mouse
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # render the text on screen and add background to text
        MENU_TEXT = get_font(50).render("Pick your workout", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        # creating the button selection for exercises
        SQUATS = Button(image= pygame.image.load("assets/Play Rect.png"), pos=(640, 200), text_input= "Squats", font= get_font(35), base_color= "#d7fcd4", hovering_color="white")

        # adding menu text and menu rectangle to screen
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        WORKOUT_BACK = Button(image=None, pos=(640, 620),
                           text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")

        # adding buttons to the screen
        for button in [SQUATS, WORKOUT_BACK]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # listen for event to see if the game is quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WORKOUT_BACK.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                if SQUATS.checkForInput(MENU_MOUSE_POS):
                    workout("squats")

        # update the pygame
        pygame.display.update()

def about():
    while True:
        ABOUT_MOUSE_POS = pygame.mouse.get_pos()

        # Creating background as white
        SCREEN.fill("White")

        # Creating the text on the screens
        OPTIONS_TEXT = get_font(30).render("How I work", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 130))

        OPTIONS_TEXT1 = get_font(20).render("Click workout, and then select your choice of workout", True, "Black")
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(640, 250))

        OPTIONS_TEXT2 = get_font(20).render("Do your exercise, and I will help during to fix your form", True, "Black")
        OPTIONS_RECT2 = OPTIONS_TEXT1.get_rect(center=(600, 350))

        # adding the text to screen
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        SCREEN.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        SCREEN.blit(OPTIONS_TEXT2, OPTIONS_RECT2)

        # creating the back option
        ABOUT_BACK = Button(image=None, pos=(640, 500), text_input="BACK",
                         font=get_font(30), base_color="Black", hovering_color="Blue")

        ABOUT_BACK.changeColor(ABOUT_MOUSE_POS)
        ABOUT_BACK.update(SCREEN)

        # listen for event to see if the game is quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ABOUT_BACK.checkForInput(ABOUT_MOUSE_POS):
                    main_menu()

        # updating the display
        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center= (640, 100))

        EXERCISE_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), text_input="Workout",
                        font=get_font(40), base_color="#d7fcd4", hovering_color="white")
        ABOUT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400), text_input="About",
                          font=get_font(40), base_color="#d7fcd4", hovering_color="white")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 550), text_input="Quit",
                          font=get_font(40), base_color="#d7fcd4", hovering_color="white")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [EXERCISE_BUTTON, ABOUT_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EXERCISE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    workout_menu()
                if ABOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    about()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
