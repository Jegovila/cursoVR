
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# IMPORTANTE: OPENCV ELIMINÓ opencv_traincascade.exe A PARTIR DE 3.4
# ES NECESARIO CAMBIARNOS A OPENCV 3.4 PARA PODER USARLO

# ==========================================
# CONFIGURATION
# ==========================================

BASE_PATH = Path(__file__).resolve().parent

ANNOTATION_PATH = BASE_PATH / "annotations"
POSITIVE_FILE = ANNOTATION_PATH / "positives.txt"
NEGATIVE_FILE = ANNOTATION_PATH / "negatives.txt"

VEC_FILE = BASE_PATH / "samples" / "positives.vec"

TRAINING_PATH = BASE_PATH / "training"
CASCADE_PATH = BASE_PATH / "cascade"

CASCADE_FILE = CASCADE_PATH / "cascade.xml"

# OpenCV executable
TRAINCASCADE_EXE = BASE_PATH / "opencv" / "opencv_traincascade.exe"

# Sample window dimensions
WINDOW_WIDTH = 24
WINDOW_HEIGHT = 24

# Default training parameters
DEFAULT_STAGES = 5
DEFAULT_MAX_WEAK_COUNT = 20
DEFAULT_THREADS = 4

MIN_HIT_RATE = 0.995
MAX_FALSE_ALARM_RATE = 0.5

# Memory buffers (MB)
PRECALC_VAL_BUF_SIZE = 128
PRECALC_IDX_BUF_SIZE = 128


# ==========================================
# FIND OPENCV EXECUTABLE
# ==========================================

def find_traincascade():

    if TRAINCASCADE_EXE.exists():
        return str(TRAINCASCADE_EXE)

    return shutil.which("opencv_traincascade")


# ==========================================
# COUNT POSITIVE OBJECTS
# ==========================================

def count_positive_objects():

    if not POSITIVE_FILE.exists():
        print("ERROR: positives.txt not found.")
        return 0

    total = 0

    with open(POSITIVE_FILE, "r") as file:

        for line in file:

            parts = line.strip().split()

            if len(parts) < 2:
                continue

            try:
                total += int(parts[1])

            except ValueError:
                continue

    return total


# ==========================================
# COUNT AND VALIDATE NEGATIVE IMAGES
# ==========================================

def count_negative_images():

    if not NEGATIVE_FILE.exists():
        print("ERROR: negatives.txt not found.")
        return 0

    total = 0

    with open(NEGATIVE_FILE, "r") as file:

        for line_number, line in enumerate(file, 1):

            relative_path = line.strip()

            if not relative_path:
                continue

            # Negative paths are relative to annotations/
            image_path = (ANNOTATION_PATH / relative_path).resolve()

            if not image_path.exists():

                print(f"Missing negative image at line {line_number}:")
                print(relative_path)
                continue

            total += 1

    return total


# ==========================================
# ASK TRAINING PARAMETERS
# ==========================================

