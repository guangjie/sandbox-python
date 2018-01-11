#! /Users/jayden/anaconda2/envs/py36/bin/python
from datetime import datetime
import json
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

DEV_MODE = False

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

    style_title_cell = ' style="padding: 8px; background: #ddd; font-weight: bold;" '
    style_normal_cell = ' style="padding: 8px;" '

    body = '<p>Hi Team, </p>'

    body += '<p>Here are the tasks that have been released for Week {}.</p>'.format(now.strftime('%W'))
    body += '<table>'
    body += '<thead>'
    body += '<tr>'
    body += '<td ' + style_title_cell + '>Key</td>'
    body += '<td ' + style_title_cell + '>Summary</td>'
    body += '</tr>'
    body += '</thead>'
    body += '<tbody>'

    for issue in issue_results['issues']:
        issue_key = issue['key']
        issue_summary = issue['fields']['summary']
        body += '<tr>'
        body += '<td' + style_normal_cell + '><a href="{0}{1}">{1}</a></td>'.format(jira_base_url, issue_key)
        body += '<td' + style_normal_cell + '><a href="{0}{1}">{2}</a></td>'.format(jira_base_url, issue_key, issue_summary)
        body += '</tr>'

    body += '<tbody></table>'
    body += '<p>Regards<br/>' + config["user"]["name"] + '</p>'

    if not DEV_MODE:
        from_addr = config["user"]["email"]
        to_addr = config["report"]["deployment"]["emailTo"]
        cc_addr = config["report"]["deployment"]["emailCc"]
    else:
        from_addr = config["dev"]["from_addr"]
        to_addr = config["dev"]["to_addr"]
        cc_addr = config["dev"]['cc_addr']

    msg = MIMEMultipart()

    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Cc'] = cc_addr

    msg['Subject'] = 'Deployed Tasks for Week ' + now.strftime('%W [%d %b %Y]')

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(config["smtp"]["server"], config["smtp"]["server_port"])
    server.starttls()
    server.login(from_addr, config["smtp"]["password"])
    text = msg.as_string()
    combine_to_addr = to_addr.split(',') + cc_addr.split(',')
    server.sendmail(from_addr, combine_to_addr, text)
    server.quit()
    print('Email Sent!')
else:
    print('No Tasks Deployed')
