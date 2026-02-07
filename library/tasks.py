from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass
    
@shared_task
def check_overdue_loans():
   
        today = datetime.today()
        overdue_records = Loan.objects.select_related("member__user", "book").filter(is_returned=False, due_date__lt=today)
        
        for overdue_record in overdue_records:
            try:
                member = overdue_record.member
                user = member.user
                book = overdue_record.book
                member_email = user.email
                book_title = book.title
                send_mail(
                    subject='Overdue Book Reminder',
                    message=f'Hello {user.username},\n\nThis is a reminder of "{book_title}".\nPlease return it as soon as possible.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[member_email],
                    fail_silently=False,
                )
            except Loan.DoesNotExist:
                pass
