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

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAINTENANCE_COOLDOWN = {}

def json_safe(data):
    return json.loads(json.dumps(data, default=str))


@app.websocket("/ws/machines")
async def machine_stream(ws: WebSocket):

    await ws.accept()

    print("WebSocket connected")

    try:

        while True:

            machines = run_digital_twin()

            # Maintenance cooldown protection
            for m in machines:

                mid = m["machine_id"]

                if mid in MAINTENANCE_COOLDOWN:

                    elapsed = time.time() - MAINTENANCE_COOLDOWN[mid]

                    if elapsed < 10:

                        MACHINE_MEMORY[mid]["tool_wear"] = 0.02
                        MACHINE_MEMORY[mid]["vibration_index"] = 0.25
                        MACHINE_MEMORY[mid]["anomaly_score"] = 0.01

                    else:
                        del MAINTENANCE_COOLDOWN[mid]

            analyzed = machine_analyzer.analyze_machines(machines)

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
        print("WebSocket closed:", e)


@app.post("/maintenance/{machine_id}")
def perform_maintenance(machine_id: str):

    if machine_id not in MACHINE_MEMORY:
        return {"error": "machine not found"}

    MACHINE_MEMORY[machine_id]["tool_wear"] = 0.01
    MACHINE_MEMORY[machine_id]["vibration_index"] = 0.15
    MACHINE_MEMORY[machine_id]["anomaly_score"] = 0.005

    MAINTENANCE_COOLDOWN[machine_id] = time.time()

    print(f"Maintenance executed on {machine_id}")

    return {
        "status": "maintenance completed",
        "machine": machine_id
    }