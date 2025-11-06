# -*- coding: utf-8 -*-
"""
Energy Quest - Jogo de plataforma educativo
Desenvolvido como parte do processo seletivo da Kodland

Este jogo utiliza Pygame Zero para criar uma experiência de plataforma
onde o jogador coleta cristais de energia e resolve desafios.
"""

import random

# Importação defensiva para compatibilidade com diferentes ambientes Pygame Zero
try:
    from pygame import Rect
except ImportError:
    # Pygame Zero fornece sua própria implementação de Rect
    pass

from pgzero.builtins import Actor

# ============================================================
# CONFIGURAÇÃO DO JOGO
# ============================================================
TITLE = "Energy Quest"
WIDTH = 800
HEIGHT = 600

# ============================================================
# CONSTANTES DO JOGADOR
# ============================================================
PLAYER_SPEED = 5
JUMP_SPEED = 15
GRAVITY = 0.8
MAX_FALL_SPEED = 20
PLAYER_MAX_HEALTH = 6

# ============================================================
# LAYOUT DO HUD (HEAD-UP DISPLAY)
# ============================================================
HUD_MARGIN_TOP = 15
HUD_MARGIN_LEFT = 20
HUD_MARGIN_RIGHT = 20
HEART_SIZE = 28
HEART_SPACING = 5
HEARTS_Y = HUD_MARGIN_TOP
HEART_CENTER_Y = HUD_MARGIN_TOP + HEART_SIZE // 2
HUD_TEXT_SIZE = 26
HUD_TEXT_CENTER_Y = HEART_CENTER_Y

# ============================================================
# CONSTANTES DE GAMEPLAY
# ============================================================
GEM_MIN_DIST = 90
GEM_HITBOX_HALF = 15
KEY_HITBOX_HALF = 15
ENEMY_HITBOX_HALF = 20
DOOR_TIP_HITBOX_WIDTH = 50
DOOR_TIP_HITBOX_HEIGHT = 80
KEY_MIN_DIST_FROM_DOOR = 100

# ============================================================
# CONSTANTES DOS INIMIGOS
# ============================================================
ENEMY_SPEED = 2
ENEMY_DAMAGE = 2

# ============================================================
# ESTADOS DO JOGO
# ============================================================
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
VICTORY = "victory"
TUTORIAL = "tutorial"

# ============================================================
# VARIÁVEIS GLOBAIS DO JOGO
# ============================================================
game_state = MENU
player_health = PLAYER_MAX_HEALTH
collected_gems = 0
total_gems = 0
has_key = False
music_enabled = True
sound_enabled = True
current_level = 0
door_tip_active = False
intro_music_started = False

# ============================================================
# DEFINIÇÃO DOS NÍVEIS DO JOGO
# ============================================================
# Cada nível contém plataformas, gemas, inimigos, chave e porta
levels = [
    {
        'background': 'backgrounds/background_color_trees',
        'music': 'grasslands_theme',
        'platforms': [
            Rect(100, 450, 200, 20),
            Rect(400, 450, 200, 20),
            Rect(200, 350, 150, 20),
            Rect(500, 350, 150, 20),
            Rect(0, HEIGHT - 20, WIDTH, 20),  # Piso de segurança
        ],
        'gems': [
            {'pos': (150, 400), 'color': 'blue'},
            {'pos': (450, 400), 'color': 'red'},
            {'pos': (250, 300), 'color': 'green'}
        ],
        'key_pos': (550, 300),
        'key_color': 'blue',
        'door_pos': (700, 400),
        'enemies': [
            {'type': 'pink', 'patrol': [(500, 350), (650, 350)]}  # Apenas 1 inimigo no nível inicial
        ]
    },
    {
        'background': 'backgrounds/background_color_desert',
        'music': 'desert_theme',
        'platforms': [
            Rect(50, 450, 150, 20),
            Rect(300, 450, 200, 20),
            Rect(600, 450, 150, 20),
            Rect(200, 350, 100, 20),
            Rect(500, 350, 100, 20),
            Rect(0, HEIGHT - 20, WIDTH, 20),  # Piso de segurança
        ],
        'gems': [
            {'pos': (100, 400), 'color': 'yellow'},
            {'pos': (350, 400), 'color': 'green'},
            {'pos': (650, 400), 'color': 'red'},
            {'pos': (250, 300), 'color': 'blue'}
        ],
        'key_pos': (550, 300),
        'key_color': 'red',
        'door_pos': (750, 400),
        'enemies': [
            {'type': 'beige', 'patrol': [(50, 450), (200, 450)]},
            {'type': 'pink', 'patrol': [(300, 450), (500, 450)]},
            {'type': 'purple', 'patrol': [(600, 450), (750, 450)]}
        ]
    },
    {
        'background': 'backgrounds/background_color_mushrooms',
        'music': 'mushroom_theme',
        'platforms': [
            Rect(80, 460, 180, 18),
            Rect(320, 420, 160, 18),
            Rect(560, 380, 160, 18),
            Rect(240, 300, 120, 18),
            Rect(480, 260, 120, 18),
            Rect(0, HEIGHT - 20, WIDTH, 20),
        ],
        'gems': [
            {'pos': (120, 420), 'color': 'blue'},
            {'pos': (360, 380), 'color': 'green'},
            {'pos': (600, 340), 'color': 'yellow'},
            {'pos': (260, 260), 'color': 'red'}
        ],
        'key_pos': (500, 220),
        'key_color': 'yellow',
        'door_pos': (740, 360),
        'enemies': [
            {'type': 'pink', 'patrol': [(320, 420), (480, 420)]},
            {'type': 'purple', 'patrol': [(560, 380), (720, 380)]}
        ]
    },
    {
        'background': 'backgrounds/background_clouds',
        'music': 'jungle_theme',
        'platforms': [
            Rect(60, 460, 160, 18),
            Rect(260, 430, 180, 18),
            Rect(520, 400, 180, 18),
            Rect(180, 320, 140, 18),
            Rect(420, 280, 140, 18),
            Rect(0, HEIGHT - 20, WIDTH, 20),
        ],
        'gems': [
            {'pos': (100, 420), 'color': 'red'},
            {'pos': (300, 390), 'color': 'blue'},
            {'pos': (560, 360), 'color': 'green'},
            {'pos': (200, 280), 'color': 'yellow'}
        ],
        'key_pos': (440, 240),
        'key_color': 'green',
        'door_pos': (760, 360),
        'enemies': [
            {'type': 'beige', 'patrol': [(60, 460), (220, 460)]},
            {'type': 'pink', 'patrol': [(260, 430), (440, 430)]},
            {'type': 'purple', 'patrol': [(520, 400), (700, 400)]}
        ]
    },
    {
        'background': 'backgrounds/background_color_trees',
        'music': 'dungeon_theme',
        'platforms': [
            Rect(100, 470, 180, 18),
            Rect(360, 430, 180, 18),
            Rect(620, 390, 150, 18),
            Rect(280, 320, 140, 18),
            Rect(520, 280, 140, 18),
            Rect(0, HEIGHT - 20, WIDTH, 20),
        ],
        'gems': [
            {'pos': (140, 430), 'color': 'blue'},
            {'pos': (400, 390), 'color': 'yellow'},
            {'pos': (660, 350), 'color': 'red'},
            {'pos': (300, 280), 'color': 'green'}
        ],
        'key_pos': (540, 240),
        'key_color': 'red',
        'door_pos': (740, 350),
        'enemies': [
            {'type': 'beige', 'patrol': [(360, 430), (540, 430)]},
            {'type': 'pink', 'patrol': [(620, 390), (760, 390)]},
            {'type': 'purple', 'patrol': [(100, 470), (280, 470)]}
        ]
    }
]

