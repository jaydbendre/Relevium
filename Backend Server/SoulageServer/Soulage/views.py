from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import numpy as np
import pandas as pd
import json
from .models import Data_Collection, Request, Donations, Topics, Organisations, User, Tweet_Sentiment, Tweet_Image_class, POC_requests, User_Organisation_Map

import datetime as dt

months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sept",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}

progress_bar_class = {
    0: "progress-bar progress-bar-danger",
    1: "progress-bar progress-bar-warning",
    2: "progress-bar progress-bar-info",
    3: "progress-bar progress-bar-success",

}
important_usernames = [
    "cnnbrk",
    "nytimes",
    "cnn",
    "bbcworld",
    "ndtv",
    "aajtak",
    "ABPNews",
    "TimesNow",
    "MoHFW_INDIA",
    "mygovindia"
]

"""
WEBSITE
"""

"""
Index of the webpage
"""
location_data = {
    "location1": (8.68008, 39.68547),
    "location2": (26.27027, 175.15021),
    "location3": (18.05972, -146.72540),
    "location4": (16.78504, 156.86359),
    "location5": (3.04360, 95.91908),
    "location6": (12.04289, 79.76505),
    "location7": (40.85454, 39.61262),
    "location8": (10.15598, 147.08270),
    "location9": (10.24108, -41.60236),
    "location10": (27.80297, 121.36428),
    "Kolkata": (27.80297, 121.36428)
}

classes = {'Explicit': 0,
           'Meme': 1,
           'Nature': 2,
           'Other': 3,
           'Poster': 4,
           'Potrait': 5,
           'Protests': 6,
           'cyclone': 7,
           'earthquake': 8,
           'flood': 9,
           'wildfire': 10}


def index(request):
    return render(request, "index.html")
    pass


def logout(request):
    request.session = ""
    return render(request, "index.html")


def render_admin_login(request):
    return render(request, "login.html", {"Error": ""})


def admin_login(request):
    username = request.POST["username"]
    password = request.POST["password"]

    user_data = User.objects.get(email=username, password=password)
    if user_data == None:
        return render(request, "login.html", {"Error": "Invalid Credentials"})
    else:
        if user_data.role == 0:
            # return HttpResponse(user_data)
            data = dict()
            request.session["role"] = "Administrator"
            request.session["name"] = user_data.first_name + \
                " " + user_data.last_name
            # data["donation_amount_wk_1"] = [
            #     0, 0, 10000, 2000, 8000, 5000, 7500]
            # data["donation_amount_wk_2"] = [
            #     6000, 1000, 5000, 7000, 2700, 8500, 9600]

            # data["donation_total_wk_1"] = sum(data["donation_amount_wk_1"])
            # data["donation_total_wk_2"] = sum(data["donation_amount_wk_2"])

            # users = User.objects.all().values("location").annotate(
            #     count=Count("location")).order_by("-location")

            # data["markers"] = []
            # data["mapData"] = dict()
            # for user in users:
            #     data["markers"].append({
            #         "latLng": [location_data[user["location"]][0], location_data[user["location"]][1]],
            #         "name": "{} : {}".format(user["location"], user["count"])
            #     })

            #     data["mapData"][user["location"]] = user["count"]
            return render_admin_dashboard(request)

            return render(request, "Admin/admin_dashboard.html", {"data": data})
        elif user_data.role == 4:
            request.session["role"] = "Validating Entity"
            request.session["name"] = user_data.first_name + \
                " " + user_data.last_name
            return render(request, "VE/ve_index.html")
        elif user_data.role == 2:
            request.session["role"] = "Organisational POC"
            request.session["name"] = user_data.first_name + \
                " " + user_data.last_name
            user_org = User_Organisation_Map.objects.get(user_id=user_data.id)
            request.session["org_id"] = user_org.org_id.id
            import ast
            user_org_map = User_Organisation_Map.objects.filter(
                org_id=request.session["org_id"])

            data = dict()
            number_of_users = len(user_org_map)

            donations = Request.objects.filter(
                is_approved=1, org_id=request.session["org_id"])

            pending_donations = Request.objects.filter(
                is_approved=0, is_active=1, org_id=request.session["org_id"])

            total_money = 0
            for donation in donations:
                description = ast.literal_eval(donation.description)
                total_money += description["collected_amount"]
            data["count_user"] = number_of_users
            data["count_donations"] = len(donations)
            data["count_money"] = "₹{}".format(total_money)
            data["count_pending"] = len(pending_donations)
            return render(request, "OrganizationalPOC/poc_index.html", {"data": data})
    pass


