import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
import cv2
from cv_bridge import CvBridge
import os
from pathlib import Path

# Input and output directories
INPUT_DIR = "mcap-Files"  # Set to the root directory containing your MCAP files
OUTPUT_DIR = "Frames"

class FrameExtractor():

    def __init__(self):
        self.count = 1
        self.bridge = CvBridge()
        self.reader = rosbag2_py.SequentialReader()

    def clean_up(self):
        del self.reader

    def load_mcap(self, input_bag):
        input_bag = str(input_bag)
        self.reader.open(
            rosbag2_py.StorageOptions(uri=input_bag, storage_id="mcap"),
            rosbag2_py.ConverterOptions(input_serialization_format="cdr", output_serialization_format="cdr"),
        )

        self.topic_types = self.reader.get_all_topics_and_types()
        relative_path = os.path.relpath(os.path.dirname(input_bag), INPUT_DIR)
        self.output_loc = os.path.join(OUTPUT_DIR, relative_path, Path(input_bag).stem)
        
        os.makedirs(self.output_loc, exist_ok=True)
        
        for view in ["front", "left", "right", "rear", "stereo_left", "stereo_right"]:
            os.makedirs(os.path.join(self.output_loc, view), exist_ok=True)

    def topic_type_name(self, topic_name):
        for topic_type in self.topic_types:
            if topic_type.name == topic_name:
                return topic_type.type
        raise ValueError(f"Topic {topic_name} not in bag")

    def image_write(self, message, view):
        cv2_image = self.bridge.imgmsg_to_cv2(message, "bgr8")
        image_path = os.path.join(self.output_loc, view, f"frame_{self.count:06d}.jpg")
        cv2.imwrite(image_path, cv2_image)
        self.count += 1

    def extraction(self):
        topic_list = ["/sensors/camera/front/image", "/sensors/camera/rear/image",
                      "/sensors/camera/left/image", "/sensors/camera/right/image",
                      "/sensors/camera/stereo_left/image", "/sensors/camera/stereo_right/image"]
        
        while self.reader.has_next():
            topic, data, timestamp = self.reader.read_next()
            if topic in topic_list:
                view = topic.split("/")[3]
                msg_type = get_message(self.topic_type_name(topic))
                msg = deserialize_message(data, msg_type)
                self.image_write(msg, view)
        
        self.clean_up()


def process_directory(input_dir, output_dir):
    """Recursively processes directories to find MCAP files and extract frames."""
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".mcap") and "lidar" not in file:
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                extractor = FrameExtractor()
                extractor.load_mcap(file_path)
                extractor.extraction()
                del extractor

if __name__ == "__main__":
    process_directory(INPUT_DIR, OUTPUT_DIR)
    print("Frame extraction complete.")
