# -*- coding: utf-8 -*-
"""演示入口：`python main.py`（维护者文件，勿改）。
等价于 PYTHONPATH=src python -m main。"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "src"))

from main.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()

def hp_ratio(hp, max_hp):
    """
    Calculate the HP ratio as a percentage.

    Parameters:
    hp (int): Current health points.
    max_hp (int): Maximum health points.

    Returns:
    float: The HP ratio as a percentage.
    """
    if max_hp <= 0:
        raise ValueError("max_hp must be greater than 0")
    print(f"血量为：{hp}，最大血量为：{max_hp}")
    
    return (hp / max_hp) * 100
hp_ratio(100, 200)






def status_report(name,robot_type,hp,max_hp,battery):
    """
    Generate a status report for a robot.

    Parameters:
    name (str): The name of the robot.
    robot_type (str): The type of the robot.
    hp (int): Current health points.
    max_hp (int): Maximum health points.

    Returns:
    str: A formatted status report.
    """
    ratio = hp_ratio(hp, max_hp)
    report = f"Robot Name: {name}\nType: {robot_type}\nHP: {hp}/{max_hp} ({ratio:.2f}%)\nBattery: {battery}%"
    if battery < 20:
            print("Warning: Battery level is low!")
    if battery < 10:
            print("Critical Warning: Battery level is critically low!")
    if battery >= 50 and battery < 100:
            print("Battery is OK!")
    if battery < 50 and battery >= 20:
            print("Warning: Battery level is low!")
    return report

    
print(status_report("Alpha", "Combat", 100, 200, 80))


import json

def analyze_damage_log(lines):
    by_armor = {"front":0, "left":0, "right":0}
    total = 0
    seen_ids = set()
    event_cnt = 0

    for line in lines:
        s = line.strip()
        # 空行、注释直接跳过
        if not s or s.startswith("#"):
            continue

        # JSON类型行
        if s.startswith("{"):
            try:
                obj = json.loads(s)
                # 缺少必要字段
                if "armor" not in obj or "damage" not in obj:
                    continue
                arm = obj["armor"]
                dmg = obj["damage"]
                # 部位校验
                if arm not in ("front", "left", "right"):
                    continue
                # 伤害必须正整数
                if type(dmg) is not int or dmg <= 0:
                    continue
                # id去重
                if "id" in obj:
                    eid = obj["id"]
                    if eid in seen_ids:
                        continue
                    seen_ids.add(eid)
                by_armor[arm] += dmg
                total += dmg
                event_cnt += 1
            except json.JSONDecodeError:
                print(f"Invalid JSON entry: {s}")
                continue
        else:
            chunks = s.split(",")
            valid = True
            sensor_hit = {"front":0,"left":0,"right":0}
            for seg in chunks:
                seg = seg.strip()
                if ":" not in seg:
                    valid = False
                    break
                k, v = seg.split(":", 1)
                k = k.strip()
                v = v.strip()
                if k not in ("F","L","R"):
                    valid = False
                    break
                if not v.isdigit():
                    valid = False
                    break
                num = int(v)
                if num <= 0:
                    valid = False
                    break
                if k == "F":
                    sensor_hit["front"] += num
                elif k == "L":
                    sensor_hit["left"] += num
                elif k == "R":
                    sensor_hit["right"] += num
            if valid:
                by_armor["front"] += sensor_hit["front"]
                by_armor["left"] += sensor_hit["left"]
                by_armor["right"] += sensor_hit["right"]
                total += sum(sensor_hit.values())
                event_cnt += 1
    most_hit = None
    if total > 0:
        max_val = max(by_armor.values())
        for pos in ["front","left","right"]:
            if by_armor[pos] == max_val:
                most_hit = pos
                break
    avg = total / event_cnt if event_cnt > 0 else 0

    return {
        "total": total,
        "by_armor": by_armor,
        "most_hit": most_hit,
        "avg": avg
    }       



