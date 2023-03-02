import openai
import os
import pandas as pd
openai.api_key = os.getenv('OPEN_API_KEY')
result = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "Find entities from the given article. Create a dataframe with two column which are the names are Entity name and Entity value and put the valuea accordingly. I want to you check names, locations(it might be a place like a school name, or hospital name), ids, dates, companies, emails, phone numbers, and IBANs. There might be more than one name, location etc. Find all of them. Giving article: 'Dr. Curt Langlotz chose to schedule a meeting on 06/23. my Emaill address is alka@gmail.com. I live in Berlin normally and I am 23 years old. PROCEDURE: Chest xray. COMPARISON: last seen on 1/1/2020 and also record dated of March 1st, 2019. FINDINGS: patchy airspace opacities. IMPRESSION: The results of the chest xray of January 1 2020 are the most concerning ones. The patient was transmitted to another service of UH Medical Center under the responsability of Dr. Perez. We used the system MedClinical data transmitter and sent the data on 2/1/2020, under the ID 5874233. We received the confirmation of Dr Perez. He is reachable at 567-493-1234. My name is Abdullah kandilli.'"}

    ]
)

content_value = result['choices'][0]['message']['content']

print(content_value)
