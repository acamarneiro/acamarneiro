import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatchInput(BaseModel):
    team_a: str
    team_b: str
    events: list

@app.post("/api/ai/tagming-automatico")
async def processar_tagging_ia(data: MatchInput):
    try:
        eventos_str = "\n".join([
            f"Tempo: {e.get('time')}s | Time: {e.get('teamName')} | Atleta: {e.get('p1')} | Ação: {e.get('action')}"
            for e in data.events
        ])

        prompt = f\"\"\"
        Você é um analista tático sênior de Futsal. Com base nos eventos registrados da partida entre {data.team_a} e {data.team_b}, analise o desempenho, identifique padrões e sugira quais lances devem ser revisados no vídeo.

        Eventos atuais:
        {eventos_str}
        \"\"\"

        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
        )

        return {
            "status": "success",
            "analise_ia": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))