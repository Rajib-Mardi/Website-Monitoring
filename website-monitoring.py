import time

import boto3
import requests
import smtplib
import os
import paramiko
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = 'ap-southeast-1'


def restart_server_and_container():
    # restart aws server
    print('Rebooting the server.... ')
    ec2_nginx_server = boto3.client('ec2', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                    region_name=AWS_REGION)
    instance_id = 'i-075fef9e1d58fd1c1'
    ec2_nginx_server.reboot_instances(InstanceIds=[instance_id])

    ec2_nginx_server = boto3.client('ec2', region_name='ap-southeast-1')
    # restart the applicaton
    while True:
        response = ec2_nginx_server.describe_instances(InstanceIds=['i-075fef9e1d58fd1c1'])
        instance_status = response['Reservations'][0]['Instances'][0]['State']['Name']
        if instance_status == 'running':
            time.sleep(100)
            restart_container()
            break


def send_notification(email_msg):
    print('Sending an email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)


def restart_container():
    print('Restarting the Application.....')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='18.143.73.242', username='ec2-user',
                key_filename='/Users/Rajib/Downloads/monitoring-website.pem')
    stdin, stdout, stderr = ssh.exec_command('docker start deed03b844af')
    print(stdout.readlines())
    ssh.close()


def monitor_application():
    try:
        response = requests.get('http://ec2-18-143-73-242.ap-southeast-1.compute.amazonaws.com:8080/')
        if response.status_code == 200:
            print('Application is running successfully! ')
        else:
            print('Application down fix it!')
            msg = f'Application returned {response.status_code}'
            send_notification(msg)
            restart_container()
    except Exception as ex:
        print(f'Connection error happened: {ex}')
        msg = 'Application not accessible at all'
        send_notification(msg)
        restart_server_and_container()


schedule.every(5).seconds.do(monitor_application)

while True:
    schedule.run_pending()
