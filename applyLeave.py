#! /Users/jayden/anaconda2/envs/py36/bin/python
import json
import inquirer
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

wb = Workbook()
ws = wb.active

# Data can be assigned directly to cells
questions = [
    inquirer.Text(
        'name',
        message="What is your Name?",
    ),
    inquirer.List(
        'department',
        message="Which Department?",
        choices=['Product', 'Production', 'Sales&Marketing', 'Management', 'Delivery', 'Development'],
    ),
    inquirer.List(
        'request_type',
        message="Which Request Type?",
        choices=['Team', 'Project', 'Presales'],
    ),
    inquirer.List(
        'project_type',
        message="Which Project Shortcut?",
        choices=data["user"]["projects"],
    ),
    inquirer.List(
        'lott_type',
        message="Which LOTT Type?",
        choices=['Leave', 'OT', 'Travel'],
    ),
    inquirer.List(
        'lott_detail_type',
        message="Which Detail Type for LOTT?",
        choices=[
            'OT-Compensation',
            'Travel-Within China',
            'Travel-Outside China',
            'S.Annual Leave',
            'C.Annual Leave',
            'Compensation Leave',
            'Marriage',
            'Sick Leave',
            'Paid Sick Leave',
            'Maternity Leave',
            'Paternity Leave',
            'Personal Leave'
        ],
    ),
    inquirer.Text(
        'description',
        message="What is the purpose of the leave?",
    ),
    inquirer.Text(
        'start_date',
        message="What is the Start Date?",
    ),
    inquirer.Text(
        'start_time',
        message="What is the Start Time?",
    ),
    inquirer.Text(
        'end_date',
        message="What is the End Date?",
    ),
    inquirer.Text(
        'end_time',
        message="What is the End Time?",
    ),
    inquirer.Text(
        'quantity',
        message="What is the Quantity?",
    )
]

answers = inquirer.prompt(questions)

ws.merge_cells('A1:L1')

style_font_main_header = Font(name='Calibri (Body)', size='24', bold=True)
style_font_sub_header = Font(name='Calibri (Body)', size='11', bold=True)
style_fill_light_grey = PatternFill(fill_type='solid', start_color='FFB7B7B7', end_color='FFB7B7B7')
style_fill_dark_grey = PatternFill(fill_type='solid', start_color='FF808080', end_color='FF808080')
style_alignment_center = Alignment(horizontal='centerContinuous', vertical='bottom')

ws['A1'] = data["forms"]["leave"]["title"]
a1 = ws['A1']
a1.alignment = style_alignment_center
a1.fill = style_fill_light_grey
a1.font = style_font_main_header

# Rows can also be appended
ws.append(['Name', 'Department Shortcut Dimension', 'Request Type', 'Project Shortcut', 'LOTT Type', 'Detail Type for LOTT', 'Description', 'Start Date', 'Start Time', 'To Date', 'To Time', 'Quantity (Days)'])

for i in range(1, 13):
    ws.cell(row=2, column=i).fill = style_fill_light_grey
    ws.cell(row=2, column=i).font = style_font_sub_header
    ws.cell(row=2, column=i).alignment = style_alignment_center

ws.append([
    answers['name'],
    answers['department'],
    answers['request_type'],
    answers['project_type'],
    answers['lott_type'],
    answers['lott_detail_type'],
    answers['description'],
    answers['start_date'],
    answers['start_time'],
    answers['end_date'],
    answers['end_time'],
    answers['quantity'],
])
# Save the file
wb.save(data["user"]["doc_folder"] + 'sample.xlsx')

fromaddr = data["user"]["email"]
toaddr = data["user"]["email"]

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Leave Application for ' + answers['name'] + 'from ' + answers['start_date']

body = '<style>' \
       '    .td-title {' \
       '        padding: 8px; ' \
       '        background: #ddd; ' \
       '        font-weight: bold;' \
       '    } ' \
       '    .td-normal {' \
       '        padding: 8px;' \
       '    }' \
       '</style>' \
       '<table>' \
       '    <tbody>'

body += '        <tr>' \
       '            <td class="td-title">Name</td>' \
       '            <td class="td-normal">' + answers['name'] + '</td>' \
       '        </tr>' \
       '        <tr>' \
       '            <td class="td-title">Department Shortcut Dimension</td>' \
       '            <td class="td-normal">' + answers['department'] + '</td>' \
       '        </tr>' \
       '        <tr>' \
       '            <td class="td-title">Request Type</td>' \
       '            <td class="td-normal">' + answers['request_type'] + '</td>' \
       '        </tr>' \
       '        <tr>' \
       '            <td class="td-title">Project Shortcut</td>' \
       '            <td class="td-normal">' + answers['project_type'] + '</td>' \
       '        </tr>' \
       '        <tr>' \
       '            <td class="td-title">LOTT Type</td>' \
       '            <td class="td-normal">' + answers['lott_type'] + '</td>' \
       '        </tr>' \
       '        <tr>' \
       '            <td class="td-title">Detail Type for LOTT</td>' \
       '            <td class="td-normal">' + answers['lott_detail_type'] + '</td>' \
       '        </tr>' \
       '        <tr>' \
       '            <td class="td-title">Description</td>' \
       '            <td class="td-normal">' + answers['description'] + '</td>' \
       '        </tr>' \
       '        <tr>' \
       '            <td class="td-title">Start Date</td>' \
       '            <td class="td-normal">' + answers['start_date'] + '</td>' \
       '        </tr>' \
       '        <tr>' \
       '            <td class="td-title">Start Time</td>' \
       '            <td class="td-normal">' + answers['start_time'] + '</td>' \
       '        </tr>' \
       '        <tr>' \
       '            <td class="td-title">To Date</td>' \
       '            <td class="td-normal">' + answers['end_date'] + '</td>' \
       '        </tr>' \
       '        <tr>' \
       '            <td class="td-title">To Time</td>' \
       '            <td class="td-normal">' + answers['end_time'] + '</td>' \
       '        </tr>' \
       '        <tr>' \
       '            <td class="td-title">Quantity (Days)</td>' \
       '            <td class="td-normal">' + answers['quantity'] + '</td>' \
       '        </tr>' \
       '    </tbody>' \
       '</table>'

msg.attach(MIMEText(body, 'html'))

filename = "leave_application.xlsx"
attachment = open(data["user"]["doc_folder"] + "sample.xlsx", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP(data["smtp"]["server"], data["smtp"]["server_port"])
server.starttls()
server.login(fromaddr, data["smtp"]["password"])
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

# ws['A2'] = datetime.datetime.now()
