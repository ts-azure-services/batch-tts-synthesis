#!/usr/bin/env python
# coding: utf-8
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
# Source: https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch-synthesis

import argparse
import json
import logging
import os
import sys
import time
# from pathlib import Path
from dotenv import load_dotenv
import requests

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
        format="[%(asctime)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
logger = logging.getLogger(__name__)

# Your Speech resource key and region
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
load_dotenv('./variables.env')

SUBSCRIPTION_KEY = os.environ.get('SPEECH_KEY')
SERVICE_REGION = os.environ.get('SPEECH_LOCATION')

NAME = "Simple synthesis"
DESCRIPTION = "Simple synthesis description"

# The service host suffix.
# For azure.cn the host suffix is "customvoice.api.speech.azure.cn"
SERVICE_HOST = "customvoice.api.speech.microsoft.com"


def submit_synthesis(voice=None):
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Content-Type': 'application/json'
    }

    # with open(Path(__file__).absolute().parent.parent / 'Gatsby-chapter1.txt', 'r') as f:
    #     text = f.read()

    with open('./inputs/sample.txt', 'r') as f:
        text = f.read()

    payload = {
        'displayName': NAME,
        'description': DESCRIPTION,
        "textType": "PlainText",
        'synthesisConfig': {
            "voice": voice,
        },
        # Replace with your custom voice name and deployment ID if you want to use custom voice.
        # Multiple voices are supported, the mixture of custom voices and platform voices is allowed.
        # Invalid voice name or deployment ID will be rejected.
        'customVoices': {
            # "YOUR_CUSTOM_VOICE_NAME": "YOUR_CUSTOM_VOICE_ID"
        },
        "inputs": [
            {
                "text": text
            },
        ],
        "properties": {
            "outputFormat": "audio-24khz-160kbitrate-mono-mp3",
            # "destinationContainerUrl": "<blob container url with SAS token>"
        },
    }

    response = requests.post(url, json.dumps(payload), headers=header)
    if response.status_code < 400:
        logger.info('Batch synthesis job submitted successfully')
        logger.info(f'Job ID: {response.json()["id"]}')
        return response.json()["id"]
    else:
        logger.error(f'Failed to submit batch synthesis job: {response.text}')


def get_synthesis(job_id):
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/{job_id}'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.info('Get batch synthesis job successfully')
        logger.info(response.json())
        return response.json()['status']
    else:
        logger.error(f'Failed to get batch synthesis job: {response.text}')


def download_results(job_id):
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/{job_id}'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    response = requests.get(url, headers=header)
    if response.status_code < 400:
        download_link = None
        download_link = response.json()['outputs']['result']
        if download_link:
            # Create an outputs directory
            if not os.path.exists('./outputs'):
                os.makedirs('./outputs')

            # Download response
            response = requests.get(download_link, stream=True)
            with open('./outputs/results.zip', 'wb') as fd:
                for chunk in response.iter_content(chunk_size=128):
                    fd.write(chunk)
            logger.info('Downloaded results successfully.')
    else:
        logger.error(f'Failed to download results: {response.text}')


def list_synthesis_jobs(skip: int = 0, top: int = 100):
    """List all batch synthesis jobs in the subscription"""
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis?skip={skip}&top={top}'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.info(f'List batch synthesis jobs successfully, got {len(response.json()["values"])} jobs')
        logger.info(response.json())
    else:
        logger.error(f'Failed to list batch synthesis jobs: {response.text}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Long audio tool to submit voice synthesis requests.')
    parser.add_argument('--voice', default=False, required=True, help='Specified voice.')
    args = parser.parse_args()

    # Submit job
    try:
        job_id = submit_synthesis(voice=args.voice)
    except Exception as err:
        print(err)

    # Check on job
    if job_id is not None:
        while True:
            status = get_synthesis(job_id)
            if status == 'Succeeded':
                logger.info('batch synthesis job succeeded')
                # Download results
                download_results(job_id)
                break
            elif status == 'Failed':
                logger.error('batch synthesis job failed')
                break
            else:
                logger.info(f'batch synthesis job is still running, status [{status}]')
                time.sleep(5)
