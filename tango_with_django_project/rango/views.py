from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm


# Create your views here.

from django.http import HttpResponse

#def index(request):
#	return HttpResponse("Rango says hey there partner, like, pet! <br/> <a href='/rango/about/'>About</a>")
	
def about(request):
	context_dict = {'boldaboutmessage': "this is the boldaboutmessage context message"}
	return render(request, 'rango/about.html', context=context_dict)
	#return HttpResponse("Rango says here is the About page <br/> <a href='/rango/'>Index</a> ")

#def index(request):
	# Construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage is the same as {{ boldmessage }} in the template!
	#context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	#return render(request, 'rango/index.html', context=context_dict)

def index(request):
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary
	# that will be passed to the template engine.
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list, 'pages': page_list}	
	# Render the response and send it back!
	return render(request, 'rango/index.html', context_dict)

def show_category(request, category_name_slug):
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None
	return render(request, 'rango/category.html', context_dict)
	
def add_category(request):
	form = CategoryForm()

	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.
			cat=form.save(commit=True)
			print(cat, cat.slug)
			# Now that the category is saved
			# We could give a confirmation message
			# But since the most recent category added is on the index page
			# Then we can direct the user back to the index page.
			return index(request)
		else:
			# The supplied form contained errors -
			# just print them to the terminal.
			print(form.errors)
		# Will handle the bad form, new form, or no form supplied cases.
		# Render the form with error messages (if any).
	return render(request, 'rango/add_category.html', {'form': form})
