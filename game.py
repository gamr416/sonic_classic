import pygame
from map import Map

SIZE = WIDTH, HEIGHT = 1200, 600
SCREEN = pygame.display.set_mode(SIZE)
FPS = 30
TILE_SIZE = 40


class Game:
    def __init__(self, map, sonic):
        self.map = map
        self.sonic = sonic
        self.left = False
        self.last_left = False
        self.right = False
        self.last_right = True
        self.last_way = None
        self.counter_way = 0
        self.MAX_COUNTER_WAY = 4
        self.count_jump = 0
        self.bg_pic = pygame.image.load('Sonic Sprites/background.jpg')
        self.second_bg = self.bg_pic
        self.JUMP = False
        self.fall_after_jump = False
        self.down = False
        self.bg_pic_x = 0
        self.second_bg_x = self.second_bg.get_width()
        self.first_screen = False
        self.second_screen = False
        self.flag_start_bg = False
        self.world_offset = [0, -560]
        self.entered_camera_move = False
        self.wall_stop_r = False
        self.wall_stop_l = False
        self.ring_amount = 0
        self.finish_font = pygame.font.Font('font/sonic-press-start-button.otf', 40)
        self.back_finish_font = pygame.font.Font('font/sonic-press-start-button.otf', 40)
        self.playing_seconds = 0
        self.time_flag = False
        self.health_flag = False
        self.invincibility = False
        self.count_invis = 0
        self.level_count = self.map.level
        self.total_score = 0
        # self.get_damaged = False
        # self.damaged_way = False
        # self.damage_length = 8
        # self.damaged_height = 4
        # self.fall_after_damage = False
        # self.count_damage_jump = 1
        self.fall = True

    def blit_all_tiles(self, window, tmxdata, world_offset):
        for layer in tmxdata:
            for tile in layer.tiles():
                img = pygame.transform.scale(tile[2], (40, 40))
                x_pixel = tile[0] * 40 + world_offset[0]
                y_pixel = tile[1] * 40 + world_offset[1]
                window.blit(img, (x_pixel, y_pixel))

    def render(self, screen):
        if self.invincibility and self.count_invis % 5 == 0:
            pass
        elif (self.JUMP or self.fall_after_jump) and self.last_right:
            self.sonic.render_jump_right(screen)
        elif (self.JUMP or self.fall_after_jump) and self.last_left:
            self.sonic.render_jump_left(screen)
        elif self.wall_stop_r:
            self.sonic.render_wall_stop_right(screen)
        elif self.wall_stop_l:
            self.sonic.render_wall_stop_left(screen)
        elif self.left and not self.JUMP and not self.fall_after_jump:
            self.sonic.render_left_run(screen)
        elif self.right and not self.JUMP and not self.fall_after_jump:
            self.sonic.render_right_run(screen)
        elif self.down and self.last_right:
            self.sonic.render_down_right(screen)
        elif self.down and self.last_left:
            self.sonic.render_down_left(screen)
        else:
            if self.last_left:
                self.sonic.render_idle_left(screen)
            elif self.last_right:
                self.sonic.render_idle_right(screen)
        self.count_invis += 2

    def update_sonic(self):
        gh_sound = pygame.mixer.Sound('music/GHzone.MP3')
        title_sound = pygame.mixer.Sound('music/Titlemus.MP3')
        over_sound = pygame.mixer.Sound('music/gameover.mp3')
        ring_sound = pygame.mixer.Sound('music/ring.mp3')
        finish_sound = pygame.mixer.Sound('music/sonic-level-finish.mp3')

        starting = True
        running = True
        ending = False
        finishing = False
        over = False
        title_sound.play()
        title_sound.set_volume(0.1)
        start_ticks = pygame.time.get_ticks()
        clock = pygame.time.Clock()
        while starting:
            starting_seconds = (pygame.time.get_ticks() - start_ticks) // 100
            self.bg_pic_x -= 20 / FPS
            self.second_bg_x -= 20 / FPS
            if self.bg_pic_x + self.second_bg.get_width() <= WIDTH and self.flag_start_bg:
                self.second_bg_x = WIDTH
                self.flag_start_bg = False
            if self.second_bg_x + self.bg_pic.get_width() <= WIDTH and not self.flag_start_bg:
                self.bg_pic_x = WIDTH
                self.flag_start_bg = True
            SCREEN.blit(self.bg_pic, (self.bg_pic_x, 0))
            SCREEN.blit(self.second_bg, (self.second_bg_x, 0))
            self.sonic.render_start_sonic(SCREEN)
            if starting_seconds >= 50:
                font = pygame.font.Font('font/sonic-press-start-button.otf', 20)
                text = font.render('PRESS SPACE TO START', True, (255, 255, 0))
                text_rect = text.get_rect(center=(WIDTH / 40 * 19, HEIGHT / 40 * 31))
                SCREEN.blit(text, text_rect)
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    starting = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    starting = False
                    running = False
            pygame.display.update()
            clock.tick(FPS)
            pygame.display.flip()
        title_sound.stop()
        clock = pygame.time.Clock()
        next_x, next_y = self.sonic.get_position()
        map_next_x, map_next_y = next_x, next_y
        jump_height = 6
        last_jump = 6
        max_jump = False
        count = 1
        gh_sound.play(-1)
        gh_sound.set_volume(0.1)
        playing_ticks = pygame.time.get_ticks()
        SCREEN.fill((0, 0, 0))
        finish_ticks = pygame.time.get_ticks()
        invincibility_tick = pygame.time.get_ticks()
        while running:
            invincibility_seconds = (pygame.time.get_ticks() - invincibility_tick) // 100
            map_next_x = next_x - self.world_offset[0] / TILE_SIZE + 0.5
            map_next_y = next_y - self.world_offset[1] / TILE_SIZE
            if finishing:
                finish_text = (
                    self.finish_font.render(f'SCORE {self.ring_amount * 100 + (600 - self.playing_seconds // 10)}',
                                            True, (255, 255, 0)))
                lower_finish_text = (
                    self.finish_font.render(f'SCORE {self.ring_amount * 100 + (600 - self.playing_seconds // 10)}',
                                            True, (0, 0, 0)))
                finish_seconds = (pygame.time.get_ticks() - finish_ticks) // 100
                self.bg_pic_x -= 20 / FPS
                self.second_bg_x -= 20 / FPS
                if self.bg_pic_x + self.second_bg.get_width() <= WIDTH and self.flag_start_bg:
                    self.second_bg_x = WIDTH
                    self.flag_start_bg = False
                if self.second_bg_x + self.bg_pic.get_width() <= WIDTH and not self.flag_start_bg:
                    self.bg_pic_x = WIDTH
                    self.flag_start_bg = True
                SCREEN.blit(self.bg_pic, (self.bg_pic_x, 0))
                SCREEN.blit(self.second_bg, (self.second_bg_x, 0))
                self.blit_all_tiles(SCREEN, self.map.map, self.world_offset)
                self.render(SCREEN)
                SCREEN.blit(lower_finish_text, (WIDTH // 2 - finish_text.get_width() // 2 + 2,
                                                HEIGHT // 2 - finish_text.get_height() // 2 + 2))
                SCREEN.blit(finish_text, (WIDTH // 2 - finish_text.get_width() // 2,
                                          HEIGHT // 2 - finish_text.get_height() // 2))
                if self.JUMP:
                    if 0.5 ** count < last_jump and self.map.is_free((map_next_x, map_next_y - 0.5 ** count)):
                        self.world_offset[1] += 0.5 * TILE_SIZE
                        last_jump -= 0.5 ** count
                    elif 0.5 ** count >= last_jump and self.map.is_free((map_next_x, map_next_y - 0.5 ** count)):
                        self.world_offset[1] += last_jump * TILE_SIZE
                        count = 1
                        last_jump = 5
                        self.JUMP = False
                        self.fall = True
                        self.fall_after_jump = True
                    elif not self.map.is_free((map_next_x, map_next_y - 0.5 ** count)):
                        self.JUMP = False
                        self.fall = True
                        last_jump = 5
                        count = 1
                        self.fall_after_jump = True
                if not self.JUMP and self.map.is_free((map_next_x, map_next_y + 1)):
                    self.world_offset[1] -= 0.5 * TILE_SIZE
                if not self.map.is_free((map_next_x, map_next_y + 1)):
                    self.fall_after_jump = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        finishing = False
                    if finish_seconds > 120 and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.total_score += self.ring_amount * 100 + (600 - self.playing_seconds // 10)
                            self.level_count -= 1
                            if self.level_count != 0:
                                finishing = False
                                self.map = Map([1, 2, 16, 17, 18, 19, 24, 25], [20],
                                               [67, 134, 111, 112, 135], self.level_count)
                                self.world_offset = [0, -520]
                                finish_ticks = pygame.time.get_ticks()
                                gh_sound.set_volume(0.1)
                                self.ring_amount = 0
                                playing_ticks = pygame.time.get_ticks()
                            else:
                                starting = False
                                running = False
                                ending = False
                                finishing = False
                                over = True
                clock.tick(FPS)
                pygame.display.flip()

            else:
                SCREEN.fill((0, 0, 0))
                self.bg_pic_x -= 20 / FPS
                self.second_bg_x -= 20 / FPS
                if self.bg_pic_x + self.second_bg.get_width() <= WIDTH and self.flag_start_bg:
                    self.second_bg_x = WIDTH
                    self.flag_start_bg = False
                if self.second_bg_x + self.bg_pic.get_width() <= WIDTH and not self.flag_start_bg:
                    self.bg_pic_x = WIDTH
                    self.flag_start_bg = True
                SCREEN.blit(self.bg_pic, (self.bg_pic_x, 0))
                SCREEN.blit(self.second_bg, (self.second_bg_x, 0))
                self.blit_all_tiles(SCREEN, self.map.map, self.world_offset)
                self.render(SCREEN)
                self.wall_stop_r = False
                self.wall_stop_l = False
                self.playing_seconds = (pygame.time.get_ticks() - playing_ticks) // 100
                if self.playing_seconds >= 6000:
                    running = False
                    gh_sound.stop()
                    self.time_flag = True
                    ending = True
                if self.JUMP:
                    if 0.5 ** count < last_jump and self.map.is_free((map_next_x, map_next_y - 0.5 ** count)):
                        self.world_offset[1] += 0.5 * TILE_SIZE
                        last_jump -= 0.5 ** count
                        self.fall = False
                    elif 0.5 ** count >= last_jump and self.map.is_free((map_next_x, map_next_y - last_jump ** count)):
                        self.world_offset[1] += last_jump * TILE_SIZE
                        count = 1
                        last_jump = 5
                        self.JUMP = False
                        self.fall_after_jump = True
                        self.fall = True
                    elif not self.map.is_free((map_next_x, map_next_y - 0.5 ** count)):
                        self.JUMP = False
                        last_jump = 5
                        count = 1
                        self.fall_after_jump = True
                        self.fall = True
                if not self.JUMP and ((( not self.map.is_free((map_next_x + 0.1, map_next_y + 1.25)))
                                       or (not self.map.is_free((map_next_x - 0.1, map_next_y + 1.25))))):
                    self.Jump = False
                    self.fall = False
                    self.fall_after_jump = False
                elif not self.JUMP and (((self.map.is_free((map_next_x, map_next_y + 1.25)))
                                       or (self.map.is_free((map_next_x, map_next_y + 1.25))))):
                    self.world_offset[1] -= 0.5 * TILE_SIZE
                if not self.map.is_free((map_next_x, map_next_y + 1)):
                    self.Jump = False
                    self.fall = False
                    self.fall_after_jump = False
                if (((self.map.get_tile_id((map_next_x + 0.25, map_next_y + 1)) == 17)
                     or (self.map.get_tile_id((map_next_x - 0.25, map_next_y + 1)) == 17))
                        and not self.JUMP
                        and self.ring_amount == 0
                        and not self.invincibility):
                    running = False
                    gh_sound.stop()
                    self.health_flag = True
                    ending = True
                elif (self.invincibility
                      and self.map.get_tile_id((map_next_x, map_next_y + 1)) == 17
                      and not self.JUMP):
                    pass
                elif (((self.map.get_tile_id((map_next_x + 0.25, map_next_y + 1)) == 17)
                       or (self.map.get_tile_id((map_next_x - 0.25, map_next_y + 1)) == 17))
                      and not self.JUMP
                      and self.ring_amount > 0
                      and not self.invincibility):
                    self.ring_amount = 0
                    self.invincibility = True
                    # self.get_damaged = True
                    # self.damaged_way = self.last_right
                    invincibility_tick = pygame.time.get_ticks()
                    invincibility_seconds = (pygame.time.get_ticks() - invincibility_tick) // 100
                # if self.get_damaged:
                #     if 0.5 ** self.count_damage_jump < self.damaged_height and self.map.is_free((map_next_x, map_next_y - 0.5 ** self.count_damage_jump)):
                #         self.world_offset[1] += 0.5 * TILE_SIZE
                #         self.damaged_height -= 0.5 ** self.count_damage_jump
                #     elif 0.5 ** self.count_damage_jump >= self.damaged_height and self.map.is_free(
                #             (map_next_x, map_next_y - self.damaged_height ** self.count_damage_jump)):
                #         self.world_offset[1] += self.damaged_height * TILE_SIZE
                #         self.count_damage_jump = 1
                #         self.damaged_height = 5
                #         self.JUMP = False
                #         self.fall_after_damage = True
                #         self.get_damaged = False
                #     elif not self.map.is_free((map_next_x, map_next_y - 0.5 ** self.count_damage_jump)):
                #         self.JUMP = False
                #         self.damaged_height = 5
                #         self.count_damage_jump = 1
                #         self.JUMP = False
                #         self.get_damaged = False
                #     if self.damaged_way:
                #         pass
                if invincibility_seconds > 20 and self.invincibility:
                    self.invincibility = False
                if not self.map.is_free((map_next_x, map_next_y + 1)):
                    self.fall_after_jump = False
                if (pygame.key.get_pressed()[pygame.K_a]
                        and self.map.is_free((map_next_x, map_next_y))):
                    if self.last_way != 'LEFT':
                        self.counter_way = 2
                        self.left = True
                        self.right = False
                        self.last_right = False
                        self.last_left = True
                        if self.map.is_free((map_next_x - (2 ** self.MAX_COUNTER_WAY) / FPS, map_next_y + 0.5)):
                            self.world_offset[0] += 4 * TILE_SIZE / FPS
                        else:
                            try:
                                if self.counter_way >= self.MAX_COUNTER_WAY:
                                    if not self.map.is_free((map_next_x - (2 ** self.MAX_COUNTER_WAY) / FPS,
                                                             map_next_y + 0.5)):
                                        self.wall_stop_l = True
                            except ValueError:
                                pass
                    else:
                        self.left = True
                        self.right = False
                        self.last_right = False
                        self.last_left = True
                        self.counter_way += 0.05
                        if self.counter_way > self.MAX_COUNTER_WAY and self.map.is_free(
                                (map_next_x - (2 ** self.MAX_COUNTER_WAY) / FPS, map_next_y + 0.5)):
                            self.counter_way = 4
                            self.world_offset[0] += (2 ** self.MAX_COUNTER_WAY) * TILE_SIZE / FPS
                        elif self.counter_way < self.MAX_COUNTER_WAY and self.map.is_free(
                                (map_next_x - (2 ** self.MAX_COUNTER_WAY) / FPS, map_next_y + 0.5)):
                            self.world_offset[0] += (2 ** self.counter_way) * TILE_SIZE / FPS
                        else:
                            try:
                                if self.counter_way >= self.MAX_COUNTER_WAY:
                                    if not self.map.is_free((map_next_x - (2 ** self.MAX_COUNTER_WAY) / FPS,
                                                             map_next_y + 0.5)):
                                        self.wall_stop_l = True
                                        self.counter_way = 2
                                else:
                                    if not self.map.is_free((map_next_x - (2 ** self.MAX_COUNTER_WAY) / FPS,
                                                             map_next_y + 0.5)):
                                        self.wall_stop_l = True
                            except ValueError:
                                pass
                    self.last_way = 'LEFT'
                elif (pygame.key.get_pressed()[pygame.K_d]
                      and self.map.is_free((map_next_x, map_next_y))):
                    if self.last_way != 'RIGHT':
                        self.counter_way = 2
                        self.left = False
                        self.right = True
                        self.last_right = True
                        self.last_left = False
                        if self.map.is_free((map_next_x + (2 ** self.MAX_COUNTER_WAY) / FPS, map_next_y + 0.5)):
                            self.world_offset[0] -= 3 * TILE_SIZE / FPS
                        else:
                            try:
                                if not self.map.is_free((map_next_x + (2 ** self.MAX_COUNTER_WAY) / FPS, map_next_y + 0.5)):
                                    self.wall_stop_r = True
                            except ValueError:
                                pass
                    else:
                        self.left = False
                        self.right = True
                        self.last_right = True
                        self.last_left = False
                        self.counter_way += 0.05
                        if (self.counter_way > self.MAX_COUNTER_WAY
                                and self.map.is_free((map_next_x + (2 ** self.MAX_COUNTER_WAY) / FPS, map_next_y + 0.5))):
                            self.world_offset[0] -= (2 ** self.MAX_COUNTER_WAY * TILE_SIZE) / FPS
                            self.counter_way = 4
                        elif (self.counter_way < self.MAX_COUNTER_WAY
                              and self.map.is_free((map_next_x + (2 ** self.MAX_COUNTER_WAY) / FPS, map_next_y + 0.5))):
                            self.world_offset[0] -= (2 ** self.counter_way * TILE_SIZE) / FPS
                        else:
                            try:
                                if self.counter_way >= self.MAX_COUNTER_WAY:
                                    if not self.map.is_free((map_next_x + (2 ** self.MAX_COUNTER_WAY) / FPS,
                                                             map_next_y + 0.5)):
                                        self.wall_stop_r = True
                                        self.counter_way = 2
                                else:
                                    if not self.map.is_free((map_next_x + (2 ** self.MAX_COUNTER_WAY) / FPS,
                                                             map_next_y + 0.5)):
                                        self.wall_stop_r = True
                            except ValueError:
                                pass
                    self.last_way = 'RIGHT'
                else:
                    self.left = False
                    self.right = False
                if (pygame.key.get_pressed()[pygame.K_s]
                        and not pygame.key.get_pressed()[pygame.K_SPACE]
                        and not self.map.is_free((map_next_x, map_next_y + 1))
                        and not pygame.key.get_pressed()[pygame.K_a]
                        and not pygame.key.get_pressed()[pygame.K_d]):
                    self.down = True

                if not pygame.key.get_pressed()[pygame.K_s]:
                    self.down = False

                # if pygame.key.get_pressed()[pygame.K_s] and pygame.key.get_pressed()[pygame.K_SPACE] and self.map.is_free(
                #         (map_next_x, map_next_y + 1)):
                #     self.world_offset[1] -= 1 * TILE_SIZE / FPS

                if not pygame.key.get_pressed()[pygame.K_d] and not pygame.key.get_pressed()[pygame.K_a]:
                    self.last_way = None
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if (event.key == pygame.K_SPACE
                                and not pygame.key.get_pressed()[pygame.K_s]
                                and not self.map.is_free((map_next_x, map_next_y + 1))):
                            self.JUMP = True
                            self.sonic.jump_iter = 0
                upper_font = pygame.font.Font('font/sonic-1-hud-font.ttf', 25)
                lower_font = pygame.font.Font('font/sonic-1-hud-font.ttf', 25)
                time_text = upper_font.render(f"TIME {self.playing_seconds // 600} "
                                              f": {self.playing_seconds // 10 % 60}",
                                              True, (255, 255, 0))
                lower_time_text = lower_font.render(f"TIME {self.playing_seconds // 600} "
                                                    f": {self.playing_seconds // 10 % 60}",
                                                    True, (0, 0, 0))
                ring_text = upper_font.render(f"RINGS {self.ring_amount}",
                                              True, (255, 255, 0))
                lower_ring_text = lower_font.render(f"RINGS {self.ring_amount}",
                                                    True, (0, 0, 0))
                if self.map.get_tile_id((map_next_x, map_next_y)) in self.map.ring_tiles:
                    ring_sound.stop()
                    self.ring_amount += 1
                    ring_sound.play()
                    ring_sound.set_volume(0.1)
                    self.map.map.layers[0].data[int(map_next_y)][int(map_next_x)] = 0
                if self.map.get_tile_id((map_next_x, map_next_y)) in self.map.finish_tiles:
                    finish_sound.play()
                    finish_sound.set_volume(0.2)
                    gh_sound.set_volume(0)
                    finishing = True
                SCREEN.blit(lower_time_text, (27, 12))
                SCREEN.blit(lower_ring_text, (27, 42))
                SCREEN.blit(time_text, (25, 10))
                SCREEN.blit(ring_text, (25, 40))
                self.sonic.set_position((next_x, next_y))
                clock.tick(FPS)
                pygame.display.flip()
        if ending:
            over_sound.play()
            over_sound.set_volume(0.1)
        ending_ticks = pygame.time.get_ticks()
        while ending:
            ending_seconds = (pygame.time.get_ticks() - ending_ticks) // 100
            if self.time_flag:
                font = pygame.font.Font('font/sonic-press-start-button.otf', 30)
                text = font.render(f'TIME OVER', True, (255, 255, 0))
                lower_text = font.render(f'TIME OVER', True, (0, 0, 0))
                text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                lower_text_rect = lower_text.get_rect(center=(WIDTH / 2 + 2, HEIGHT / 2 + 2))
                SCREEN.blit(lower_text, lower_text_rect)
                SCREEN.blit(text, text_rect)
            elif self.health_flag:
                font = pygame.font.Font('font/sonic-press-start-button.otf', 30)
                text = font.render(f'GAME OVER', True, (255, 255, 0))
                lower_text = font.render(f'GAME OVER', True, (0, 0, 0))
                text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                lower_text_rect = lower_text.get_rect(center=(WIDTH / 2 + 2, HEIGHT / 2 + 2))
                SCREEN.blit(lower_text, lower_text_rect)
                SCREEN.blit(text, text_rect)
            if ending_seconds > 60:
                restart_font = pygame.font.Font('font/sonic-press-start-button.otf', 20)
                restart_text = restart_font.render(f'TO RESTART PRESS SPACE', True, (255, 255, 0))
                lower_restart_text = restart_font.render(f'TO RESTART PRESS SPACE', True, (0, 0, 0))
                lower_restart_text_rect = lower_restart_text.get_rect(center=(WIDTH / 2 + 2, HEIGHT / 2 + 52))
                text_rect = restart_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
                SCREEN.blit(lower_restart_text, lower_restart_text_rect)
                SCREEN.blit(restart_text, text_rect)
            if pygame.key.get_pressed()[pygame.K_SPACE] and ending_seconds > 60:
                over_sound.stop()
                ending = False
                starting = True
                running = True
                self.__init__(Map([1, 2, 16, 17, 18, 19, 24, 25],
                                  [20], [67, 134, 111, 112, 135], 2), self.sonic)

                self.update_sonic()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ending = False
            pygame.display.flip()
        while over:
            SCREEN.fill((0, 0, 0))
            end_font = pygame.font.Font('font/sonic-press-start-button.otf', 50)
            end_text = end_font.render("THANKS FOR PLAYING", True, (255, 255, 0))
            end_score_font = pygame.font.Font('font/sonic-press-start-button.otf', 20)
            end_score = end_score_font.render(f"TOTAL SCORE {self.total_score}", True, (255, 255, 0))
            SCREEN.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height()))
            SCREEN.blit(end_score, (WIDTH // 2 - end_score.get_width() // 2, HEIGHT // 2 - end_score.get_height() // 2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    over = False
            pygame.display.flip()
        pygame.display.update()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
