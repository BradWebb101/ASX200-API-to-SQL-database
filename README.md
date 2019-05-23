# ASX200 - API to SQL database

## Table of contents
* [Introduction](#Introduction)
* [Technologies](#Technologies)
* [Setup](#Setup)

## Introduction 
This project is to reduce script running time and allow for easier access to ASX200 stock prices due request limits on free API's. 
This script is running on a Raspberry Pi, using Cron as a scheduler, The script requests stock prices at close of ASX market and updates the SQL server. Using SQL alchemy as the connection engine.

## Technologies
Project was created with Python 3.7, libraries include:
* Pandas
* SQL Alchemy
* Time

## Setup
To run this project, install it locally using npm:

```
$cd .../ASX-API-SQL
$npm install
$npm start
```