"""
Administrative view functions
"""


"""Load  Admin Dashboard
"""


def render_admin_dashboard(request):
    data = dict()
    data["donation_amount_wk_1"] = [
        0, 0, 10000, 2000, 8000, 5000, 7500]
    data["donation_amount_wk_2"] = [
        6000, 1000, 5000, 7000, 2700, 8500, 9600]

    data["donation_total_wk_1"] = sum(data["donation_amount_wk_1"])
    data["donation_total_wk_2"] = sum(data["donation_amount_wk_2"])

    users = User.objects.all().values("location").annotate(
        count=Count("location")).order_by("-location")

    data["markers"] = []
    data["mapData"] = dict()
    for user in users:
        data["markers"].append({
            "latLng": [location_data[user["location"]][0], location_data[user["location"]][1]],
            "name": "{} : {}".format(user["location"], user["count"])
        })

        data["mapData"][user["location"]] = user["count"]

    return render(request, "Admin/admin_dashboard.html", {"data": data})


"""
Load tables editable by admin    
"""


def admin_tables(request):

    users = User.objects.all().values("id", "first_name", "last_name",
                                      "email", "twitter_user_name", "location", "date_of_birth", "role")

    donations = Request.objects.all().values("id", "description", "org_id",
                                             "topic_id", "initiated_at", "decision_passed_at")

    org = Organisations.objects.all().values(
        "id", "org_name", "typeOrg", "location", "POC_user_id")

    tweets = Data_Collection.objects.all().values(
        "id", "text", "user_name", "created_at", "media_type")[0:100]
    data = dict()
    data["users"] = users
    data["donations"] = donations
    data["organisations"] = org
    data["tweets"] = tweets
    return render(request, "Admin/admin_tables.html", {"data": data})


def model_tester(request):
    return render(request, "Admin/test_model.html")


"""
Validating Entity 
"""

"""
Page after login VE
"""


def render_ve_dashboard(request):
    return render(request, "VE/ve_index.html")
    pass


def model_tester(request):
    return render(request, "VE/test_model.html")


def ve_request_donation(request):
    # {"Contact_number": 9234312434, "Location": "Mumbai", "Info": "Regarding Covid-19", "Requirements": [
    #     "Face Masks", "Sanitizers", "Medicines"], "goal": [100, 100, 50], "Current": [20.0, 20.0, 5.0], "collected_amount": 5000}
    requests = Request.objects.filter(is_active=1, is_approved=0).all()

    request_data = list()
    import ast
    for r in requests:
        if r.description == "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum":
            continue
        description = ast.literal_eval(r.description)

        data_dict = {
            "id": r.id,
            "info": description["Info"],
            "location": description["Location"]
        }
        organization = Organisations.objects.get(id=r.org_id.id)

        data_dict["org_name"] = organization.org_name
        data_dict["requested_at"] = r.initiated_at
        request_data.append(
            data_dict
        )

    return render(request, "VE/ve_request_decision.html", {"data": request_data, "accept": "", "reject": ""})


def ve_organization_request(request):

    {
        "organization_name": "organization omega",
        "domain": "Pet relief",
        "website": "https://this_is_my_org.com/in",
        "networth": 7000000,
        "hq_location": "Kolkata"
    }
    poc_requests = POC_requests.objects.filter(is_active=1).all()

    import ast
    data = list()
    for poc in poc_requests:
        details = ast.literal_eval(poc.organisation_details)
        data.append({
            "id": poc.id,
            "poc_name": poc.name,
            "org_name": details["organization_name"],
            "domain": details["domain"],
            "networth": "₹{}".format(details["networth"]),
            "hq_location": details["hq_location"],
            "website": details["website"],
            "requested_at": poc.requested_at
        })

    return render(request, "VE/ve_poc_requests.html", {"data": data, "accept": "", "reject": ""})


