# About

A project that visualizes the total utilization of coding languages throughout my GitHub Repositories. Leverages Python and a few resources/libraries. 

# Run App

    python -m pip install -r requirements.txt
    uvicorn main:app --reload --proxy-headers --host 0.0.0.0 --port 8000
