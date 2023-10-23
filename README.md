# Super-Awesome-Totally-Cool Research Project #1

<div align="center" style="margin-bottom: 20px;">
  <img src="https://manimresearchstudy.onrender.com/assets/img/Github%20Logo.png" alt="Project Logo">
</div>

<div align="center">
  <img src="https://img.shields.io/badge/version-0.8.2-green" alt="Version">
  <a href="https://colab.research.google.com/drive/1cq88wa9YAMwSbDkBDCzqMuhMvcGvpMEa?usp=sharing">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab">
  </a>
  <img src="https://img.shields.io/badge/York_University_Department_of_Psychology-red" alt="Department">
</div>

--- 
## Table of Contents
- [Introduction](#introduction)
- [Tools & Process](#tools--process)
- [Getting Started](#getting-started)
- [Research Goal](#research-goal)
- [Features](#features)
- [License](#license)
- [Acknowledgements](#acknowledgements)
---

## Introduction 

### 🐨

Welcome to the **Super-Awesome-Totally-Cool Research Project #1** repository!  &copy; 2023 
 
Are you interested in conducting online research studies with participants? User experience research? Or the ability to A/B test a product, design or idea?

This repo should help you with that!

## Tools & Process

### 🐨

List of all the software, tools, libraries, and services I used in order to complete this research project. Here is an overview of how they all intermingle:

![Overview](https://manimresearchstudy.onrender.com/assets/img/diagram.png)

Manim was used to create the educational animations for **Group A** to view. You can find the link to the Google Colab notebook above.

## Getting Started

### 🐨

The requirements.txt file is fairly small:

```py
fastapi==0.79.0
uvicorn==0.18.2
Jinja2==3.1.2
filelock==3.0.12
```

Once you have cloned the repository, navigate to your terminal and run this command:

```shell
uvicorn main:app --reload
```

This will start a server on `http://127.0.0.1:8000` in your browser

## Research Goal

### 🐨

> This research project is arranged by Dr. Herbert; a full-time faculty member in the Psychology Department, Faculty of Health

This research project aims to investigate the effectiveness of using Manim animations in educating participants on core statistical concepts. The study will focus on concepts that are taught in 2000-level statistics courses at York University: 
1. Central tendency
and
2. Variability

The project will involve creating animations using the Manim graphic engine to explain these statistical concepts. Participants will then be asked to complete a pre-survey before being randomly assigned to either an animated or static content group. One group will view dynamic animations created by Manim with a voice-over explaining the concepts, while the other group will view the same type of statistics content via a static source such as an image or infographic.

After viewing the content, participants will take a post-survey to evaluate their understanding of the statistical concepts. The data collected from the surveys will be compared between the animated and static content groups to identify any differences in learning outcomes. This study aims to contribute to the ongoing discussion on the use of animations in educational content and provide insights into their effectiveness as a learning tool.


## Features

### 🐨

The web app was designed with these key features in mind:

- Feature 1: Users navigate to a homepage that introduces the study's goals and asks for user consent.
- Feature 2: Users who wish to participate are randomly assigned to two groups; A or B.
- Feature 3: Users are asked to participate in surveys that were made in Qualtrics.
- Feature 4: Participants are automatically redirected to the last page that debriefs them on the study.

The idea was to ensure that user experience was never sacrificed. The content should be delivered in an easy and streamlined way, to fit within accessibility guidelines and to be responsive so they could interact with it on their preferred device of choice.


```mermaid
graph LR
    A[homepage] --> B[consent page]
    B[consent page] --> C[presurvey prompt]
    C[pre-survey prompt] --> |qualtrics| E[group assignment]
    C[pre-survey prompt] --> |pre-survey| E[group assignment]
    E[group assignment] --> F[Group A]
    E[group assignment] --> G[Group B]
    F[Group A] --> H[post-survey prompt A]
    G[Group B] --> I[post-survey prompt B]
    H[post-survey prompt A] --> |qualtrics| J[Debrief page]
    I[post-survey prompt B] --> |post-survey| J[Debrief page]
```
