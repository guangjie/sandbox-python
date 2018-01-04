#! /Users/jayden/anaconda2/envs/py36/bin/python
import json
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

conf_jira = config["jira"]
jira_search = conf_jira["search_urls"]
jira_base_url = 'https://jira.modix.de/jira/browse/'

r = requests.get(
    jira_search['ready_for_release'],
    auth=(conf_jira['user'], conf_jira['password'])
)
issue_results = r.json()

body = '<ul>'
for issue in issue_results['issues']:
    issue_key = issue['key']
    issue_summary = issue['fields']['summary']
    body += '<li><a href="' + jira_base_url + issue_key + '">' + issue_summary + '</a></li>'

body += '</ul>'

fromaddr = config["user"]["email"]
toaddr = config["user"]["email"]

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Deployed Tasks for  '

msg.attach(MIMEText(body, 'html'))

server = smtplib.SMTP(config["smtp"]["server"], config["smtp"]["server_port"])
server.starttls()
server.login(fromaddr, config["smtp"]["password"])
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
