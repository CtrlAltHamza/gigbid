import os
import sys

# Ensure root directory is in Python module search path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import gradio as gr
from apps.api.main import app as fastapi_app

# Define an interactive Gradio dashboard for reviewers on Hugging Face Spaces
with gr.Blocks(title="GigBid Multi-Agent Copilot API") as demo:
    gr.Markdown("""
    # 🤖 GigBid Multi-Agent Freelancer Copilot — API Service
    **AI-4016 Advanced Agentic AI (FAST-NUCES Islamabad)**
    
    This Hugging Face Space hosts the complete autonomous FastAPI backend for GigBid.
    The React 19 frontend is deployed on **Vercel** and communicates directly with these endpoints.
    """)

    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            ### 📡 Live API Endpoints:
            * 📖 **Interactive Swagger Docs**: [/docs](/docs)
            * 🟢 **Health Check**: [/api/health](/api/health)
            * 💼 **Ranked Marketplace Jobs**: [/api/jobs](/api/jobs)
            * 📊 **Telemetry & Analytics**: [/api/analytics](/api/analytics)
            * 🧠 **Learned Memory Rules**: [/api/settings/memory](/api/settings/memory)
            """)

    with gr.Accordion("🔍 Quick Endpoint Test (Fetch Top Jobs)", open=False):
        btn = gr.Button("Fetch Active Marketplace Jobs", variant="primary")
        json_output = gr.JSON()

        def fetch_top_jobs():
            from apps.api.routers.jobs import get_jobs
            return get_jobs(limit=3)

        btn.click(fn=fetch_top_jobs, outputs=json_output)

# Mount Gradio app into the FastAPI application
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
