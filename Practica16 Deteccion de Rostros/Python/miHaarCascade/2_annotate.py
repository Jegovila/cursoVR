
import cv2
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================

BASE_PATH = Path(__file__).resolve().parent

ANNOTATION_PATH = BASE_PATH / "annotations"
ANNOTATION_PATH.mkdir(parents=True, exist_ok=True)

ANNOTATION_FILE = ANNOTATION_PATH / "positives.txt"
POSITIVE_PATH = BASE_PATH / "dataset" / "positive"

WINDOW_NAME = "Haar Cascade - ROI Annotation"

MAX_WIDTH = 1100
MAX_HEIGHT = 750

# ==========================================
# LOAD IMAGES
# ==========================================

extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]

images = []

for ext in extensions:
    images.extend(POSITIVE_PATH.glob(ext))

images = sorted(images)

if not images:
    print("No se encontraron imágenes positivas.")
    exit()


# ==========================================
# LOAD EXISTING ANNOTATIONS
# ==========================================

annotations = {}

if ANNOTATION_FILE.exists():

    with open(ANNOTATION_FILE, "r") as file:

        for line in file:

            parts = line.strip().split()

            if len(parts) >= 2:

                filename = parts[0].replace("\\", "/")

                try:
                    count = int(parts[1])

                    if len(parts) == 2 + count * 4:

                        rois = []

                        for i in range(count):

                            offset = 2 + i * 4

                            x, y, w, h = map(
                                int,
                                parts[offset:offset + 4]
                            )

                            rois.append((x, y, w, h))

                        annotations[filename] = rois

                except ValueError:
                    pass


# ==========================================
# FUNCTIONS
# ==========================================

def get_relative_path(image_path):

    # Path relative to annotations/positives.txt
    return Path("..", "dataset", "positive", image_path.name).as_posix()


def save_annotations():

    with open(ANNOTATION_FILE, "w") as file:

        for image_path in images:

            filename = get_relative_path(image_path)

            if filename in annotations:

                rois = annotations[filename]

                values = [filename, str(len(rois))]

                for x, y, w, h in rois:
                    values.extend(map(str, [x, y, w, h]))

                file.write(" ".join(values) + "\n")

    print(f"Anotaciones guardadas: {ANNOTATION_FILE}")


# ==========================================
# INTERFACE VARIABLES
# ==========================================

index = 0

rois = []

drawing = False
start_point = None
current_point = None

display_scale = 1.0


# ==========================================
# MOUSE CALLBACK
# ==========================================

def mouse_callback(event, x, y, flags, param):

    global drawing
    global start_point
    global current_point
    global rois

    if event == cv2.EVENT_LBUTTONDOWN:

        drawing = True

        start_point = (x, y)
        current_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE and drawing:

        current_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP and drawing:

        drawing = False

        current_point = (x, y)

        x1 = min(start_point[0], x)
        y1 = min(start_point[1], y)

        x2 = max(start_point[0], x)
        y2 = max(start_point[1], y)

        w = x2 - x1
        h = y2 - y1

        if w > 5 and h > 5:

            # Convert display coordinates to original image
            x1 = int(x1 / display_scale)
            y1 = int(y1 / display_scale)

            w = int(w / display_scale)
            h = int(h / display_scale)

            rois.append((x1, y1, w, h))

            print(f"ROI #{len(rois)} added: {(x1, y1, w, h)}")

        start_point = None
        current_point = None


# ==========================================
# DISPLAY FUNCTION
# ==========================================

