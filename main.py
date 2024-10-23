"""
FILE: main.py

DESCRIPTION: This file is the main entry point for the application. It is responsible for
    initializing the application and starting the main event loop.
"""
# TODO: import the necessary modules

import chromium
import openai
import transformers


# TODO: parse the correct args
def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description="A simple image viewer application.")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    # TODO: initialize the application
    # TODO: get the list of job application links
    # TODO: automate Notion webhooks
    # TODO: use chromium to open the job application links
    # TODO: download application HTML
    # TODO: remove Boilerplate HTML
    # TODO: use openai get all the questions nad metadata
    # TODO: add job application to Notion database
    # TODO: use openai and premade profile context to write custom answers
    # TODO: add answers to the application to the Notion database

    # TODO: add cron job to check email inbox for job application responses
    # TODO: use openai to classify the email
    # TODO: update database for job application status