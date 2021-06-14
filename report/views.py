from django.shortcuts import render
from datetime import datetime
from order.models import Order, OrderDetail
from receipt.models import Receipt, ReceiptDetail
from payment.models import Payment


def report_day(req):
    report_data = {
        'total': 0,
        'sum_total_with_category': {},
        'total_discount': 0,
        'submit': False,
        'payments': {},
        'receipt_details_count': 0,
        'receipt_details': {},
        'date': '---'
    }

    for payment in Payment.objects.all():
        report_data['payments'][payment.name] = 0

    if req.method == 'POST':
        report_data['submit'] = True

        date_str = req.POST['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        year = f'{date_obj.year}'
        month = f'0{date_obj.month}'if date_obj.month < 10 else date_obj.month
        day = f'0{date_obj.day}'if date_obj.day < 10 else date_obj.day

        report_data['date'] = date_obj.strftime('%d/%m/%Y')

        receipts = Receipt.objects.filter(
            created_at__year=year,
            created_at__month=month,
            created_at__day=day,
            status='new'
        )

        if receipts.exists():
            for receipt in receipts:
                # sum total discount
                report_data['total_discount'] += receipt.get_total_discount()

                # sum total
                report_data['total'] += receipt.total

                #sum total with category
                for detail in receipt.details(status=True):
                    category = detail.menu.category.parent
                    total = detail.amount()

                    if category in report_data['sum_total_with_category']:
                        report_data['sum_total_with_category'][category] += total 
                    else:
                        report_data['sum_total_with_category'][category] = total 
                    
                #sum qty of menu
                for detail in receipt.details(status=True):
                    menu_name = detail.menu.name
                    if menu_name in report_data['receipt_details']:
                        report_data['receipt_details'][menu_name] += detail.qty
                    else:
                        report_data['receipt_details'][menu_name] = detail.qty

                report_data['receipt_details_count'] = len(report_data['receipt_details'])

                # sum total payment
                for receipt_payment in receipt.payments():
                    report_data['payments'][receipt_payment.payment.name] += receipt_payment.amount

    return render(req, 'report/day.html', {
        'report_data': report_data
    })


def report_month(req):
    report_data = {
        'total': 0,
        'sum_total_with_category': {},
        'total_discount': 0,
        'submit': False,
        'payments': {},
        'receipt_details_count': 0,
        'receipt_details': {},
        'date': '---'
    }

    for payment in Payment.objects.all():
        report_data['payments'][payment.name] = 0

    if req.method == 'POST':
        report_data['submit'] = True
        month = req.POST['month']
        year = req.POST['year']

        if not month:
            return render(req, 'report/month.html', {
                'report_data': report_data,
                'month_error': 'ກະລຸນາໃສ່ຂໍ້ມູນເດືອນ'
            })

        if not year:
            return render(req, 'report/month.html', {
                'report_data': report_data,
                'year_error': 'ກະລຸນາໃສ່ຂໍ້ມູນປີ'
            })

        report_data['date'] = f'{month}/{year}'

        receipts = Receipt.objects.filter(
            created_at__month=month,
            created_at__year=year,
            status='new'
        )

        if receipts.exists():
            for receipt in receipts:
                # sum total discount
                report_data['total_discount'] += receipt.get_total_discount()

                # sum total
                report_data['total'] += receipt.total

                #sum total with category
                for detail in receipt.details(status=True):
                    category = detail.menu.category.parent
                    total = detail.amount()

                    if category in report_data['sum_total_with_category']:
                        report_data['sum_total_with_category'][category] += total 
                    else:
                        report_data['sum_total_with_category'][category] = total 
                
                #sum qty of menu
                for detail in receipt.details(status=True):
                    menu_name = detail.menu.name
                    if menu_name in report_data['receipt_details']:
                        report_data['receipt_details'][menu_name] += detail.qty
                    else:
                        report_data['receipt_details'][menu_name] = detail.qty

                report_data['receipt_details_count'] = len(report_data['receipt_details'])

                # sum total payment
                for receipt_payment in receipt.payments():
                    report_data['payments'][receipt_payment.payment.name] += receipt_payment.amount

    return render(req, 'report/month.html', {
        'report_data': report_data,
        'month_error': False,
        'year_error': False
    })


def report_year(req):
    report_data = {
        'total': 0,
        'sum_total_with_category': {},
        'total_discount': 0,
        'submit': False,
        'payments': {},
        'receipt_details_count': 0,
        'receipt_details': {},
        'date': '---'
    }

    for payment in Payment.objects.all():
        report_data['payments'][payment.name] = 0

    if req.method == 'POST':
        report_data['submit'] = True
        year = req.POST['year']

        if not year:
            return render(req, 'report/month.html', {
                'report_data': report_data,
                'year_error': 'ກະລຸນາໃສ່ຂໍ້ມູນປີ'
            })

        report_data['date'] = year

        receipts = Receipt.objects.filter(
            created_at__year=year,
            status='new'
        )

        if receipts.exists():
            for receipt in receipts:
                # sum total discount
                report_data['total_discount'] += receipt.get_total_discount()

                # sum total
                report_data['total'] += receipt.total

                #sum total with category
                for detail in receipt.details(status=True):
                    category = detail.menu.category.parent
                    total = detail.amount()

                    if category in report_data['sum_total_with_category']:
                        report_data['sum_total_with_category'][category] += total 
                    else:
                        report_data['sum_total_with_category'][category] = total 
                
                #sum qty of menu
                for detail in receipt.details(status=True):
                    menu_name = detail.menu.name
                    if menu_name in report_data['receipt_details']:
                        report_data['receipt_details'][menu_name] += detail.qty
                    else:
                        report_data['receipt_details'][menu_name] = detail.qty

                report_data['receipt_details_count'] = len(report_data['receipt_details'])

                # sum total payment
                for receipt_payment in receipt.payments():
                    report_data['payments'][receipt_payment.payment.name] += receipt_payment.amount

    return render(req, 'report/year.html', {
        'report_data': report_data,
        'year_error': False
    })
