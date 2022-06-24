# importing twilio
from twilio.rest import Client

account_sid = 'AC1c8f2e49cf4e0851203887cdcf744c36'
auth_token = '7ce205a03e95f45debdfcba9d655b583'

client = Client(account_sid, auth_token)
message = client.messages.create(
							from_='+18646607895',
							body ='rey vachinda',
							to ='+917093594943'
						)
