import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6L-N100rQpdH8Exv1bE2DpUnusYEktp4avkwfhCZbHNVg")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Say hello")

print(response.text)