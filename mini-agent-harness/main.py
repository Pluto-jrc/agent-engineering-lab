import json

total_runs = 0
successful_runs = 0
total_steps = 0

with open("data/runs.jsonl", "r", encoding="utf-8") as f:
    # 逐行读取josnl文件并解析为python对象
    for line in f:
        record = json.loads(line)
        total_runs += 1
        total_steps += record["steps"]
        # 统计成功的运行次数和总步数
        if record["success"]:
            successful_runs += 1

failed_runs = total_runs - successful_runs
if total_runs > 0:
    success_rate = (successful_runs / total_runs) * 100
else:
    success_rate = 0

if total_runs > 0:
    average_steps = total_steps / total_runs
else:
    average_steps = 0

print(f"Total runs: {total_runs}")
print(f"Successful runs: {successful_runs}")
print(f"Failed runs: {failed_runs}")
print(f"Success rate: {success_rate:.1f}%")
print(f"Average steps: {average_steps:.1f}")

# Total runs: 5
# Successful runs: 3
# Failed runs: 2
# Success rate: 60.0%
# Average steps: 4.0
