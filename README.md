# Brain Stroke Detector


## Objective

This repository contains the capstone project for the [ML Zoomcamp](https://github.com/alexeygrigorev/mlbookcamp-code) course provided by [DataTalks.Club](https://datatalks.club/). The brain stroke detector is currently available online at [http://stroke.peco602.com/](http://stroke.peco602.com/).


## Context

The objective of this project is to develop a stroke detector for brain CT scans. Stroke is the second leading cause of death and the major cause of disability in the world, with an annual mortality of 5.5 million [[ref](https://pubmed.ncbi.nlm.nih.gov/29791947/)]. In 2017, the stroke-related costs was 45.5 billion USD in USA [[ref](https://pubmed.ncbi.nlm.nih.gov/33501848/)] and 60 billion Eur in Europe, with health care accounting for 27 billion EUR (45%), representing 1.7% of health expenditure [[ref](https://pubmed.ncbi.nlm.nih.gov/32232166/)].


## Dataset

The CT scan image dataset can be downloaded from Kaggle at this [link](https://www.kaggle.com/datasets/afridirahman/brain-stroke-ct-image-dataset) and contains both brains affected by a stroke and healthy ones.


## Deployment

The service is dockerised and can be easily deployed via the following steps:

1. Clone the `brain-stroke-detector` repository locally:

    ```bash
    $ git clone https://github.com/Peco602/brain-stroke-detector.git
    ```

2. Install the pre-requisites necessary to run the service:

    ```bash
    $ cd brain-stroke-detector
    $ sudo apt install make
    $ make prerequisites
    ```

    It is also suggested to add the current user to the `docker` group to avoid running the next steps as `sudo`:

    ```bash
    $ sudo groupadd docker
    $ sudo usermod -aG docker $USER
    ```

    then, logout and log back in so that the group membership is re-evaluated.

3. Pull the Docker images:

    ```bash
    $ make pull
    ```

4. Launch the service:

    ```bash
    $ make run
    ```

Once ready, the following services will be available:

| Service | Port | Interface | Description |
| --- | --- | --- | --- |
| Flask | 8080 | 0.0.0.0 | API service |
| Streamlit | 8051 | 0.0.0.0 | Web application |


## Testing

The stroke detector can be accessed via the Streamlit web application available at `http://localhost:8051` or by sending the CT scans to be tested directly to the service APIs via `curl`:

```bash
$ curl -F "img=@./data/normal.jpg" localhost:8080/predict
{"stroke": false}
$ curl -F "img=@./data/stroke.jpg" localhost:8080/predict
{"stroke": true}
```


## Disposal

The service can be disposed via:

```
$ make kill
```


## Training

The Jupyter notebook `notebook.ipynb` contains the model experiments. A Convolutional Neural Network (CNN) is used to perform stroke detection on the CT scan image dataset. Since the dataset is small, the training of the entire neural network would not provide good results so the concept of Transfer Learning is used to train the model to get more accurate results. Transfer Learning represents a method wherein a model developed for a particular task is used as a starting point for another task. In particular, the `InceptionV3` model with `imagenet` weights will be used for the current task.

The training can be performed again via the following steps:

1. Download the stroke dataset from [here]((https://www.kaggle.com/datasets/afridirahman/brain-stroke-ct-image-dataset))

2. Extract the dataset in the `data` folder with the following structure:

    ```
    data
        Brain_Data_Organised
            Normal
            Stroke
    ```

3. Configure the development evironment:

    ```bash
    $ make setup
    ```

4. Launch the training script:

    ```bash
    $ make train
    ```

5. Re-build the container with the re-trained model:

    ```bash
    $ make build
    ```

5. Launch the service:

    ```
    $ make run
    ```


## GitHub Actions

- **Continuous Integration**: On every push and pull request on `main` and `dev` branches, the Docker images are built, tested and then pushed to DockerHub.


## Applied technologies

| Name | Scope |
| --- | --- |
| Jupyter Notebooks | Exploratory data analysis and selection of the best model. |
| Docker | Application containerization. |
| Docker-Compose | Multi-container Docker applications definition and running. |
| Flask | Web server. |
| pytest | Python unit testing suite. |
| pylint | Python static code analysis. |
| black | Python code formatting. |
| isort | Python import sorting. |
| Pre-Commit Hooks | Simple code issue identification before submission. |
| GitHub Actions | CI/CD pipelines. |
| Streamlit | Web application |


## Disclaimer

This prediction service has been developed as the capstone project for the ML Zoomcamp course from DataTalks.Club. It does not provide medical advice and it is intended for informational purposes only. It cannot be considered a substitute for professional medical advice, diagnosis or treatment. Never ignore professional medical advice in seeking treatment because of something you have read here.
