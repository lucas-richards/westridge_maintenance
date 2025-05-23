import os
import django


# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
# from training.models import KPI, KPIValue, Profile, TrainingEvent, TrainingModule, ProfileTrainingEvents
from workorder.models import WorkOrder, WorkOrderRecord, KPI as KPI2, KPIValue as KPIValue2, CheckListItem, PurchasePart
import datetime as dt
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import logging
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Calculate and save daily KPI values'

    def save_kpi2(self, kpi_name, value):
        kpi, created = KPI2.objects.get_or_create(name=kpi_name)
        today = timezone.now().date()
        KPIValue2.objects.update_or_create(
            kpi=kpi,
            date=today,
            defaults={'value': value}
        )

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        # profiles = Profile.objects.all()
        # active_profiles = profiles.filter(active=True)
        # training_modules = TrainingModule.objects.filter(other=False).order_by('name')

        # training = {
        #     'performed': 0,
        #     'not_performed': 0,
        #     'total': 0
        # }
        # retraining = {
        #     'performed': 0,
        #     'overdue': 0,
        #     'not_performed': 0,
        #     'total': 0
        # }
        # profiles_fully_trained = 0
        # training_not_performed_users = []
        # retraining_not_performed_users = []
        # retraining_overdue_users = []

        # for profile in active_profiles:
        #     try:
        #         profile_training_events = ProfileTrainingEvents.objects.filter(profile=profile).first()
        #         training_events_now = profile_training_events.row.split(',')
        #         fully_trained = True

        #         for i, training_module in enumerate(training_modules):
        #             if training_events_now[i] == '-':
        #                 continue
        #             elif training_events_now[i][0] == 'T':
        #                 fully_trained = False
        #                 if training_module.retrain_months:
        #                     retraining['total'] += 1
        #                     retraining['not_performed'] += 1
        #                     retraining_not_performed_users.append(profile.user)
        #                 else:
        #                     training['total'] += 1
        #                     training['not_performed'] += 1
        #                     training_not_performed_users.append(profile.user)
        #                 continue

        #             try:
        #                 parsed_date = dt.datetime.strptime(training_events_now[i], '%m/%d/%y')
        #                 current_date = dt.datetime.now()
        #                 delta = current_date - parsed_date
        #                 months_difference = delta.days // 30

        #                 if training_module.retrain_months:
        #                     if months_difference > training_module.retrain_months:
        #                         retraining['overdue'] += 1
        #                         fully_trained = False
        #                         retraining_overdue_users.append(profile.user)
        #                     else:
        #                         retraining['performed'] += 1
        #                     retraining['total'] += 1
        #                 else:
        #                     training['performed'] += 1
        #                     training['total'] += 1

        #             except ValueError:
        #                 continue
        #     except:
        #         print('Error for:', profile.user.username)
        #         continue

        #     if fully_trained:
        #         profiles_fully_trained += 1

        # perc_fully_trained = round(profiles_fully_trained / active_profiles.count() * 100) if active_profiles.count() else 0
        # training_not_performed_users = list(set(training_not_performed_users))
        # retraining_not_performed_users = list(set(retraining_not_performed_users))
        # retraining_overdue_users = list(set(retraining_overdue_users))

        # training['performed'] = round(training['performed'] / training['total'] * 100) if training['total'] else 0
        # retraining['performed'] = round(retraining['performed'] / retraining['total'] * 100) if retraining['total'] else 0
        # retraining['overdue'] = round(retraining['overdue'] / retraining['total'] * 100) if retraining['total'] else 0
        # training['not_performed'] = round(training['not_performed'] / training['total'] * 100) if training['total'] else 0
        # retraining['not_performed'] = round(retraining['not_performed'] / retraining['total'] * 100) if retraining['total'] else 0

        # self.save_kpi('Training Performed', training['performed'])
        # self.save_kpi('Retraining Performed', retraining['performed'])
        # self.save_kpi('Retraining Overdue', retraining['overdue'])
        # self.save_kpi('Training Not Performed', training['not_performed'])
        # self.save_kpi('Retraining Not Performed', retraining['not_performed'])
        # self.save_kpi('Percentage Fully Trained', perc_fully_trained)
        
        # self.stdout.write(self.style.SUCCESS('Successfully saved daily training KPI values'))


        
        # Maintenance APP
        # works great
        # schedule a work order record according to the recurrence and if the last work order record is done or cancelled
        new_workorders = []
        try:
            work_orders = WorkOrder.objects.all()
            for work_order in work_orders:
                # last_work_order_record = work_order.workorderrecord_set.last()
                last_work_order_record = work_order.workorderrecord_set.order_by('due_date').last()
                if last_work_order_record:
                    if last_work_order_record.status in ['done', 'cancelled']:
                        if last_work_order_record.completed_on:
                            if work_order.recurrence == 'Daily':
                                if last_work_order_record.completed_on + dt.timedelta(days=1) > last_work_order_record.due_date:
                                    new_due_date = last_work_order_record.completed_on + dt.timedelta(days=1)
                                else:
                                    new_due_date = last_work_order_record.due_date + dt.timedelta(days=1)
                                print('Daily:',last_work_order_record.due_date, new_due_date)
                            elif work_order.recurrence == 'Weekly':
                                if last_work_order_record.completed_on + dt.timedelta(weeks=1) > last_work_order_record.due_date:
                                    new_due_date = last_work_order_record.completed_on + dt.timedelta(weeks=1)
                                else:
                                    new_due_date = last_work_order_record.due_date + dt.timedelta(days=1)
                                print('Weekly:',last_work_order_record.due_date, new_due_date)
                            elif work_order.recurrence == 'Monthly':
                                if last_work_order_record.completed_on + relativedelta(months=1) > last_work_order_record.due_date:
                                    new_due_date = last_work_order_record.completed_on + relativedelta(months=1)
                                else:
                                    new_due_date = last_work_order_record.due_date + dt.timedelta(days=1)
                                print('Monthly:',last_work_order_record.due_date, new_due_date)
                            elif work_order.recurrence == 'Quarterly':
                                if last_work_order_record.completed_on + relativedelta(months=3) > last_work_order_record.due_date:
                                    new_due_date = last_work_order_record.completed_on + relativedelta(months=3)
                                else:
                                    new_due_date = last_work_order_record.due_date + dt.timedelta(days=1)
                                print('Quarterly:',last_work_order_record.due_date, new_due_date)
                            elif work_order.recurrence == 'Biannually':
                                if last_work_order_record.completed_on + relativedelta(months=6) > last_work_order_record.due_date:
                                    new_due_date = last_work_order_record.completed_on + relativedelta(months=6)
                                else:
                                    new_due_date = last_work_order_record.due_date + dt.timedelta(days=1)
                                print('Biannually:',last_work_order_record.due_date, new_due_date)
                            elif work_order.recurrence == 'Yearly':
                                if last_work_order_record.completed_on + relativedelta(years=1) > last_work_order_record.due_date:
                                    new_due_date = last_work_order_record.completed_on + relativedelta(years=1)
                                else:
                                    new_due_date = last_work_order_record.due_date + dt.timedelta(days=1)
                                print('Yearly:',last_work_order_record.due_date, new_due_date)
                            elif work_order.recurrence == '3 Years':
                                if last_work_order_record.completed_on + relativedelta(years=3) > last_work_order_record.due_date:
                                    new_due_date = last_work_order_record.completed_on + relativedelta(years=3)
                                else:
                                    new_due_date = last_work_order_record.due_date + dt.timedelta(days=1)
                                print('3 Years:',last_work_order_record.due_date, new_due_date)
                            else:
                                new_due_date = ''

                            if new_due_date:
                                new = WorkOrderRecord.objects.create(workorder=work_order, due_date=new_due_date)
                                print('new:', new)
                                print('due_date:', new.due_date)
                                new_workorders.append(new)
                        
                        if last_work_order_record.checklist_items.exists():
                            for item in last_work_order_record.checklist_items.all():
                                item_data = {
                                    'workorder_record': new,
                                    'title': item.title,
                                    'description': item.description,
                                    'status': '',  # Set the status to empty
                                    # Add any other fields that need to be copied
                                }
                                new_checklist = CheckListItem.objects.create(**item_data)
                                print('new_checklist:', new_checklist)
                                print('new record:', new)

                        #  if last record purchase parts exist add them to
                        if last_work_order_record.purchase_parts.exists():
                            for part in last_work_order_record.purchase_parts.all():
                                part_data = {
                                    'workorder_record': new,
                                    'title': part.title,
                                    'description': part.description,
                                    # Add any other fields that need to be copied
                                }
                                new_part = PurchasePart.objects.create(**part_data)
                                print('new_part:', new_part)
                                print('new record:', new)

                else:
                    WorkOrderRecord.objects.create(work_order=work_order, due_date=timezone.now())


            # get the last record or each work order and check for those with different from done and cancelled if they are overdue by checking if the due date is later than today
            work_orders = WorkOrder.objects.all()
            productivity_value = WorkOrderRecord.objects.filter(status='done', completed_on__date=today).count()
            overdue = 0
            overdue_high = 0
            for work_order in work_orders:
                last_work_order_record = work_order.workorderrecord_set.last()
                if last_work_order_record and last_work_order_record.status not in ['done', 'cancelled'] and last_work_order_record.due_date.date() < timezone.now().date():
                    # if asset criticalliy is high then overdue_high += 1
                    if work_order.asset and work_order.asset.criticality.lower() == 'high':
                        overdue_high += 1
                    else:
                        overdue += 1
            # save to over due kpi
            self.save_kpi2('Overdue', overdue)
            self.save_kpi2('Overdue High Criticality', overdue_high)
            self.save_kpi2('Productivity', productivity_value)
            print('overdue:', overdue)
            print('overdue_high:', overdue_high)
            print('productivity_value:', productivity_value)


            # if there are no work orders records for today, then set the productivity kpi value to 0
            
            work_order_records_today = WorkOrderRecord.objects.filter(completed_on=today).count()
            self.save_kpi2('Productivity', work_order_records_today)

            # count how many work order records have status done and create a kpivalue with that number
            value = WorkOrderRecord.objects.filter(status='done').count()
            self.save_kpi2('Status Done', value)

            #  count how many work orders have the last work order record are on time and create a kpivalue with that number in timing kpi
            work_orders_records = WorkOrderRecord.objects.all()
            on_time = round(work_orders_records.filter(due_date__gte=timezone.now()).exclude(status__in=['done', 'cancelled']).count(), 0)
            work_orders_excluding = work_orders_records.exclude(status__in=['done', 'cancelled'])

            #  get percentage rounded to 0 decimals
            percentage = round(on_time / work_orders_excluding.count() * 100) if work_orders_excluding.count() else 0
            self.save_kpi2('Timing On Time', percentage)

            # get the total of work orders and save it in workordersqty kpiwith todays date
            work_orders_qty = WorkOrder.objects.all().count()
            self.save_kpi2('Work Orders Qty', work_orders_qty)

            self.stdout.write(self.style.SUCCESS('Successfully saved daily maintenance KPI values'))

            # send email succesfully 
            email_user = os.environ.get('EMAIL_USER')
            email_password = os.environ.get('EMAIL_PASS')
            author_email = os.environ.get('EMAIL_USER')
            recipients = [f"lrichards@westridgelabs.com"]
            subject = f'Maintenance KPI Calculation'
            message = f'''
            <div style="padding-left: 16px; border: 1px solid #ddd; border-radius: 4px;">
                <div style=" border-bottom: 1px solid #ddd;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: baseline;">
                            <p style="min-width: 50px; margin-right: 8px; font-weight: bold;">Success</p>
                            <p class="truncate" style="min-width: 250px; margin-right: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">KPI Calculation was successful</p>
                        </div>
                    </div>
                </div>
                <div style="margin-top: 16px;">
                    <p style="font-weight: bold;">New Work Orders Records Created:</p>
                    <ul>
                        {''.join([f'<li>{work_order}</li>' for work_order in new_workorders])}
                    </ul>
                </div>
            '''
            try:
                send_mail(subject, '', email_user, recipients, html_message=message, auth_user=email_user, auth_password=email_password)
                logging.info(f'Successfully sent reminder update email to {recipients}')
                print(f'Successfully sent reminder update email to {recipients}')
            except Exception as e:
                logging.error(f'Error sending reminder update email to {recipients}: {str(e)}')
                print(f'Error sending reminder update email to {recipients}: {str(e)}')



        except Exception as e:
            email_user = os.environ.get('EMAIL_USER')
            email_password = os.environ.get('EMAIL_PASS')
            author_email = os.environ.get('EMAIL_USER')
            recipients = [f"{os.environ.get('EMAIL_USER')}"]

            subject = f'Error - Maintenance KPI Calculation'
            message = f'''
            <div style="padding-left: 16px; border: 1px solid #ddd; border-radius: 4px;">
                <div style=" border-bottom: 1px solid #ddd;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: baseline;">
                            <p style="min-width: 50px; margin-right: 8px; font-weight: bold;">Error</p>
                            <p class="truncate" style="min-width: 250px; margin-right: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{str(e)}</p>
                        </div>
                    </div>
                </div>
            '''
            try:
                send_mail(subject, '', email_user, recipients, html_message=message, auth_user=email_user, auth_password=email_password)
                logging.info(f'Successfully sent reminder update email to {recipients}')
                print(f'Successfully sent reminder update email to {recipients}')
            except Exception as e:
                logging.error(f'Error sending reminder update email to {recipients}: {str(e)}')
                print(f'Error sending reminder update email to {recipients}: {str(e)}')



                    

# Call the function to calculate and save daily KPI values
if __name__ == '__main__':
    Command().handle()

