# Event Management API

This repository contains the backend codebase for an Event Management API.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Usage](#usage)
- [API Documentation](#api-documentation)


## Description

The Event Management API allows users to schedule, retrieve, update, and delete events. It also includes advanced features such as sorting events, event reminders, batch operations, rate limiting, and real-time notifications using WebSockets.

## Features

- Schedule a new event.
- Retrieve a list of all scheduled events.
- Retrieve details of a specific event.
- Update details of a specific event.
- Delete a specific event.
- Sort events by date, popularity, or creation time.
- Event reminders 30 minutes before the event's scheduled time.
- Batch operations for creating, updating, or deleting multiple events.
- Rate limiting to prevent API abuse.
- Allow users to subscribe to events and receive notifications for updates or cancellations.

## Usage

- First clone this repo by using following command
````
git clone https://github.com/Mushkinides/eventsapi.git
cd eventsapi
````

- Then install fastapi using the "all" flag 
````
pip install fastapi[all]
````

- Then go to repo folder in your local computer and run the follwoing command
````
uvicorn main:app --reload
````

## After run this API you need a database in postgres 
Create a database in postgres then create a file name .env and write the following things in you file 
````
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = passward_that_you_set
DATABASE_NAME = name_of_database
DATABASE_USERNAME = User_name
````

# API Documentation
````
http://127.0.0.1:8000/docs 
````