def ve_request_decision(request, id, decision):
    import ast

    requests = Request.objects.filter(id=id).update(
        is_active=0, is_approved=decision, decision_passed_at=dt.datetime.now())

    requests = Request.objects.filter(is_active=1, is_approved=0).all()

    request_data = list()

    for r in requests:
        if type(r.description) == None:
            pass
        print(r.description)
        description = ast.literal_eval(r.description)

        data_dict = {
            "id": r.id,
            "info": description["Info"],
            "location": description["Location"]
        }
        organization = Organisations.objects.get(id=r.org_id.id)

        data_dict["org_name"] = organization.org_name
        data_dict["requested_at"] = r.initiated_at
        request_data.append(
            data_dict
        )

    if decision:
        return render(request, "VE/ve_request_decision.html", {"data": request_data, "accept": "Accepted Successfully", "reject": ""})
    else:
        return render(request, "VE/ve_request_decision.html", {"data": request_data, "accept": "", "reject": "Request Rejected"})
    return


def ve_poc_decision(request, id, decision):
    import ast
    {
        "organization_name": "organization omega",
        "domain": "Pet relief",
        "website": "https://this_is_my_org.com/in",
        "networth": 7000000,
        "hq_location": "Kolkata"
    }
    requests = POC_requests.objects.filter(id=id).update(
        is_active=0, is_approved=decision, decision_passed_at=dt.datetime.now())

    org_data = POC_requests.objects.get(id=id)
    fname, lname = org_data.name.split(" ")
    details = ast.literal_eval(org_data.organisation_details)

    if decision:
        User.objects.create(
            first_name=fname,
            last_name=lname,
            email=org_data.email,
            password="default_password",
            location=details["hq_location"],
            date_of_birth=dt.datetime.now().date(),
            verified_at=dt.datetime.now(),
            role=2
        )

        user_data = User.objects.get(email=org_data.email)

        Organisations.objects.create(
            org_name=details["organization_name"],
            typeOrg=3,
            is_verified=1,
            location=details["hq_location"],
            joining_time=dt.datetime.now(),
            POC_user_id=user_data.id
        )

    poc_requests = POC_requests.objects.filter(is_active=1).all()

    data = list()
    for poc in poc_requests:
        details = ast.literal_eval(poc.organisation_details)
        data.append({
            "id": poc.id,
            "poc_name": poc.name,
            "org_name": details["organization_name"],
            "domain": details["domain"],
            "networth": "₹{}".format(details["networth"]),
            "hq_location": details["hq_location"],
            "website": details["website"],
            "requested_at": poc.requested_at
        })

    if decision:
        return render(request, "VE/ve_poc_requests.html", {"data": data, "accept": "Accepted Successfully", "reject": ""})
    else:
        return render(request, "VE/ve_poc_requests.html", {"data": data, "accept": "", "reject": "Request Rejected"})
    return


"""
Organisational Pocket
"""


def poc_index(request):
    import ast
    user_org_map = User_Organisation_Map.objects.filter(
        org_id=request.session["org_id"])

    data = dict()
    number_of_users = len(user_org_map)

    donations = Request.objects.filter(
        is_approved=1, org_id=request.session["org_id"])

    pending_donations = Request.objects.filter(
        is_approved=0, is_active=1, org_id=request.session["org_id"])

    total_money = 0
    for donation in donations:
        description = ast.literal_eval(donation.description)
        total_money += description["collected_amount"]
    data["count_user"] = number_of_users
    data["count_donations"] = len(donations)
    data["count_money"] = "₹{}".format(total_money)
    data["count_pending"] = len(pending_donations)
    return render(request, "OrganizationalPOC/poc_index.html", {"data": data})


