# ASX200 - API ----> SQL database

## Table of contents
* [Introduction](#Introduction)
* [Technologies](#Technologies)
* [Setup](#Setup)

## Introduction 
This project is to reduce script running time and allow for easier access to ASX200 stock prices. Currently there is limited free API's for ASX200 stock prices, current API for this file has a limit of 5 requests per minute. This means over 40 minutes to run a full request for ASX200 stock prices. 
This script is running on my Raspberry Pi, using Cron as a scheduler to request updated stock rpices at close of ASX market and updates SQL server. 

## Technologies
Project was created with Python 3.7, libraries include:
*Pandas
*SQL Alchemy
*Time

## Setup
To run this project, install it locally using npm:

```
$cd .../ASX-API-SQL
$npm install
$npm start
```