def ask_parameters(total_positive, total_negative):

    print("\n------------------------------------------")
    print(" TRAINING PARAMETERS")
    print("------------------------------------------")

    print(f"Available positive samples: {total_positive}")
    print(f"Available negative images: {total_negative}")

    default_pos = max(1, int(total_positive * 0.9))
    default_neg = max(1, int(total_negative * 0.9))

    try:

        print("\nNumber of positive samples")

        value = input(
            f"numPos [{default_pos}]: "
        ).strip()

        num_pos = int(value) if value else default_pos

        print("\nNumber of negative samples")

        value = input(
            f"numNeg [{default_neg}]: "
        ).strip()

        num_neg = int(value) if value else default_neg

        print("\nNumber of training stages")

        value = input(
            f"numStages [{DEFAULT_STAGES}]: "
        ).strip()

        num_stages = int(value) if value else DEFAULT_STAGES

        print("\nMaximum weak classifiers per stage")

        value = input(
            f"maxWeakCount [{DEFAULT_MAX_WEAK_COUNT}]: "
        ).strip()

        max_weak_count = (
            int(value) if value else DEFAULT_MAX_WEAK_COUNT
        )

        if (
            num_pos <= 0 or
            num_neg <= 0 or
            num_stages <= 0 or
            max_weak_count <= 0
        ):
            raise ValueError()

        if num_pos > total_positive:
            print("\nERROR: numPos exceeds available positive samples.")
            return None

        if num_neg > total_negative:
            print("\nERROR: numNeg exceeds available negative images.")
            return None

        return num_pos, num_neg, num_stages, max_weak_count

    except ValueError:

        print("\nERROR: Invalid training parameters.")
        return None


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("------------------------------------------")
    print(" HAAR CASCADE - TRAINING")
    print("------------------------------------------")

    # Check executable
    executable = find_traincascade()

    if executable is None:

        print("\nERROR: opencv_traincascade.exe not found.")
        return

    print(f"\nExecutable: {executable}")

    # Check vector file
    if not VEC_FILE.exists() or VEC_FILE.stat().st_size == 0:

        print("\nERROR: positives.vec not found or empty.")
        return

    print(f"Positive vector file: {VEC_FILE}")

    # Check negative file
    if not NEGATIVE_FILE.exists():

        print("\nERROR: negatives.txt not found.")
        return

    # Count samples
    total_positive = count_positive_objects()
    total_negative = count_negative_images()

    print("\n------------------------------------------")
    print(" DATASET INFORMATION")
    print("------------------------------------------")

    print(f"Positive samples: {total_positive}")
    print(f"Negative images: {total_negative}")

    if total_positive < 2 or total_negative < 2:

        print("\nERROR: Not enough training samples.")
        return

    # Ask parameters
    parameters = ask_parameters(
        total_positive,
        total_negative
    )

    if parameters is None:
        return

    num_pos, num_neg, num_stages, max_weak_count = parameters

    # Create output directories
    TRAINING_PATH.mkdir(parents=True, exist_ok=True)
    CASCADE_PATH.mkdir(parents=True, exist_ok=True)

    # Create a separate folder for this training run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path = TRAINING_PATH / f"run_{timestamp}"
    output_path.mkdir(parents=True, exist_ok=True)

    # Build command
    command = [
        executable,

        "-data", str(output_path),
        "-vec", str(VEC_FILE),
        "-bg", str(NEGATIVE_FILE),

        "-numPos", str(num_pos),
        "-numNeg", str(num_neg),

        "-numStages", str(num_stages),

        "-w", str(WINDOW_WIDTH),
        "-h", str(WINDOW_HEIGHT),

        "-featureType", "HAAR",
        "-mode", "BASIC",

        "-minHitRate", str(MIN_HIT_RATE),
        "-maxFalseAlarmRate", str(MAX_FALSE_ALARM_RATE),

        "-maxWeakCount", str(max_weak_count),

        "-precalcValBufSize", str(PRECALC_VAL_BUF_SIZE),
        "-precalcIdxBufSize", str(PRECALC_IDX_BUF_SIZE),

        "-numThreads", str(DEFAULT_THREADS)
    ]

    # Display configuration
    print("\n------------------------------------------")
    print(" TRAINING CONFIGURATION")
    print("------------------------------------------")

    print(f"Positive samples: {num_pos}")
    print(f"Negative images: {num_neg}")
    print(f"Stages: {num_stages}")
    print(f"Maximum weak classifiers: {max_weak_count}")
    print(f"Window size: {WINDOW_WIDTH} x {WINDOW_HEIGHT}")
    print(f"Threads: {DEFAULT_THREADS}")

    print(f"\nTraining output: {output_path}")

    print("\n------------------------------------------")
    print(" STARTING TRAINING")
    print("------------------------------------------")

    print("\nCommand:")
    print(subprocess.list2cmdline(command))

    # Execute training
    try:

        result = subprocess.run(
            command,
            cwd=str(ANNOTATION_PATH),
            check=False
        )

        if result.returncode != 0:

            print("\nERROR: opencv_traincascade failed.")
            return

    except Exception as error:

        print(f"\nExecution error: {error}")
        return

    # Check generated cascade
    generated_cascade = output_path / "cascade.xml"

    if not generated_cascade.exists():

        print("\nERROR: cascade.xml was not generated.")
        return

    # Copy final cascade
    shutil.copy2(
        generated_cascade,
        CASCADE_FILE
    )

    print("\n------------------------------------------")
    print(" TRAINING COMPLETED")
    print("------------------------------------------")

    print(f"\nCascade file: {CASCADE_FILE}")
    print(f"Training files: {output_path}")

    print("\nReady for detection!")


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    main()
