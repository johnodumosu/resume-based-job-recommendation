
# Resume-Based Job Recommendation and Skill Gap Analysis

## Project Overview
The goal of this project is to build an application that integrates an LLM and can accept a Resume or CV, and based on the skills listed on the resume, it should suggest appropriate jobs that are best fit for the users. Also, it can suggest additional skills needed for that job if not listed on the resume.

## Dataset
I used a prebuilt LLM using OpenAI, Cohere, and HuggingFace. 


## Tech Stack
➔ Python3
➔ Libraries - NLTK, spaCY, scikit-learn
➔ Tools - PyMuPDF, pdfMiner, GPT-3, Llama 2

## Development Process
### 1. Data Collection
* Gather a few diverse dataset of job descriptions and corresponding required skills.
* Collect sample resumes for testing and validation.


### 2. Preprocess Data
* Clean and preprocess job descriptions and resumes (PyMuPDF, pdfMiner).
* Extract key information such as skills, job titles, education, and experience.


### 3. Integration with LLM
* Choose a suitable LLM (e.g., GPT-3, Llama 2) for natural language understanding.
* Integrate the LLM into your application using its API.

### 4. Skill Extraction
* Utilize the LLM to extract skills from the processed resumes.
* Map the extracted skills to a standardized set for consistency.

### 5. Job Recommendation
* Use the LLM to analyze job descriptions and recommend jobs based on the extracted skills.
* Employ a matching algorithm to find the best-fit jobs.

### 6. Skill Gap Analysis
* Identify skills listed in job descriptions but not present in the user's resume.
* Suggest additional skills needed for each recommended job.

### 7. User Interface
* Develop an intuitive user interface to accept resumes and display job recommendations and skill gap analysis.

### 8. Testing and Validation
* Test the application with a variety of resumes and job descriptions.
* Validate the accuracy of job recommendations and skill gap analysis.


### 9. Deployment
* Deploy the application for public use.
* Monitor user feedback and continuously improve the recommendation algorithm.

 
 

## Architecture Diagram:
![Logo](https://project-architecture0102.s3.eu-west-2.amazonaws.com/youtube_data_engineering_architectural+diagram.jpg)










    




