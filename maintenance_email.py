import os
import django
import logging


# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from workorder.models import WorkOrder, WorkOrderRecord
import datetime as dt

class Command(BaseCommand):
    help = 'Send maintenance email with overdue and coming up WOs'
    
    def handle(self, *args, **kwargs):
        email_user = os.environ.get('EMAIL_USER')
        email_password = os.environ.get('EMAIL_PASS')
        author_email = 'lrichards@westridgelabs.com'
        recipients = ['lrichards@westridgelabs.com','ibeza@westridgelabs.com' ]

        subject = 'Due Maintenance Work Orders'
        workorders = WorkOrder.objects.all()
        records = []

        for workorder in workorders:
            last_record = WorkOrderRecord.objects.filter(workorder=workorder).exclude(status__in=['done', 'cancelled']).order_by('-due_date').first()
            if last_record:
                last_record.time_until_due = (last_record.due_date - timezone.now() + dt.timedelta(days=1)).days if last_record.due_date else None
                if last_record.time_until_due is not None and last_record.time_until_due <= 7:
                    records.append(last_record)
        
        records = sorted(records, key=lambda x: x.due_date)

        for record in records:
            record.status = record.get_status_display()

        # Build the message
        if records:
            message_parts = ["""
            <div style="padding-left: 16px; border: 1px solid #ddd; border-radius: 4px;">
            """]

            for data in records:
                message_parts.append(f'''
                <div style=" border-bottom: 1px solid #ddd;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: baseline;">
                            {self.get_status_badge(data.status)}
                            <p style="min-width: 50px; margin-right: 8px; font-weight: bold;">WO{data.workorder.id}</p>
                            <p style="min-width: 250px; margin-right: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{data.workorder.title}</p>
                        </div>
                        <div>
                            {self.get_due_status(data)}
                        </div>
                    </div>
                </div>
                ''')

            message_parts.append('</div>')
            message = ''.join(message_parts)
        else:
            message = '''
            <div style="padding: 8px; margin-top: 8px; border: 1px solid #ddd; border-radius: 4px;">
                <h5>No records found</h5>
            </div>
            '''

        try:
            send_mail(subject, '', email_user, recipients, html_message=message, auth_user=email_user, auth_password=email_password)
            logging.info(f'Successfully sent schedule update email to {recipients}')
            print(f'Successfully sent schedule update email to {recipients}')
        except Exception as e:
            logging.error(f'Error sending schedule update email to {recipients}: {str(e)}')
            print(f'Error sending schedule update email to {recipients}: {str(e)}')


        # Check all workorders notification property and send email if the last record of the notification is not cancelled or done and due date is within the notification settings
        workorders = WorkOrder.objects.all()
        for workorder in workorders:
            last_record = WorkOrderRecord.objects.filter(workorder=workorder).exclude(status__in=['done', 'cancelled']).order_by('-due_date').first()
            if last_record and last_record.due_date:
                if workorder.notification == 'day before' and (last_record.due_date - timezone.now()).days <= 2:
                    self.send_notification_email(workorder, last_record)
                elif workorder.notification == 'week before' and (last_record.due_date - timezone.now()).days <= 7:
                    self.send_notification_email(workorder, last_record)
                elif workorder.notification == 'month before' and (last_record.due_date - timezone.now()).days <= 30:
                    self.send_notification_email(workorder, last_record)
        
    def send_notification_email(self, workorder, record):
        if workorder.assigned_to and workorder.assigned_to.email:
            email_user = os.environ.get('EMAIL_USER')
            email_password = os.environ.get('EMAIL_PASS')
            author_email = 'lrichards@westridgelabs.com'
            recipients = [f'{workorder.assigned_to.email}']

            subject = f'{workorder.title} is due soon'
            message = f'''
            <div style="padding: 16px; border: 1px solid #ddd; border-radius: 4px;">
                <h3 style="color: #007bff;">Reminder: Work Order Due Soon</h3>
                <p style="font-size: 16px;">This is a reminder that the work order <strong>{workorder.title}</strong> is due on <strong>{record.due_date.date()}</strong>.</p>
                <p style="font-size: 14px;">Please ensure that the necessary actions are taken before the due date.</p>
                <p style="font-size: 14px;">Thank you.</p>
            </div>
            '''
            try:
                send_mail(subject, '', email_user, recipients, html_message=message, auth_user=email_user, auth_password=email_password)
                logging.info(f'Successfully sent reminder update email to {recipients}')
                print(f'Successfully sent reminder update email to {recipients}')
            except Exception as e:
                logging.error(f'Error sending reminder update email to {recipients}: {str(e)}')
                print(f'Error sending reminder update email to {recipients}: {str(e)}')
        


    def get_status_badge(self, status):
        badge_styles = {
            'On Hold': 'margin-right: 8px; background-color: #ffc107; color: #fff; padding: 2px 4px; border-radius: 4px;',
            'In Progress': 'margin-right: 8px; background-color: #007bff; color: #fff; padding: 2px 4px; border-radius: 4px;',
            'Scheduled': 'margin-right: 8px; background-color: #17a2b8; color: #fff; padding: 2px 4px; border-radius: 4px;',
        }
        return f'<span style="min-width: 70px; {badge_styles.get(status, "")}">{status}</span>'

    def get_due_status(self, record):
        if record.time_until_due > 0:
            return '<p style="margin-right: 8px; color: #ffc107;font-weight:bold;">Coming up</p>'
        else:
            return '<p style="margin-right: 8px; color: #dc3545;font-weight:bold;">Overdue</p>'

# Call the function to send email
if __name__ == '__main__':
    Command().handle()