def poc_imp_tweets(request):
    data = dict()

    tweet_data = Data_Collection.objects.filter(
        user_name__in=important_usernames)

    data["tweet"] = list()
    for tweet in tweet_data:
        created_at = dt.datetime.strptime(
            tweet.created_at, "%Y-%m-%d %H:%M:%S")
        data["tweet"].append(
            {
                "text": tweet.text,
                "time": "{}th {} {}".format(created_at.day, months[created_at.month], str(created_at.year)[2:]),
                "username": tweet.user_name,
                "profile_url": "static/assets/img/imp_username/{0}.png".format(tweet.user_name)
            }
        )

    data["imp_tweet_handle"] = important_usernames
    # return HttpResponse(data.items())
    return render(request, "OrganizationalPOC/poc_imp_tweets.html", {"data": data})


def render_poc_users(request):
    users = User_Organisation_Map.objects.filter(
        org_id=request.session["org_id"])

    data = list()
    for user in users:
        user_data = User.objects.get(id=user.user_id.id)
        data_dict = {
            "fname": user_data.first_name,
            "lname": user_data.last_name,
            "email": user_data.email,
            "handle": user_data.twitter_user_name,
            "lop": user_data.location,
        }

        if user_data.role == 2:
            data_dict["role"] = "POC"
        else:
            data_dict["role"] = "Org. User"

        data.append(data_dict)
    return render(request, "OrganizationalPOC/poc_users.html", {"data": data})


def view_poc_donations(request):
    import ast
    donations = Request.objects.filter(
        is_approved=1, org_id=request.session["org_id"])

    {'Contact_number': 923422222222, 'Location': 'Pune', 'Info': 'Regarding Flood', 'Requirements': [
        'Food Packets', 'Syringes', 'Shelter Cloth'], 'goal': [100, 1000, 500], 'Current': [20, 200.0, 100], 'collected_amount': 1220}

    data = list()
    i = 0
    for donation in donations:
        description = ast.literal_eval(donation.description)
        print(donation.id)
        data_dict = {
            "info": description["Info"],
            "location": description["Location"],
            "contact": "+91 {}".format(description["Contact_number"]),
            "collected_amount": "₹ {}".format(description["collected_amount"])
        }

        data_dict["progress"] = dict()
        for r, c, g, i in zip(description["Requirements"], description["Current"], description["goal"], range(3)):
            data_dict["progress"][r] = {
                "current": c,
                "goal": g,
                "percent": "{:.2f}".format(c/g * 100),
                "progress_bar_class": progress_bar_class[i]
            }

        data.append(data_dict)

    # return HttpResponse(data)
    return render(request, "OrganizationalPOC/poc_view_donations.html", {"data": data})


"""
APIS
"""
"""
Retrieve topics
"""


@api_view(["GET"])
def get_topics(request):
    topics = Topics.objects.values("topic_name")

    topic_list = [t["topic_name"] for t in topics]
    return Response(topic_list)


"""
Retrieving specific topic donations
"""


@api_view(["GET"])
def get_request_pool(request, topic_name):
    topic = Topics.objects.get(topic_name=topic_name)

    requests = Request.objects.filter(topic_id=topic, is_active=1)

    data = list()
    for r in requests:
        description_data = json.loads(r.description)
        if description_data == None:
            pass
        else:
            request_data = {
                "contact_number": description_data["Contact_number"],
                "location": description_data["Location"],
                "info": description_data["Info"],
                "requirements": description_data["Requirements"],
                "goal": description_data["goal"],
                "current": description_data["Current"],
                "percent_complete": [(current/goal) * 100 for current, goal in zip(description_data["Current"], description_data["goal"])],
                "initiated_at": r.initiated_at
            }

            # organisation_name = organisation_name.org_name

            request_data["initiated_by"] = r.org_id.org_name

        data.append(request_data)

    return Response(data)


"""
Donations made by naive user 
"""


