import os
import random
import shutil
import pathlib
import tempfile
import argparse


def move_dataset(inputdir: str, outputdir: str, initial_image_counter=0):
    path = pathlib.Path(inputdir).resolve()
    output = pathlib.Path(outputdir).resolve()
    counter = initial_image_counter
    for entry in os.listdir(path):
        fullpath = os.path.join(path, entry)
        if os.path.isfile(fullpath) \
                and os.path.basename(entry) == "speeds.txt":
            with open(fullpath) as data:
                for line in data:
                    counter += 1
                    image, x, y, z, h = line.split()
                    newname = f"{str(counter).rjust(10, '0')}.{image.split('.')[1]}"
                    shutil.copy(os.path.join(path, image),
                                os.path.join(output, newname))
                    distdata = os.path.join(output, "speeds.txt")
                    with open(distdata, "a") as dist:
                        dist.write(f"{newname} {x} {y} {z} {h}\n")
    return counter


def merge_datasets(inputdir: str, output: str):
    path = pathlib.Path(inputdir).resolve()
    counter = 0
    for entry in os.listdir(path):
        fullpath = os.path.join(path, entry)
        if not os.path.isdir(fullpath):
            continue
        print(f"Merging {entry}")
        counter = move_dataset(fullpath, output, counter)


def split(inputdir: str, outputdir: str, percentage: float):
    path = pathlib.Path(inputdir).resolve()
    output = pathlib.Path(outputdir).resolve()
    inputdata = os.path.join(path, "speeds.txt")
    testpath = os.path.join(output, "test")
    testdata = os.path.join(testpath, "speeds.txt")
    trainpath = os.path.join(output, "train")
    traindata = os.path.join(trainpath, "speeds.txt")
    with open(inputdata, "r") as data:
        for line in data:
            r = random.random()
            image, x, y, z, h = line.split()
            if r > percentage:
                shutil.copy(os.path.join(path, image),
                            os.path.join(trainpath, image))
                with open(traindata, "a") as file:
                    file.write(f"{line}\n")
            else:
                shutil.copy(os.path.join(path, image),
                            os.path.join(testpath, image))
                with open(testdata, "a") as file:
                    file.write(f"{line}\n")


def main():
    argparser = argparse.ArgumentParser(description="Join Deep Pilot datasets")
    argparser.add_argument("--dir", "-d", required=True,
                           help="Top directory containing the datasets subdirectories")
    argparser.add_argument(
        "--preserve", "-p", action="store_true", help="Preserve merge before spliting")
    argparser.add_argument(
        "--output_dir", "-o",  help="The output directory containing the resulting dataset")
    argparser.add_argument("--split", "-s", default=0.2,
                           help="Split percentage for test portion")
    args = argparser.parse_args()
    mergedir = ""
    if args.preserve:
        mergedir = os.path.join(args.output_dir, "merge")
        try:
            os.mkdir(mergedir)
        except:
            pass
    else:
        mergedir = tempfile.mkdtemp()

    merge_datasets(args.dir, mergedir)
    try:
        os.mkdir(os.path.join(args.output_dir, "train"))
        os.mkdir(os.path.join(args.output_dir, "test"))
    except:
        pass

    split(mergedir, args.output_dir, args.split)


if __name__ == "__main__":
    main()
