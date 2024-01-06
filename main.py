import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

Stock_api_key = "AOS60LWYDXPXLYOJ"
news_api = "e0c9e491d3014cd8aa207fba4a0f4388"

account_sid = "ACbaeeb29afee61d40c4812b59f5bf560a"
auth_token = "d3d6fabf167a464bf5f627000438a47a"


# another method to get data from url in json formate
# url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=AOS60LWYDXPXLYOJ"
# r = requests.get(url)
# data = r.json()
# print(data)

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_prams = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":Stock_api_key,
}

response = requests.get(STOCK_ENDPOINT, params=stock_prams)
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_close = yesterday_data["4. close"]
print(yesterday_close)

#TODO 2. - Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_data_close = day_before_yesterday_data["4. close"]
print(day_before_yesterday_data_close)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(day_before_yesterday_data_close) - float(yesterday_close)
Up_down = None
if difference > 0:
    Up_down = "⬆️"
else:
    Up_down = "⬇️"

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
difference_percentage = round((difference / float(yesterday_close)) *100)
print(difference_percentage)
#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
## STEP 2: https://newsapi.org/ 
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if abs(difference_percentage) <5:
    news_params = {
        "apiKey":news_api,
        "q":COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    artical = news_response.json()["articles"]
    print(artical)
    

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
three_articals = artical[:3]
# print(three_articals)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
# [newitem for item in list]
formated_articals = [f"{STOCK_NAME}:{Up_down}{difference_percentage}% \nHeadline: {artical['title']}. \n Brief:{artical['description']}" for artical in three_articals]

#TODO 9. - Send each article as a separate message via Twilio. 
client = Client(account_sid, auth_token)
for artical in formated_articals:

    message = client.messages \
        .create(
        body=artical,
        from_="+13036474357",
        to='+923164499323'
    )


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

