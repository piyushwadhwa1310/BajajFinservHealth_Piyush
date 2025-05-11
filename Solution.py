import requests

generate_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"

payload = {
    "name": "Piyush Wadhwa",
    "regNo": "0827CI221099",
    "email": "piyushwadhwa220271@acropolis.in"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(generate_url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    webhook_url = data["webhook"]
    access_token = data["accessToken"]
else:
    print("[✘] Failed to generate webhook.")
    exit()

sql_query = """
SELECT 
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    TIMESTAMPDIFF(YEAR, e.DOB, CURDATE()) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE DAY(p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1;
""".strip()

submit_headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

submit_payload = {
    "finalQuery": sql_query
}

submit_response = requests.post(webhook_url, json=submit_payload, headers=submit_headers)

if submit_response.status_code == 200:
    print("[✔] SQL query submitted successfully.")
    print("Response:", submit_response.json())
else:
    print("[✘] Failed to submit SQL query.")
    print("Status Code:", submit_response.status_code)
    print("Response:", submit_response.text)
