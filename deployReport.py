#! /Users/jayden/anaconda2/envs/py36/bin/python
from datetime import datetime
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
    jira_search['deployed'],
    auth=(conf_jira['user'], conf_jira['password'])
)
issue_results = r.json()

if len(issue_results['issues']) > 0:
    now = datetime.now()

    body = '<p>Hi Team, </p>'

    body += '<style>' \
            '    .td-title {' \
            '        padding: 8px; ' \
            '        background: #ddd; ' \
            '        font-weight: bold;' \
            '    } ' \
            '    .td-normal {' \
            '        padding: 8px;' \
            '    }' \
            '</style>' \

    body += '<p>Here are the tasks that have been released for Week ' + now.strftime('%W') + '.</p>'

    body += '<table>'
    body += '<thead><tr><td class="td-title">Key</td><td class="td-title">Summary</td></tr></thead>'
    body += '<tbody>'

    for issue in issue_results['issues']:
        issue_key = issue['key']
        issue_summary = issue['fields']['summary']
        body += '<tr>'
        body += '<td class="td-normal"><a href="' + jira_base_url + issue_key + '">' + issue_key + '</a></td>'
        body += '<td class="td-normal"><a href="' + jira_base_url + issue_key + '">' + issue_summary + '</a></td>'
        body += '</tr>'

    body += '<tbody></table>'
    body += '<p>Regards<br/>Jayden Chua</p>'

    fromaddr = config["user"]["email"]
    toaddr = config["report"]["deployment"]["emailTo"]

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Cc'] = config["report"]["deployment"]["emailCc"]

    msg['Subject'] = 'Deployed Tasks for Week ' + now.strftime('%W [%d %b %Y]')

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(config["smtp"]["server"], config["smtp"]["server_port"])
    server.starttls()
    server.login(fromaddr, config["smtp"]["password"])
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print('Email Sent!')
else:
    print('No Tasks Deployed')
