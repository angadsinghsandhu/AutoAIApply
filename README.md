# AutoAIApply

This is a simple project to demonstrate how to apply AutoAI model in a web application. The project is based on the [AutoAI](https://cloud.ibm.com/docs/watson-studio/visual-recognition/autoai-overview.html) model created in Watson Studio. The model is trained to predict the price of a car based on its features.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. You can download it from [here](https://www.python.org/downloads/).

### Installing

1. Clone the repository

```shell
git clone
```

1. Install `uv` as the package manager

```shell
pip install uv
```

1. Create a virtual environment

```shell
uv venv
```

1. Activate the virtual environment

```shell
source venv/bin/activate
```

1. Install the dependencies

```shell
uv sync
```

1. Run the application

```shell
python -m main
```

### Usage

Applications have the following faucets:

- Checking for new job applications (and adding them to the database)
- Visiting the job application page and adding information about the job application to the database
- Filling out the job application form
- Checking Email for the status of the job application