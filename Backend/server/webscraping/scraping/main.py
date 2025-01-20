from bs4 import BeautifulSoup
import requests
import json
from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

@app.get("/jobs/")
async def get_jobs(familiar_skills: str = Query(...)):
    job_list = []

    try:
        response = requests.get(
            'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=')
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch data from jobs website")
            
        soup = BeautifulSoup(response.text, 'lxml')
        jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

        for index, job in enumerate(jobs):
            try:
                published_date_elem = job.find('span', class_='sim-posted')
                if not published_date_elem or not published_date_elem.span:
                    continue
                    
                published_date = published_date_elem.span.text
                if 'few' not in published_date:
                    continue

                company_name_elem = job.find('h3', class_='joblist-comp-name')
                if not company_name_elem:
                    continue
                    
                skills_elem = job.find('span', class_='srp-skills')
                if not skills_elem:
                    continue
                    
                header_elem = job.find('header')
                if not header_elem or not header_elem.h2 or not header_elem.h2.a:
                    continue

                company_name = company_name_elem.text.strip()
                skills = skills_elem.text.strip()
                more_info = header_elem.h2.a.get('href', '')

                # Print the actual job data being processed
                print(f"\nProcessing Job {index}:")
                print(f"Company: {company_name}")
                print(f"Skills: {skills}")
                print(f"URL: {more_info}")

                if any(skill.lower() in skills.lower() for skill in familiar_skills.split(',')):
                    job_details = {
                        'Company Name': company_name,
                        'Required Skills': skills,
                        'More Info': more_info
                    }
                    job_list.append(job_details)
                    print(f'Job details added: {index}')

            except Exception as e:
                print(f"Error processing job {index}: {str(e)}")
                continue

        # Print the final response
        print("\nFinal Response:")
        print(json.dumps(job_list, indent=2))
        
        return job_list

    except Exception as e:
        print(f"Error in job scraping: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process jobs: {str(e)}")