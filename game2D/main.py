import pygame
from pygame.locals import *

# Initialiser Pygame
pygame.init()

# Définir la taille de la fenêtre
screen_width, screen_height = 640, 360
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeu de Sprites Animé avec Pygame")

# Charger l'image des sprites et définir les dimensions
sprite_sheet = pygame.image.load("./assets/personnal_character/sprite.png").convert_alpha()
sprite_width, sprite_height = 16, 16  # Taille de chaque sprite individuel
target_sprite_width, target_sprite_height = 32, 32  # Taille redimensionnée pour le jeu

# Charger les sprites en fonction des directions et mouvements
directions = ["down", "left", "up", "right"]
sprites = {direction: [] for direction in directions}

# Découper et redimensionner les sprites
for i, direction in enumerate(directions):
    for j in range(4):  # 4 images par direction
        sprite = sprite_sheet.subsurface((j * sprite_width, i * sprite_height, sprite_width, sprite_height))
        sprite = pygame.transform.scale(sprite, (target_sprite_width, target_sprite_height))
        sprites[direction].append(sprite)

# Position initiale du personnage et paramètres d'animation
player_x, player_y = 50, 50
speed = 8
current_direction = "down"
animation_index = 0
animation_speed = 0.2
animation_counter = 0

# Dimensions des bords pour restreindre les mouvements
border_thickness = 10

# Boucle principale
running = True
clock = pygame.time.Clock()
while running:
    print("player_x: ", player_x, "player_y: ", player_y)
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Récupérer les touches pressées
    keys = pygame.key.get_pressed()
    moving = False
    new_x, new_y = player_x, player_y
    if keys[K_z]:  # Haut
        new_y -= speed
        current_direction = "up"
        moving = True
    elif keys[K_s]:  # Bas
        new_y += speed
        current_direction = "down"
        moving = True
    elif keys[K_q]:  # Gauche
        new_x -= speed
        current_direction = "left"
        moving = True
    elif keys[K_d]:  # Droite
        new_x += speed
        current_direction = "right"
        moving = True

    # Limiter les mouvements aux bords de la fenêtre
    if border_thickness <= new_x <= screen_width - target_sprite_width - border_thickness:
        player_x = new_x
    if border_thickness <= new_y <= screen_height - target_sprite_height - border_thickness:
        player_y = new_y

    # Gérer l'animation
    if moving:
        animation_counter += animation_speed
        if animation_counter >= 1:
            animation_counter = 0
            animation_index = (animation_index + 1) % 4  # Boucle entre 0 et 3
    else:
        animation_index = 0  # Réinitialiser au sprite d'attente

    # Remplir l'écran de fond
    screen.fill((0, 0, 0))  # Fond noir

    # Dessiner les bords
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, screen_width, border_thickness))  # Bord supérieur
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, border_thickness, screen_height))  # Bord gauche
    pygame.draw.rect(screen, (255, 255, 255), (0, screen_height - border_thickness, screen_width, border_thickness))  # Bord inférieur
    pygame.draw.rect(screen, (255, 255, 255), (screen_width - border_thickness, 0, border_thickness, screen_height))  # Bord droit

    # Afficher le sprite animé dans la direction actuelle
    screen.blit(sprites[current_direction][animation_index], (player_x, player_y))

    # Rafraîchir l'affichage
    pygame.display.flip()

    # Limiter la vitesse de la boucle
    clock.tick(30)  # 30 images par seconde

pygame.quit()
