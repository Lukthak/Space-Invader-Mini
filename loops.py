"""
MAIN del juego donde estan todos los LOOPS
"""
from entity import Player,Enemy,Shoot
import pygame,time
import datetime
import os
import colors
import firebase_admin
import threading
from firebase_admin import credentials, db


# Configuración del archivo de claves JSON
cred = credentials.Certificate('space-invader-mini-firebase-adminsdk-fqoic-c1c0583615.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://space-invader-mini-default-rtdb.firebaseio.com/'
})

# Referencia a la base de datos de Firebase
ref = db.reference('high_score') 

# Iniciar PYGAME
pygame.init()
pygame.mixer.init()

# Crear pantalla
width = 800 #ancho
height = 600 #alto
screen = pygame.display.set_mode((width,height))

# Interruptor global
execute = True

# Sonidos generales
select_sound = pygame.mixer.Sound("sound/select.wav")
enter_sound = pygame.mixer.Sound("sound/enter.wav")
enter_sound2 = pygame.mixer.Sound("sound/enter2.wav")
nopass_sound = pygame.mixer.Sound("sound/nopass.wav")
gameover_sound = pygame.mixer.Sound("sound/gameover.wav")
admin_select = pygame.mixer.Sound("sound/admin_select.wav")

#Muisca
song1 = ("sound/song1.wav")
high_sc = 0
#  
def load_high_score():
    '''
    high_score_data = ref.get()
    if high_score_data is None:
        #no existe asi q crea una con 0
        ref.set({'high_score':0})
        return 0
    high_score = high_score_data['high_score']
    print("SE CARGO EL HIGHSCORE: ",high_score)
    return high_score 
    '''
    global high_sc
    while True:
        ref = db.reference('high_score')
        high_score_dta = ref.get()

        if high_score_dta is None:
            ref.set({'high_score':0})
            high_sc = 0
        else:
            high_sc = high_score_dta['high_score']


high_score_thd = threading.Thread(target=load_high_score)
high_score_thd.daemon = True #esto lo q hace es q se cierre el thread al terminar
high_score_thd.start()


def save_high_score(high_score):
    ref = db.reference('high_score')
    ref.set({
        'high_score': high_score
    })
    print("High score saved to Firebase.")

# Menu principal 0
def main_menu():
    pygame.init()
    # Título/Icono
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load("sprites/icon.png")
    pygame.display.set_icon(icon)

    global execute
    execute = True
    selected_button = 0  # Indica el botón seleccionado    

    # Crear fuentes para los botones
    font = pygame.font.Font("pixelart_font.ttf", 32)
    
    # Definir los textos de los botones
    buttons = ["Play", "Options", "Log Out", "Quit"]
    
    # Posiciones de los botones (puedes ajustar estos valores)
    button_x = width // 2
    button_y_start = height // 2.4
    button_y_offset = 65

    while execute:
        # Color de fondo
        screen.fill(colors.CHARCOAL)
        
        # Dibujar los botones en pantalla
        for i, text in enumerate(buttons):
            color = colors.PASTEL_ORANGE if i == selected_button else colors.WHITE
            label = font.render(text, True, color)
            label_rect = label.get_rect(center=(button_x, button_y_start + i * button_y_offset))
            screen.blit(label, label_rect)
        
        # Límite de botones
        if selected_button < 0:
            selected_button = len(buttons) - 1
        if selected_button > len(buttons) - 1:
            selected_button = 0

        # Iterador de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Close")
                return 3
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    select_sound.play()
                    selected_button += 1  # Cambiar selección hacia abajo
                elif event.key == pygame.K_UP:
                    select_sound.play()
                    selected_button -= 1  # Cambiar selección hacia arriba
                elif event.key == pygame.K_ESCAPE:
                    # MODO ADMIN
                    return 10
                elif event.key == pygame.K_RETURN:
                    if selected_button == 0:  # Play
                        enter_sound.play()
                        return 1
                    elif selected_button == 1:  # Options
                        return 4
                    elif selected_button == 2:  # Log Out
                        print("Logging Out")
                        return 5
                    elif selected_button == 3:  # Quit
                        print("Close")
                        return 3  # EVENTO CERRAR

        try:
            pygame.display.flip()
        except pygame.error:
            print("Main menu - Error.")

        pygame.time.Clock().tick(60)


