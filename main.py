import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Local GEO & AI Search Optimizer", version="1.0")

# Initialize Groq client (100% compatible with OpenAI SDK & has a generous free tier)
# Get your free key at: https://console.groq.com
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

class AIAuditRequest(BaseModel):
    business_name: str
    industry: str
    city: str

class SchemaRequest(BaseModel):
    business_name: str
    industry: str
    address: str
    phone: str
    website: str
    city: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Local GEO & AI Search Optimizer</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased">
        <div class="max-w-4xl mx-auto px-4 py-12">
            <!-- Header -->
            <div class="text-center mb-10">
                <span class="px-3 py-1 text-xs font-semibold bg-emerald-500/10 text-emerald-400 rounded-full border border-emerald-500/20">Developed by Srinjoy Chatterjee</span>
                <h1 class="text-4xl font-extrabold tracking-tight mt-3 text-white">Local GEO & AI Search Optimizer</h1>
                <p class="text-slate-400 mt-2">Audit your business visibility in AI search engines and generate optimized local Schema markup.</p>
            </div>

            <!-- Tabs / Cards Grid -->
            <div class="grid md:grid-cols-2 gap-8">
                <!-- AI Audit Card -->
                <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
                    <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        <span>🔍</span> AI Visibility Audit
                    </h2>
                    <form id="auditForm" class="space-y-4">
                        <div>
                            <label class="block text-xs font-medium text-slate-400 mb-1">Business Name</label>
                            <input type="text" id="audit_business" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-500 text-white" placeholder="e.g. Apex Plumbing">
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-slate-400 mb-1">Industry</label>
                            <input type="text" id="audit_industry" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-500 text-white" placeholder="e.g. Plumber">
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-slate-400 mb-1">City</label>
                            <input type="text" id="audit_city" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-500 text-white" placeholder="e.g. Austin, TX">
                        </div>
                        <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2.5 rounded-lg transition text-sm">Run AI Audit</button>
                    </form>
                    <div id="auditResult" class="mt-4 hidden p-4 bg-slate-950 rounded-xl border border-slate-800 text-xs font-mono overflow-x-auto text-emerald-300"></div>
                </div>

                <!-- Schema Generator Card -->
                <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
                    <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        <span>⚡</span> Schema Markup Generator
                    </h2>
                    <form id="schemaForm" class="space-y-3">
                        <div>
                            <label class="block text-xs font-medium text-slate-400 mb-1">Business Name</label>
                            <input type="text" id="schema_business" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-white">
                        </div>
                        <div class="grid grid-cols-2 gap-2">
                            <div>
                                <label class="block text-xs font-medium text-slate-400 mb-1">Industry</label>
                                <input type="text" id="schema_industry" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-white">
                            </div>
                            <div>
                                <label class="block text-xs font-medium text-slate-400 mb-1">City</label>
                                <input type="text" id="schema_city" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-white">
                            </div>
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-slate-400 mb-1">Street Address</label>
                            <input type="text" id="schema_address" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-white">
                        </div>
                        <div class="grid grid-cols-2 gap-2">
                            <div>
                                <label class="block text-xs font-medium text-slate-400 mb-1">Phone</label>
                                <input type="text" id="schema_phone" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-white">
                            </div>
                            <div>
                                <label class="block text-xs font-medium text-slate-400 mb-1">Website URL</label>
                                <input type="text" id="schema_website" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-white">
                            </div>
                        </div>
                        <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2.5 rounded-lg transition text-sm">Generate Schema</button>
                    </form>
                    <div id="schemaResult" class="mt-4 hidden p-4 bg-slate-950 rounded-xl border border-slate-800 text-xs font-mono overflow-x-auto text-emerald-300 max-h-40"></div>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('auditForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const btn = e.target.querySelector('button');
                btn.innerText = "Analyzing...";
                const payload = {
                    business_name: document.getElementById('audit_business').value,
                    industry: document.getElementById('audit_industry').value,
                    city: document.getElementById('audit_city').value
                };
                try {
                    const res = await fetch('/api/audit-ai-visibility', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(payload)
                    });
                    const data = await res.json();
                    const resultDiv = document.getElementById('auditResult');
                    resultDiv.classList.remove('hidden');
                    resultDiv.innerText = JSON.stringify(data, null, 2);
                } catch(err) {
                    alert('Error running audit');
                } finally {
                    btn.innerText = "Run AI Audit";
                }
            });

            document.getElementById('schemaForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const btn = e.target.querySelector('button');
                btn.innerText = "Generating...";
                const payload = {
                    business_name: document.getElementById('schema_business').value,
                    industry: document.getElementById('schema_industry').value,
                    city: document.getElementById('schema_city').value,
                    address: document.getElementById('schema_address').value,
                    phone: document.getElementById('schema_phone').value,
                    website: document.getElementById('schema_website').value
                };
                try {
                    const res = await fetch('/api/generate-ai-schema', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(payload)
                    });
                    const data = await res.json();
                    const resultDiv = document.getElementById('schemaResult');
                    resultDiv.classList.remove('hidden');
                    resultDiv.innerText = JSON.stringify(data, null, 2);
                } catch(err) {
                    alert('Error generating schema');
                } finally {
                    btn.innerText = "Generate Schema";
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/api/audit-ai-visibility")
def audit_ai_visibility(data: AIAuditRequest):
    prompt = (
        f"Act as a local consumer search engine. A user asks: 'What are the top 3 best {data.industry} "
        f"businesses in {data.city}? Give me specific names.'\n\n"
        f"Analyze your response knowledge base for {data.city} {data.industry}. "
        f"Is '{data.business_name}' explicitly recommended? Answer strictly in JSON format with keys: "
        f"'is_mentioned' (boolean), 'competitors_listed' (list of strings), and 'recommendation_summary' (string)."
    )
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # Active Groq model endpoint
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
            temperature=0.0
        )
        return {
            "target_business": data.business_name,
            "location": f"{data.city}",
            "audit_result": json.loads(response.choices[0].message.content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-ai-schema")
def generate_ai_schema(data: SchemaRequest):
    schema_markup = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": data.business_name,
        "description": f"Top-rated {data.industry} serving {data.address}.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": data.address,
            "addressLocality": data.city,
            "addressCountry": "US"
        },
        "telephone": data.phone,
        "url": data.website,
        "priceRange": "$$"
    }
    return {
        "instructions": "Paste this JSON-LD script inside the <head> tag of the business website.",
        "json_ld": schema_markup
    }