@api_view(["POST"])
def make_donation(request):
    donation_data = request.data["donation_data"]
    user_id = request.data["user_id"]
    request_id = request.data["request_id"]
    '''
    {
        "request_id" :
        "amount" : 
        "donated" : 
        "transaction_ref_no" :
        "mop" : 
    }
    '''

    requests = Donations(
        donate=donation_data,
        donated_at=dt.datetime.now(),
        is_complete=1,
        request_id_id=request_id,
        user_id_id=user_id
    ).save()

    # donation_data = json.loads(donation_data)

    requests = Request.objects.get(id=request_id)
    description = json.loads(requests.description)
    print(description.keys())
    if donation_data["amount"] == "" and donation_data["donated"] != None:
        donated = donation_data["donated"]
        donated = [float(description["Current"][i]) +
                   float(donation_data["donated"][i]) for i in range(len(donated))]

        description["Current"] = str(donated)

    elif donation_data["amount"] != None and donation_data["donated"] == "":
        if "collected_amount" not in description.keys():
            description["collected_amount"] = 0
        description["collected_amount"] += donation_data["amount"]
    else:
        donated = donation_data["donated"]
        donated = [float(description["Current"][i]) +
                   float(donation_data["donated"][i]) for i in range(len(donated))]

        if "collected_amount" not in description.keys():
            description["collected_amount"] = 0
        description["Current"] = str(donated)
        description["collected_amount"] += donation_data["amount"]

    requests = Request.objects.filter(id=request_id)
    requests.update(description=description)

    return Response("Updated Successfully")


"""
Validating Entity
"""


"""
Approve or reject donation requests
"""


@api_view(["POST"])
def approve_reject_requests(request):
    request_id = request.data["request_id"]
    decision = request.data["decision"]
    # print(type(request_id), type(decision))
    requests = Request.objects.filter(id=request_id)

    requests.update(
        is_approved=decision, decision_passed_at=dt.datetime.now()
    )

    return Response("Dumped Successfully")


"""
Get Dashboard data 
"""


@api_view(["GET"])
def get_dashboard_data(request):
    records = Data_Collection.objects.order_by("-created_at")[:20]

    final_data = list()
    for record in records:

        sentiment = Tweet_Sentiment.objects.get(tweet_id_id=record.id)
        sentiment = sentiment.__dict__
        # return HttpResponse(sentiment)

        data = dict()
        data["chart_data"] = list()
        sent_to_color = {"empty": "#000000", "sadness": "#808080", "enthusiasm": "#FF8C00", "neutral": "#FFFFE0", "worry": "#FFFF00",
                         "surprise": "#4169E1", "love": "#FF1493", "fun": "#FF0000", "hate": "#4B0082", "happiness": "#32CD32", "boredom": "#696969", "relief": "#ADFF2F", "anger": "#800000"}

        for k, v in sentiment.items():
            if k == "_state" or k == "id" or k == "tweet_id_id":
                continue
            else:
                data["chart_data"].append(
                    {
                        "name": k,
                        "percent": v,
                        "color": sent_to_color[k],
                        "legendFontColor": "#7F7F7F",
                        "legendFontSize": 15
                    }
                )

        data["tweet_data"] = {
            "text": record.text,
            "created_at": record.created_at,
            "tweeted_by": record.user_name.encode(encoding="UTF-8"),
            "id": record.id
        }

        if record.media_type != None:
            data["media_data"] = {
                "media_type": record.media_type,
                "media_url": record.media_url
            }

            image_class = Tweet_Image_class.objects.get(tweet_id_id=record.id)

            image_class = image_class.__dict__

            for k, v in image_class.items():
                if k == "_state" or k == "id" or k == "tweet_id_id":
                    continue
                else:
                    data["media_data"][k] = v
            # response = requests.get(record.media_url)
            # img = image.load_img(BytesIO(response.content),
            #                      target_size=(128, 128), color_mode="rgb")

            # img = image.img_to_array(img)

            # img = np.expand_dims(img, axis=0)

            # results = NeuralnetworkConfig.image_class_predictor.predict(img)
            # i = 0
            # for keys in classes.keys():
            #     data["media_data"]["class_data"][keys] = results[0][i] * 100
            #     i += 1
            # records = Data_Collection.objects
    # data["total_users"] = records.values(
    #     "user_name").distinct().count()
    # data["total_tweets"] = records.values("id").count()
    # data["total_locations"] = records.values(
    #     "place").distinct().count()

        final_data.append(data)

    return Response(final_data)
