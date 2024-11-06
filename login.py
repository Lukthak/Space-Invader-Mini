import pygame,colors

def login_screen():
    pygame.init()
    # Título/Ícono
    pygame.display.set_caption("Space Invader Login")
    icon = pygame.image.load("sprites/icon.png")
    pygame.display.set_icon(icon)

    global execute
    execute = True
    username = ""
    password = ""
    input_active = "username"  # Empezar con el campo de username activo

    # Colores
    active_color = colors.PASTEL_ORANGE
    inactive_color = colors.WHITE

    # Fuentes
    font = pygame.font.Font("pixelart_font.ttf", 32)

    # Posiciones de conjunto
    conjunto_x = width // 2 - 150  # Ajustar posición X del conjunto
    conjunto_y = height // 3.1  # Ajustar posición Y del conjunto

    # Espaciado
    label_y_offset = 40  # Espaciado vertical entre etiquetas y cajas
    box_y_offset = 130  # Espaciado vertical entre cajas

    while execute:
        # Color de fondo
        screen.fill(colors.CHARCOAL)

        # Textos de etiquetas
        user_label = font.render("Username:", True, colors.WHITE)
        pass_label = font.render("Password:", True, colors.WHITE)
        
        # Rectángulos para las entradas de texto justo debajo de las etiquetas
        user_rect = pygame.Rect(conjunto_x, conjunto_y + label_y_offset, 300, 50)
        pass_rect = pygame.Rect(conjunto_x, conjunto_y + label_y_offset + box_y_offset, 300, 50)
        
        # Dibujar las etiquetas
        screen.blit(user_label, (user_rect.x, user_rect.y - label_y_offset))
        screen.blit(pass_label, (pass_rect.x, pass_rect.y - label_y_offset))
        
        # Colores según el campo activo
        user_color = active_color if input_active == "username" else inactive_color
        pass_color = active_color if input_active == "password" else inactive_color

        # Dibujar los rectángulos de entrada de texto
        pygame.draw.rect(screen, user_color, user_rect, 2)
        pygame.draw.rect(screen, pass_color, pass_rect, 2)

        # Renderizar textos de entrada
        user_text = font.render(username, True, user_color)
        pass_text = font.render('*' * len(password), True, pass_color)
        
        screen.blit(user_text, (user_rect.x + 10, user_rect.y + 10))
        screen.blit(pass_text, (pass_rect.x + 10, pass_rect.y + 10))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Close")
                return 3
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 10  # MODO ADMIN
                elif event.key == pygame.K_TAB:
                    # Alternar entre username y password
                    if input_active == "username":
                        input_active = "password"
                    else:
                        input_active = "username"
                elif event.key == pygame.K_RETURN:
                    if username and password:
                        print(f"Logging in with Username: {username}, Password: {password}")
                        return 0
                        #return {"username": username, "password": password}  # Retornar las credenciales
                elif input_active == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif input_active == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        try:
            pygame.display.flip()
        except pygame.error:
            print("Login screen - Error.")
        
        pygame.time.Clock().tick(60)

# Asumiendo que tienes configurado tu `screen`, `width`, y `height` en otro lugar del código principal
screen = pygame.display.set_mode((800, 600))
width, height = 800, 600

# Llamar a la pantalla de inicio de sesión

