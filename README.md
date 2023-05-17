# Welcome to TLDR

---

---

![tlfr_logo](https://github.com/TooLong-DidntRead/tldr_api/assets/113124260/94245722-0389-4ad1-9fa2-af8136e8368b)

## Table of Contents
- [Product Overview](#product-overview)
- [MVP and Future Features](#mvp-and-future-features)
- [Deployment](#deployment)
- [Built With](#built-with)
- [Database Schema](#database-schema)
- [Endpoints](#end-points)
- [Running the Test Suit](#running-the-test-suit)
- [Front-End Repository](#front-end-respository)
- [Contributors](#contributors)

Product Overview

Our web platform is a tool that helps you understand the terms and conditions of services you sign up for in a simpler way. Instead of having to read through long and complex legal documents, you can copy and paste them into our platform and select the things you're most concerned about, like privacy or recurring payments. Our platform will then show you a summary of how those specific things might affect you, with an overall score that helps you see how good or bad they are. We also give you suggestions for what you can do if you don't like what you see. We want to make it easier for you to understand what you're agreeing to when you use a service, and help you protect your rights.

## MVP and Future Features

### MVP

* Integration with ChatGPT's API: The first and most important build out is to integrate our platform with ChatGPT's API, which will analyze the terms and conditions of service providers and generate easy-to-read summaries.

### Future Features

* User Authentication and Authorization: To ensure the security of our users' data, we need to implement a robust authentication and authorization system that restricts access to sensitive information only to authorized users.
* Data Storage and Retrieval: We need to implement a system for storing and retrieving user data, including the terms and conditions they input and their selected concerns, follow-up actions, and other preferences. This data will be used to generate summaries and suggestions for future interactions.
* Follow-up Actions Automation: To enable users to take follow-up actions with ease, we need to build out a system for automating tasks such as generating emails, creating events in Google Calendar, and sending reminders. This will help users take control of their interactions with service providers and protect their interests.
* Scalability: As the user base grows, we need to ensure that our platform is scalable and can handle large volumes of data and traffic. We need to implement best practices for performance optimization, load balancing, and fault tolerance to ensure that the platform remains stable and reliable.

## Deployment
![Render](https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white)

## Built With
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

![CircleCI](https://img.shields.io/badge/circleci-343434?style=for-the-badge&logo=circleci&logoColor=white)

## Database Schema

## Endpoints

<br>

<details>
  
  <summary>POST:User TOS Concerns Summary</summary>
  
  Request:
  
  ```JS
  POST /api/v1/processTOS
  ```
  
  Params: 

  | Name | Requirement | Type | Description |
  | ----- | ----------- | -----| -------------- | 
  | `tos` | Required | string | Terms of Service
  | `concerns` | Optional | string | User Concerns

  <i>Note: </i>

  <br>

  Response: 

  | Result | Status |
  | ------- | ------| 
  | `Success` | 201 |
  | `Failure`| 401 |
  | `Internal Server Error` | 500 |


  ```JSON
{
    "data": {
        "concerns": {
            "privacy": {
                "ranking": 10,
                "impact": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                "actionable": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
            },
            "security": {
                "ranking": 4,
                "impact": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                "actionable": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
            },
            "intellectualProperty": {
                "ranking": 9,
                "impact": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                "actionable": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
            },
            "liability": {
                "ranking": 10,
                "impact": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                "actionable": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
            },
            "cancellation": {
                "ranking": 3,
                "impact": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                "actionable": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
            },
            "payment": {
                "ranking": 1,
                "impact": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                "actionable": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
            }
        }
    }
}
  ```
 </details>
 
 <br>
  
 ## Running the Test Suit

 1. `Navigate to desired directory`
 1. `Run git clone git@github.com:TooLong-DidntRead/tldr_api.git`
 1. `Run cd tldr_api`
 1. `Run pip install -r requirements.txt`
 1. `Run pip freeze`
 1. `Run python manage.py migrate`
 1. `Run pytest`
 
 ## Front-End Repository 
 
 [TLDR Front-End Repo](https://github.com/TooLong-DidntRead/tldr_fe)

 ## Contributors 

| **Isaac Alter** [Github](https://github.com/Isaac3924) | **Jesus Borjas** [Github](https://github.com/Jesusborjas006) | **Chrissy Coope** [Github](https://github.com/chrissycooper) | **Axel De La Guardia** [Github](https://github.com/axeldelaguardia) | **Jason Kirchman** [Github](https://github.com/kirch1) | **Elle Majors** [Github](https://github.com/Elle-M) | **Hady Matar** [Github](https://github.com/hadyematar23) | **Conner Van Loan** [Github](https://github.com/C-V-L) |
  



