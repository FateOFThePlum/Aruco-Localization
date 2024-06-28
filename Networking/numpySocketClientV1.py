import logging
import numpy as np
from numpysocket import NumpySocket


logger = logging.getLogger("Simple Client")
logger.setLevel(logging.INFO)

with NumpySocket() as s:
    s.connect(("localhost", 9999)) #TODO: IP address will need to be configured for individual use. 

    logger.info("Sending Numpy Array:")
    frame = np.arange(1000)
    s.sendall(frame)