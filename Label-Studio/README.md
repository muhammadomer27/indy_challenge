# Steps to Setup and Use Label Studio

1. Set up Label Studio in a virtual enviroment by following the below steps:
    ```
    python3 -m venv labelstudioenv

    source ./labelstudioenv/bin/activate

    pip install -r requirements.txt

    label-studio
    ```
    Now label studio should start in your default browser.

2. Create the following path
    ```
    mkdir /yolo/datasets/one/
    ```

3. Copy all the images in **selectedImages** folder which was created earlier and keep it inside **/yolo/datasets/one/images** and keep all the labels in the auto annotated folder in **/yolo/datasets/one/labels** .Create a **classes.txt** as well and keep it in **/yolo/datasets/one/**.

4. Use the tool provided by Label Studio to convert the auto annotated files into label studio format. To use the tool, run the following command:

    ```
    label-studio-converter import yolo -i /yolo/datasets/one -o /yolo/datasets/output.json --image-root-url "/data/local-files/?d=one/images"
    ```

5. Use the generated output.json file to import into Label Studio

6. Do annotations using label studio and export them in YOLO format. 

7. All the exported labels in the exported zip file.