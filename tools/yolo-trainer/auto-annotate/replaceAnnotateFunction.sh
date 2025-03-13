#!/bin/bash  
# This script is to modify the annotator.py file from Ultralytics to generate auto annotations in required format

cp /usr/local/lib/python3.10/dist-packages/ultralytics/data/annotator.py /usr/local/lib/python3.10/dist-packages/ultralytics/data/annotator_backup.py

cp annotator.py /usr/local/lib/python3.10/dist-packages/ultralytics/data/annotator.py

