# Deploy SpeedVolt on Render

This project includes `render.yaml`, so you can deploy it as a Render Blueprint.

1. Push this project to GitHub.
2. In Render, choose **New > Blueprint**.
3. Select this repository.
4. Render will create the Python web service and a Postgres database.
5. When Render asks for `ADMIN_PASSWORD`, enter a strong password.

Render will run:

```text
pip install -r requirements.txt
bash -c 'flask --app run init-db && gunicorn run:app --bind 0.0.0.0:$PORT'
```

The free Render Postgres plan is good for testing, but it expires after 30 days. Use a paid database before relying on it for real customer orders.
