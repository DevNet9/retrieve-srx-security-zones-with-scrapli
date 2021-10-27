# Get Security Zones with Scrapli

[![N|Solid](https://upload.wikimedia.org/wikipedia/commons/3/31/Juniper_Networks_logo.svg)](https://junos-ansible-modules.readthedocs.io/en/stable/)

## Overview

This example will show how to retrieve security zone information on Juniper's SRX firewalls.

In addition to the Python script, this project also ships with additional tools to help you along your way. You will find a Dockerfile for running the project in an isolated environment, and an Invoke `tasks.py` file for those of us that hate typing out everything all the time.

## ⚙️ `How it works`

The data is collected from the firewalls by issuing NETCONF RPCs to retrieve the data as XML, to which we will convert into a Python dictionary.

Let's take a second to review the documentation in the `files/docs/` directory.

Name | Description
---- | -----------
[app_async.py](files/docs/app_async.py.rst) | Retrieve security zone information from SRX with `asyncio`
[app_sync.py](files/docs/app_sync.py.rst) | Retrieve security zone information from a single SRX

## 📝 `Dependencies`

Refer to the Poetry Lock file located at [poetry.lock](poetry.lock) for detailed descriptions on each package installed.

## 🚀 `Executing the script`

This project provides two unique methods of executing the playbook:

[Executing with Docker](files/docs/execute_with_docker.rst) | Execute with Docker

[Executing with Python](files/docs/execute_with_python.rst) | Execute with Python