def get_image_half_size(name: str, default: tuple[int, int]) -> tuple[int, int]:
    """
    Obtém metade do tamanho da imagem para cálculos de posicionamento.
    
    Args:
        name: Caminho da imagem no diretório de assets
        default: Tupla (largura, altura) padrão caso a imagem não seja carregada
    
    Returns:
        Tupla com (largura/2, altura/2) da imagem
    """
    try:
        surf = images.load(name)
        return surf.get_width() // 2, surf.get_height() // 2
    except Exception:
        return default

player = None
PLAYER_HALF_W, PLAYER_HALF_H = get_image_half_size('player/prof_bolota_idle', (20, 20))

# Hitbox ligeiramente menor que o sprite visual para melhor sensação de colisão
PLAYER_HIT_W = max(12, int(PLAYER_HALF_W * 0.6))
PLAYER_HIT_H = max(18, int(PLAYER_HALF_H * 0.85))

door = None
door_open = False
key = None

enemies = []
gems = []
platforms = []

menu_buttons = []
game_over_buttons = []
victory_buttons = []

class Button:
    """
    Classe que representa um botão clicável da interface.
    
    Attributes:
        rect: Retângulo delimitador do botão
        text: Texto exibido no botão
        action: Função callback executada ao clicar
        hover: Estado de hover do mouse
    """
    
    def __init__(self, x, y, width, height, text, action):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hover = False
    
    def draw(self):
        bg = (70, 70, 90) if self.hover else (45, 45, 60)
        border = (20, 20, 30)
        screen.draw.filled_rect(self.rect, bg)
        screen.draw.rect(self.rect, border)
        draw_text_fallback(self.text, center=self.rect.center, color=(255, 255, 255), fontsize=28)

def make_buttons(base_x: int, base_y: int, width: int, height: int,
                 items: list[tuple[str, callable]], spacing: int = 60) -> list:
    """
    Cria uma lista de botões alinhados verticalmente.
    
    Args:
        base_x: Posição X inicial
        base_y: Posição Y inicial
        width: Largura de cada botão
        height: Altura de cada botão
        items: Lista de tuplas (texto, função_callback)
        spacing: Espaçamento vertical entre botões
    
    Returns:
        Lista de objetos Button
    """
    buttons = []
    for i, (text, action) in enumerate(items):
        y = base_y + i * spacing
        buttons.append(Button(base_x, y, width, height, text, action))
    return buttons

def align_buttons_vertical(buttons: list, base_y: int, spacing: int = 60) -> None:
    """Realinha botões existentes verticalmente a partir de uma nova posição Y."""
    for i, btn in enumerate(buttons):
        btn.rect.y = base_y + i * spacing

