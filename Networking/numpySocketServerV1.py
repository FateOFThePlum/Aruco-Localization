import logging
import cv2
from numpysocket import NumpySocket

logger = logging.getLogger("Simple Server")
logger.setLevel(logging.INFO)

with NumpySocket() as s:
    s.bind(("", 9999))
    s.listen()
    conn, addr = s.accept()
    while conn:
        logger.info(f"Connected: {addr}")
        frame = conn.recv()

        logger.info("Array received")
        logger.info(frame)
        try:
            cv2.imshow("Frame", frame[0][0])
        except IndexError:
            print("Index Error")
        cv2.waitKey(1)

    logger.info(f"Disconnected: {addr}")