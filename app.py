import gradio as gr

def search_business(business_type):
    return f"กำลังค้นหา Lead สำหรับ: {business_type}"

with gr.Blocks(
    title="SmartLead AI Agent",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown("""
    # 🚀 SmartLead AI Agent
    ค้นหา Leads และลูกค้าเป้าหมายอัตโนมัติ
    """)

    with gr.Row():
        business = gr.Textbox(
            label="Business Type",
            placeholder="เช่น Restaurant, Dentist, Real Estate"
        )

    search_btn = gr.Button(
        "🔍 Search Leads",
        variant="primary"
    )

    result = gr.Textbox(
        label="Results",
        lines=10
    )

    search_btn.click(
        fn=search_business,
        inputs=business,
        outputs=result
    )

demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=True
)