def show_image():

    global display_scale

    image_path = images[index]

    frame = cv2.imread(str(image_path))

    if frame is None:
        return

    height, width = frame.shape[:2]

    display_scale = min(
        MAX_WIDTH / width,
        MAX_HEIGHT / height,
        1.0
    )

    new_width = int(width * display_scale)
    new_height = int(height * display_scale)

    display = cv2.resize(
        frame,
        (new_width, new_height)
    )

    # Draw all saved/current ROIs
    for i, (x, y, w, h) in enumerate(rois):

        p1 = (
            int(x * display_scale),
            int(y * display_scale)
        )

        p2 = (
            int((x + w) * display_scale),
            int((y + h) * display_scale)
        )

        cv2.rectangle(
            display,
            p1,
            p2,
            (0, 255, 0),
            2
        )

        cv2.putText(
            display,
            str(i + 1),
            (p1[0], max(20, p1[1] - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # Draw temporary ROI while dragging
    if drawing and start_point and current_point:

        cv2.rectangle(
            display,
            start_point,
            current_point,
            (0, 255, 255),
            2
        )

    filename = get_relative_path(image_path)

    annotated_count = len(annotations)

    cv2.putText(
        display,
        f"Image: {index + 1}/{len(images)}",
        (15, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        display,
        f"ROI: {len(rois)}",
        (15, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0),
        2
    )

    cv2.putText(
        display,
        f"Annotated images: {annotated_count}/{len(images)}",
        (15, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    instructions = [
        "Mouse: Draw ROI",
        "A: Save and next | N: Skip | B: Back",
        "R: Remove last ROI | X: Clear all ROIs",
        "Q: Save and quit"
    ]

    for i, instruction in enumerate(instructions):

        cv2.putText(
            display,
            instruction,
            (15, new_height - 85 + i * 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )

    cv2.imshow(WINDOW_NAME, display)


# ==========================================
# MAIN PROGRAM
# ==========================================

# Load first image's existing annotations
filename = get_relative_path(images[index])

if filename in annotations:
    rois = list(annotations[filename])

cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

print("--------------------------------------")
print(" HAAR CASCADE - MULTIPLE ROI ANNOTATION")
print("--------------------------------------")
print("Mouse: Draw ROI")
print("A: Save and next")
print("N: Next without annotation")
print("B: Previous image")
print("R: Remove last ROI")
print("X: Remove all ROIs")
print("Q: Save and quit")
print("--------------------------------------")

running = True

while running:

    show_image()

    key = cv2.waitKey(20) & 0xFF

    filename = get_relative_path(images[index])

    # SAVE AND NEXT
    if key == ord('a'):

        if len(rois) > 0:

            annotations[filename] = list(rois)

            save_annotations()

            if index < len(images) - 1:

                index += 1

                filename = get_relative_path(images[index])

                rois = list(annotations.get(filename, []))

            else:

                print("¡Última imagen!")
                running = False

        else:

            print("Selecciona al menos un ROI.")

    # NEXT WITHOUT ANNOTATION
    elif key == ord('n'):

        rois = []

        if index < len(images) - 1:

            index += 1

            filename = get_relative_path(images[index])

            rois = list(annotations.get(filename, []))

        else:

            print("Última imagen.")
            running = False

    # PREVIOUS IMAGE
    elif key == ord('b'):

        if index > 0:

            index -= 1

            filename = get_relative_path(images[index])

            rois = list(annotations.get(filename, []))

    # REMOVE LAST ROI
    elif key == ord('r'):

        if rois:

            rois.pop()

            print("Último ROI eliminado.")

    # REMOVE ALL ROIS
    elif key == ord('x'):

        rois = []

        print("Todos los ROI eliminados.")

    # SAVE AND QUIT
    elif key == ord('q'):

        if rois:
            annotations[filename] = list(rois)

        save_annotations()

        running = False


# ==========================================
# FINISH
# ==========================================

# Save current image if it has ROIs
if rois:
    filename = get_relative_path(images[index])
    annotations[filename] = list(rois)

save_annotations()

cv2.destroyAllWindows()

total_rois = sum(len(v) for v in annotations.values())

print("--------------------------------------")
print("ANNOTATION FINISHED")
print(f"Total images: {len(images)}")
print(f"Annotated images: {len(annotations)}")
print(f"Total ROIs: {total_rois}")
print("--------------------------------------")
