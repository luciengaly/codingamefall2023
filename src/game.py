import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import List
import random
from random import randint, uniform
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from entity import Entity
from fish import Fish, FishType
from vector import Vector
from ugly import Ugly
from drone import Drone
from collision import Collision
from closest import Closest
from scan import Scan
from player import Player
from constants import *
from agent import RandomAgent


def calculate_direction_vector(direction_index, num_directions, current_position):
    # Extract current position coordinates
    x, y = current_position

    # Calculate angle based on direction index and total directions
    angle = (360 / num_directions) * direction_index

    # Convert angle to radians
    angle_rad = math.radians(angle)

    # Calculate target position based on angle and distance (200 units)
    target_x = x + 600 * math.cos(angle_rad)
    target_y = y + 600 * math.sin(angle_rad)

    # Project the target position onto the map boundaries if out of bounds
    if target_x > 10000:
        target_x = 10000
    elif target_x < 0:
        target_x = 0

    if target_y > 10000:
        target_y = 10000
    elif target_y < 0:
        target_y = 0

    # Calculate direction vector from current position to target position
    direction_vector = (int(target_x), int(target_y))

    return direction_vector


class Game(gym.Env):
    def __init__(self):
        self.fish_colors_4_rendering = {
            "fish_1": (0.8, 0.2, 0.2),  # Rouge
            "fish_2": (0.2, 0.8, 0.2),  # Vert
            "fish_3": (0.2, 0.2, 0.8),  # Bleu
            "fish_4": (0.8, 0.8, 0.2),  # Jaune
            "fish_5": (0.8, 0.2, 0.8),  # Magenta
            "fish_6": (0.2, 0.8, 0.8),  # Cyan
            "fish_7": (0.5, 0.2, 0.8),  # Violet
            "fish_8": (0.8, 0.5, 0.2),  # Orange
            "fish_9": (0.5, 0.8, 0.2),  # Olive
            "fish_10": (0.2, 0.5, 0.8),  # Turquoise
            "fish_11": (0.8, 0.2, 0.5),  # Rose
            "fish_12": (0.2, 0.8, 0.5),  # Vert clair
        }
        self.player_colors = {
            0: (0, 0, 1),  # Bleu pour le joueur 0
            1: (1, 0, 0),  # Rouge pour le joueur 1
        }

        self.action_space = spaces.Discrete(NUM_DIRECTIONS_ACT * 2)
        self.observation_space = spaces.MultiDiscrete(
            nvec=[
                WIDTH,  # myDronePosX
                HEIGHT,  # myDronePosY
                # WIDTH,  # oppDronePosX
                # HEIGHT,  # oppDronePosY
                DRONE_MAX_BATTERY,  # myDroneBattery
                # DRONE_MAX_BATTERY,  # oppDroneBattery
                97,  # myScore
                # 97,  # oppScore
                # myFishScanned
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                # # oppFishScanned
                # 2,
                # 2,
                # 2,
                # 2,
                # 2,
                # 2,
                # 2,
                # 2,
                # 2,
                # 2,
                # 2,
                # 2,
                # 3,  # jellyPinkFirstScan
                # 3,  # fishPinkFirstScan
                # 3,  # crabPinkFirstScan
                # 3,  # jellyYellowFirstScan
                # 3,  # fishYellowFirstScan
                # 3,  # crabYellowFirstScan
                # 3,  # jellyGreenFirstScan
                # 3,  # fishGreenFirstScan
                # 3,  # crabGreenFirstScan
                # 3,  # jellyBlueFirstScan
                # 3,  # fishBlueFirstScan
                # 3,  # crabBlueFirstScan
                # 3,  # allColorOfJellyFirstScan
                # 3,  # allColorOfFishFirstScan
                # 3,  # allColorOfCrabFirstScan
                # 3,  # allTypeOfPinkFirstScan
                # 3,  # allTypeOfYellowFirstScan
                # 3,  # allTypeOfGreenFirstScan
                # 3,  # allTypeOfBlueFirstScan
                WIDTH,  # jellyPinkPosX
                HEIGHT,  # jellyPinkPosY
                # FISH_SWIM_SPEED * 2,  # jellyPinkPosVX
                # FISH_SWIM_SPEED * 2,  # jellyPinkPosVY
                WIDTH,  # fishPinkPosX
                HEIGHT,  # fishPinkPosY
                # FISH_SWIM_SPEED * 2,  # fishPinkPosVX
                # FISH_SWIM_SPEED * 2,  # fishPinkPosVY
                WIDTH,  # crabPinkPosX
                HEIGHT,  # crabPinkPosY
                # FISH_SWIM_SPEED * 2,  # crabPinkPosVX
                # FISH_SWIM_SPEED * 2,  # crabPinkPosVY
                WIDTH,  # jellyYellowPosX
                HEIGHT,  # jellyYellowPosY
                # FISH_SWIM_SPEED * 2,  # jellyYellowPosVX
                # FISH_SWIM_SPEED * 2,  # jellyYellowPosVY
                WIDTH,  # fishYellowPosX
                HEIGHT,  # fishYellowPosY
                # FISH_SWIM_SPEED * 2,  # fishYellowPosVX
                # FISH_SWIM_SPEED * 2,  # fishYellowPosVY
                WIDTH,  # crabYellowPosX
                HEIGHT,  # crabYellowPosY
                # FISH_SWIM_SPEED * 2,  # crabYellowPosVX
                # FISH_SWIM_SPEED * 2,  # crabYellowPosVY
                WIDTH,  # jellyGreenPosX
                HEIGHT,  # jellyGreenPosY
                # FISH_SWIM_SPEED * 2,  # jellyGreenPosVX
                # FISH_SWIM_SPEED * 2,  # jellyGreenPosVY
                WIDTH,  # fishGreenPosX
                HEIGHT,  # fishGreenPosY
                # FISH_SWIM_SPEED * 2,  # fishGreenPosVX
                # FISH_SWIM_SPEED * 2,  # fishGreenPosVY
                WIDTH,  # crabGreenPosX
                HEIGHT,  # crabGreenPosY
                # FISH_SWIM_SPEED * 2,  # crabGreenPosVX
                # FISH_SWIM_SPEED * 2,  # crabGreenPosVY
                WIDTH,  # jellyBluePosX
                HEIGHT,  # jellyBluePosY
                # FISH_SWIM_SPEED * 2,  # jellyBluePosVX
                # FISH_SWIM_SPEED * 2,  # jellyBluePosVY
                WIDTH,  # fishBluePosX
                HEIGHT,  # fishBluePosY
                # FISH_SWIM_SPEED * 2,  # fishBluePosVX
                # FISH_SWIM_SPEED * 2,  # fishBluePosVY
                WIDTH,  # crabBluePosX
                HEIGHT,  # crabBluePosY
                # FISH_SWIM_SPEED * 2,  # crabBluePosVX
                # FISH_SWIM_SPEED * 2,  # crabBluePosVY
            ],
            start=[
                0,  # myDronePosX
                0,  # myDronePosY
                # 0,  # oppDronePosX
                # 0,  # oppDronePosY
                0,  # myDroneBattery
                # 0,  # oppDroneBattery
                0,  # myScore
                # 0,  # oppScore
                # myFishScanned
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                # # oppFishScanned
                # 0,
                # 0,
                # 0,
                # 0,
                # 0,
                # 0,
                # 0,
                # 0,
                # 0,
                # 0,
                # 0,
                # 0,
                # 0,  # jellyPinkFirstScan
                # 0,  # fishPinkFirstScan
                # 0,  # crabPinkFirstScan
                # 0,  # jellyYellowFirstScan
                # 0,  # fishYellowFirstScan
                # 0,  # crabYellowFirstScan
                # 0,  # jellyGreenFirstScan
                # 0,  # fishGreenFirstScan
                # 0,  # crabGreenFirstScan
                # 0,  # jellyBlueFirstScan
                # 0,  # fishBlueFirstScan
                # 0,  # crabBlueFirstScan
                # 0,  # allColorOfJellyFirstScan
                # 0,  # allColorOfFishFirstScan
                # 0,  # allColorOfCrabFirstScan
                # 0,  # allTypeOfPinkFirstScan
                # 0,  # allTypeOfYellowFirstScan
                # 0,  # allTypeOfGreenFirstScan
                # 0,  # allTypeOfBlueFirstScan
                0,  # jellyPinkPosX
                0,  # jellyPinkPosY
                # -FISH_SWIM_SPEED,  # jellyPinkPosVX
                # -FISH_SWIM_SPEED,  # jellyPinkPosVY
                0,  # fishPinkPosX
                0,  # fishPinkPosY
                # -FISH_SWIM_SPEED,  # fishPinkPosVX
                # -FISH_SWIM_SPEED,  # fishPinkPosVY
                0,  # crabPinkPosX
                0,  # crabPinkPosY
                # -FISH_SWIM_SPEED,  # crabPinkPosVX
                # -FISH_SWIM_SPEED,  # crabPinkPosVY
                0,  # jellyYellowPosX
                0,  # jellyYellowPosY
                # -FISH_SWIM_SPEED,  # jellyYellowPosVX
                # -FISH_SWIM_SPEED,  # jellyYellowPosVY
                0,  # fishYellowPosX
                0,  # fishYellowPosY
                # -FISH_SWIM_SPEED,  # fishYellowPosVX
                # -FISH_SWIM_SPEED,  # fishYellowPosVY
                0,  # crabYellowPosX
                0,  # crabYellowPosY
                # -FISH_SWIM_SPEED,  # crabYellowPosVX
                # -FISH_SWIM_SPEED,  # crabYellowPosVY
                0,  # jellyGreenPosX
                0,  # jellyGreenPosY
                # -FISH_SWIM_SPEED,  # jellyGreenPosVX
                # -FISH_SWIM_SPEED,  # jellyGreenPosVY
                0,  # fishGreenPosX
                0,  # fishGreenPosY
                # -FISH_SWIM_SPEED,  # fishGreenPosVX
                # -FISH_SWIM_SPEED,  # fishGreenPosVY
                0,  # crabGreenPosX
                0,  # crabGreenPosY
                # -FISH_SWIM_SPEED,  # crabGreenPosVX
                # -FISH_SWIM_SPEED,  # crabGreenPosVY
                0,  # jellyBluePosX
                0,  # jellyBluePosY
                # -FISH_SWIM_SPEED,  # jellyBluePosVX
                # -FISH_SWIM_SPEED,  # jellyBluePosVY
                0,  # fishBluePosX
                0,  # fishBluePosY
                # -FISH_SWIM_SPEED,  # fishBluePosVX
                # -FISH_SWIM_SPEED,  # fishBluePosVY
                0,  # crabBluePosX
                0,  # crabBluePosY
                # -FISH_SWIM_SPEED,  # crabBluePosVX
                # -FISH_SWIM_SPEED,  # crabBluePosVY
            ],
        )

    def reset(self, seed=None, options=None):
        self.entity_count = 0
        self.players = []
        self.init_drones()
        self.random = None
        self.viewer_events = []
        self.game_turn = 0
        self.chased_fish_count = [0, 0]
        self.max_turns_spent_with_scan = [0, 0]
        self.max_y = [0, 0]
        self.turn_saved_fish = [[-1] * 12, [-1] * 12]
        self.times_aggroed = [0, 0]
        self.drones_eaten = 0
        self.fish_scanned = 0
        self.game_summary = []
        self.turn_summary = ""
        self.fishes_scanned_this_turn = 0
        self.points_prec_turn = 0

        self.first_to_scan = {}
        self.first_to_scan_temp = {}

        self.first_to_scan_all_fish_of_color = {}
        self.first_to_scan_all_fish_of_color_temp = {}

        self.first_to_scan_all_fish_of_type = {}
        self.first_to_scan_all_fish_of_type_temp = {}

        self.uglies: List[Ugly] = []
        self.fishes: List[Fish] = []
        self.done = False
        random.seed(seed)
        self.init_fish()
        self.init_uglies()
        for player in self.players:
            if SIMPLE_SCANS:
                player.visible_fishes = set(self.fishes)

        self.opponent = RandomAgent()

        observation = self._get_observation()
        info = self.turn_summary
        return observation
        # return observation, info

    def step(self, action):
        self.turn_summary = ""
        opp_action = self.opponent.move(self.action_space)
        actions = [action, opp_action]
        for player in self.players:
            # TODO: modifier si plusieurs drone
            for drone in player.drones:
                if actions[player.get_index()] <= NUM_DIRECTIONS_ACT:
                    dir_index = actions[player.get_index()]
                    light_switch = 0
                else:
                    dir_index = actions[player.get_index()] % NUM_DIRECTIONS_ACT
                    light_switch = 1
                vx, vy = calculate_direction_vector(
                    dir_index, NUM_DIRECTIONS_ACT, (drone.get_x(), drone.get_y())
                )
                drone.move = Vector(vx, vy)
                drone.light_switch = light_switch

        self.clear_player_info()
        self.do_batteries()
        self.update_drones()
        self.move_entities()
        self.update_ugly_targets()
        self.do_scan()
        self.do_report()
        self.upkeep_drones()
        self.update_fish()
        self.update_ugly_speeds()

        if self.is_game_over():
            self.compute_score_on_end()
            self.done = True
        else:
            self.done = False

        self.game_summary.append(self.turn_summary)
        self.game_turn += 1

        observation = self._get_observation()
        reward = self.calculate_reward()
        info = self.turn_summary

        return observation, reward, self.done, {}

    def render(self):
        fishes = [
            {
                "x": fish.get_x(),
                "y": fish.get_y(),
                "type": f"fish_{(fish.color * 3 + fish.type.value) + 1}",
            }
            for fish in self.fishes
        ]
        drones = []
        game_infos = {}
        for player in self.players:
            for drone in player.drones:
                drones.append(
                    {
                        "x": drone.get_x(),
                        "y": drone.get_y(),
                        "move": drone.move,
                        "light_switch": drone.is_light_on(),
                        "player": player.get_index(),
                    }
                )
                game_infos[player.get_index()] = {
                    "score": player.points,
                    "countFishSaved": player.count_fish_saved,
                }
        game_map = self.create_game_map()
        self.add_fish_and_players(game_map, fishes, drones)
        plt.title(
            f"turn: {self.game_turn} - myScore: {game_infos[0]['score']} - oppScore: {game_infos[1]['score']} - myFish: {sum(game_infos[0]['countFishSaved'])} - oppFish: {sum(game_infos[1]['countFishSaved'])}",
            fontsize=10,
        )
        plt.imshow(game_map)
        plt.show()
        return game_map

    def normalize_position(self, pos):
        return pos // 100

    def add_fish_and_players(self, game_map, fishes, drones):
        for fish in fishes:
            x, y = self.normalize_position(fish["x"]), self.normalize_position(
                fish["y"]
            )
            color = (
                self.fish_colors_4_rendering[fish["type"]]
                if fish["type"] in self.fish_colors_4_rendering
                else (0, 0, 0)
            )
            game_map[y, x] = np.array(color) * 255

        for drone in drones:
            x, y = self.normalize_position(drone["x"]), self.normalize_position(
                drone["y"]
            )
            color = (
                self.player_colors[drone["player"]]
                if drone["player"] in self.player_colors
                else (1, 1, 1)
            )
            game_map[y, x] = np.array(color) * 255
            if drone["light_switch"]:
                radius = 20
            else:
                radius = 8
            circle = Circle(
                (x, y),
                radius=radius,
                color=color,
                fill=False,
            )
            plt.gca().add_patch(circle)

    def create_game_map(self):
        game_map = np.ones((100, 100, 3), dtype=np.uint8) * 255
        return game_map

    def _get_observation(self):
        observation = np.zeros(self.observation_space.shape)
        for player in self.players:
            if player.get_index() == 0:
                for drone in player.drones:
                    observation[0] = drone.get_x()
                    observation[1] = drone.get_y()
                    observation[2] = drone.battery
                observation[3] = player.points
                observation[4] = 0
                observation[5] = 0
                observation[6] = 0
                observation[7] = 0
                observation[8] = 0
                observation[9] = 0
                observation[10] = 0
                observation[11] = 0
                observation[12] = 0
                observation[13] = 0
                observation[14] = 0
                observation[15] = 0
                for scan in player.scans:
                    fish_index = scan.color * 3 + scan.type.value
                    observation[8 + fish_index] += 1

        for fish in self.fishes:
            if fish.type.value == 0 and fish.color == 0:
                (
                    observation[16],
                    observation[17],
                    _,
                    _,
                ) = fish.get_obs()
            if fish.type.value == 1 and fish.color == 0:
                (
                    observation[18],
                    observation[19],
                    _,
                    _,
                ) = fish.get_obs()
            if fish.type.value == 2 and fish.color == 0:
                (
                    observation[20],
                    observation[21],
                    _,
                    _,
                ) = fish.get_obs()
            if fish.type.value == 0 and fish.color == 1:
                (
                    observation[22],
                    observation[23],
                    _,
                    _,
                ) = fish.get_obs()
            if fish.type.value == 1 and fish.color == 1:
                (
                    observation[24],
                    observation[25],
                    _,
                    _,
                ) = fish.get_obs()
            if fish.type.value == 2 and fish.color == 1:
                (
                    observation[26],
                    observation[27],
                    _,
                    _,
                ) = fish.get_obs()
            if fish.type.value == 0 and fish.color == 2:
                (
                    observation[28],
                    observation[29],
                    _,
                    _,
                ) = fish.get_obs()
            if fish.type.value == 1 and fish.color == 2:
                (
                    observation[30],
                    observation[31],
                    _,
                    _,
                ) = fish.get_obs()
            if fish.type.value == 2 and fish.color == 2:
                (
                    observation[32],
                    observation[33],
                    _,
                    _,
                ) = fish.get_obs()
            if fish.type.value == 0 and fish.color == 3:
                (
                    observation[34],
                    observation[35],
                    _,
                    _,
                ) = fish.get_obs()
            if fish.type.value == 1 and fish.color == 3:
                (
                    observation[36],
                    observation[37],
                    _,
                    _,
                ) = fish.get_obs()
            if fish.type.value == 2 and fish.color == 3:
                (
                    observation[38],
                    observation[39],
                    _,
                    _,
                ) = fish.get_obs()

        return observation
    
    # def _get_observation(self):
    #     observation = np.zeros(self.observation_space.shape)
    #     for player in self.players:
    #         if player.get_index() == 0:
    #             for drone in player.drones:
    #                 observation[0] = drone.get_x()
    #                 observation[1] = drone.get_y()
    #                 observation[4] = drone.battery
    #             observation[6] = player.points
    #             observation[8] = 0
    #             observation[9] = 0
    #             observation[10] = 0
    #             observation[11] = 0
    #             observation[12] = 0
    #             observation[13] = 0
    #             observation[14] = 0
    #             observation[15] = 0
    #             observation[16] = 0
    #             observation[17] = 0
    #             observation[18] = 0
    #             observation[19] = 0
    #             for scan in player.scans:
    #                 fish_index = scan.color * 3 + scan.type.value
    #                 observation[8 + fish_index] += 1
    #         elif player.get_index() == 1:
    #             for drone in player.drones:
    #                 observation[2] = drone.get_x()
    #                 observation[3] = drone.get_y()
    #                 observation[5] = drone.battery
    #             observation[7] = player.points
    #             observation[20] = 0
    #             observation[21] = 0
    #             observation[22] = 0
    #             observation[23] = 0
    #             observation[24] = 0
    #             observation[25] = 0
    #             observation[26] = 0
    #             observation[27] = 0
    #             observation[28] = 0
    #             observation[29] = 0
    #             observation[30] = 0
    #             observation[31] = 0
    #             for scan in player.scans:
    #                 fish_index = scan.color * 3 + scan.type.value
    #                 observation[20 + fish_index] += 1
    #     observation[32] = 2
    #     observation[33] = 2
    #     observation[34] = 2
    #     observation[35] = 2
    #     observation[36] = 2
    #     observation[37] = 2
    #     observation[38] = 2
    #     observation[39] = 2
    #     observation[40] = 2
    #     observation[41] = 2
    #     observation[42] = 2
    #     observation[43] = 2
    #     for scan, player_id in self.first_to_scan.items():
    #         if scan.type.value == 0 and scan.color == 0:
    #             observation[32] = player_id
    #         elif scan.type.value == 1 and scan.color == 0:
    #             observation[33] = player_id
    #         elif scan.type.value == 2 and scan.color == 0:
    #             observation[34] = player_id
    #         elif scan.type.value == 0 and scan.color == 1:
    #             observation[35] = player_id
    #         elif scan.type.value == 1 and scan.color == 1:
    #             observation[36] = player_id
    #         elif scan.type.value == 2 and scan.color == 1:
    #             observation[37] = player_id
    #         elif scan.type.value == 0 and scan.color == 2:
    #             observation[38] = player_id
    #         elif scan.type.value == 1 and scan.color == 2:
    #             observation[39] = player_id
    #         elif scan.type.value == 2 and scan.color == 2:
    #             observation[40] = player_id
    #         elif scan.type.value == 0 and scan.color == 3:
    #             observation[41] = player_id
    #         elif scan.type.value == 1 and scan.color == 3:
    #             observation[42] = player_id
    #         elif scan.type.value == 2 and scan.color == 3:
    #             observation[43] = player_id
    #         else:
    #             raise RuntimeError("Unknown scan.type.value or scan.color")

    #     for _type, player_id in self.first_to_scan_all_fish_of_type.items():
    #         if _type.value == 0:
    #             observation[44] = player_id
    #         elif _type.value == 1:
    #             observation[45] = player_id
    #         elif _type.value == 2:
    #             observation[46] = player_id
    #         else:
    #             raise RuntimeError("Unknown _type.value")

    #     for color, player_id in self.first_to_scan_all_fish_of_color.items():
    #         if color == 0:
    #             observation[47] = player_id
    #         elif color == 1:
    #             observation[48] = player_id
    #         elif color == 2:
    #             observation[49] = player_id
    #         elif color == 3:
    #             observation[50] = player_id
    #         else:
    #             raise RuntimeError("Unknown color")

    #     for fish in self.fishes:
    #         if fish.type.value == 0 and fish.color == 0:
    #             (
    #                 observation[51],
    #                 observation[52],
    #                 observation[53],
    #                 observation[54],
    #             ) = fish.get_obs()
    #         if fish.type.value == 1 and fish.color == 0:
    #             (
    #                 observation[55],
    #                 observation[56],
    #                 observation[57],
    #                 observation[58],
    #             ) = fish.get_obs()
    #         if fish.type.value == 2 and fish.color == 0:
    #             (
    #                 observation[59],
    #                 observation[60],
    #                 observation[61],
    #                 observation[62],
    #             ) = fish.get_obs()
    #         if fish.type.value == 0 and fish.color == 1:
    #             (
    #                 observation[63],
    #                 observation[64],
    #                 observation[65],
    #                 observation[66],
    #             ) = fish.get_obs()
    #         if fish.type.value == 1 and fish.color == 1:
    #             (
    #                 observation[67],
    #                 observation[68],
    #                 observation[69],
    #                 observation[70],
    #             ) = fish.get_obs()
    #         if fish.type.value == 2 and fish.color == 1:
    #             (
    #                 observation[71],
    #                 observation[72],
    #                 observation[73],
    #                 observation[74],
    #             ) = fish.get_obs()
    #         if fish.type.value == 0 and fish.color == 2:
    #             (
    #                 observation[75],
    #                 observation[76],
    #                 observation[77],
    #                 observation[78],
    #             ) = fish.get_obs()
    #         if fish.type.value == 1 and fish.color == 2:
    #             (
    #                 observation[79],
    #                 observation[80],
    #                 observation[81],
    #                 observation[82],
    #             ) = fish.get_obs()
    #         if fish.type.value == 2 and fish.color == 2:
    #             (
    #                 observation[83],
    #                 observation[84],
    #                 observation[85],
    #                 observation[86],
    #             ) = fish.get_obs()
    #         if fish.type.value == 0 and fish.color == 3:
    #             (
    #                 observation[87],
    #                 observation[88],
    #                 observation[89],
    #                 observation[90],
    #             ) = fish.get_obs()
    #         if fish.type.value == 1 and fish.color == 3:
    #             (
    #                 observation[91],
    #                 observation[92],
    #                 observation[93],
    #                 observation[94],
    #             ) = fish.get_obs()
    #         if fish.type.value == 2 and fish.color == 3:
    #             (
    #                 observation[95],
    #                 observation[96],
    #                 observation[97],
    #                 observation[98],
    #             ) = fish.get_obs()

    #     return observation

    def old_get_observation(self):
        observation = {}
        for player in self.players:
            if player.get_index() == 0:
                for drone in player.drones:
                    observation["myDronePosX"] = drone.get_x()
                    observation["myDronePosY"] = drone.get_y()
                    observation["myDroneBattery"] = drone.battery
                observation["myScore"] = player.points
                myFishScanned = np.zeros(12, dtype=np.int8)
                for scan in player.scans:
                    fish_index = scan.color * 3 + scan.type.value
                    myFishScanned[fish_index] += 1
                observation["myFishScanned"] = myFishScanned
            elif player.get_index() == 1:
                for drone in player.drones:
                    observation["oppDronePosX"] = drone.get_x()
                    observation["oppDronePosY"] = drone.get_y()
                    observation["oppDroneBattery"] = drone.battery
                observation["oppScore"] = player.points
                myFishScanned = np.zeros(12, dtype=np.int8)
                for scan in player.scans:
                    fish_index = scan.color * 3 + scan.type.value
                    myFishScanned[fish_index] += 1
                observation["oppFishScanned"] = myFishScanned
        observation["jellyPinkFirstScan"] = -1
        observation["fishPinkFirstScan"] = -1
        observation["crabPinkFirstScan"] = -1
        observation["jellyYellowFirstScan"] = -1
        observation["fishYellowFirstScan"] = -1
        observation["crabYellowFirstScan"] = -1
        observation["jellyGreenFirstScan"] = -1
        observation["fishGreenFirstScan"] = -1
        observation["crabGreenFirstScan"] = -1
        observation["jellyBlueFirstScan"] = -1
        observation["fishBlueFirstScan"] = -1
        observation["crabBlueFirstScan"] = -1
        for scan, player_id in self.first_to_scan.items():
            if scan.type.value == 0 and scan.color == 0:
                observation["jellyPinkFirstScan"] = player_id
            elif scan.type.value == 1 and scan.color == 0:
                observation["fishPinkFirstScan"] = player_id
            elif scan.type.value == 2 and scan.color == 0:
                observation["crabPinkFirstScan"] = player_id
            elif scan.type.value == 0 and scan.color == 1:
                observation["jellyYellowFirstScan"] = player_id
            elif scan.type.value == 1 and scan.color == 1:
                observation["fishYellowFirstScan"] = player_id
            elif scan.type.value == 2 and scan.color == 1:
                observation["crabYellowFirstScan"] = player_id
            elif scan.type.value == 0 and scan.color == 2:
                observation["jellyGreenFirstScan"] = player_id
            elif scan.type.value == 1 and scan.color == 2:
                observation["fishGreenFirstScan"] = player_id
            elif scan.type.value == 2 and scan.color == 2:
                observation["crabGreenFirstScan"] = player_id
            elif scan.type.value == 0 and scan.color == 3:
                observation["jellyBlueFirstScan"] = player_id
            elif scan.type.value == 1 and scan.color == 3:
                observation["fishBlueFirstScan"] = player_id
            elif scan.type.value == 2 and scan.color == 3:
                observation["crabBlueFirstScan"] = player_id
            else:
                raise RuntimeError("Unknown scan.type.value or scan.color")

        for _type, player_id in self.first_to_scan_all_fish_of_type.items():
            if _type.value == 0:
                observation["allColorOfJellyFirstScan"] = player_id
            elif _type.value == 1:
                observation["allColorOfFishFirstScan"] = player_id
            elif _type.value == 2:
                observation["allColorOfCrabFirstScan"] = player_id
            else:
                raise RuntimeError("Unknown _type.value")

        for color, player_id in self.first_to_scan_all_fish_of_color.items():
            if color == 0:
                observation["allTypeOfPinkFirstScan"] = player_id
            elif color == 1:
                observation["allTypeOfYellowFirstScan"] = player_id
            elif color == 2:
                observation["allTypeOfGreenFirstScan"] = player_id
            elif color == 3:
                observation["allTypeOfBlueFirstScan"] = player_id
            else:
                raise RuntimeError("Unknown color")

        for fish in self.fishes:
            if fish.type.value == 0 and fish.color == 0:
                (
                    observation["jellyPinkPosX"],
                    observation["jellyPinkPosY"],
                    observation["jellyPinkPosVX"],
                    observation["jellyPinkPosVY"],
                ) = fish.get_obs()
            if fish.type.value == 1 and fish.color == 0:
                (
                    observation["fishPinkPosX"],
                    observation["fishPinkPosY"],
                    observation["fishPinkPosVX"],
                    observation["fishPinkPosVY"],
                ) = fish.get_obs()
            if fish.type.value == 2 and fish.color == 0:
                (
                    observation["crabPinkPosX"],
                    observation["crabPinkPosY"],
                    observation["crabPinkPosVX"],
                    observation["crabPinkPosVY"],
                ) = fish.get_obs()
            if fish.type.value == 0 and fish.color == 1:
                (
                    observation["jellyYellowPosX"],
                    observation["jellyYellowPosY"],
                    observation["jellyYellowPosVX"],
                    observation["jellyYellowPosVY"],
                ) = fish.get_obs()
            if fish.type.value == 1 and fish.color == 1:
                (
                    observation["fishYellowPosX"],
                    observation["fishYellowPosY"],
                    observation["fishYellowPosVX"],
                    observation["fishYellowPosVY"],
                ) = fish.get_obs()
            if fish.type.value == 2 and fish.color == 1:
                (
                    observation["crabYellowPosX"],
                    observation["crabYellowPosY"],
                    observation["crabYellowPosVX"],
                    observation["crabYellowPosVY"],
                ) = fish.get_obs()
            if fish.type.value == 0 and fish.color == 2:
                (
                    observation["jellyGreenPosX"],
                    observation["jellyGreenPosY"],
                    observation["jellyGreenPosVX"],
                    observation["jellyGreenPosVY"],
                ) = fish.get_obs()
            if fish.type.value == 1 and fish.color == 2:
                (
                    observation["fishGreenPosX"],
                    observation["fishGreenPosY"],
                    observation["fishGreenPosVX"],
                    observation["fishGreenPosVY"],
                ) = fish.get_obs()
            if fish.type.value == 2 and fish.color == 2:
                (
                    observation["crabGreenPosX"],
                    observation["crabGreenPosY"],
                    observation["crabGreenPosVX"],
                    observation["crabGreenPosVY"],
                ) = fish.get_obs()
            if fish.type.value == 0 and fish.color == 3:
                (
                    observation["jellyBluePosX"],
                    observation["jellyBluePosY"],
                    observation["jellyBluePosVX"],
                    observation["jellyBluePosVY"],
                ) = fish.get_obs()
            if fish.type.value == 1 and fish.color == 3:
                (
                    observation["fishBluePosX"],
                    observation["fishBluePosY"],
                    observation["fishBluePosVX"],
                    observation["fishBluePosVY"],
                ) = fish.get_obs()
            if fish.type.value == 2 and fish.color == 3:
                (
                    observation["crabBluePosX"],
                    observation["crabBluePosY"],
                    observation["crabBluePosVX"],
                    observation["crabBluePosVY"],
                ) = fish.get_obs()

        return observation

    def calculate_reward(self):
        reward = 0
        for player in self.players:
            if player.get_index() == 0:
                if player.points > self.points_prec_turn:
                    reward = player.points - self.points_prec_turn
                    self.points_prec_turn += reward
                else:
                    reward = -1
        # if self.done:
        #     if self.players[0].points > self.players[1].points:
        #         reward += 1000
        #     elif self.players[0].points < self.players[1].points:
        #         reward -= 1000
        #     else:
        #         reward -= reward
        # else:
        #     # reward = self.players[0].points - self.players[1].points
        #     for player in self.players:
        #         for drone in player.drones:
        #             if player.get_index() == 0:
        #                 if self.fishes_scanned_this_turn < len(
        #                     drone.fishes_scanned_this_turn
        #                 ):
        #                     reward = (
        #                         len(drone.fishes_scanned_this_turn)
        #                         - self.fishes_scanned_this_turn
        #                     )
        #                     self.fishes_scanned_this_turn += reward

        return reward

    def init_fish(self):
        self.fishes = []

        for col in range(0, COLORS_PER_FISH, 2):
            for type_idx in range(len(FishType)):
                position_found = False
                iterations = 0

                low_y = HEIGHT // 4 * (type_idx + 1)
                high_y = HEIGHT

                while not position_found:
                    x = randint(
                        FISH_X_SPAWN_LIMIT,
                        WIDTH - FISH_X_SPAWN_LIMIT * 2,
                    )
                    if type_idx == 0:
                        y = HEIGHT // 4 + FISH_SPAWN_MIN_SEP
                        low_y = HEIGHT // 4
                        high_y = HEIGHT // 2
                    elif type_idx == 1:
                        y = HEIGHT // 2 + FISH_SPAWN_MIN_SEP
                        low_y = HEIGHT // 2
                        high_y = 3 * HEIGHT // 4
                    else:
                        y = 3 * HEIGHT // 4 + FISH_SPAWN_MIN_SEP
                        low_y = 3 * HEIGHT // 4
                        high_y = HEIGHT
                    y += randint(0, HEIGHT // 4 - FISH_SPAWN_MIN_SEP * 2)

                    too_close = any(
                        other.get_pos().in_range(Vector(x, y), FISH_SPAWN_MIN_SEP)
                        for other in self.fishes
                    )
                    too_close_to_center = abs(CENTER.get_x() - x) <= FISH_SPAWN_MIN_SEP
                    if not too_close and not too_close_to_center or iterations > 100:
                        position_found = True
                    iterations += 1

                f = Fish(
                    int(x),
                    int(y),
                    FishType(type_idx),
                    col,
                    self.entity_count,
                    low_y,
                    high_y,
                )
                self.entity_count += 1

                snapped = uniform(0, 7) * 3.14159 / 4
                direction = Vector(
                    round(math.cos(snapped), 2), round(math.sin(snapped), 2)
                )

                if FISH_WILL_MOVE:
                    f.speed = direction.mult(FISH_SWIM_SPEED).round()

                self.fishes.append(f)

                other_pos = f.pos.hsymmetric(CENTER.get_x())
                o = Fish(
                    int(other_pos.get_x()),
                    int(other_pos.get_y()),
                    FishType(type_idx),
                    col + 1,
                    self.entity_count,
                    f.low_y,
                    f.high_y,
                )
                self.entity_count += 1
                o.speed = f.speed.hsymmetric()
                self.fishes.append(o)

    def init_uglies(self) -> None:
        uglies = []

        ugly_count = 1 + randint(0, 2) if ENABLE_UGLIES else 0

        for _ in range(ugly_count):
            x = randint(0, WIDTH // 2)
            y = HEIGHT // 2 + randint(0, HEIGHT // 2)

            for k in range(2):
                ugly = Ugly(x, y, self.entity_count)
                if k == 1:
                    ugly.pos = ugly.pos.hsymmetric(CENTER.get_x())

                uglies.append(ugly)
                self.entity_count += 1

        self.uglies = uglies

    def init_drones(self):
        idxs = [0, 2, 1, 3]
        idx_idx = 0

        for i in range(DRONES_PER_PLAYER):
            x = int(WIDTH / (DRONES_PER_PLAYER * 2 + 1) * (idxs[idx_idx] + 1))
            idx_idx += 1

            self.get_active_players()
            for player in self.players:
                d = Drone(x, DRONE_START_Y, self.entity_count, player)
                self.entity_count += 1

                if player.get_index() == 1:
                    d.pos = d.pos.hsymmetric(CENTER.get_x())

                player.drones.append(d)

    def get_active_players(self):
        for j in range(NUMBER_OF_PLAYER):
            self.players.append(Player(j))

    def get_collision(self, drone: Drone, ugly: Ugly) -> Collision:
        if ugly.get_pos().in_range(drone.get_pos(), DRONE_HIT_RANGE + UGLY_EAT_RANGE):
            return Collision(0.0, ugly, drone)

        if drone.get_speed().is_zero() and ugly.get_speed().is_zero():
            return Collision.NONE

        x = ugly.get_x()
        y = ugly.get_y()
        ux = drone.get_x()
        uy = drone.get_y()

        x2 = x - ux
        y2 = y - uy
        r2 = UGLY_EAT_RANGE + DRONE_HIT_RANGE
        vx2 = ugly.get_speed().get_x() - drone.get_speed().get_x()
        vy2 = ugly.get_speed().get_y() - drone.get_speed().get_y()

        a = vx2 * vx2 + vy2 * vy2

        if a <= 0.0:
            return Collision.NONE

        b = 2.0 * (x2 * vx2 + y2 * vy2)
        c = x2 * x2 + y2 * y2 - r2 * r2
        delta = b * b - 4.0 * a * c

        if delta < 0.0:
            return Collision.NONE

        t = (-b - delta**0.5) / (2.0 * a)

        if t <= 0.0 or t > 1.0:
            return Collision.NONE

        return Collision(t, ugly, drone)

    def update_ugly_speeds(self):
        for ugly in self.uglies:
            target = ugly.target
            if target:
                attack_vec = Vector(ugly.pos, target)
                if attack_vec.length() > UGLY_ATTACK_SPEED:
                    attack_vec = attack_vec.normalize().mult(UGLY_ATTACK_SPEED)
                ugly.speed = attack_vec.round()
            else:
                if ugly.speed.length() > UGLY_SEARCH_SPEED:
                    ugly.speed = ugly.speed.normalize().mult(UGLY_SEARCH_SPEED).round()

                if not ugly.speed.is_zero():
                    closest_uglies = self.get_closest_to(
                        ugly.pos, [u for u in self.uglies if u != ugly]
                    )
                    if closest_uglies and closest_uglies.distance <= FISH_AVOID_RANGE:
                        avoid = closest_uglies.get_mean_pos()
                        avoid_dir = Vector(avoid, ugly.pos).normalize()
                        if not avoid_dir.is_zero():
                            ugly.speed = avoid_dir.mult(FISH_SWIM_SPEED).round()

                next_pos = ugly.pos.add(ugly.speed)

                if (
                    next_pos.get_x() < 0
                    and next_pos.get_x() < ugly.pos.get_x()
                    or next_pos.get_x() > WIDTH - 1
                    and next_pos.get_x() > ugly.pos.get_x()
                ):
                    ugly.speed = ugly.speed.hsymmetric()

                if (
                    next_pos.get_y() < UGLY_UPPER_Y_LIMIT
                    and next_pos.get_y() < ugly.pos.get_y()
                    or next_pos.get_y() > HEIGHT - 1
                    and next_pos.get_y() > ugly.pos.get_y()
                ):
                    ugly.speed = ugly.speed.vsymmetric()

    def get_closest_to(
        self, from_vector: Vector, target_entities: List[Entity]
    ) -> Closest:
        closests = []
        min_dist = 0

        for entity in target_entities:
            dist = entity.get_pos().sqr_euclidean_to(from_vector)
            if not closests or dist < min_dist:
                closests.clear()
                closests.append(entity)
                min_dist = dist
            elif dist == min_dist:
                closests.append(entity)

        return Closest(closests, math.sqrt(min_dist))

    def do_batteries(self):
        for player in self.players:
            for drone in player.drones:
                if drone.dead:
                    drone.light_on = False
                    continue

                if (
                    drone.light_switch
                    and drone.battery >= LIGHT_BATTERY_COST
                    and not drone.dead
                ):
                    drone.light_on = True
                else:
                    if drone.light_switch and not drone.dead:
                        self.turn_summary += f"{player.get_nickname_token()}'s drone {drone.id} does not have enough battery to activate light\n"
                    drone.light_on = False

                if drone.is_light_on():
                    drone.drain_battery()
                else:
                    drone.recharge_battery()

    def do_scan(self):
        for player in self.players:
            for drone in player.drones:
                if drone.is_dead_or_dying():
                    continue

                scannable_fish = [
                    fish
                    for fish in self.fishes
                    if fish.pos.in_range(
                        drone.pos,
                        LIGHT_SCAN_RANGE if drone.is_light_on() else DARK_SCAN_RANGE,
                    )
                ]

                for fish in scannable_fish:
                    player.visible_fishes.add(fish)

                    if len(drone.scans) < DRONE_MAX_SCANS:
                        scan = Scan(fish)
                        if scan not in player.scans:
                            if scan not in drone.scans:
                                drone.scans.append(scan)
                                drone.fishes_scanned_this_turn.append(fish.id)

                if SIMPLE_SCANS:
                    player.visible_fishes = set(self.fishes)

                if len(drone.fishes_scanned_this_turn) > 0:
                    summary_scan = ", ".join(map(str, drone.fishes_scanned_this_turn))
                    if len(drone.fishes_scanned_this_turn) == 1:
                        self.turn_summary += f"{player.get_nickname_token()}'s drone {drone.id} scans fish {drone.fishes_scanned_this_turn[0]}\n"
                    else:
                        self.turn_summary += f"{player.get_nickname_token()}'s drone {drone.id} scans {len(drone.fishes_scanned_this_turn)} fish: {summary_scan}\n"

    def apply_scans_for_report(self, player, drone):
        points_scored = False
        for scan in drone.scans:
            if scan not in self.first_to_scan:
                if scan in self.first_to_scan_temp:
                    self.first_to_scan_temp.pop(scan)
                else:
                    self.first_to_scan_temp[scan] = player.get_index()

            fish_index = scan.color * 3 + scan.type.value
            self.turn_saved_fish[player.get_index()][fish_index] = self.game_turn
            self.fish_scanned += 1

        if len(drone.scans) > 0:
            player.count_fish_saved.append(len(drone.scans))

        if player.scans != (player.scans | set(drone.scans)):
            player.scans |= set(drone.scans)
            points_scored = True

        for other in player.drones:
            if drone != other:
                other.scans = list(set(other.scans) - set(drone.scans))

        drone.scans.clear()
        return points_scored

    def update_ugly_target(self, ugly):
        targetable_drones = []
        for player in self.players:
            for drone in player.drones:
                if (
                    drone.pos.in_range(
                        ugly.pos,
                        LIGHT_SCAN_RANGE if drone.is_light_on() else DARK_SCAN_RANGE,
                    )
                    and not drone.is_dead_or_dying()
                ):
                    targetable_drones.append(drone)

        if targetable_drones:
            closest_targets = self.get_closest_to(ugly.pos, targetable_drones)
            mean_pos = closest_targets.get_mean_pos()
            for d in closest_targets.entities:
                self.times_aggroed[d.owner.get_index()] += 1
                mean_pos += d.pos

            mean_pos /= len(closest_targets.entities)
            ugly.target = mean_pos
            return True

        ugly.target = None
        return False

    def update_ugly_targets(self):
        for ugly in self.uglies:
            found_target = self.update_ugly_target(ugly)
            ugly.found_target = found_target

    def clear_player_info(self):
        for player in self.players:
            player.visible_fishes.clear()

    def update_drones(self):
        for player in self.players:
            for drone in player.drones:
                move_speed = (
                    DRONE_MOVE_SPEED
                    - DRONE_MOVE_SPEED
                    * DRONE_MOVE_SPEED_LOSS_PER_SCAN
                    * len(drone.scans)
                )
                if drone.dead:
                    float_vec = Vector(0, -1) * DRONE_EMERGENCY_SPEED
                    drone.speed = float_vec
                elif drone.move is not None:
                    move_vec = Vector(drone.pos, drone.move)
                    if move_vec.length() > move_speed:
                        move_vec = move_vec.normalize().mult(move_speed)
                    drone.speed = move_vec.round()
                elif drone.get_x() < HEIGHT - 1:
                    sink_vec = Vector(0, 1) * DRONE_SINK_SPEED
                    drone.speed = sink_vec

    def do_report(self):
        for player in self.players:
            points_scored = False
            for drone in player.drones:
                if drone.is_dead_or_dying():
                    continue
                if SIMPLE_SCANS or (drone.scans and drone.get_y() <= DRONE_START_Y):
                    drone_scored = self.apply_scans_for_report(player, drone)
                    points_scored |= drone_scored
                    if drone_scored:
                        drone.did_report = True

            if points_scored:
                self.turn_summary += (
                    f"{player.get_nickname_token()} reports their findings.\n"
                )

            self.detect_first_to_combo_bonuses(player)

        self.persist_first_to_scan_bonuses()
        for player in self.players:
            player.points = self.compute_player_score(player)

    def upkeep_drones(self):
        for player in self.players:
            for drone in player.drones:
                if drone.dying:
                    drone.dead = True
                    drone.dying = False
                elif drone.dead and drone.get_y() == DRONE_UPPER_Y_LIMIT:
                    drone.dead = False

                # Stats
                if not drone.scans:
                    drone.turns_spent_with_scan = 0
                else:
                    drone.turns_spent_with_scan += 1
                    if drone.turns_spent_with_scan > drone.max_turns_spent_with_scan:
                        drone.max_turns_spent_with_scan = drone.turns_spent_with_scan

                if drone.get_y() > drone.max_y:
                    drone.max_y = drone.get_y()

    def update_fish(self):
        for fish in self.fishes:
            fish.is_fleeing = False
            flee_from = None

            if FISH_WILL_FLEE:
                closest_drones = self.get_closest_to(
                    fish.pos,
                    [
                        d
                        for p in self.players
                        for d in p.drones
                        if d.is_engine_on and not d.dead
                    ],
                )

                if (
                    closest_drones.entities
                    and closest_drones.distance <= FISH_HEARING_RANGE
                ):
                    flee_from = closest_drones.get_mean_pos()
                    fleeing_from_player = None

                    for d in closest_drones.entities:
                        idx = d.owner.get_index()
                        if fleeing_from_player is None or fleeing_from_player == idx:
                            fleeing_from_player = idx
                        else:
                            fleeing_from_player = -1

                    fish.fleeing_from_player = fleeing_from_player

            if flee_from:
                flee_dir = Vector(flee_from, fish.pos).normalize()
                flee_vec = flee_dir.mult(self.FISH_FLEE_SPEED)
                fish.speed = flee_vec.round()
                fish.is_fleeing = True
            else:
                closest_fishes = self.get_closest_to(
                    fish.pos, [f for f in self.fishes if f != fish]
                )

                swim_vec = fish.speed.normalize().mult(FISH_SWIM_SPEED)

                if (
                    closest_fishes.entities
                    and closest_fishes.distance <= FISH_AVOID_RANGE
                ):
                    avoid = closest_fishes.get_mean_pos()
                    avoid_dir = Vector(avoid, fish.pos).normalize()
                    swim_vec = avoid_dir.mult(FISH_SWIM_SPEED)

                next_pos = fish.pos.add(swim_vec)

                if next_pos.get_x() < 0 or next_pos.get_x() > WIDTH - 1:
                    swim_vec = swim_vec.hsymmetric()

                y_highest = min(HEIGHT - 1, fish.high_y)

                if next_pos.get_y() < fish.low_y or next_pos.get_y() > y_highest:
                    swim_vec = swim_vec.vsymmetric()

                fish.speed = swim_vec.epsilon_round().round()

    def snap_to_ugly_zone(self, ugly: Ugly):
        if ugly.get_y() > HEIGHT - 1:
            ugly.pos = Vector(ugly.get_x(), HEIGHT - 1)
        elif ugly.get_y() < UGLY_UPPER_Y_LIMIT:
            ugly.pos = Vector(ugly.get_x(), UGLY_UPPER_Y_LIMIT)

    def snap_to_fish_zone(self, fish: Fish):
        if fish.get_y() > HEIGHT - 1:
            fish.pos = Vector(fish.get_x(), HEIGHT - 1)
        elif fish.get_y() > fish.high_y:
            fish.pos = Vector(fish.get_x(), fish.high_y)
        elif fish.get_y() < fish.low_y:
            fish.pos = Vector(fish.get_x(), fish.low_y)

    def snap_to_drone_zone(self, drone: Drone):
        if drone.get_y() > HEIGHT - 1:
            drone.pos = Vector(drone.get_x(), HEIGHT - 1)
        elif drone.get_y() < DRONE_UPPER_Y_LIMIT:
            drone.pos = Vector(drone.get_x(), DRONE_UPPER_Y_LIMIT)

        if drone.get_x() < 0:
            drone.pos = Vector(0, drone.get_y())
        elif drone.get_x() >= WIDTH:
            drone.pos = Vector(WIDTH - 1, drone.get_y())

    def player_scanned(self, player: Player, fish: Fish):
        scan = Scan(fish)
        return self.player_scanned_with_scan(player, scan)

    def player_scanned_with_scan(self, player: Player, scan: Scan):
        return scan in player.scans

    def has_scanned_all_remaining_fish(self, player: Player):
        for fish in self.fishes:
            if not self.player_scanned(player, fish):
                return False
        return True

    def player_scanned_all_fish_of_type(self, player: Player, fish_type: FishType):
        for color in range(COLORS_PER_FISH):
            if not self.player_scanned_with_scan(
                player, Scan({"type": fish_type, "color": color})
            ):
                return False
        return True

    def player_scanned_all_fish_of_color(self, player: Player, color: int):
        for fish_type in FishType:
            if not self.player_scanned_with_scan(
                player, Scan({"type": fish_type, "color": color})
            ):
                return False
        return True

    def both_players_have_scanned_all_remaining_fish(self):
        for player in self.players:
            if not self.has_scanned_all_remaining_fish(player):
                return False
        return True

    def compute_max_player_score(self, player: Player):
        total = self.compute_player_score(player)
        p2 = self.players[1 - player.get_index()]

        for color in range(COLORS_PER_FISH):
            for type in FishType:
                scan = Scan({"type": type, "color": color})
                if not self.player_scanned_with_scan(player, scan):
                    if self.is_fish_scanned_by_player_drone(
                        scan, player
                    ) or not self.has_fish_escaped(scan):
                        total += type.value + 1
                        if self.first_to_scan.get(scan, -1) == -1:
                            total += type.value + 1

        for type in FishType:
            if self.is_type_combo_still_possible(player, type):
                total += COLORS_PER_FISH
                if self.first_to_scan_all_fish_of_type.get(type) != p2.get_index():
                    total += COLORS_PER_FISH

        for color in range(COLORS_PER_FISH):
            if self.is_color_combo_still_possible(player, color):
                total += len(FishType)
                if self.first_to_scan_all_fish_of_color.get(color) != p2.get_index():
                    total += len(FishType)

        return total

    def is_fish_scanned_by_player_drone(self, scan: Scan, player: Player):
        for drone in player.drones:
            for drone_scan in drone.scans:
                if drone_scan == scan:
                    return True
        return False

    def has_fish_escaped(self, scan: Scan):
        for fish in self.fishes:
            if fish.color == scan.color and fish.type == scan.type:
                return False
        return True

    def is_type_combo_still_possible(self, player: Player, fish_type: FishType):
        if self.player_scanned_all_fish_of_type(player, fish_type):
            return False
        for color in range(COLORS_PER_FISH):
            scan = Scan({"type": fish_type, "color": color})
            if (
                self.has_fish_escaped(scan)
                and not self.is_fish_scanned_by_player_drone(scan, player)
                and not self.player_scanned_with_scan(player, scan)
            ):
                return False
        return True

    def is_color_combo_still_possible(self, player: Player, color: int):
        if self.player_scanned_all_fish_of_color(player, color):
            return False
        for fish_type in FishType:
            scan = Scan({"type": fish_type, "color": color})
            if (
                self.has_fish_escaped(scan)
                and not self.is_fish_scanned_by_player_drone(scan, player)
                and not self.player_scanned_with_scan(player, scan)
            ):
                return False
        return True

    def compute_player_score(self, player: Player):
        total = 0

        for scan in player.scans:
            total += scan.type.value + 1
            if self.first_to_scan.get(scan) == player.get_index():
                total += scan.type.value + 1

        for fish_type in FishType:
            if self.player_scanned_all_fish_of_type(player, fish_type):
                total += COLORS_PER_FISH
            if self.first_to_scan_all_fish_of_type.get(fish_type) == player.get_index():
                total += COLORS_PER_FISH

        for color in range(COLORS_PER_FISH):
            if self.player_scanned_all_fish_of_color(player, color):
                total += len(FishType)
            if self.first_to_scan_all_fish_of_color.get(color) == player.get_index():
                total += len(FishType)

        return total

    def has_first_to_scan_bonus(self, player: Player, scan: Scan):
        return self.first_to_scan.get(scan, -1) == player.get_index()

    def has_first_to_scan_all_fish_of_type(self, player: Player, fish_type: FishType):
        return (
            self.first_to_scan_all_fish_of_type.get(fish_type, -1) == player.get_index()
        )

    def has_first_to_scan_all_fish_of_color(self, player: Player, col: int):
        return self.first_to_scan_all_fish_of_color.get(col, -1) == player.get_index()

    def detect_first_to_combo_bonuses(self, player: Player):
        for fish_type in FishType:
            if fish_type not in self.first_to_scan_all_fish_of_type:
                if self.player_scanned_all_fish_of_type(player, fish_type):
                    if fish_type in self.first_to_scan_all_fish_of_type_temp:
                        del self.first_to_scan_all_fish_of_type_temp[fish_type]
                    else:
                        self.first_to_scan_all_fish_of_type_temp[
                            fish_type
                        ] = player.get_index()

        for color in range(COLORS_PER_FISH):
            if color not in self.first_to_scan_all_fish_of_color:
                if self.player_scanned_all_fish_of_color(player, color):
                    if color in self.first_to_scan_all_fish_of_color_temp:
                        del self.first_to_scan_all_fish_of_color_temp[color]
                    else:
                        self.first_to_scan_all_fish_of_color_temp[
                            color
                        ] = player.get_index()

    def persist_first_to_scan_bonuses(self):
        player_scans_map = {}

        for k, v in self.first_to_scan_temp.items():
            self.first_to_scan.setdefault(k, v)

            player_name = self.players[v].get_nickname_token()
            player_scans_map.setdefault(player_name, [])
            player_scans_map[player_name].append(k)

        for player_scans in player_scans_map.items():
            scans = ", ".join(str(scan.fish_id) for scan in player_scans[1])
            if len(player_scans[1]) == 1:
                self.turn_summary += f"{player_scans[0]} was the first to save the scan of creature {scans}\n"
            else:
                self.turn_summary += f"{player_scans[0]} was the first to save the scans of {len(player_scans[1])} creatures: {scans}\n"

        for k, v in self.first_to_scan_all_fish_of_type_temp.items():
            self.first_to_scan_all_fish_of_type.setdefault(k, v)
            player_name = self.players[v].get_nickname_token()
            fish_species = f"{k.value} ({k.name.lower()})"
            self.turn_summary += f"{player_name} saved the scans of every color of {fish_species} first\n"

        for k, v in self.first_to_scan_all_fish_of_color_temp.items():
            self.first_to_scan_all_fish_of_color.setdefault(k, v)
            player_name = self.players[v].get_nickname_token()
            self.turn_summary += f"{player_name} has saved the scans of every {k} colored ({COLORS[k]}) creature first\n"

        self.first_to_scan_temp.clear()
        self.first_to_scan_all_fish_of_type_temp.clear()
        self.first_to_scan_all_fish_of_color_temp.clear()

    def move_entities(self):
        for player in self.players:
            for drone in player.drones:
                if drone.dead:
                    continue

                # Collision avec les Uglies
                for ugly in self.uglies:
                    col = self.get_collision(drone, ugly)
                    if col.happened():
                        drone.dying = True
                        drone.scans.clear()
                        drone.die_at = col.t

                        self.turn_summary += f"{player.get_nickname_token()}'s drone {drone.id} is hit by monster {ugly.id}!\n"

                        self.drones_eaten += 1
                        break

        # Déplacement des Drones
        for player in self.players:
            for drone in player.drones:
                speed = drone.get_speed()
                drone.pos = drone.pos.add(speed)
                self.snap_to_drone_zone(drone)

        # Déplacement des Poissons
        for fish in self.fishes:
            fish.pos = fish.pos.add(fish.get_speed())
            self.snap_to_fish_zone(fish)

        # Suppression des Poissons hors des limites
        fish_to_remove = [
            fish for fish in self.fishes if fish.get_x() > WIDTH - 1 or fish.get_x() < 0
        ]
        for fish in fish_to_remove:
            if fish.fleeing_from_player is not None and fish.fleeing_from_player != -1:
                self.chased_fish_count[fish.fleeing_from_player] += 1
        self.fishes = [fish for fish in self.fishes if fish not in fish_to_remove]

        # Réinitialisation des informations de fuite des poissons restants
        for fish in self.fishes:
            fish.fleeing_from_player = None

        # Déplacement des Uglies
        for ugly in self.uglies:
            ugly.pos = ugly.pos.add(ugly.speed)
            self.snap_to_ugly_zone(ugly)

    def is_game_over(self):
        # Vérification si tous les joueurs ont scanné tous les poissons restants
        if self.both_players_have_scanned_all_remaining_fish():
            return True

        # Autres conditions de fin de partie
        if self.game_turn >= 200:
            return True

        player_0_score = self.compute_max_player_score(self.players[0])
        player_1_score = self.compute_max_player_score(self.players[1])

        if (
            player_0_score < self.players[1].points
            or player_1_score < self.players[0].points
        ):
            return True

        return False

    def compute_score_on_end(self):
        for player in self.players:
            for drone in player.drones:
                self.apply_scans_for_report(player, drone)

            self.detect_first_to_combo_bonuses(player)

        self.persist_first_to_scan_bonuses()

        for player in self.players:
            score = self.compute_player_score(player)
            player.points = score
