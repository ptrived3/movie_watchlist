"""
File: auth.py

Every team must implement authentication on all non-public endpoints. Your team chooses **one** of the two following strategies:
"""

import os
import secrets
from dotenv import load_dotenv
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


load_dotenv()       # load out current env into our program

security = HTTPBasic()      # basic auth scheme

# get the stores username and password from .env
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")

# if no credentials
if USERNAME is None or PASSWORD is None:
    raise RuntimeError("API_USERNAME and API_PASSWORD must be set in .env")


def verify(credentials: HTTPBasicCredentials = Depends(security)):
    print(">>> VERIFY IS RUNNING <<<")   # temporary debug line
    print("SENT username:", repr(credentials.username), "password:", repr(credentials.password))
    print("EXPECTED username:", repr(USERNAME), "password:", repr(PASSWORD))

    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid username or password",
            headers = {"WWW-Authenticate": "Basic"},
        )
    return credentials.username