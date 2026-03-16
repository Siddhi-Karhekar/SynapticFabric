import random

# ==========================================
# MACHINE MEMORY
# ==========================================

MACHINE_MEMORY = {
    "M_1": {"tool_wear": 0.2, "vibration_index": 0.4, "anomaly_score": 0.05},
    "M_2": {"tool_wear": 0.2, "vibration_index": 0.4, "anomaly_score": 0.05},
    "M_3": {"tool_wear": 0.2, "vibration_index": 0.4, "anomaly_score": 0.05},
}


# ==========================================
# DIGITAL TWIN SIMULATOR
# ==========================================

def run_digital_twin():

    machines = []

    for machine_id in MACHINE_MEMORY:

        state = MACHINE_MEMORY[machine_id]

        # -------------------------------
        # GRADUAL DEGRADATION
        # -------------------------------

        state["tool_wear"] += random.uniform(0.001, 0.003)
        state["vibration_index"] += random.uniform(0.001, 0.003)
        state["anomaly_score"] += random.uniform(0.001, 0.003)

        # -------------------------------
        # CLAMP VALUES
        # -------------------------------

        state["tool_wear"] = max(0, min(state["tool_wear"], 1))
        state["vibration_index"] = max(0, min(state["vibration_index"], 1.5))
        state["anomaly_score"] = max(0, min(state["anomaly_score"], 1))

        # -------------------------------
        # SENSOR SIMULATION
        # -------------------------------

        temperature = 295 + state["vibration_index"] * 10 + random.uniform(-1, 1)

        torque = random.uniform(38, 48)

        # -------------------------------
        # MACHINE OUTPUT
        # -------------------------------

        machines.append({
            "machine_id": machine_id,
            "temperature": round(temperature, 2),
            "torque": round(torque, 2),
            "tool_wear": round(state["tool_wear"], 3),
            "vibration_index": round(state["vibration_index"], 3),
            "anomaly_score": round(state["anomaly_score"], 3),
        })

    return machines