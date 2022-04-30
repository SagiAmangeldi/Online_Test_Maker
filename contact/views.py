from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .forms import ContactForm

@login_required
def contact(request):

    form = ContactForm(request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data

        ult_message = "---Contact US message---\n"
        ult_message += "username: %s, e-mail: %s\n" %(request.user.username, request.user.email)
        ult_message += cd['message']
        send_mail(cd['subject'],
                ult_message,
                'Dayindal.com Support <support@dayindal.com>',
                ['askaryusupov@gmail.com', 'berikmindetbay@gmail.com', 'support@dayindal.com'],
        )

        return HttpResponseRedirect(reverse('contact:thanks'))

    return render(request, 'contact/contact.html', {'form': form})