# Llamar al menú principal



# Pausa UNA LOOP SUPERPUESTO (MUCHO CUIDADO)
def pause(execute_pause):
    pygame.init()
    print ("Screen Choose: Pause")
    # Titulo/Icon
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load("sprites/icon.png")
    pygame.display.set_icon(icon)

    #Ejecucion del loop
    execute = True
    execute_pause = True
    selected_button = 0  # Indica el botón seleccionado 

    # Crear fuentes para los botones
    font = pygame.font.Font("pixelart_font.ttf",32)

    # Definir los textos de los botones
    buttons = ["Continue","Options", "Quit"]


    while execute_pause:
        #Color pantalla
        screen.fill((colors.BLACK))  
       
        # Dibujar los botones en pantalla
        for i, text in enumerate(buttons):
            color = colors.GREEN if i == selected_button else colors.WHITE
            label = font.render(text, True, color)
            label_rect = label.get_rect(center=(width // 2, height // 2.4 + i * 65))
            screen.blit(label, label_rect)
        # Limtie de botones
        if selected_button < 0:
            selected_button = (len(buttons)-1)
        if selected_button > len(buttons)-1:
            selected_button = 0


        # Iterador de eventos
        for event in pygame.event.get():
            # Evento cerrar
            if event.type == pygame.QUIT: 
                print ("pause.Close")
                return 3
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # ESC continua el juego tambien
                    print ("Continue")
                    enter_sound2.play()
                    execute_pause = False
                    return 4
                elif event.key == pygame.K_DOWN:
                    select_sound.play()
                    selected_button += 1  # Cambiar selección hacia abajo
                elif event.key == pygame.K_UP:
                    select_sound.play()
                    selected_button -= 1  # Cambiar selección hacia arriba
                elif event.key == pygame.K_RETURN:
                    if selected_button == 0:  # Continue
                        enter_sound2.play()
                        print ("Continue")
                        execute_pause = False
                       
                    elif selected_button == 1:  # Options
                        print ("Options/NOT CREATED")
                        nopass_sound.play()
                        # no hay todavia
                    elif selected_button == 2:  # Quit
                        pygame.mixer.music.stop()
                        #Mandando señal MEPP
                        return 0
                        
                        
                        


         # Actualizar pantalla
        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Juego principal 1
def principal_game():
    # Inicializar high score al inicio del juego desde Firebase
    
    pygame.init() 
    

    # Titulo/Icon
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load("sprites/icon.png")
    pygame.display.set_icon(icon)

    # Crea una instancia de Player
    player = Player(width, height)


    # Lista enemigos
    enemies = pygame.sprite.Group()

    # Cantidad de enemigos
    level_executed = False
    enemy_counter = 0
    dificult = 1
    for number_of_enemies in range(dificult):  
        enemy = Enemy()
        enemies.add(enemy)
        
    # Puntaje
    score = 0
    font = pygame.font.Font("pixelart_font.ttf",32)
    score_x = 10
    score_y = 5

    def show_score(score_x,score_y):
        text = font.render(f"{score}", True, (colors.WHITE))
        screen.blit (text,(score_x,score_y))


    # HIGH SCORE
    # Actualizar el high score y guardar en un hilo separado
    def show_high_score(high_score_x, high_score_y,enemy_counter):
        # Consigue high score
        #hs = load_high_score()
        hs = high_sc
        # Impresion de numero en pantalla.
        font = pygame.font.Font("pixelart_font.ttf", 32)
        text = font.render(f"{hs}", True, (colors.LIGHT_RED))
        screen.blit(text, (high_score_x, high_score_y))
        
        if enemy_counter > hs:
            hs = enemy_counter 
            print (hs)

            # FB Load
            ref = db.reference('high_score').set({"high_score":hs})
            print(f"Se guardo high score: {hs} en referencia {ref} ")

    # Disparos
    shoots = pygame.sprite.Group()
    shoot = Shoot(width, height)
    last_shoot_time = 0
    shoot_cooldown = 500  # Cooldown de 500 milisegundos (0.5 segundos)

    # Bug de colision
    bug_colision = True

    # Ejecucion del loop
    execute = True
    music_on = False
    pause_selection = 1
   
    #high_score = load_high_score() 
    high_score = high_sc

    while execute:

        # Color pantalla
        screen.fill((colors.CHARCOAL))  

        # Iterador de eventos
        for event in pygame.event.get():
            # Evento cerrar
            if event.type == pygame.QUIT: 
                return 3
            # Evento disparar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #print("Highscore antes de guardar: ",high_score)
                    #save_high_score(high_score) 
                    #print("Highscore despues ed guardas: ",high_score)
                    #high_score = load_high_score() 
                    #print("EL MALDITO HIGHSCORE DE MIERDA despues de cargar el guardado: ", high_score)
                    pause_selection = pause(True)
                    
                    if pause_selection == 0:
                        execute = False
                        return 0
                    elif pause_selection == 2:
                        pass
                    elif pause_selection == 3:
                        return 3
                
                    if pause_selection == 1:
                        continue
                    
                if event.key == pygame.K_q:
                    current_time = pygame.time.get_ticks() #Obteniendo tiempo del PYGAME
                    if current_time - last_shoot_time >= shoot_cooldown:
                        # Crear disparo (Esos calculos son exactamente donde deben aparecer)
                        shoot = Shoot(player.rect.x + (45 / 2) - (shoot.rect.width / 2), player.rect.y)
                        shoot.play_shoot_sound()
                        # Añadir al grupo de disparos
                        shoots.add(shoot)
                        # Actualizar el tiempo del último disparo
                        last_shoot_time = current_time

            # Mover jugador basado en la tecla presionada
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.x_movement = -player.speed
            elif keys[pygame.K_RIGHT]:
                player.x_movement = +player.speed
            # Si suelta se queda quieto
            else:
                player.x_movement = 0

        # Niveles
        if enemy_counter % 5 == 0 and enemy_counter != 0 and not level_executed and len(enemies) < 10:
            dificult = +1 
            if len(enemies) + dificult > 10:  # Asegura que no haya más de 10 enemigos 
                dificult = 10 - len(enemies)
            for _ in range(dificult):   
                enemy = Enemy()
                enemies.add(enemy)
            level_executed = True  # Marca que el código se ha ejecutado una vez

        # Restablecer level_executed cuando el contador de enemigos cambia
        if enemy_counter % 5 != 0:
            level_executed = False
        
        # MUSICA
        if enemy_counter >= 5 and music_on == False:
            pygame.mixer.music.load(song1)
            pygame.mixer.music.play(-1)
            music_on = True

        
        # Colisiones
        colision_shoot = pygame.sprite.groupcollide(shoots, enemies, False, False)
        if colision_shoot:
            for shoot in colision_shoot:
                for enemy in colision_shoot[shoot]:
                    score += 1
                    enemy.play_death_sound()
                    enemy.respawn()
                    shoot.kill()  # Elimina la bala del grupo
                    enemy_counter += 1 #Contador de enemigos matados
        

        colision_player = pygame.sprite.spritecollideany(player, enemies)
        
        # Perder juego
        if colision_player and bug_colision == False:
            for enemy in enemies:
                pygame.mixer.music.stop()
                gameover_sound.play() 
                time.sleep(0.75)
                print (enemy_counter)
                save_high_score(high_score) # Cuando se pierde se actualiza el high score
                return 4 # Pantalla GAME OVER

        else:
            bug_colision = False

        # Actualiza pos del Player
        player.update_position()  
        # Imprime a Player con pos actualizada    
        player.draw(screen)
    
        # Ac pos enemigo
        enemies.update()
        # Imprime enemigo
        enemies.draw(screen)

        # Ac pos disparo
        shoots.update()
        # Imprime disparo
        shoots.draw(screen) 

        # Mostrar puntaje
        show_score(score_x, score_y)    
        # Mostrar HIGH SCORE 
        show_high_score(score_x, (score_y+40), enemy_counter)
        # Actualizar pantalla
        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Opciones 2
# def options(): 

# Game over 3
def game_over():
    pygame.init()

    # Titulo/Icon
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load("sprites/icon.png")
    pygame.display.set_icon(icon)

    # Ejecución del loop
    global execute  # Variable global para cerrar todo al mismo tiempo
    execute = True
    selected_button = 0  # Indica el botón seleccionado

    # Crear fuentes para los botones
    font = pygame.font.Font("pixelart_font.ttf", 32)

    # Definir los textos de los botones
    buttons = ["Retry", "Main Menu", "Quit"]

    while execute:
        # Color pantalla
        screen.fill((colors.BLACK))
        
        # Dibujar los botones en pantalla
        for i, text in enumerate(buttons):
            color = colors.RED if i == selected_button else colors.WHITE
            label = font.render(text, True, color)
            label_rect = label.get_rect(center=(width // 2, height // 2.4 + i * 65))
            screen.blit(label, label_rect)

        # Límite de botones
        if selected_button < 0:
            selected_button = (len(buttons) - 1)
        if selected_button > len(buttons) - 1:
            selected_button = 0

        # Iterador de eventos
        for event in pygame.event.get():
            # Evento cerrar
            if event.type == pygame.QUIT:
                return 3
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    select_sound.play()
                    selected_button += 1  # Cambiar selección hacia abajo
                elif event.key == pygame.K_UP:
                    select_sound.play()
                    selected_button -= 1  # Cambiar selección hacia arriba
                elif event.key == pygame.K_RETURN:
                    if selected_button == 0:  # Retry
                        enter_sound2.play()
                        return 1  # Reinicia el juego
                    elif selected_button == 1:  
                        enter_sound2.play()
                        return 0  # Regresa al menú principal
                    elif selected_button == 2:  # Quit
                        return 3

        # Actualizar pantalla
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
# Cerrar 4
# Esta implementado en "loop_manager.py"

# Modo admin --------------------------------- #

# LOG de pantallas
def log_screen_change(screen_choose):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    screen_names = {
        0: "Main Menu",
        1: "Principal Game",
        2: "Pause",
        3: "Exit",
        4: "Game Over",
        10: "Admin"
    }
    screen_name = screen_names.get(screen_choose, "Unknown")
    with open("log.txt", "a") as log_file:
        log_file.write(f"{current_time}: Screen Choose: {screen_choose} ({screen_name})\n")

# LOG final de pantallas
def log_end():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a") as log_file:
        log_file.write(f"END LOG ({current_time})\n")

# Modo admin terminal 10
def admin_mode():
    pygame.init()

    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load("sprites/icon.png")
    pygame.display.set_icon(icon)

    while execute:
        # Limpia la pantalla y configura el texto "ADMIN MODE - TERMINAL"
        screen.fill(colors.BLACK)
        font = pygame.font.Font("pixelart_font.ttf", 32)
        admin_text = font.render("ADMIN MODE - TERMINAL", True, (255, 0, 0))
        screen.blit(admin_text, (width // 2 - admin_text.get_width() // 2, height // 2 - admin_text.get_height() // 2))
        pygame.display.flip()
        
        # Reproduce un sonido para indicar la selección del modo admin
        admin_select.play()
        time.sleep(0.75)

        # Limpia la consola
        os.system('cls')
        
        # Imprime las opciones del modo admin en la consola
        print("ADMIN MODE: Choose a screen to execute")
        print("0: Main Menu")
        print("1: Principal Game")
        print("2: Options")
        print("3: Exit")
        print("4: Game Over")
        
        # Captura la elección del usuario
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            # Si la entrada no es un número válido, reproduce un sonido de error y vuelve al menú principal
            nopass_sound.play()
            print("Invalid input.")
            return 10

        # Verifica si la elección es válida (entre 0 y 4)
        try:
            if choice <= 4:
                admin_select.play()
                return int(choice)
            else:
                # Si la elección es inválida, reproduce un sonido de error y vuelve al menú principal
                nopass_sound.play()
                print("Invalid input.")
                return 10
        except ValueError:
            # Captura errores adicionales y vuelve al menú principal
            nopass_sound.play()
            print("Invalid input.")
            return 10



print ("Loops: Ready")


