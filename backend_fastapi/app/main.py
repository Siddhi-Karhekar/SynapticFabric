# ==========================================
# SYNAPTICFABRIC — FASTAPI BACKEND
# ==========================================

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import time

from digital_twin.simulator import run_digital_twin, MACHINE_MEMORY
from backend_fastapi.ai_engine.machine_analyzer import machine_analyzer
from backend_fastapi.database.database import engine
from backend_fastapi.database.models import Base
from backend_fastapi.database.logger import log_machine_state
from backend_fastapi.analytics.realtime_analytics import compute_realtime_analytics

# IMPORT CHATBOT ROUTER
from backend_fastapi.app.chatbot_api import router as chatbot_router


# ==========================================
# APP INIT
# ==========================================

app = FastAPI(title="SynapticFabric API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTER CHATBOT ROUTER
app.include_router(chatbot_router)


# ==========================================
# HELPERS
# ==========================================

MAINTENANCE_COOLDOWN = {}

def json_safe(data):
    return json.loads(json.dumps(data, default=str))


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():
    return {"status": "SynapticFabric backend running"}


# ==========================================
# WEBSOCKET MACHINE STREAM
# ==========================================

@app.websocket("/ws/machines")
async def machine_stream(ws: WebSocket):

    await ws.accept()
    print("✅ WebSocket connected")

    try:

        while True:

            machines = run_digital_twin()

            # Prevent degradation immediately after maintenance
            for m in machines:

                mid = m["machine_id"]

                if mid in MAINTENANCE_COOLDOWN:

                    if time.time() - MAINTENANCE_COOLDOWN[mid] < 10:

                        m["tool_wear"] = 0.05
                        m["vibration_index"] = 0.30
                        m["anomaly_score"] = 0.02

            analyzed = machine_analyzer.analyze_machines(machines)

            # Store logs
            for machine in analyzed:
                log_machine_state(machine)

            analytics = compute_realtime_analytics(analyzed)

            payload = {
                "machines": analyzed,
                "factory_analytics": analytics
            }

            await ws.send_json(json_safe(payload))

            await asyncio.sleep(1)

    except Exception as e:
        print("⚠ WebSocket disconnected:", e)


# ==========================================
# PERFORM MAINTENANCE
# ==========================================

@app.post("/maintenance/{machine_id}")
def perform_maintenance(machine_id: str):

    if machine_id not in MACHINE_MEMORY:
        return {"error": "machine not found"}

    # Reset machine state
    MACHINE_MEMORY[machine_id]["tool_wear"] = 0.05
    MACHINE_MEMORY[machine_id]["vibration_index"] = 0.35
    MACHINE_MEMORY[machine_id]["anomaly_score"] = 0.02

    # Cooldown so degradation doesn't happen instantly
    MAINTENANCE_COOLDOWN[machine_id] = time.time()

    return {
        "status": "maintenance completed",
        "machine": machine_id
    }