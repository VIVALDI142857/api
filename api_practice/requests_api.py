import requests
import pandas as pd
import numpy as np

url = 'http://localhost:8000/predictions'

response = requests.get(url)
print(response.text)