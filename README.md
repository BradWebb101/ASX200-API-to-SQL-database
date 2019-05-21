# ASX200 - API to SQL database

## Table of contents
* [Introduction](#Introduction)
* [Technologies](#Technologies)
* [Setup](#Setup)

## Introduction 
This project is to reduce script running time and allow for easier access to ASX200 stock prices due to limitations on free stock price API's requests. 
This script is running on my Raspberry Pi, using Cron as a scheduler to request updated stock prices at close of ASX market and updates SQL server. Using SQL alchemy to SQL queries to create database, update tables and report on stock updates. 

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