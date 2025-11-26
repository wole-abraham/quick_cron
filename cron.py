from supabase import create_client
import requests
import os
from datetime import date

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]
webhook = os.environ["WEBHOOK_URL"]

supabase = create_client(url, key)


def fetch_today():
    today_str = date.today().isoformat()

    res = (
        supabase
        .table("survey")
        .select(
            "date_of_activity, reporter_name, bridge_fullname_concat, side, "
            "activity_category, activity_type, coor_x_design, coor_y_design, input_x, input_y"
        )
        .eq("date_of_activity", today_str)
        .execute()
    )

    return res.data or []


def bridge_html(rows):
    if not rows:
        return "<h2>No survey records for today.</h2>"

    html = """
    <html>
    <body>
    <p>Dear All, Kindly check the activities for the bridges daily construction summarized as the tabel below</p>
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;">
        <tr style="background-color:#333;color:white;">
            <th>date_of_activity</th>
            <th>reporter_name</th>
            <th>bridge_fullname_concat</th>
            <th>side</th>
            <th>activity_category</th>
            <th>activity_type</th>
            <th>coor_x_design</th>
            <th>coor_y_design</th>
            <th>input_x</th>
            <th>input_y</th>
        </tr>
    """

    for row in rows:
        html += "<tr>"
        html += f"<td>{row['date_of_activity']}</td>"
        html += f"<td>{row['reporter_name']}</td>"
        html += f"<td>{row['bridge_fullname_concat']}</td>"
        html += f"<td>{row['side']}</td>"
        html += f"<td>{row['activity_category']}</td>"
        html += f"<td>{row['activity_type']}</td>"
        html += f"<td>{row['coor_x_design']}</td>"
        html += f"<td>{row['coor_y_design']}</td>"
        html += f"<td>{row['input_x']}</td>"
        html += f"<td>{row['input_y']}</td>"
        html += "</tr>"

    html += """
    </table>
    <p>In addition you will see the link below for the dashbaord showing details for each activity</p>
    <p>
  <a href="https://app.powerbi.com/view?r=eyJrIjoiNTNkYjUxZDUtNjAxZi00OTYyLTkxMDAtOWMwNmJhZTA1NmFhIiwidCI6IjlkZjZjN2Q4LTk4YzktNDliYS05NmZkLTBhNzIzMjVhZGMwYSJ9">
    View Dashboard
  </a>
</p>
    </body>
    </html>
    """

    return html


def send_webhook(html):
    
    return requests.post(
        "https://hook.eu2.make.com/svxxuei9ivon08wka4dwjih5l2tfrkcy",
        data=html,
        headers={"Content-Type": "text/html"}
    )


def main():
    rows = fetch_today()
    
    html = bridge_html(rows)
    r = send_webhook(html)
    print("Webhook:", r.status_code, r.text)


if __name__ == "__main__":
    main()
