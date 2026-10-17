import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Local GEO & AI Search Optimizer", version="1.0")

# Initialize OpenAI client (Render will pull OPENAI_API_KEY from environment variables)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

@app.get("/")
def read_root():
    return {"status": "online", "message": "Local GEO Automation Engine is running."}

@app.post("/api/audit-ai-visibility")
def audit_ai_visibility(data: AIAuditRequest):
    """
    Simulates an AI search engine query to check if a local business 
    is recommended by an LLM, returning a visibility score and gap analysis.
    """
    prompt = (
        f"Act as a local consumer search engine. A user asks: 'What are the top 3 best {data.industry} "
        f"businesses in {data.city}? Give me specific names.'\n\n"
        f"Analyze your response knowledge base for {data.city} {data.industry}. "
        f"Is '{data.business_name}' explicitly recommended? Answer in JSON format with keys: "
        f"'is_mentioned' (boolean), 'competitors_listed' (list of strings), and 'recommendation_summary' (string)."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return {
            "target_business": data.business_name,
            "location": f"{data.city}",
            "audit_result": eval(response.choices[0].message.content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-ai-schema")
def generate_ai_schema(data: SchemaRequest):
    """
    Generates advanced machine-readable JSON-LD Schema markup optimized 
    for AI crawlers and LLM retrieval systems to index local entities.
    """
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
        "instructions": "Paste this JSON-LD script inside the <head> tag of the business website so AI search browsers parse entity data seamlessly.",
        "json_ld": schema_markup
    }