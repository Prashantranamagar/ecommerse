from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import auth, messages
from .models import Account
from django.contrib.auth.decorators import login_required

# VERIFICATION EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
	if request.method == "POST":
		form=RegistrationForm(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			phone_number = form.cleaned_data['phone_number']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			username = email.split("@")[0]
			user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
			user.phone_number =phone_number
			user.save()

			#USER ACTIVATION
			current_site = get_current_site(request)
			mail_subject = 'Please activate your account.'
			message = render_to_string('accounts/account_verification_email.html', {
				'user':user,
				'domain': current_site,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': default_token_generator.make_token(user),
				})
			to_email = email
			send_email = EmailMessage(mail_subject, message, to=[to_email])
			send_email.send()

			#messages.success(request, "Thank u for regestring with us . We have send you  a verification to your email, Plese verify it.")
			return redirect('account/login/command=verification&email='+email)
	else:
		form = RegistrationForm()
	
	return render(request, 'accounts/register.html', {'form':form})



def login(request):

	if request.method == "POST":
		email= request.POST.get('email')
		password= request.POST.get('password')

		user = auth.authenticate(email=email, password=password)

		if user is not None:
			auth.login(request, user)
			messages.success(request, "You are logged in.")
			return redirect('dashboard')
		else:
			messages.error(request, "Invalid login credentials")
			return redirect('login')
	return render(request, 'accounts/login.html')



@login_required(login_url ='login')
def logout(request):
	auth.logout(request)
	messages.success(request, "You are logout.")
	return redirect('login') 		


def activate(request, uidb64, token):
	try:
		uid = urlsafe_based64_decode(uid64).decode()
		user = Account._default_manager.get(pk=uid)

	except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
		user = None

	if user is not None and default_token_generator.ckeck_token(user, token):
		user.is_active = True
		user.save()
		message.success(request, "Congratulations! Your account is activate")
		return redirect('login')
	else:
		message.error(request, "Invalid activation link")
		return redirect('register')


def forgotpassword(request):

	if request.method == "POST":
		email = request.POST.get['email']
		if Account.objects.filter(email=email).exists():
			user = Account.objects.get(email__exact=email)

			#Reset Password email
			current_site= get_current_site(request)
			mail_subject = "Reset Your Password"
			message = render_to_string('accounts/reset_password_email.html', {
				'user':user,
				'domail': current_site,
				'uid':urlsafe_base64_encode(force_bytes(user.pk)),
				'token':default_token_generator.make_token(user),
				})

			to_email = email
			send_email = EmailMessage(mail_subject, message, to=[to_email])
			send_email.send()
	return render(request, 'forgotpassword.html')


@login_required(login_url = 'login')
def dashboard(request):
	return render(request, 'accounts/dashboard.html')
