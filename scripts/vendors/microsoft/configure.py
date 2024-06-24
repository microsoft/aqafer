import os
import json
import argparse

def main(github_pool, num_lists):
  github_runner = None
  test_lists = []
  platforms = ["windows-x64", "windows-arm64", "linux-x64", "linux-arm64", "macos-x64", "macos-arm64"]

  for platform in platforms:
    if platform in github_pool:
      if "macos" in github_pool and "arm64" in github_pool:
        github_runner = "config=['self-hosted', 'macOS', 'ARM64']"
      elif "macos" in github_pool and "x64" in github_pool:
        github_runner = "config='macos-11'"
      else:
        github_runner = f"config=['self-hosted', '1ES.Pool={ github_pool }']"

  with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    print(github_runner, file=fh)

  for list in range(num_lists):
    test_lists.append(f"testList_{list}")

  with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    print(f"testConfig={json.dumps(test_lists)}", file=fh)

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('--pool', type=str, help='Pool to run tests on')
  parser.add_argument('--testLists', type=int, help='Number of test lists')
  args = parser.parse_args()

  num_lists = args.testLists
  main(args.pool, num_lists)

