# TORCS AI Racing Project – IBM AI Racing League

## Project Overview

This project was created for the IBM AI Racing League competition.  
The goal of the project was to build an autonomous driving agent for the TORCS racing simulator. The agent is written in Python and controls the car without manual input.

The car receives information from the TORCS environment, such as track sensors, speed, car angle, position on the track and distance from obstacles. Based on this data, the agent decides how to steer, accelerate and brake in order to complete the lap as fast and safely as possible.

The final version of the agent is able to complete the Corkscrew standing start time trial with a stable driving line and very low damage.

---

## Final Result

- **Track:** Corkscrew
- **Standing start lap time:** 03:25
- **Top speed:** 103 km/h
- **Damage:** 2
- **Car:** IBM F1 car / TORCS racing car

---

## Fastest Lap Video

Video of the fastest standing start lap:

**Video link:**  
https://drive.google.com/file/d/1KnL4w4qWRX415iloyWLIpzUnJ07pxFn8/view?usp=sharing

---

## Presentation with IBM SkillsBuild Badges

Presentation showing completed IBM SkillsBuild badges:

**Presentation link:**  
TU WKLEJ LINK DO PREZENTACJI

---

## Custom F1 Car Livery

Custom F1 car livery prepared for the competition, including the university logo and team identifier:

**Livery link:**  
https://drive.google.com/file/d/1u8_s0YGb6qVh6BIx-t6_rHyzEBXlv0kC/view?usp=sharing

---

## Repository Files

This repository contains the main files required to run the autonomous agent:

- `sample_agent.py` – main autonomous driving agent
- `gym_torcs.py` – TORCS environment wrapper
- `example_experiment.py` – script used to run the experiment
- `practice.xml` – TORCS practice race configuration
- `README.md` – project documentation

---

## How the Agent Works

The agent uses sensor-based decision making. It reads the TORCS track sensors and calculates how much free space is available in front of the car and on both sides of the track.

The main driving logic is based on:

1. **Track sensor analysis**  
   The agent reads the distance sensors from the TORCS environment and estimates the safest direction to drive.

2. **Steering control**  
   The steering value is calculated using weighted track sensor data. The agent avoids sudden left-right movements by smoothing the steering response.

3. **Speed control**  
   The car drives faster on straight sections and slows down before corners. The target speed changes depending on the distance to the next corner, steering angle, car angle and position on the track.

4. **Braking control**  
   The agent uses braking when the car approaches a sharp corner or when the speed is too high for the current section of the track.

5. **Stability control**  
   The code limits sudden steering changes to prevent drifting, spinning and crashing into the walls.

---

## Development Strategy

The development process focused on creating a stable rule-based AI agent instead of using random driving or manual control. The first versions of the agent were able to move the car, but they often crashed into walls, turned too aggressively or reacted too slowly to corners.

The final version was improved by:

- smoothing track sensor readings,
- reducing sudden steering changes,
- adding speed control for corners,
- adding braking logic,
- limiting acceleration during sharp turns,
- testing multiple versions on the Corkscrew track,
- tuning the agent based on lap time, top speed and damage.

The final setup achieved a balance between speed and stability.

---

## Use of IBM SkillsBuild and IBM Granite

As part of the project, IBM SkillsBuild materials were used to support the learning process and understand AI-related concepts, project development and responsible technology use.

IBM Granite was used as support during the project development process, especially for improving the project strategy, structuring the documentation and explaining the logic behind the autonomous driving agent.

The project combines practical Python programming with AI-inspired decision making in a racing simulation environment.

---

## How to Run the Project

First, start TORCS with the practice configuration:

```bash
cd C:\Users\devicename\Downloads\Tree\torcs\torcs
wtorcs.exe -r
C:\Users\devicename\Downloads\Tree\torcs\gym_torcs\practice.xml
