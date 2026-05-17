from gym_torcs import TorcsEnv
from sample_agent import Agent
import time
import numpy as np

vision = False
episode_count = 1
max_steps = 50000

reward = 0
done = False
step = 0

env = TorcsEnv(vision=vision, throttle=True)
agent = Agent(3)

print("TORCS Experiment Start.")

for i in range(episode_count):
    print("Episode:", i)

    ob = env.reset(relaunch=False)
    total_reward = 0.0

    bad_reward_streak = 0
    low_speed_streak = 0

    for j in range(max_steps):
        action = agent.act(ob, reward, done, vision)

        ob, reward, done, _ = env.step(action)

        total_reward += reward
        step += 1

        if step % 500 == 0:
            print("Step:", step, "Reward:", total_reward)

        if done:
            print("Episode finished by TORCS at step:", step)
            break

        if reward <= -0.5:
            bad_reward_streak += 1
        else:
            bad_reward_streak = 0

        if bad_reward_streak >= 250:
            print("Stopped: car is stuck or crashing for too long.")
            break

        try:
            speed = float(np.array(ob.speedX).item())

            if abs(speed) < 1.0:
                low_speed_streak += 1
            else:
                low_speed_streak = 0

            if low_speed_streak >= 500:
                print("Stopped: car speed is too low for too long.")
                break

        except Exception:
            pass

    print("TOTAL REWARD:", total_reward)
    print("Total Step:", step)

print("Run finished. TORCS will stay open for 10 seconds.")
time.sleep(10)

print("Finish.")