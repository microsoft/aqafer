import argparse
import tarfile
import zipfile
import os
from pathlib import Path
from platform import system

def get_test_resources_path(destination) -> str:
    child_directories = [child for child in destination.iterdir() if child.is_dir()]
    test_jdk_home = None
    testimage_path = None

    # should only be two directories to check for
    for child in child_directories:
        if "-test-image" in child.name :
            testimage_path = str(child)
        elif "-test-image" not in child.name:
            test_jdk_home = str(child)

    return test_jdk_home, testimage_path

def expand_zip_archive(zip_archive, destination) -> None:
    if zipfile.is_zipfile(zip_archive):
        with zipfile.ZipFile(zip_archive) as zip:
            zip.extractall(destination)
    else:
        raise Exception(f"{zip_archive} is not a valid zip archive")

def expand_tar_archive(tar_archive, destination) -> None:
    if tarfile.is_tarfile(tar_archive):
        with tarfile.open(tar_archive) as tar:
            tar.extractall(destination)
    else:
        raise Exception(f"{tar_archive} is not a valid tar archive")

def set_openjdk_environment_variables(env_var_name, env_value) -> None:
    github_env = os.getenv("GITHUB_ENV")

    with open(github_env, 'a') as file:
        file.write(f"{ env_var_name }={ env_value }\n")

def main(source: Path, destination: Path) -> None:
    env_vars = {
        "TEST_JDK_HOME": None,
        "TESTIMAGE_PATH": None,
    }

    child_directories = [child for child in source.iterdir()]

    for child in child_directories:
        if system() == "Windows":
            expand_zip_archive(child, destination)
        else:
            expand_tar_archive(child, destination)

    env_vars["TEST_JDK_HOME"], env_vars["TESTIMAGE_PATH"] = get_test_resources_path(destination)
    set_openjdk_environment_variables("TEST_JDK_HOME", env_vars["TEST_JDK_HOME"])
    set_openjdk_environment_variables("TESTIMAGE_PATH", env_vars["TESTIMAGE_PATH"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, help='Path to the archive to extract')
    parser.add_argument('--destination', type=str, help='Destination directory for the extracted archive')
    args = parser.parse_args()

    source = Path(args.source)
    destination = Path(args.destination)
    main(source, destination)

