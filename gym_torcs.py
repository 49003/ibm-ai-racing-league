import gym
from gym import spaces
import numpy as np
import snakeoil3_gym as snakeoil3
import copy
import collections as col


class TorcsEnv:
    terminal_judge_start = 999999
    termination_limit_progress = 0

    default_speed = 100

    initial_reset = True

    def __init__(self, vision=False, throttle=False, gear_change=False):
        self.vision = vision
        self.throttle = throttle
        self.gear_change = gear_change
        self.initial_run = True

        if throttle is False:
            self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        else:
            self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(3,))

        if vision is False:
            high = np.array([
                1., np.inf, np.inf, np.inf,
                np.inf, np.inf, np.inf,
                1., np.inf, 1., np.inf
            ])

            low = np.array([
                0., -np.inf, -np.inf, -np.inf,
                -np.inf, -np.inf, -np.inf,
                0., -np.inf, 0., -np.inf
            ])

            self.observation_space = spaces.Box(low=low, high=high)

        else:
            high = np.array([
                1., np.inf, np.inf, np.inf,
                np.inf, np.inf, np.inf,
                1., np.inf, 1., np.inf, 255
            ])

            low = np.array([
                0., -np.inf, -np.inf, -np.inf,
                -np.inf, -np.inf, -np.inf,
                0., -np.inf, 0., -np.inf, 0
            ])

            self.observation_space = spaces.Box(low=low, high=high)

    def step(self, u):
        client = self.client
        this_action = self.agent_to_torcs(u)
        action_torcs = client.R.d

        action_torcs['steer'] = float(np.clip(this_action['steer'], -1.0, 1.0))

        speed = float(client.S.d['speedX'])

        if self.throttle is False:
            target_speed = self.default_speed

            if speed < target_speed:
                client.R.d['accel'] += 0.01
                client.R.d['brake'] = 0.0
            else:
                client.R.d['accel'] -= 0.01
                client.R.d['brake'] = 0.05

            if client.R.d['accel'] > 0.2:
                client.R.d['accel'] = 0.2

            if client.R.d['accel'] < 0.0:
                client.R.d['accel'] = 0.0

            if speed < 10:
                client.R.d['accel'] = 0.5
                client.R.d['brake'] = 0.0

        else:
            action_torcs['accel'] = float(np.clip(this_action.get('accel', 0.0), 0.0, 1.0))
            action_torcs['brake'] = float(np.clip(this_action.get('brake', 0.0), 0.0, 1.0))

        if self.gear_change is True:
            action_torcs['gear'] = int(this_action.get('gear', 1))

        else:
            speed = float(client.S.d['speedX'])

            if speed > 175:
                action_torcs['gear'] = 6
            elif speed > 140:
                action_torcs['gear'] = 5
            elif speed > 105:
                action_torcs['gear'] = 4
            elif speed > 70:
                action_torcs['gear'] = 3
            elif speed > 35:
                action_torcs['gear'] = 2
            else:
                action_torcs['gear'] = 1

        obs_pre = copy.deepcopy(client.S.d)

        client.respond_to_server()
        client.get_servers_input()

        obs = client.S.d
        self.observation = self.make_observaton(obs)

        track = np.array(obs['track'])
        sp = np.array(obs['speedX'])
        progress = sp * np.cos(obs['angle'])
        reward = progress

        if obs['damage'] - obs_pre['damage'] > 0:
            reward = -1

        if track.min() < 0:
            reward = -1

        if np.cos(obs['angle']) < 0:
            reward = -1

        self.time_step += 1

        return self.get_obs(), reward, client.R.d['meta'], {}

    def reset(self, relaunch=False):
        self.time_step = 0

        if self.initial_reset is not True:
            self.client.R.d['meta'] = True
            self.client.respond_to_server()

            if relaunch is True:
                self.reset_torcs()
                print("Manual TORCS restart required on Windows.")

        self.client = snakeoil3.Client(p=3001, vision=self.vision)
        self.client.MAX_STEPS = np.inf

        client = self.client
        client.get_servers_input()

        obs = client.S.d
        self.observation = self.make_observaton(obs)

        self.last_u = None
        self.initial_reset = False

        return self.get_obs()

    def end(self):
        pass

    def get_obs(self):
        return self.observation

    def reset_torcs(self):
        print("Manual TORCS restart required on Windows.")

    def agent_to_torcs(self, u):
        torcs_action = {'steer': float(u[0])}

        if self.throttle is True:
            torcs_action.update({'accel': float(u[1])})

            if len(u) >= 3:
                torcs_action.update({'brake': float(u[2])})
            else:
                torcs_action.update({'brake': 0.0})

        if self.gear_change is True:
            if len(u) >= 4:
                torcs_action.update({'gear': int(u[3])})
            else:
                torcs_action.update({'gear': 1})

        return torcs_action

    def obs_vision_to_image_rgb(self, obs_image_vec):
        image_vec = obs_image_vec
        rgb = []
        temp = []

        for i in range(0, 12286, 3):
            temp.append(image_vec[i])
            temp.append(image_vec[i + 1])
            temp.append(image_vec[i + 2])
            rgb.append(temp)
            temp = []

        return np.array(rgb, dtype=np.uint8)

    def make_observaton(self, raw_obs):
        if self.vision is False:
            names = [
                'focus',
                'angle',
                'trackPos',
                'distFromStart',
                'speedX',
                'speedY',
                'speedZ',
                'opponents',
                'rpm',
                'track',
                'wheelSpinVel'
            ]

            Observation = col.namedtuple('Observaion', names)

            return Observation(
                focus=np.array(raw_obs['focus'], dtype=np.float32) / 200.,
                angle=np.array(raw_obs['angle'], dtype=np.float32),
                trackPos=np.array(raw_obs['trackPos'], dtype=np.float32),
                distFromStart=np.array(raw_obs['distFromStart'], dtype=np.float32),
                speedX=np.array(raw_obs['speedX'], dtype=np.float32),
                speedY=np.array(raw_obs['speedY'], dtype=np.float32),
                speedZ=np.array(raw_obs['speedZ'], dtype=np.float32),
                opponents=np.array(raw_obs['opponents'], dtype=np.float32) / 200.,
                rpm=np.array(raw_obs['rpm'], dtype=np.float32),
                track=np.array(raw_obs['track'], dtype=np.float32),
                wheelSpinVel=np.array(raw_obs['wheelSpinVel'], dtype=np.float32)
            )

        else:
            names = [
                'focus',
                'angle',
                'trackPos',
                'distFromStart',
                'speedX',
                'speedY',
                'speedZ',
                'opponents',
                'rpm',
                'track',
                'wheelSpinVel',
                'img'
            ]

            Observation = col.namedtuple('Observaion', names)

            image_rgb = self.obs_vision_to_image_rgb(raw_obs['img'])

            return Observation(
                focus=np.array(raw_obs['focus'], dtype=np.float32) / 200.,
                angle=np.array(raw_obs['angle'], dtype=np.float32),
                trackPos=np.array(raw_obs['trackPos'], dtype=np.float32),
                distFromStart=np.array(raw_obs['distFromStart'], dtype=np.float32),
                speedX=np.array(raw_obs['speedX'], dtype=np.float32),
                speedY=np.array(raw_obs['speedY'], dtype=np.float32),
                speedZ=np.array(raw_obs['speedZ'], dtype=np.float32),
                opponents=np.array(raw_obs['opponents'], dtype=np.float32) / 200.,
                rpm=np.array(raw_obs['rpm'], dtype=np.float32),
                track=np.array(raw_obs['track'], dtype=np.float32),
                wheelSpinVel=np.array(raw_obs['wheelSpinVel'], dtype=np.float32),
                img=image_rgb
            )