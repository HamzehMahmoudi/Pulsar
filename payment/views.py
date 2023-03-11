from django.shortcuts import render, redirect

# Create your views here.
import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from azbankgateways.exceptions import AZBankGatewaysException
from django.views.generic import View
# Create your views here.
from payment.models import Transaction
from accounts.models import AppToken
from django.utils import timezone

class Pay(View):
    def post(self, request):
        amount = 1000
        user_mobile_number = request.user.phone  
        project_id:str = request.POST.get('project_id', '')
        if project_id.isnumeric():
            project_id = int(project_id)
        else:
            return HttpResponseBadRequest()
        factory = bankfactories.BankFactory()
        try:
            bank = factory.auto_create() # or factory.create(bank_models.BankType.BMI) or set identifier
            bank.set_request(request)
            bank.set_amount(amount)
            bank.set_client_callback_url(reverse('callback-gateway'))
            bank.set_mobile_number(user_mobile_number)
            bank_record = bank.ready()
            tc = bank_record.tracking_code
            t = Transaction.objects.create(tracking_code=tc, project_id=project_id)
            return bank.redirect_gateway()
        except AZBankGatewaysException as e:
            logging.critical(e)
            raise e
    
    def get(self, request):
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        if not tracking_code:
            logging.debug("این لینک معتبر نیست.")
            raise Http404

        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        except bank_models.Bank.DoesNotExist:
            logging.debug("این لینک معتبر نیست.")
            raise Http404

        # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
        if bank_record.is_success:
            t = Transaction.objects.get(tracking_code=bank_record.tracking_code)
            project= t.project
            month = timezone.now() + timezone.timedelta(days=30)
            token = AppToken.objects.create(project=project, expire_on=month.date())
            return redirect('projects')

        # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
        return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")