# Create your views here.
from django.shortcuts import render
from discoverify.models import *
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import string
from random import randint
from django.template import RequestContext
from django.shortcuts import render_to_response
import datetime
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import simplejson
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def logout_view(request):
	logout(request)
	return HttpResponseRedirect('http://bits-oasis.org/2014/discoverify/')

def home_view(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('index.html', context_dict, context)

def create_dummy_view(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('createPathWizard.html', context_dict, context)

def path_details_view(request,path_id):
	selected_path = Path.objects.get(id=int(path_id))
	all_steps = selected_path.steps.all()
	no_of_steps = len(all_steps)
	context = RequestContext(request)
	context_dict = {'selected_path':selected_path,'no_of_steps':no_of_steps,'all_steps':all_steps}
	return render_to_response('learnPage.html', context_dict, context)


def edit_path_view(request,path_id):
	if not request.user.is_authenticated():
		return HttpResponse('Forbidden')
	selected_path = Path.objects.get(id=int(path_id))
	if request.user != selected_path.author:
		return HttpResponse("You don't own this learning path")
	tags = ''.join([x.name for x in selected_path.tag.all()])
	all_steps = selected_path.steps.all()
	context = RequestContext(request)
	context_dict = {'selected_path':selected_path,'tags':tags,'all_steps':all_steps}
	return render_to_response('editPage.html', context_dict, context)


def step_details_view(request,step_id=0):
	if request.POST:
		step_id=request.POST['step_id']
	selected_step = Step.objects.get(id=int(step_id))

	context = RequestContext(request)
	context_dict = {'selected_step':selected_step}
	return render_to_response('stepage.html', context_dict, context)


def add_step_end(request):
	if request.POST:
		if not request.user.is_authenticated():
			return HttpResponse('Forbidden')
		path_id=request.POST['path_id']
		selected_path = Path.objects.get(id=int(path_id))
		if request.user != selected_path.author:
			return HttpResponse("You don't own this learning path")
		new_step_number = len(selected_path.steps.all())+1
		####### Not adding exception handling now
		short_desc = request.POST['short_description']
		long_desc = request.POST['long_description']
		resources = 'more placeholder stuff'
		#add forums stuff
		new_step = Step(number=new_step_number,short_description=short_desc,long_description=long_desc,resources=resources)
		new_step.save()		
		for x in range(1,5):
			if not request.POST['url_link'+str(x)]:
				continue 
			l = Link(name='placeholder',url_link=request.POST['url_link'+str(x)],linl_type=request.POST['category'+str(x)])
			l.save()
			new_step.links.add(l)
			new_step.save()
		selected_path.steps.add(new_step)
		return HttpResponse('{"message":"sucess","status":"1","step_no":%s,"step_id":%s,"step_desc":"%s"}' %(new_step.number,new_step.id,new_step.short_description))





def create_path(request):
	if request.POST:
		if not request.user.is_authenticated():
			return HttpResponse('Forbidden')
		try:
			name = request.POST['name']
			short_description = request.POST['short_description']
			img = request.FILES['img']
		except:
			return HttpResponse('Incomplete Data Sent')
		author = request.user
		online = False
		no_registrations = 0
		upvotes = 0
		#create forum stuff
		time = "0"
	
		new_path = Path(name=name,short_description=short_description,author=author,online=online,img=img,no_registrations=no_registrations,upvotes=upvotes,time=time)
		new_path.save()
		path_id = new_path.id
		return HttpResponseRedirect('/2014/discoverify/editpath/%s' % path_id)
# Create your views here.


def update_path(request):
	if request.POST:
		if not request.user.is_authenticated():
			return HttpResponse('Forbidden')
		path_id=request.POST['path_id']
		selected_path = Path.objects.get(id=int(path_id))
		if request.user != selected_path.author:
			return HttpResponse("You don't own this learning path")
		if 'long_description' in request.POST:
			selected_path.long_description = request.POST['long_description']
			selected_path.save()
		elif 'prereq' in request.POST:
			selected_path.prereq = request.POST['prereq']
			selected_path.save()
		elif 'outcomes' in request.POST:
			selected_path.outcomes = request.POST['outcomes']
			selected_path.save()
		elif 'short_description' in request.POST:
			selected_path.short_description = request.POST['short_description']
			selected_path.save()
		elif 'faq' in request.POST:
			selected_path.faq = request.POST['faq']
			selected_path.save()
		# elif img in request.POST:
		# 	selected_path.img = request.POST['img']
		elif 'tags' in request.POST:
			tags_cs = request.POST['tags']
			tags = tags_cs.split(',')
			all_old_tags = [x.name for x in Tag.objects.all()]
			for x in tags:
				if x in all_old_tags:
					old_matching_tag = Tag.objects.get(name=x)
					selected_path.tag.add(old_matching_tag)
				else:
					t = Tag(name=x)
					t.save()
					all_old_tags.append(x)
					selected_path.tag.add(t)
		selected_path.save()
	return HttpResponse('{"message":"sucess","status":"1"}')


def update_step(request,step_id):
	selected_step = Step.objects.get(id=int(step_id))
	if request.POST:
		if not request.user.is_authenticated():
			return HttpResponse('Forbidden')
		path_id=request.POST['path_id']
		selected_path = Path.objects.get(id=int(path_id))
		if request.user != selected_path.author:
			return HttpResponse("You don't own this learning path")
		####### Not adding exception handling now
		short_desc = request.POST['short_description']
		long_desc = request.POST['long_description']
		resources = 'more placeholder stuff'
		selected_step.short_description = short_desc
		selected_step.long_description = long_desc
		selected_step.save()
		all_links = [x for x in selected_step.links.all()]
		for link in all_links:
			selected_step.links.remove(link)
			selected_step.save()
		for x in range(1,5):
			if not request.POST['url_link'+str(x)]:
				continue 
			l = Link(name='placeholder',url_link=request.POST['url_link'+str(x)],linl_type=request.POST['category'+str(x)])
			l.save()
			selected_step.links.add(l)
			selected_step.save()
		selected_step.save()
		return HttpResponse('{"message":"sucess","status":"1"}')
	else:
		resp = {}
		resp['num'] = str(selected_step.number)
		resp['short_description'] = str(selected_step.short_description)
		resp['long_description'] = str(selected_step.long_description)
		resp['links'] = []
		for link in selected_step.links.all():
			t = {}
			t['id'] = str(link.id)
			t['name'] = str(link.name)
			t['linl_type'] = str(link.linl_type)
			t['url_link'] = str(link.url_link)
			resp['links'].append(t)
		json = simplejson.dumps(resp)
		return HttpResponse(json, mimetype='application/json')


def remove_step(request):
	if request.POST:
		if not request.user.is_authenticated():
			return HttpResponse('Forbidden')
		step_id=request.POST['step_id']
		path_id= request.POST['path_id']
		selected_step = Step.objects.get(id=int(step_id))
		selected_path = Path.objects.get(id=int(path_id))
		if request.user != selected_path.author:
			return HttpResponse("You don't own this learning path")
		#Now check if the step to be remmoved is the last tep
		#Dirty hack again :/
		if selected_step.number == max([x.number for x in selected_path.steps.all()]):
			selected_path.steps.remove(selected_step)
			return HttpResponse('{"status":"1","message":"sucess"}')
		else:
			all_steps_with_higer_number = [x for x in selected_path.steps.all() if x.number>selected_step.number]
			selected_path.steps.remove(selected_step)
			for x in all_steps_with_higer_number:
				x.number -= 1
				x.save()
			return HttpResponse('{"status":"1","message":"sucess"}')


def get_steps(request):
	if request.POST:
		path_id=request.POST['path_id']
	selected_path = Path.objects.get(id=int(path_id))
	resp={}
	resp['Steps']=[]
	all_steps = selected_path.steps.all()
	for step in all_steps:
		temp = {}
		temp['id'] = step.id
		temp['number'] = step.number
		temp['short_description'] = step.short_description
		temp['long_description'] = step.long_description
		temp['resources'] = step.resources
		# temp['links'] = []
		# for link in step.links.all():
		# 	t = {}
		# 	t['id'] = link.id
		# 	t['name'] = link.name
		# 	t['linl_type'] = link.linl_type
		# 	t['url_link'] = link.url_link
		# 	temp['links'].append(t)
		resp['Events'].append(temp)
	json = simplejson.dumps(resp)
	return HttpResponse(json, mimetype='application/json')


def InitialRegistrationView(request):
# Registration details

	if request.POST:
		# return HttpResponse(request.POST['name'])
		try:
			name = request.POST['name']
			password = request.POST['password']
			email = request.POST['email']
			# bio = request.POST['bio']
			# website = int(request.POST['website'])
		except:
			return HttpResponse('An error occured')

		member = UserInfo()
		member.name = name
		member.email = email
		member.bio = ''
		member.website = ''

		#add school related check
		registered_members = UserInfo.objects.all()

		list_of_registered_emails = [x.email for x in registered_members]
		if email in list_of_registered_emails: #check for already registered emails....no need to check if valid as we are using email field on fronted side
			status = '{ "status" : 0 , "message" : "This email/phone is already registered! Please Login!" }'
			return HttpResponse(status)
		#now create the user account
		u = User(username=email, email = email)
		u.save()
		user_pass = password
		u.set_password(user_pass)
		u.save()
		#now assign user 
		member.user = u
		member.save()

		status = '{ "status" : 1 , "message" : "Successfully Registered !", "participant_username": participant_username}'

		return HttpResponseRedirect('http://bits-oasis.org/hackiton/')
	else:
		return HttpResponseRedirect('http://bits-oasis.org/hackiton/register.html')


def user_login(request):

	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)


		if user:

			if user.is_active:

				login(request, user)
				# name = user.participant_set.all()[0].name
				# status = '{"status":"1","message":"login Successfull", "name": "%s"}' % name
				# if request.user.is_authenticated():
				# 	return HttpResponse('login ho ra h re')	
				# request.session['testing'] = request.user
				return HttpResponseRedirect('/2014/discoverify/profile/')
			else:
				status = '{"status":"0","message":"Your account is frozen and edits cannot be made now."}'
				return HttpResponse(status)
		else:
			# print "Invalid login details"
			status = '{"status":"0","message":"Invalid Login Details"}'
			return HttpResponse(status)

	else:

		return HttpResponse('Why you do this?')

def profile(request):
	if request.user.is_authenticated():
		profile = request.user.userinfo_set.all()[0]
		all_courses = Path.objects.filter(author=request.user)
		context = RequestContext(request)
		context_dict = {'all_courses':all_courses,'profile':profile}
		return render_to_response('prof.html', context_dict, context)

	else:
		return HttpResponseRedirect('http://bits-oasis.org/hackiton/login.html')