def init_screen_buttons(button_list_name: str, items: list[tuple[str, callable]], 
                        base_y: int = None, width: int = 280, height: int = 44, 
                        spacing: int = 60) -> list:
    """Inicializa botões centralizados horizontalmente para uma tela."""
    if base_y is None:
        base_y = HEIGHT // 2 - 20
    
    base_x = WIDTH // 2 - width // 2
    return make_buttons(base_x, base_y, width, height, items, spacing)

def init_game_over_buttons():
    """Inicializa os botões da tela de Game Over."""
    global game_over_buttons
    items = [("Reiniciar", restart_level), ("Voltar ao menu", back_to_menu)]
    game_over_buttons = init_screen_buttons('game_over', items)

def restart_level():
    """Reinicia o nível atual mantendo o progresso."""
    set_state(PLAYING)
    load_level(current_level)

def back_to_menu():
    """Retorna ao menu principal, resetando o estado do jogo."""
    global current_level, game_state, intro_music_started
    
    # Para a música antes de limpar as variáveis
    try:
        music.stop()
    except Exception:
        pass
    
    # Reseta variáveis globais para novo jogo
    current_level = 0
    intro_music_started = False
    reset_menu_context()
    init_menu_buttons()
    set_state(MENU)

def init_victory_buttons():
    """Inicializa os botões da tela de vitória."""
    global victory_buttons
    items = [("Jogar novamente", play_again), ("Voltar ao menu", back_to_menu)]
    victory_buttons = init_screen_buttons('victory', items, base_y=380, spacing=60)

def play_again():
    """Reinicia o jogo desde o primeiro nível."""
    set_state(PLAYING)
    load_level(0)

def play_victory_music():
    """Reproduz a música de vitória ao completar todos os níveis."""
    if not music_enabled:
        return
    music.play('congrats')

def draw_fullscreen_background(image_name: str) -> None:
    """Preenche a tela repetindo tiles do fundo para cobrir toda a área."""
    try:
        surf = images.load(image_name)
        tile_w, tile_h = surf.get_width(), surf.get_height()
    except Exception:
        tile_w, tile_h = WIDTH, HEIGHT
    for x in range(0, WIDTH, tile_w):
        for y in range(0, HEIGHT, tile_h):
            screen.blit(image_name, (x, y))

def draw_text_fallback(text: str, **kwargs) -> None:
    """Desenha texto na tela com fallback para fonte padrão se Impact não estiver disponível."""
    try:
        screen.draw.text(text, fontname="Impact", **kwargs)
    except Exception:
        screen.draw.text(text, **kwargs)


def reset_menu_context() -> None:
    """Reseta todas as variáveis de estado do nível atual."""
    global platforms, gems, enemies, door, key, has_key, collected_gems, total_gems
    global door_open, door_tip_active, player
    platforms = []
    gems = []
    enemies = []
    door = None
    key = None
    has_key = False
    collected_gems = 0
    total_gems = 0
    door_open = False
    door_tip_active = False
    player = None

def _get_spawnable_platforms(platform_list):
    """Filtra plataformas válidas para spawnar objetos, excluindo o piso de segurança."""
    return [p for p in platform_list if p.top < HEIGHT - 25 and p.width >= 40]

def _random_point_above_platform(p: Rect, dy: int = 30) -> tuple[int, int]:
    x = random.randint(p.left + 15, p.right - 15)
    return (x, p.top - dy)


