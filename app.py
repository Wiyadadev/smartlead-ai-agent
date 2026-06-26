import os
import json
import time
import pandas as pd
import requests
import gradio as gr
from openai import OpenAI

GOOGLE_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

BASE_COLUMNS = ["Business Name", "Address", "Phone", "Website", "Rating", "Reviews"]
AI_COLUMNS = ["AI Score", "AI Summary", "AI Message"]

def search_business(business_type, location, max_results):
    if not GOOGLE_API_KEY:
        return pd.DataFrame(columns=BASE_COLUMNS), "No GOOGLE_PLACES_API_KEY found"
    if not business_type or not business_type.strip():
        return pd.DataFrame(columns=BASE_COLUMNS), "Please enter a business type"
    query = f"{business_type} in {location}" if location and location.strip() else business_type
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.websiteUri,places.rating,places.userRatingCount,places.businessStatus,nextPageToken",
    }
    body = {"textQuery": query, "pageSize": min(int(max_results), 20)}
    rows = []
    page_token = None
    try:
        while len(rows) < max_results:
            if page_token:
                body["pageToken"] = page_token
                time.sleep(2)
            resp = requests.post(url, headers=headers, json=body, timeout=15)
            data = resp.json()
            if resp.status_code != 200:
                err = data.get("error", {})
                return pd.DataFrame(columns=BASE_COLUMNS), f"Google API Error: {err.get('status')} {err.get('message','')}"
            for place in data.get("places", []):
                if len(rows) >= max_results:
                    break
                if place.get("businessStatus") == "CLOSED_PERMANENTLY":
                    continue
                rows.append({
                    "Business Name": place.get("displayName", {}).get("text", "-"),
                    "Address": place.get("formattedAddress", "-"),
                    "Phone": place.get("nationalPhoneNumber", "-"),
                    "Website": place.get("websiteUri", "-"),
                    "Rating": place.get("rating", "-"),
                    "Reviews": place.get("userRatingCount", "-"),
                })
            page_token = data.get("nextPageToken")
            if not page_token:
                break
    except Exception as e:
        return pd.DataFrame(columns=BASE_COLUMNS), f"Connection error: {e}"
    if not rows:
        return pd.DataFrame(columns=BASE_COLUMNS), "No results found"
    return pd.DataFrame(rows), f"Found {len(rows)} businesses for: {query}"

def generate_ai_insight(row, business_type):
    prompt = (
        "You are a sales and lead generation expert.\n"
        "Business info:\n"
        f"- Name: {row.get('Business Name', '-')}\n"
        f"- Type: {business_type}\n"
        f"- Address: {row.get('Address', '-')}\n"
        f"- Rating: {row.get('Rating', '-')} ({row.get('Reviews', '-')} reviews)\n"
        f"- Website: {row.get('Website', '-')}\n\n"
        "Reply in JSON only, no other text:\n"
        '{"score": <1-10>, "summary": "<1-2 sentence summary>", "message": "<cold email under 4 sentences>"}'
    )
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    content = response.choices[0].message.content.strip()
    content = content.replace("```json", "").replace("```", "").strip()
    return json.loads(content)

def analyze_leads(df, business_type, progress=gr.Progress()):
    if df is None or len(df) == 0:
        return df, "No leads to analyze. Please search first."
    if not openai_client:
        return df, "No OPENAI_API_KEY found"
    df = df.copy()
    for col in AI_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    total = len(df)
    errors = 0
    for i, row in df.iterrows():
        progress((i + 1) / total, desc=f"Analyzing {row.get('Business Name', '')}...")
        try:
            result = generate_ai_insight(row, business_type)
            df.at[i, "AI Score"] = str(result.get("score", "-"))
            df.at[i, "AI Summary"] = result.get("summary", "-")
            df.at[i, "AI Message"] = result.get("message", "-")
        except Exception as e:
            errors += 1
            df.at[i, "AI Summary"] = f"Error: {e}"
    msg = f"Analyzed {total} leads successfully"
    if errors:
        msg += f" ({errors} errors)"
    return df, msg

def export_csv(df):
    if df is None or len(df) == 0:
        return None
    path = "/tmp/smartlead_export.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path

with gr.Blocks() as demo:
    gr.HTML(
        '<div style="text-align:center;padding:28px 20px;border-radius:16px;'
        'background:linear-gradient(135deg,#4f46e5 0%,#06b6d4 100%);color:white;margin-bottom:18px;">'
        '<h1 style="margin:0;font-size:28px;">SmartLead AI Agent</h1>'
        '<p style="margin:6px 0 0 0;opacity:0.92;font-size:15px;">'
        'Find real business leads from Google Maps and analyze with AI'
        "</p></div>"
    )
    with gr.Row():
        business_type = gr.Textbox(label="Business Type", placeholder="e.g. Restaurant, Dentist, Real Estate", scale=2)
        location = gr.Textbox(label="Location / City", placeholder="e.g. Bangkok, Chiang Mai", scale=2)
        max_results = gr.Slider(label="Max Results", minimum=5, maximum=30, step=5, value=10, scale=1)
    with gr.Row():
        search_btn = gr.Button("Search Leads", variant="primary")
        analyze_btn = gr.Button("Analyze with AI", variant="secondary")
        export_btn = gr.Button("Export CSV", variant="secondary")
    status = gr.Markdown("")
    results_df = gr.Dataframe(value=pd.DataFrame(columns=BASE_COLUMNS), label="Results", wrap=True, interactive=False)
    csv_file = gr.File(label="Download CSV")
    search_btn.click(fn=search_business, inputs=[business_type, location, max_results], outputs=[results_df, status])
    analyze_btn.click(fn=analyze_leads, inputs=[results_df, business_type], outputs=[results_df, status])
    export_btn.click(fn=export_csv, inputs=[results_df], outputs=[csv_file])

demo.launch(server_name="0.0.0.0", server_port=7860)
