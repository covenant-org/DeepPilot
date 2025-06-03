import os
import random
import shutil
import pathlib
import tempfile
import argparse
from math import copysign


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
                    file.write(f"train/{line}")
            else:
                shutil.copy(os.path.join(path, image),
                            os.path.join(testpath, image))
                with open(testdata, "a") as file:
                    file.write(f"test/{line}")


def quantize(inputdir: str, outputdir: str, threshold=0):
    path = pathlib.Path(inputdir).resolve()
    output = pathlib.Path(outputdir).resolve()
    inputdata = os.path.join(path, "speeds.txt")
    outputdata = os.path.join(output, "speeds.txt")
    with open(inputdata) as inf:
        with open(outputdata, "w") as outf:
            for line in inf:
                image, x, y, z, h = line.split()
                shutil.copy(os.path.join(path, image),
                            os.path.join(output, image))
                x = float(x.strip())
                y = float(y.strip())
                z = float(z.strip())
                h = float(h.strip())
                x = copysign(1, x) if abs(x) > threshold else 0
                y = copysign(1, y) if abs(y) > threshold else 0
                z = copysign(1, z) if abs(z) > threshold else 0
                h = copysign(1, h) if abs(h) > threshold else 0
                outf.write(f"{image} {x} {y} {z} {h}\n")


def scale(inputdir: str, outputdir: str, factor=10.0):
    path = pathlib.Path(inputdir).resolve()
    output = pathlib.Path(outputdir).resolve()
    inputdata = os.path.join(path, "speeds.txt")
    outputdata = os.path.join(output, "speeds.txt")
    with open(inputdata) as inf:
        with open(outputdata, "w") as outf:
            for line in inf:
                image, x, y, z, h = line.split()
                shutil.copy(os.path.join(path, image),
                            os.path.join(output, image))
                x = float(x.strip()) * factor
                y = float(y.strip()) * factor
                z = float(z.strip()) * factor
                h = float(h.strip()) * factor
                outf.write(f"{image} {x} {y} {z} {h}\n")


def main():
    argparser = argparse.ArgumentParser(description="Join Deep Pilot datasets")
    argparser.add_argument(
        "mode", choices=["merge", "scale", "split", "quantize", "mss"])
    argparser.add_argument("--scale", type=float, default=10.0)
    argparser.add_argument("--threshold", "-t", type=float, default=0.0)
    argparser.add_argument("--dir", "-d", required=True,
                           help="Top directory containing the datasets subdirectories")
    argparser.add_argument(
        "--preserve", "-p", action="store_true", help="Preserve merge before spliting")
    argparser.add_argument(
        "--output_dir", "-o", required=True, help="The output directory containing the resulting dataset")
    argparser.add_argument("--split", "-s", default=0.2,
                           help="Split perrequired=Truecentage for test portion")
    args = argparser.parse_args()
    mergedir = args.dir
    print(args)

    if args.mode == "quantize":
        os.makedirs(args.output_dir, exist_ok=True)
        quantize(args.dir, args.output_dir, args.threshold)

    if args.mode in ["merge", "all"]:
        if args.preserve:
            mergedir = os.path.join(args.output_dir, "merge")
        else:
            if args.mode == "merge":
                mergedir = args.output_dir
            else:
                mergedir = tempfile.mkdtemp()
        os.makedirs(mergedir, exist_ok=True)

        merge_datasets(args.dir, mergedir)
    if args.mode in ["scale", "all"]:
        outputdir = args.output_dir
        if args.mode == "all":
            outputdir = os.path.join(outputdir, "scaled")
        os.makedirs(outputdir, exist_ok=True)
        scale(mergedir, outputdir, args.scale)
        mergedir = outputdir

    if args.mode in ["split", "all"]:
        os.makedirs(os.path.join(args.output_dir, "train"), exist_ok=True)
        os.makedirs(os.path.join(args.output_dir, "test"), exist_ok=True)
        split(mergedir, args.output_dir, args.split)


if __name__ == "__main__":
    main()
