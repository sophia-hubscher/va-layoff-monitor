import requests
from bs4 import BeautifulSoup
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# URL of the Virginia WARN notices page
url = 'https://www.virginiaworks.gov/warn-notices/'

COMPANY = 'COMPANY NAME'
EMAIL = 'YOUREMAIL@gmail.com'
PASSWORD = 'APP PASSWORD'

# File to store the last notified date
NOTIFIED_DATE_FILE = 'last_notified_date.txt'

# Load the last notified date from a file
def load_last_notified_date():
    if not os.path.exists(NOTIFIED_DATE_FILE):
        return datetime.date.min  # Return a very old date if file doesn't exist
    with open(NOTIFIED_DATE_FILE, 'r') as file:
        date_str = file.read().strip()
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

# Save the last notified date to a file
def save_last_notified_date(date):
    with open(NOTIFIED_DATE_FILE, 'w') as file:
        file.write(date.strftime('%Y-%m-%d'))

# Function to fetch and parse the WARN notices page
def fetch_warn_notices():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Function to extract company layoff information
def extract_layoffs(soup):
    # Find the table containing the layoff data
    table = soup.find('table')
    if not table:
        print('No table found on the page.')
        return None

    # Iterate over the rows in the table
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 1:
            company_name = columns[0].get_text(strip=True)
            if COMPANY in company_name:
                notice_date = columns[1].get_text(strip=True)
                impact_date = columns[2].get_text(strip=True)
                employees_affected = columns[3].get_text(strip=True)
                location = columns[4].get_text(strip=True)
                contact_person = columns[5].get_text(strip=True)
                reduction_type = columns[6].get_text(strip=True)
                return {
                    'company_name': company_name,
                    'notice_date': notice_date,
                    'impact_date': impact_date,
                    'employees_affected': employees_affected,
                    'location': location,
                    'contact_person': contact_person,
                    'reduction_type': reduction_type
                }
    return None

# Function to send an email alert
def send_email_alert(layoff_info):
    subject = f'Alert: New Layoff Notice'
    body = (
        f'Company: {layoff_info['company_name']}\n'
        f'Notice Date: {layoff_info['notice_date']}\n'
        f'Impact Date: {layoff_info['impact_date']}\n'
        f'Employees Affected: {layoff_info['employees_affected']}\n'
        f'Location: {layoff_info['location']}\n'
        f'Contact Person: {layoff_info['contact_person']}\n'
        f'Reduction Type: {layoff_info['reduction_type']}\n'
    )

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, PASSWORD)
            server.send_message(msg)
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')

# Main function to check for new layoffs and send alerts
def main():
    soup = fetch_warn_notices()
    layoff_info = extract_layoffs(soup)
    if layoff_info:
        # Convert notice_date to a datetime object for comparison
        notice_date = datetime.datetime.strptime(layoff_info['notice_date'], '%m/%d/%Y').date()
        
        # Load the last notified date
        last_notified_date = load_last_notified_date()
        
        if notice_date > last_notified_date:
            print('New layoff detected! Sending alert...')
            send_email_alert(layoff_info)
            # Update the last notified date
            save_last_notified_date(notice_date)
        else:
            print('No new layoffs since the last check.')
    else:
        print('No layoff information found.')

if __name__ == '__main__':
    main()
