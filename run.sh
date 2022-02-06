#!/usr/bin/env bash

export GOOGLE_APPLICATION_CREDENTIALS="${PWD}/service-account-file.json"

singularity exec container.sif python example.py
