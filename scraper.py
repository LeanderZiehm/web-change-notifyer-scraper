import requests
from bs4 import BeautifulSoup
from database import get_connection, upsert_job

BASE_URL = "https://www.bmwgroup.jobs/"

URL = "https://www.bmwgroup.jobs/de/en/students/finalthesis/_jcr_content/main/layoutcontainer_359813111/jobfinder30_copy_cop_1986864682.jobfinder_table.content.html"

PARAMS = {
    "textSearch": "Studienabschlussarbeit | Thesis",
    "filterSearch": "location_DE,jobType_INTERNSHIP",
    "rowIndex": 0,
    "blockCount": 40
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bmwgroup.jobs/de/en/students/finalthesis.html",
    "X-Requested-With": "XMLHttpRequest"
}

def parse_jobs(html):
    print("parse jobs")
    print(html)
    soup = BeautifulSoup(html, "html.parser")
    job_table = soup.select_one(".grp-jobfinder__table")
    if not job_table:
        print("no job table")
        return []

    jobs = []
    for wrapper in job_table.select(".grp-jobfinder__wrapper"):
        job = {}
        job['id'] = wrapper.get("data-job-id")
        refno_div = wrapper.select_one(".grp-jobfinder-cell-refno")
        job['ref_no'] = refno_div.text.strip()
        job['location'] = refno_div.get("data-job-location")
        job['legal_entity'] = refno_div.get("data-job-legal-entity")
        job['field'] = refno_div.get("data-job-field")
        job['type'] = refno_div.get("data-job-type")

        title_div = wrapper.select_one(".grp-jobfinder__cell-title")
        job['title'] = title_div.text.strip()

        publication_div = wrapper.select_one(".grp-jobfinder__cell-publication div")
        job['published_date'] = publication_div.text.replace("Published:", "").strip()

        link_tag = wrapper.select_one("a.grp-jobfinder__link-jobdescription")
        job['link'] = BASE_URL + link_tag.get("href") if link_tag else None

        new_job_div = wrapper.select_one(".grp-jobfinder__new-job")
        job['is_new'] = 1 if new_job_div else 0

        jobs.append(job)
    return jobs

def fetch_and_store_jobs():
    print("fetch_and_store_jobs")
    response = requests.get(URL, params=PARAMS, headers=HEADERS)
    if response.status_code != 200:
        print("not 200")
        return []
    
    print("BRO")
    jobs = parse_jobs(response.text)
    print(jobs)
    conn = get_connection()
    for job in jobs:
        upsert_job(conn, job)
    return jobs