#    ┌──────────────────────────────────────────────────────────┐
#    │                                                          │
#    │                        StereoPair                        │
#    │                                                          │
#    │       A super class representing a pair of images.       │
#    │                                                          │
#    └──────────────────────────────────────────────────────────┘
from PIL import Image


class StereoPair:

    def __init__(self, left: Image = None, right: Image = None, name: str = None, timestamp: str = None):
        self.left_image: Image = left
        self.right_image: Image = right
        self.timestamp: str = timestamp
        self.name: str = name
