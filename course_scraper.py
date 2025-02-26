#!/usr/bin/env python
# coding: utf-8

# ## University Courses Scraper

# In[1]:


# import libraries

import requests  # make a request to a url
from bs4 import BeautifulSoup  # parse the requests as html
import pandas as pd  # data manipulation
from time import sleep
import re


# In[3]:


# Load the CSV file
csv_file = "./bsc_course_links.csv"  # Update with the actual file path
df = pd.read_csv(csv_file)


# In[5]:


df.head()


# In[7]:


df.shape


# In[9]:


# List to store scraped data
scraped_data = []


# In[11]:


# Function to scrape course details
def scrape_course(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract image source
        img_tag = soup.find("img", class_="!z-1 maw-w-full absolute h-full w-screen object-cover sm:rounded-none md:rounded-t-lg lg:rounded-t-lg")
        if img_tag and img_tag.has_attr("src"):
            img_src = img_tag["src"].strip()
        else:
            img_src = ""
            
        # Extract institution name
        a_tag = soup.find("a", class_="text-grey-800 block cursor-pointer text-xs font-semibold underline mb-2 md:text-base")
        if a_tag:
            institution_name = a_tag.text.strip()
        else:
            institution_name = ""
            # print("Institution Name:",institution_name)

        # Extract course title
        h1_tag = soup.find("h1", class_="title-xl2 text-base font-bold mb-4")
        if h1_tag:
            course_title = h1_tag.text.strip()
        else:
            course_title = ""

        # univerity location
        p_tag = soup.find("p", class_="text-xs font-normal text-gray-700 mb-6 md:text-base")
        if p_tag:
            university_location = p_tag.text.strip() 
        else:
            university_location = ""
            
        # Extract course duration
        infos = soup.find_all("p", class_="text-base")
        if infos:
            course_duration = infos[0].text
            study_mode = infos[2].text
            campus_type = infos[-1].text
          
        else:
            course_duration = ""
            study_mode = ""
            campus_type = ""


        # Extract Description
        div_tag  = soup.find("div", class_="block text")
        if div_tag:
            course_infomation = div_tag.text.strip()
        else:
            course_infomation = "Unknown"
            
        return {"Image Source": img_src, 
                "Institution Name": institution_name, 
                "Course Title": course_title,
                "University Location": university_location,
                "Course Duration": course_duration,
                "Study Mode": study_mode,
                "Campus Type": campus_type,
                "Course Infomation": course_infomation}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {"URL": url}


# In[17]:


df[0:10]


# In[21]:


# Iterate through the course URLs and scrape data
for index, row in df[0:5].iterrows():
    course_url = row["course_links"]
    print(f"Scraping: {course_url}")
    data = scrape_course(course_url)
    scraped_data.append(data)
    
    # Delay between requests to avoid getting blocked
    sleep(2)

# Convert scraped data to a DataFrame
scraped_df = pd.DataFrame(scraped_data)



# In[23]:


scraped_df


# In[25]:


scraped_df.isnull().sum()


# In[29]:


# Save to CSV
scraped_df.to_csv("./scraped_bsc_courses.csv", index=False)
print("Scraping completed. Data saved to scraped_courses.csv")


# In[ ]:





# In[ ]:




