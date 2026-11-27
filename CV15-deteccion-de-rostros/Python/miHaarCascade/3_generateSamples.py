import cv2
import subprocess
import shutil
from pathlib import Path

# IMPORTANTE: OPENCV ELIMINÓ opencv_createsamples.exe A PARTIR DE 3.4
# ES NECESARIO CAMBIARNOS A OPENCV 3.4 PARA PODER USARLO

# ==========================================
# CONFIGURATION
# ==========================================

BASE_PATH = Path(__file__).resolve().parent

POSITIVE_PATH = BASE_PATH / "dataset" / "positive"
NEGATIVE_PATH = BASE_PATH / "dataset" / "negative"

ANNOTATION_PATH = BASE_PATH / "annotations"
ANNOTATION_FILE = ANNOTATION_PATH / "positives.txt"

SAMPLES_PATH = BASE_PATH / "samples"
VEC_FILE = SAMPLES_PATH / "positives.vec"

NEGATIVE_FILE = ANNOTATION_PATH / "negatives.txt"

# OpenCV executable:
CREATESAMPLES_EXE = BASE_PATH / "opencv" / "opencv_createsamples.exe"

# Default sample dimensions
DEFAULT_WIDTH = 24
DEFAULT_HEIGHT = 24

# Show generated samples for visual inspection
SHOW_SAMPLES = False


# ==========================================
# FIND OPENCV EXECUTABLE
# ==========================================

def find_createsamples():

    if CREATESAMPLES_EXE:

        exe = Path(CREATESAMPLES_EXE)

        if exe.exists():
            return str(exe)

        return None

    return shutil.which("opencv_createsamples")


# ==========================================
# LOAD POSITIVE ANNOTATIONS
# ==========================================

def load_annotations():

    if not ANNOTATION_FILE.exists():
        print("ERROR: positives.txt no encontrado.")
        return 0

    total_objects = 0
    valid_images = 0

    with open(ANNOTATION_FILE, "r") as file:

        for line_number, line in enumerate(file, 1):

            parts = line.strip().split()

            if not parts:
                continue

            try:

                if len(parts) < 2:
                    raise ValueError()

                # Resolve paths relative to annotations/
                image_path = (ANNOTATION_PATH / parts[0]).resolve()
                count = int(parts[1])

                if count <= 0:
                    raise ValueError()

                if len(parts) != 2 + count * 4:
                    raise ValueError()

                if not image_path.exists():
                    print(f"Missing image: {parts[0]}")
                    continue

                image = cv2.imread(str(image_path))

                if image is None:
                    print(f"Invalid image: {parts[0]}")
                    continue

                height, width = image.shape[:2]

                valid = True

                for i in range(count):

                    offset = 2 + i * 4

                    x, y, w, h = map(
                        int,
                        parts[offset:offset + 4]
                    )

                    if (
                        x < 0 or y < 0 or
                        w <= 0 or h <= 0 or
                        x + w > width or
                        y + h > height
                    ):
                        valid = False
                        break

                if not valid:
                    print(f"Invalid ROI: {parts[0]}")
                    continue

                total_objects += count
                valid_images += 1

            except (ValueError, IndexError):

                print(f"Invalid annotation at line {line_number}")

    print(f"Valid positive images: {valid_images}")
    print(f"Total annotated objects: {total_objects}")

    return total_objects


# ==========================================
# GENERATE NEGATIVE DESCRIPTION FILE
# ==========================================

def generate_negative_file():

    extensions = [
        "*.jpg", "*.jpeg", "*.png", "*.bmp"
    ]

    negative_images = []

    for ext in extensions:
        negative_images.extend(NEGATIVE_PATH.glob(ext))

    negative_images = sorted(negative_images)

    with open(NEGATIVE_FILE, "w") as file:

        for image_path in negative_images:

            # Paths relative to annotations/negatives.txt
            relative_path = Path(
                "..", "dataset", "negative", image_path.name
            ).as_posix()

            file.write(relative_path + "\n")

    print(f"Negative images: {len(negative_images)}")

    return len(negative_images)


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("------------------------------------------")
    print(" HAAR CASCADE - SAMPLE GENERATOR")
    print("------------------------------------------")

    # Check OpenCV executable
    executable = find_createsamples()

    if executable is None:

        print("\nERROR: opencv_createsamples.exe not found.")
        print("\nInstall/build the OpenCV training utilities.")
        print("Alternatively, set CREATESAMPLES_EXE")
        print("to the full path of opencv_createsamples.exe.")

        return

    print(f"\nExecutable: {executable}")

    # Check annotations
    total_objects = load_annotations()

    if total_objects == 0:

        print("\nERROR: No valid positive annotations.")
        return

    # Generate negative file
    if not NEGATIVE_PATH.exists():

        print("\nERROR: Negative folder not found.")
        return

    total_negatives = generate_negative_file()

    if total_negatives == 0:

        print("\nERROR: No negative images found.")
        return

    # Ask sample dimensions
    print("\n------------------------------------------")
    print(" SAMPLE WINDOW DIMENSIONS")
    print("------------------------------------------")

    print("Choose dimensions appropriate for your object.")
    print("Default: 24 x 24 pixels")

    try:

        width_input = input(
            f"Sample width [{DEFAULT_WIDTH}]: "
        ).strip()

        height_input = input(
            f"Sample height [{DEFAULT_HEIGHT}]: "
        ).strip()

        sample_width = (
            int(width_input) if width_input else DEFAULT_WIDTH
        )

        sample_height = (
            int(height_input) if height_input else DEFAULT_HEIGHT
        )

        if sample_width <= 0 or sample_height <= 0:
            raise ValueError()

    except ValueError:

        print("ERROR: Invalid dimensions.")
        return

    # Prepare output directory
    SAMPLES_PATH.mkdir(parents=True, exist_ok=True)

    # Remove previous vec file
    if VEC_FILE.exists():
        VEC_FILE.unlink()

    # Build command
    command = [
        executable,
        "-info", str(ANNOTATION_FILE),
        "-num", str(total_objects),
        "-w", str(sample_width),
        "-h", str(sample_height),
        "-vec", str(VEC_FILE)
    ]

    if SHOW_SAMPLES:
        command.append("-show")

    print("\n------------------------------------------")
    print(" GENERATING POSITIVE SAMPLES")
    print("------------------------------------------")

    print("\nCommand:")
    print(subprocess.list2cmdline(command))

    # Execute OpenCV
    try:

        result = subprocess.run(
            command,
            cwd=str(BASE_PATH),
            check=False
        )

        if result.returncode != 0:

            print("\nERROR: opencv_createsamples failed.")
            return

    except Exception as error:

        print(f"\nExecution error: {error}")
        return

    # Check output
    if not VEC_FILE.exists() or VEC_FILE.stat().st_size == 0:

        print("\nERROR: Vec file was not generated correctly.")
        return

    print("\n------------------------------------------")
    print(" GENERATION COMPLETED")
    print("------------------------------------------")

    print(f"Positive images: {total_objects}")
    print(f"Negative images: {total_negatives}")
    print(f"Sample dimensions: {sample_width} x {sample_height}")

    print(f"\nVector file: {VEC_FILE}")
    print(f"Background file: {NEGATIVE_FILE}")

    print(f"Vec file size: {VEC_FILE.stat().st_size / 1024:.2f} KB")

    print("\nReady for the next module!")


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    main()
