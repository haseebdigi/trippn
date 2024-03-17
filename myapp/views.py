from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import Trip
import json
import openai
from django.core import serializers
from .forms import TripForm

import re

# ..........................
# Create your views here.




def home(request):
    return render(request, 'index.html')


def trippn(request):
    return render(request, 'trippn.html')

def schedule(request):
    return render(request, 'schedule.html')






openai.api_key = ''
def generate_response(json_data):
    try:
        # Parse JSON data
        data = json.loads(json_data)

        # Initialize a comprehensive response
        response = "# Detailed Trip Plan\n\n"
        gpt_response = ''' '''

        # Adding more context and details to each section of the trip plan
        travel_from = data.get('travel_from', 'an unknown location')
        travel_to = data.get('travel_to', 'an unknown destination')
        response += f"## Journey Overview\n\n"
        response += f"**From**: {travel_from}\n\n**To**: {travel_to}\n\n"

        start_date = data.get('start_date', 'an unspecified start date')
        end_date = data.get('end_date', 'an unspecified end date')
        response += "## Travel Dates\n\n"
        response += f"**Start Date**: {start_date}\n\n**End Date**: {end_date}\n\n"

        travellers = data.get('travellers', 1)
        response += "## Traveller Information\n\n"
        response += f"**Number of Travellers**: {travellers}\n\n"

        

        # Here, integrate with your chatbot or response generation logic
        # Since we can't directly call external APIs here, you'd replace the following
        # with your mechanism for generating or retrieving a detailed response
        response += "Further detailed trip plan based on the provided data."


        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Please generate a comprehensive trip plan based on the details provided. The response should include proper headings, bullet points, and be structured as a well-formatted document. The plan should cover all aspects of the trip in great detail."},
                {"role": "user", "content": "Generate a trip plan with proper headings and bullets, a well-formatted structured document with comprehensive lengthy details."}
            ],
            max_tokens=2000,  # Increase max_tokens for a longer response
            temperature=0.7,  # Adjust creativity
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        gpt_response += completion.choices[0].message['content']




        return gpt_response

    except Exception as e:
        print(f"Error in generating response: {str(e)}")
        return "An error occurredzzz."

    



import re


def format_response_for_html(response_text):
    # Process bold text: Text between ** ** will be bold
    formatted_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", response_text)

    # Convert markdown bullets to HTML list items
    formatted_text = re.sub(r"^\- (.*)$", r"-> \1", formatted_text, flags=re.MULTILINE)

    # Represent sentences within headings with "->"
    formatted_text = re.sub(r"(?<=<b>)(.*?)(<\/b>\n)(\w.*)", r"\1\2-> \3", formatted_text)

    # Process headings: Text starting with #, ##, or ### will be bold and remove #, ##, or ###
    formatted_text = re.sub(r"^(#+) (.*)$", r"<br><b>\2</b>", formatted_text, flags=re.MULTILINE)

    # Replace line breaks with <br> for better HTML formatting
    formatted_text = formatted_text.replace("\n", "<br>")

    return formatted_text






def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            new_trip = form.save()
            last_trip = Trip.objects.last()
            
            # Serialize last trip to JSON
            last_trip_json = serializers.serialize('json', [last_trip,])
            last_trip_data = json.loads(last_trip_json)[0]['fields']  # Adjust based on serialization
            
            # Generate chatbot response
            response = generate_response(json.dumps(last_trip_data))
            # Assuming `response` is the chatbot's raw Markdown response
            html_response = format_response_for_html(response)
            
            # Redirect to the 'schedule' URL with the generated response as a session variable
            request.session['response'] = html_response  # Store the response in session
            return redirect('schedule')  # Redirect to 'schedule' URL name
        else:
            return render(request, 'your_form_template.html', {'form': form})
        




def schedule(request):
    response = request.session.get('response', '')  # Retrieve the response from session
    return render(request, 'schedule.html', {'formatted_response': format_response_for_html(response)})









