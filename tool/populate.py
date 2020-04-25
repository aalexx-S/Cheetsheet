import sys
import os
import json
import requests


def main():
    samples = os.listdir(sys.argv[1])
    index = 0

    for sample in samples:
        if not sample.endswith(".py"):
            continue

        sample_path = os.path.join(sys.argv[1], sample)
        if not os.path.isfile(sample_path):
            continue

        code = None
        with open(sample_path, "r") as hdle:
            code = hdle.read()

        payload = {
            'language': 'python',
            'code': json.dumps(code),
        }

        url = f"""http://localhost:9200/cheetsheet/python/{index}"""

        result = requests.post(url, json=payload)
        print(result.text)
        print(f"""Install {sample_path} ...""")
        index += 1


if __name__ == "__main__":
    main()
