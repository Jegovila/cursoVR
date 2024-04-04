from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

initBB = None
fps = None
frame = None
at = ""
tracker = None

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.legacy.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.legacy.TrackerTLD_create,
    "medianflow": cv2.legacy.TrackerMedianFlow_create,
    "mosse": cv2.legacy.TrackerMOSSE_create,
    "goturn": cv2.TrackerGOTURN_create
}

at = "csrt"

def mouse_click(event, x, y, flags, param):
    global tracker
    global initBB
    global fps
    global frame
    if event == cv2.EVENT_LBUTTONDOWN:
        tracker = OPENCV_OBJECT_TRACKERS[at]()
        initBB = None
        xt = max(x-50, 0)
        yt = max(y-50, 0)
        initBB = [xt, yt, 100, 100]
        # Empieza el seguimiento y se actualizan los FPS
        tracker.init(frame, initBB)
        fps = FPS().start()
        #print(initBB)


tracker = OPENCV_OBJECT_TRACKERS[at]()
vs = cv2.VideoCapture(2, cv2.CAP_DSHOW)
    
# inicializar el estimador de FPS
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_click)

while True:
    # Captura el frame actual
    _, frame = vs.read()

    # resize tdel frame
    frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_LINEAR)
    (H, W) = frame.shape[:2]

    # revisar si ya estamos siguiendo un objeto
    if initBB is not None:
        # tomar la nueva BB del objeto
        (success, box) = tracker.update(frame)
        # checar si el seguimiento fue un éxito
        j = 1
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                (0, 255, 0), 2)
        else:
            j = 0
        
        
        # actualiza el contador de FPS
        fps.update()
        fps.stop()
        # Inicializa la información en pantalla
        error_x = 1 - (x+(w/2))/(W/2)
        error_y = 1 - (y+(h/2))/(H/2)
        
        duty_x = 200 * (x+(w/2))/(W) - 100
        duty_y = 200 * (y+(h/2))/(H) - 100

        info = [
            ("Tracker", at),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
            ("Error x", "{:.2f}".format(error_x)),
            ("Error y", "{:.2f}".format(error_y)),
        ]
        # Escribe la información en pantalla
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    # Mostrar el frame
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
                break

vs.release
# cerrar ventanas
cv2.destroyAllWindows()