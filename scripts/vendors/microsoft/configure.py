# Purpose: Set the type of runner to use in the workflow and the number of test lists to generate.
# Usage: python configure.py --pool <pool_name> --testLists <number_of_test_lists>

import os
import json
import argparse

def set_number_of_test_lists(num_lists: int) -> str:
    return [f"testList_{list}" for list in range(num_lists)]

def get_runner_config(pool_name: str) -> str:
    platforms = ["windows-x64", "windows-arm64", "linux-x64", "linux-arm64", "macos-x64", "macos-arm64"]
    for platform in platforms:
        if platform in pool_name:
            if "macos" in pool_name and "arm64" in pool_name:
                return "config='macos-14'"
            elif "macos" in pool_name and "x64" in pool_name:
                return "config='macos-11'"
            else:
                return f"config=['self-hosted', '1ES.Pool={ pool_name }']"

def main(github_pool, num_lists):
  github_runner = None
  test_lists = []

  github_runner = get_runner_config(github_pool.lower())
  test_lists = set_number_of_test_lists(num_lists)

  with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    print(github_runner, file=fh)
    print(f"testConfig={json.dumps(test_lists)}", file=fh)

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('--pool', type=str, help='Pool to run tests on')
  parser.add_argument('--testLists', type=int, help='Number of test lists')
  args = parser.parse_args()

  num_lists = args.testLists
  main(args.pool, num_lists)

