import sys
import os
import requests


def main():
    samples = os.listdir(sys.argv[1])
    #index = 0

    payloads = []
    for sample in samples:
        if not sample.endswith(".json"):
            continue

        sample_path = os.path.join(sys.argv[1], sample)
        if not os.path.isfile(sample_path):
            continue

        payload = None
        with open(sample_path, "r") as hdle:
            payload = hdle.read()
        payloads.append(payload)

    len_payloads = len(payloads)
    bound = 100000
    for id in range(0, bound):
        idx = id % len_payloads
        url = f"""http://localhost:9200/cheetsheet/python/{id}"""
        result = requests.post(url, json=payloads[idx])
        #print(f"""Install {sample_path} ...""")
        #index += 1


if __name__ == "__main__":
    main()
