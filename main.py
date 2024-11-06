import pygame
from loops import main_menu,principal_game,game_over,admin_mode,log_screen_change,log_end #Pantallas
from login import login_screen

pygame.init()
pygame.mixer.init() 

# PANTALLAS
SCREEN_MAIN_MENU = 0
SCREEN_PRINCIPAL_GAME = 1
SCREEN_OPTIONS = 2
SCREEN_EXIT = 3
SCREEN_GAME_OVER = 4
SCREEN_LOGIN = 5
ADMIN = 10

main_menu_choose = main_menu
screen_CHOOSE = 5
screen_EVENT = False
running = True

# Bucle de pantallas
while running:
    log_screen_change(screen_CHOOSE)
    print (f"Screen Choose: {screen_CHOOSE} ")
    if screen_CHOOSE == SCREEN_MAIN_MENU: #0
        screen_CHOOSE = main_menu() # Detecta el screen choose en la EJECUCION
 
    elif screen_CHOOSE == SCREEN_PRINCIPAL_GAME: #1
        screen_CHOOSE = principal_game()
        
    elif screen_CHOOSE == SCREEN_OPTIONS: #2
        print ("Options/NOT CREATED ")
        # Pantalla de opciones no hecha
        screen_CHOOSE = 10 # Vuelve admin
        
    elif screen_CHOOSE == SCREEN_EXIT: #3
        running = False

    elif screen_CHOOSE == SCREEN_GAME_OVER: #4
        screen_CHOOSE = game_over()

    elif screen_CHOOSE == SCREEN_LOGIN: #5
        screen_CHOOSE = login_screen()
    
    elif screen_CHOOSE == ADMIN: #10
        screen_CHOOSE = admin_mode()

    elif screen_CHOOSE == None:
        print ("Error")
        break

log_end()
pygame.quit()

print ("End of execute.")