def blit_scaled(image_name: str, topleft: tuple[int,int], size: tuple[int,int]) -> None:
    """Desenha imagem centralizada dentro de uma área especificada."""
    try:
        surf = images.load(image_name)
        iw, ih = surf.get_width(), surf.get_height()
        x, y = topleft
        tw, th = size
        cx = x + (tw // 2) - (iw // 2)
        cy = y + (th // 2) - (ih // 2)
        screen.blit(image_name, (cx, cy))
    except Exception:
        screen.blit(image_name, topleft)

def draw_platform_tiled(rect: Rect) -> None:
    """Desenha plataforma preenchendo o retângulo com tiles repetidos."""
    try:
        surf = images.load('tiles/box')
        tw, th = surf.get_width(), surf.get_height()
    except Exception:
        tw, th = 32, 32
    for x in range(rect.left, rect.right, tw):
        for y in range(rect.top, rect.bottom, th):
            screen.blit('tiles/box', (x, y))

def blit_image_centered(image_name: str, center: tuple[int, int], size: int) -> None:
    """Desenha imagem centralizada em uma coordenada específica."""
    try:
        surf = images.load(image_name)
        iw, ih = surf.get_width(), surf.get_height()
    except Exception:
        iw = ih = size
    topleft = (center[0] - iw // 2, center[1] - ih // 2)
    screen.blit(image_name, topleft)


def init_menu_buttons():
    """Inicializa os botões do menu principal."""
    global menu_buttons
    items = [
        ("Iniciar", start_game),
        ("Como Jogar", show_tutorial),
        ("Música: Ligada" if music_enabled else "Música: Desligada", toggle_music),
        ("Sair", quit_game),
    ]
    # Menu principal usa dimensões e espaçamento personalizados
    menu_buttons = init_screen_buttons('menu', items, base_y=200, width=200, height=50, spacing=70)

def start_game():
    """Inicia o jogo carregando o primeiro nível."""
    global game_state
    game_state = PLAYING
    load_level(0)
    play_sound('menu_click')

def toggle_music(play_feedback: bool = True):
    """Alterna entre música ligada e desligada."""
    global music_enabled, intro_music_started
    music_enabled = not music_enabled
    
    # Atualiza o texto do botão no menu
    for btn in menu_buttons:
        if btn.text.startswith("Música:"):
            btn.text = "Música: Ligada" if music_enabled else "Música: Desligada"
    try:
        if music_enabled:
            if game_state == MENU:
                music.play('intro_theme')
                intro_music_started = True
            elif game_state == PLAYING:
                music.play(levels[current_level]['music'])
            elif game_state == VICTORY:
                play_victory_music()
        else:
            music.stop()
    except Exception:
        pass
    if play_feedback:
        play_sound('menu_click')

def show_tutorial():
    """Exibe a tela de tutorial com instruções do jogo."""
    play_sound('tutorial_open')
    set_state(TUTORIAL)

def quit_game():
    """Encerra a aplicação do jogo."""
    play_sound('menu_click')
    exit()

def play_sound(sound_name: str) -> None:
    """Reproduz um efeito sonoro específico se o som estiver habilitado."""
    if not sound_enabled:
        return
    try:
        snd = getattr(sounds, sound_name, None)
        if snd:
            snd.play()
    except Exception:
        pass

def load_level(level_index: int) -> None:
    """
    Carrega e inicializa um nível específico do jogo.
    
    Esta função configura todas as entidades do nível: jogador, plataformas,
    gemas, inimigos, chave e porta. Também reinicia as variáveis de estado.
    
    Args:
        level_index: Índice do nível a ser carregado (0-based)
    """
    global current_level, platforms, gems, total_gems, enemies, door, door_open, key, has_key, collected_gems, player_health, player, PLAYER_HALF_W, PLAYER_HALF_H, PLAYER_HIT_W, PLAYER_HIT_H

    # Cria actors se ainda não foram instanciados
    if player is None:
        player = Actor('player/prof_bolota_idle', (100, 300))
        player.speed_y = 0
        PLAYER_HALF_W, PLAYER_HALF_H = get_image_half_size('player/prof_bolota_idle', (20, 20))
        PLAYER_HIT_W = max(12, int(PLAYER_HALF_W * 0.6))
        PLAYER_HIT_H = max(18, int(PLAYER_HALF_H * 0.85))
    if door is None:
        door = Actor('items/door_closed', (0, 0))
    if key is None:
        key = Actor('items/key_blue', (0, 0))
    
    current_level = level_index
    level = levels[level_index]
    
    # Reseta variáveis específicas do nível
    platforms = level['platforms']
    spawn_plats = _get_spawnable_platforms(platforms)
    gems = []
    enemies = []
    door_open = False
    has_key = False
    collected_gems = 0
    player_health = PLAYER_MAX_HEALTH
    
    # Posiciona gemas aleatoriamente sobre as plataformas, respeitando distância mínima
    for gem_data in level['gems']:
        tries = 40
        pos = None
        while tries > 0:
            plat = random.choice(spawn_plats) if spawn_plats else Rect(100, 450, 150, 20)
            candidate = _random_point_above_platform(plat, dy=30)
            ok = True
            for g in gems:
                dx = candidate[0] - g.x
                dy = candidate[1] - g.y
                if (dx*dx + dy*dy) < (GEM_MIN_DIST * GEM_MIN_DIST):
                    ok = False
                    break
            if ok:
                pos = candidate
                break
            tries -= 1
        if pos is None:
            plat = random.choice(spawn_plats) if spawn_plats else Rect(100, 450, 150, 20)
            pos = _random_point_above_platform(plat, dy=30)
        gem = Actor(f'items/gem_{gem_data["color"]}', pos)
        gems.append(gem)
    
    total_gems = len(gems)
    
    # Cria inimigos com patrulha e animação
    for enemy_data in level['enemies']:
        enemy = Actor(f'enemies/character_{enemy_data["type"]}_idle', enemy_data['patrol'][0])
        enemy.type = enemy_data['type']
        enemy.patrol_points = enemy_data['patrol']
        enemy.current_target = 1
        enemy.speed = ENEMY_SPEED
        enemy.walk_anim_counter = 0
        # Ajusta posição vertical para ficar corretamente sobre a plataforma
        try:
            _esurf = images.load(f'enemies/character_{enemy.type}_idle')
            enemy_half_h = _esurf.get_height() // 2
        except Exception:
            enemy_half_h = 20
        enemy.stand_offset = enemy_half_h
        base_platform_top = enemy_data['patrol'][0][1]
        enemy.base_y = base_platform_top - enemy.stand_offset
        enemy.y = enemy.base_y
        enemies.append(enemy)
    
    # Posiciona porta aleatoriamente no nível
    base_platform = next((p for p in platforms if p.top >= HEIGHT - 25), Rect(0, HEIGHT - 20, WIDTH, 20))
    spawn_on_floor = random.random() < 0.5
    if spawn_on_floor:
        dplat = base_platform
    else:
        dplat = random.choice(spawn_plats) if spawn_plats else base_platform

    DOOR_HALF_W, DOOR_HALF_H = get_image_half_size('items/door_closed', (24, 40))
    
    door_x = random.randint(dplat.left + DOOR_HALF_W, dplat.right - DOOR_HALF_W)
    door_y = dplat.top - DOOR_HALF_H
    door_x = max(DOOR_HALF_W, min(door_x, WIDTH - DOOR_HALF_W))
    door_y = max(DOOR_HALF_H, min(door_y, HEIGHT - DOOR_HALF_H))
    door.pos = (door_x, door_y)
    door.image = 'items/door_closed'
    door.visible = False

    # Posiciona chave mantendo distância mínima da porta
    k_candidates = [p for p in spawn_plats if p is not dplat] if spawn_plats else []
    if not k_candidates:
        k_candidates = spawn_plats if spawn_plats else [Rect(500, 350, 120, 20)]
    kplat = random.choice(k_candidates)
    KEY_HALF_W, KEY_HALF_H = get_image_half_size(f"items/key_{level['key_color']}", (12, 12))
    tries = 40
    key_x = kplat.left + KEY_HALF_W
    key_y = kplat.top - KEY_HALF_H
    while tries > 0:
        candidate_x = random.randint(kplat.left + KEY_HALF_W, kplat.right - KEY_HALF_W)
        candidate_y = kplat.top - KEY_HALF_H
        dx = candidate_x - door_x
        dy = candidate_y - door_y
        if (dx*dx + dy*dy) >= (KEY_MIN_DIST_FROM_DOOR * KEY_MIN_DIST_FROM_DOOR):
            key_x, key_y = candidate_x, candidate_y
            break
        tries -= 1
    key_x = max(KEY_HALF_W, min(key_x, WIDTH - KEY_HALF_W))
    key_y = max(KEY_HALF_H, min(key_y, HEIGHT - KEY_HALF_H))
    key.pos = (key_x, key_y)
    key.image = f"items/key_{level['key_color']}"
    key.visible = False
    
    # Posiciona jogador no início do nível (canto esquerdo)
    base_platform = next((p for p in platforms if p.top >= HEIGHT - 25), Rect(0, HEIGHT - 20, WIDTH, 20))
    player.x = max(PLAYER_HALF_W, 20 + PLAYER_HALF_W)
    player.y = base_platform.top - PLAYER_HIT_H
    player.speed_y = 0
    player.image = 'player/prof_bolota_idle'
    player.walk_anim_counter = 0
    player.jump_count = 0
    player.on_ground = False
    # Controle para mecânica de atravessar plataformas
    player.drop_through_frames = 0
    
    if music_enabled:
        music.play(level['music'])

def update_enemies() -> None:
    """Atualiza movimento de patrulha e animação de todos os inimigos."""
    for enemy in enemies:
        target_x, _ = enemy.patrol_points[enemy.current_target]
        if enemy.x < target_x:
            enemy.x += enemy.speed
        elif enemy.x > target_x:
            enemy.x -= enemy.speed
        
        # Animação de caminhada alternando entre dois frames
        enemy.walk_anim_counter = (enemy.walk_anim_counter + 1) % 20
        frame = 'walk_a' if enemy.walk_anim_counter < 10 else 'walk_b'
        try:
            enemy.image = f'enemies/character_{enemy.type}_{frame}'
        except Exception:
            enemy.image = f'enemies/character_{enemy.type}_idle'
        
        # Mantém o inimigo fixo na altura da plataforma
        if hasattr(enemy, 'base_y'):
            enemy.y = enemy.base_y
        
        # Inverte direção ao atingir ponto de patrulha
        if abs(enemy.x - target_x) <= enemy.speed:
            enemy.current_target = (enemy.current_target + 1) % len(enemy.patrol_points)

def check_collisions() -> None:
    """
    Processa física do jogador e detecta todas as colisões do jogo.
    
    Inclui: gravidade, colisão com plataformas, movimento horizontal,
    colisão com inimigos, coleta de gemas e chaves, interação com porta.
    """
    global player_health, collected_gems, has_key, door_open, door_tip_active
    prev_y = player.y
    prev_bottom = prev_y + PLAYER_HIT_H
    player.on_ground = False

    # Aplica gravidade ao jogador
    player.speed_y += GRAVITY
    player.speed_y = min(player.speed_y, MAX_FALL_SPEED)
    player.y += player.speed_y
    
    if getattr(player, 'drop_through_frames', 0) > 0:
        player.drop_through_frames -= 1
    
    player_rect = Rect(player.x - PLAYER_HIT_W, player.y - PLAYER_HIT_H, PLAYER_HIT_W * 2, PLAYER_HIT_H * 2)
    
    for platform in platforms:
        # Permite cair através de plataformas (exceto o piso de segurança)
        is_floor = platform.top >= HEIGHT - 25
        skip_vertical = (
            ((keyboard.down or keyboard.s) or getattr(player, 'drop_through_frames', 0) > 0)
            and not is_floor
        )

        # Detecta aterrissagem sobre plataformas
        if not skip_vertical:
            if (
                player.speed_y > 0
                and prev_bottom <= platform.top
                and player_rect.colliderect(platform)
                and (player_rect.right > platform.left and player_rect.left < platform.right)
            ):
                player.y = platform.top - PLAYER_HIT_H
                player.speed_y = 0
                player.image = 'player/prof_bolota_idle'
                player.jump_count = 0
                player.on_ground = True
                break
            current_bottom = player.y + PLAYER_HIT_H
            if (
                player.speed_y > 0
                and platform.left <= player.x <= platform.right
                and platform.top <= current_bottom <= platform.top + 6
            ):
                player.y = platform.top - PLAYER_HIT_H
                player.speed_y = 0
                player.image = 'player/prof_bolota_idle'
                player.jump_count = 0
                player.on_ground = True
                break
    
    # Processa movimento horizontal e animação de caminhada
    if keyboard.left or keyboard.a:
        player.x -= PLAYER_SPEED
        player.walk_anim_counter = (player.walk_anim_counter + 1) % 20
        player.image = 'player/prof_bolota_walk_1' if player.walk_anim_counter < 10 else 'player/prof_bolota_walk_2'
    elif keyboard.right or keyboard.d:
        player.x += PLAYER_SPEED
        player.walk_anim_counter = (player.walk_anim_counter + 1) % 20
        player.image = 'player/prof_bolota_walk_1' if player.walk_anim_counter < 10 else 'player/prof_bolota_walk_2'
    else:
        player.image = 'player/prof_bolota_idle'
    
    player.x = max(PLAYER_HALF_W, min(player.x, WIDTH - PLAYER_HALF_W))

    if player.y > HEIGHT - PLAYER_HIT_H and player.speed_y > 0:
        player.y = HEIGHT - PLAYER_HIT_H
        player.speed_y = 0
        player.jump_count = 0
        player.on_ground = True
    
    # Detecta colisão com inimigos e aplica dano
    for enemy in enemies:
        if player_rect.colliderect(Rect(enemy.x - ENEMY_HITBOX_HALF, enemy.y - ENEMY_HITBOX_HALF, ENEMY_HITBOX_HALF * 2, ENEMY_HITBOX_HALF * 2)):
            player_health -= ENEMY_DAMAGE
            play_sound('colisao')
            
            if player.x < enemy.x:
                player.x -= 30
            else:
                player.x += 30
            
            if player_health <= 0:
                game_over()
            break
    
    # Processa coleta de gemas
    for gem in gems[:]:
        if player_rect.colliderect(Rect(gem.x - GEM_HITBOX_HALF, gem.y - GEM_HITBOX_HALF, GEM_HITBOX_HALF * 2, GEM_HITBOX_HALF * 2)):
            gems.remove(gem)
            collected_gems += 1
            play_sound('coletar_cristal')
            
            if collected_gems >= total_gems:
                key.visible = True
    
    # Processa coleta de chave
    if key.visible and player_rect.colliderect(Rect(key.x - KEY_HITBOX_HALF, key.y - KEY_HITBOX_HALF, KEY_HITBOX_HALF * 2, KEY_HITBOX_HALF * 2)):
        has_key = True
        key.visible = False
        play_sound('coletar_cristal')
        door.visible = True
    
    # Verifica proximidade com a porta para exibir dica
    door_tip_active = player_rect.colliderect(Rect(door.x - DOOR_TIP_HITBOX_WIDTH//2, door.y - DOOR_TIP_HITBOX_HEIGHT//2, DOOR_TIP_HITBOX_WIDTH, DOOR_TIP_HITBOX_HEIGHT))

def game_over() -> None:
    """Processa fim de jogo quando o jogador perde todas as vidas."""
    global game_state
    game_state = GAME_OVER
    play_sound('fim_de_jogo')
    try:
        music.stop()
    except Exception:
        pass
    init_game_over_buttons()

def set_state(state: str) -> None:
    global game_state, intro_music_started
    game_state = state
    
    if state == MENU:
        try:
            reset_menu_context()
        except Exception:
            pass
    if music_enabled:
        if state == MENU:
            music.play('intro_theme')
            intro_music_started = True
        elif state == PLAYING:
            music.play(levels[current_level]['music'])
        elif state == VICTORY:
            play_victory_music()
        elif state in [GAME_OVER, TUTORIAL]:
            music.stop()

    if state == GAME_OVER:
        init_game_over_buttons()
    elif state == VICTORY:
        init_victory_buttons()

def draw_hearts() -> None:
    """Renderiza os corações de vida no HUD (cheios, meio ou vazios)."""
    for i in range(PLAYER_MAX_HEALTH // 2):
        center_x = HUD_MARGIN_LEFT + i * (HEART_SIZE + HEART_SPACING) + HEART_SIZE // 2
        center = (center_x, HEART_CENTER_Y)
        
        if player_health >= (i + 1) * 2:
            # Coração cheio
            blit_image_centered('hud/hud_heart', center, HEART_SIZE)
        elif player_health >= i * 2 + 1:
            # Meio coração
            blit_image_centered('hud/hud_heart_half', center, HEART_SIZE)
        else:
            # Coração vazio
            blit_image_centered('hud/hud_heart_empty', center, HEART_SIZE)

def draw_menu() -> None:
    """Renderiza a tela do menu principal."""
    # Fundo sólido verde
    screen.fill((50, 180, 100))
    
    # Título do jogo com efeito de sombra
    title_text = "Energy Quest"
    title_pos = (WIDTH//2, 110)
    for dx, dy in [(-4,0),(4,0),(0,-4),(0,4)]:
        draw_text_fallback(title_text, center=(title_pos[0]+dx, title_pos[1]+dy), fontsize=88, color="black")
    draw_text_fallback(title_text, center=title_pos, fontsize=88, color="white")
    
    # Créditos
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        draw_text_fallback('Criado por Professor Marquinhos', center=(WIDTH//2+dx, 560+dy), fontsize=22, color=(20,20,20))
    draw_text_fallback('Criado por Professor Marquinhos', center=(WIDTH//2, 560), fontsize=22, color="yellow")
    
    # Personagem principal (Professor Bolota) à esquerda do título
    char_w, char_h = 160, 160
    char_center_x = (WIDTH//2) - 280
    char_pos = (char_center_x - char_w//2, title_pos[1] - char_h//2)
    blit_scaled('player/prof_bolota_idle', char_pos, (char_w, char_h))
    
    # Botões do menu
    for btn in menu_buttons:
        btn.draw()

def draw_game() -> None:
    """Renderiza a tela principal de gameplay."""
    # Renderiza elementos do cenário
    draw_fullscreen_background(levels[current_level]['background'])
    for platform in platforms:
        draw_platform_tiled(platform)
    for gem in gems:
        gem.draw()
    if key.visible:
        key.draw()
    if getattr(door, 'visible', True):
        door.draw()
    for enemy in enemies:
        enemy.draw()
    player.draw()
    
    # ===== HUD (Interface) =====
    # Corações (vidas) - canto esquerdo
    draw_hearts()
    
    # Texto "Nível" - esquerda-centro
    nivel_x = WIDTH // 2 - 120
    draw_text_fallback(
        f"Nivel {current_level + 1}",
        center=(nivel_x, HUD_TEXT_CENTER_Y),
        color=(30, 30, 30),
        fontsize=HUD_TEXT_SIZE
    )
    
    # Texto "Gems" - direita-centro
    gems_x = WIDTH // 2 + 120
    draw_text_fallback(
        f"Gems {collected_gems}/{total_gems}",
        center=(gems_x, HUD_TEXT_CENTER_Y),
        color=(30, 30, 30),
        fontsize=HUD_TEXT_SIZE
    )
    
    # Status da música - canto direito
    music_status = "Ligada" if music_enabled else "Desligada"
    draw_text_fallback(
        f"Música (M): {music_status}",
        center=(WIDTH - HUD_MARGIN_RIGHT - 100, HUD_TEXT_CENTER_Y),
        color=(30, 30, 30),
        fontsize=HUD_TEXT_SIZE
    )
    
    # Dica de porta (quando próximo)
    if door_tip_active and getattr(door, 'visible', True):
        draw_text_fallback(
            "Aperte espaco para entrar", 
            center=(door.x, door.y - 90), 
            color=(30, 30, 30), 
            fontsize=20
        )


def draw_game_over() -> None:
    """Renderiza a tela de Game Over."""
    # Fundo sólido roxo escuro
    screen.fill((60, 50, 80))
    panel_rect = Rect(80, 100, WIDTH - 160, HEIGHT - 200)
    screen.draw.filled_rect(panel_rect, (30, 30, 45))
    screen.draw.rect(panel_rect, (90, 110, 150))
    title = "Fim de Jogo"
    for dx, dy in [(-3,0),(3,0),(0,-3),(0,3)]:
        draw_text_fallback(title, center=(WIDTH//2+dx, 160+dy), fontsize=56, color="black")
    draw_text_fallback(title, center=(WIDTH//2, 160), fontsize=56, color=(230,230,255))
    draw_text_fallback("Voce pode tentar novamente ou voltar ao menu.", center=(WIDTH//2, 210), fontsize=24, color=(200, 220, 255))
    for btn in game_over_buttons:
        btn.draw()

def draw_tutorial() -> None:
    """Renderiza a tela de tutorial com instruções do jogo."""
    # Fundo sólido azul claro
    screen.fill((100, 150, 180))
    panel_rect = Rect(80, 100, WIDTH - 160, HEIGHT - 200)
    screen.draw.filled_rect(panel_rect, (35, 35, 55))
    screen.draw.rect(panel_rect, (80, 80, 120))
    title = "Como Jogar"
    draw_text_fallback(title, center=(WIDTH/2, 140), fontsize=48, color="white")
    blit_scaled('hud/tutorial_move', (150, 200), (64, 64))
    screen.draw.text("Mover: Setas ou A/D", midleft=(230, 232), fontsize=28, color="white")
    blit_scaled('tiles/box', (150, 280), (64, 64))
    screen.draw.text("Pular: Seta Cima ou W", midleft=(230, 312), fontsize=28, color="white")
    blit_scaled('items/door_closed', (150, 360), (64, 64))
    screen.draw.text("Abrir Porta: Espaco", midleft=(230, 392), fontsize=28, color="white")
    screen.draw.text("Clique para voltar ao menu", center=(WIDTH/2, 480), fontsize=24, color="yellow")

def draw_victory() -> None:
    """Renderiza a tela de vitória ao completar todos os níveis."""
    # Fundo sólido verde
    screen.fill((50, 180, 100))
    
    # Painel maior para acomodar todos os elementos
    panel_rect = Rect(80, 100, WIDTH - 160, HEIGHT - 180)
    screen.draw.filled_rect(panel_rect, (40, 40, 70))
    screen.draw.rect(panel_rect, (120, 180, 235))
    
    # Título e mensagem
    msg1 = "Parabéns"
    msg2 = "Você completou todas as fases"
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        draw_text_fallback(msg1, center=(WIDTH//2+dx, 160+dy), fontsize=44, color=(20,20,20))
    draw_text_fallback(msg1, center=(WIDTH//2, 160), fontsize=44, color=(255,255,220))
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        draw_text_fallback(msg2, center=(WIDTH//2+dx, 210+dy), fontsize=30, color=(20,20,20))
    draw_text_fallback(msg2, center=(WIDTH//2, 210), fontsize=30, color=(240,240,220))
    
    # Desenhar personagem comemorando
    char_w, char_h = 100, 100
    char_center_x = WIDTH // 2
    char_pos = (char_center_x - char_w//2, 260)
    blit_scaled('player/prof_bolota_idle', char_pos, (char_w, char_h))
    
    # Botões posicionados corretamente dentro da janela
    for btn in victory_buttons:
        btn.draw()


def update() -> None:
    """
    Função principal de atualização chamada a cada frame.
    
    Gerencia a lógica de acordo com o estado atual do jogo.
    """
    global intro_music_started
    if game_state == MENU:
        if music_enabled and not intro_music_started:
            try:
                music.play('intro_theme')
            except Exception:
                pass
            intro_music_started = True
    elif game_state == PLAYING:
        update_enemies()
        check_collisions()
    else:
        pass

def draw() -> None:
    """
    Função principal de renderização chamada a cada frame.
    
    Delega o desenho para a função apropriada baseada no estado do jogo.
    """
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        draw_game()
    elif game_state == GAME_OVER:
        draw_game_over()
    elif game_state == VICTORY:
        draw_victory()
    elif game_state == TUTORIAL:
        draw_tutorial()

def on_key_down(key) -> None:
    """
    Callback de Pygame Zero para processar teclas pressionadas.
    
    Args:
        key: Código da tecla pressionada
    """
    if key == keys.ESCAPE:
        set_state(MENU)

    if game_state == PLAYING:
        # Mecânica de pulo duplo
        if (key == keys.UP or key == keys.W) and getattr(player, 'jump_count', 0) < 2:
            player.speed_y = -JUMP_SPEED
            player.image = 'player/prof_bolota_jump'
            play_sound('som_pulo')
            player.jump_count = getattr(player, 'jump_count', 0) + 1
            player.on_ground = False
        elif (key == keys.DOWN or key == keys.S):
            if getattr(player, 'on_ground', False):
                player.drop_through_frames = 10
                player.speed_y = max(player.speed_y, 2)
                player.y += 2
        elif key == keys.SPACE:
            try_open_door()
        elif key == keys.M:
            toggle_music(play_feedback=False)

def on_mouse_move(pos: tuple[int, int]) -> None:
    """Callback de Pygame Zero para processar movimento do mouse (hover nos botões)."""
    if game_state == MENU:
        for btn in menu_buttons:
            btn.hover = btn.rect.collidepoint(pos)

def on_mouse_down(pos: tuple[int, int]) -> None:
    """Callback de Pygame Zero para processar cliques do mouse."""
    if game_state == MENU:
        for btn in menu_buttons:
            if btn.rect.collidepoint(pos):
                btn.action()
    elif game_state == GAME_OVER:
        for btn in game_over_buttons:
            if btn.rect.collidepoint(pos):
                btn.action()
    elif game_state == VICTORY:
        for btn in victory_buttons:
            if btn.rect.collidepoint(pos):
                btn.action()
    elif game_state == TUTORIAL:
        set_state(MENU)

def try_open_door() -> None:
    """Tenta abrir a porta se o jogador possui chave e está próximo."""
    global door_open, game_state
    player_rect = Rect(player.x - PLAYER_HIT_W, player.y - PLAYER_HIT_H, PLAYER_HIT_W * 2, PLAYER_HIT_H * 2)
    if has_key and collected_gems >= total_gems and player_rect.colliderect(Rect(door.x - DOOR_TIP_HITBOX_WIDTH//2, door.y - DOOR_TIP_HITBOX_HEIGHT//2, DOOR_TIP_HITBOX_WIDTH, DOOR_TIP_HITBOX_HEIGHT)):
        door_open = True
        door.image = 'items/door_open'
        play_sound('som_alavanca')
        if current_level < len(levels) - 1:
            load_level(current_level + 1)
        else:
            set_state(VICTORY)
            play_sound('tutorial_open')
    else:
        play_sound('menu_click')

# ============================================================
# INICIALIZAÇÃO E EXECUÇÃO DO JOGO
# ============================================================
init_menu_buttons()

import pgzrun
pgzrun.go()
