import json


class InvalidLogError(Exception):
    pass


# 检查record是否符合要求的jsonl格式
def detect_invalid_record(record: dict) -> None:

    # 检查字典中是否存在必要的键
    if "success" not in record:
        raise InvalidLogError(f"Missing 'success' key in record: {record}")
    if "steps" not in record:
        raise InvalidLogError(f"Missing 'steps' key in record: {record}")

    # 检查键的值类型是否正确
    if type(record["success"]) is not bool:
        raise InvalidLogError(f"'success' key must be a boolean in record: {record}")
    if type(record["steps"]) is not int:
        raise InvalidLogError(f"'steps' key must be an integer in record: {record}")

    # 检查steps是否为非负整数
    if record["steps"] < 0:
        raise InvalidLogError(
            f"'steps' key must be a non-negative integer in record: {record}"
        )


# 将处理jsonl文件的代码封装为一个函数
def analyze_runs(file_path: str) -> dict:
    total_runs = 0
    successful_runs = 0
    total_steps = 0

    with open(file_path, "r", encoding="utf-8") as f:
        # 逐行读取jsonl文件并解析为python对象
        for line_num, line in enumerate(f, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)

                # 检查record是否为字典类型
                if not isinstance(record, dict):
                    raise InvalidLogError(
                        f"Invalid record format on line {line_num}: {line.strip()}"
                    )

                detect_invalid_record(record)

            # 判断两种异常类型
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {line_num}: {e}")
                continue

            except InvalidLogError as e:
                print(f"Invalid record on line {line_num}: {e}")
                continue

            total_runs += 1
            total_steps += record["steps"]
            # 统计成功的运行次数和总步数
            if record["success"]:
                successful_runs += 1

    failed_runs = total_runs - successful_runs

    success_rate = (successful_runs / total_runs) * 100 if total_runs > 0 else 0

    average_steps = total_steps / total_runs if total_runs > 0 else 0

    return {
        "total_runs": total_runs,
        "successful_runs": successful_runs,
        "failed_runs": failed_runs,
        "success_rate": success_rate,
        "average_steps": average_steps,
    }


def main():
    file_path = "data/runs.jsonl"
    results = analyze_runs(file_path)

    print(f"Total runs: {results['total_runs']}")
    print(f"Successful runs: {results['successful_runs']}")
    print(f"Failed runs: {results['failed_runs']}")
    print(f"Success rate: {results['success_rate']:.1f}%")
    print(f"Average steps: {results['average_steps']:.1f}")


if __name__ == "__main__":
    main()

# Total runs: 5
# Successful runs: 3
# Failed runs: 2
# Success rate: 60.0%
# Average steps: 4.0
