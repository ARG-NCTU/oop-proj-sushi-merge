import pygame
import yaml


class CollisionTypes:
    PARTICLE = 1
    WALL = 2


class ConfigNode:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


class Config:
    def __init__(self):
        with open("config.yaml", "r") as yaml_file:
            self.config = yaml.safe_load(yaml_file)

        self.screen = ConfigNode(**self.config["screen"])
        self.pad = ConfigNode(**self.config["pad"])
        self.physics = ConfigNode(**self.config["physics"])

        self.fruit_names = ["one", "two", "three", "four",
                            "five", "six", "seven", "eight", 
                            "nine", "ten", "eleven"]

        background_image = pygame.image.load("blits/background.png")
        self.background_blit = pygame.transform.scale(background_image, (self.screen.width, self.screen.height))
        #self.background_blit = pygame.image.load("blits/background.png")

        self.cloud_blit = pygame.image.load("blits/cloud.png")

        for name in self.fruit_names:
            self.config[name]["blit"] = pygame.transform.scale(
                pygame.image.load(f"blits/{name}.png"),
                size=self.config[name]["size"],
            )

        self.screen_center = (self.screen.width // 2, self.screen.height // 2)

        self.start_image = pygame.image.load("blits/open.png")
        self.start_image = pygame.transform.scale(self.start_image, (self.screen.width, self.screen.height))
        self.game_over_image = pygame.image.load("blits/end.png")
        self.game_over_image = pygame.transform.scale(self.game_over_image, (self.screen.width, self.screen.height))

        self.start_button_image = pygame.image.load("blits/enter.png")
        self.start_button_image = pygame.transform.scale(self.start_button_image, (400, 100))
        self.start_button_pos = (self.screen.width // 2 - 200, self.screen.height // 2 + 150)  
        self.again_button_image = pygame.image.load("blits/again.png")
        self.again_button_image = pygame.transform.scale(self.again_button_image, (400, 100))
        self.again_button_pos = (self.screen.width // 2 - 200, self.screen.height // 2 + 150)  

        self.next_sushi_pos = (self.screen.width - 150, 50)
        self.sushi_size = (100, 100)

    def __getitem__(self, key):
        index, field = key
        fruit = self.fruit_names[index]
        return self.config[fruit][field]
    
    @property
    def top_left(self):
        return self.pad.left, self.pad.top

    @property
    def bot_left(self):
        return self.pad.left, self.pad.bot

    @property
    def top_right(self):
        return self.pad.right, self.pad.top

    @property
    def bot_right(self):
        return self.pad.right, self.pad.bot


config = Config()
