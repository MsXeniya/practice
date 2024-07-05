from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import re
from .models import Resume  # Уточните свой путь к моделям Django

def fetch_resume_data(query='', area=1, page_size=20, exp_period='all_time', logic='normal', order_by='relevance'):
    ua = UserAgent()
    page = 0  #0, чтобы начать с первой страницы
    all_vacancies = []

    while True:  #цикл для перебора всех страниц результатов
        page += 1
        url = f"https://hh.ru/search/resume?area={area}&exp_period={exp_period}&logic={logic}&" \
              f"no_magic=true&order_by={order_by}&ored_clusters=true&pos=full_text&" \
              f"search_period=0&text={query}&items_on_page={page_size}&page={page}"
        print(f"Fetching data from URL: {url}")

        try:
            response = requests.get(url, headers={'User-Agent': ua.chrome})
            response.raise_for_status()
            print(f"Response status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching data from URL: {e}")
            break

        soup = BeautifulSoup(response.text, 'lxml')
        resume = soup.find('h1', {'data-qa': 'bloko-header-3', 'class': 'bloko-header-section-3'})

        if not resume:
            print("Resume element not found")
            break

        resume_text = resume.text
        first_number = re.search(r'\d+', resume_text.replace(' ', '')).group()
        resume_count = int(first_number) if first_number else 0
        print(f"Total resume count found: {resume_count}")

        urls = soup.find_all('a', {'data-qa': "serp-item__title", 'class': "bloko-link"})

        for url in urls:
            resume_info = {}
            href = 'https://hh.ru/' + url.attrs['href']
            print(f"Fetching resume details from URL: {href}")

            try:
                response = requests.get(href, headers={'User-Agent': ua.chrome})
                response.raise_for_status()
                print(f"Response status code for resume details: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error fetching resume details from URL: {e}")
                continue

            soup = BeautifulSoup(response.text, 'lxml')

            name_obj = soup.find('h1', {'class': 'resume-block__title-text'})
            name = name_obj.text.strip() if name_obj else 'Не указано'

            title_obj = soup.find('span', {'class': 'resume-block__title-text'})
            job_title = title_obj.text.strip() if title_obj else 'Не указано'

            skills_obj = soup.find('div', {'class': 'bloko-tag-list'})
            if skills_obj:
                skills_list = [
                    tag.text.strip()
                    for tag in skills_obj.find_all('span', {'class': 'bloko-tag__section_text'})
                ]
                skills = ', '.join(skills_list)
            else:
                skills = 'Не указано'

            print(f"Name: {name}")
            print(f"Job title: {job_title}")
            print(f"Skills: {skills}")

            resume_info['Имя'] = name
            resume_info['Должность'] = job_title
            resume_info['Навыки'] = skills

            #cохранение резюме в бд
            try:
                resume = Resume(name=name, job_title=job_title, skills=skills)
                resume.save()
                print("Resume saved to database.")
            except Exception as e:
                print(f"Error saving resume to database: {e}")

            all_vacancies.append(resume_info)

        if len(all_vacancies) >= 5:  #eсли собрано достаточно резюме, завершаем парсинг
            break

        #eсли есть еще страницы, ищем ссылку на следующую страницу
        next_page = soup.find('a', {'data-qa': "pager-next"})
        if not next_page:
            print("Next page link not found, parsing complete.")
            break

    return all_vacancies
