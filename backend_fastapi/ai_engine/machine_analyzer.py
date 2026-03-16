import random
from backend_fastapi.ai_engine.root_cause import analyze_root_cause


class MachineAnalyzer:

    def __init__(self):
        pass

    def analyze_machines(self, machines):

        analyzed = []

        for machine in machines:

            # =====================================
            # SENSOR VALUES
            # =====================================

            temperature = machine.get("temperature", 0)
            torque = machine.get("torque", 0)
            tool_wear = machine.get("tool_wear", 0)
            vibration = machine.get("vibration_index", 0)

            # =====================================
            # ANOMALY SCORE
            # =====================================

            anomaly_score = (
                ((temperature - 290) / 30) * 0.3 +
                tool_wear * 0.35 +
                vibration * 0.25 +
                (torque / 100) * 0.1
            )

            anomaly_score = max(0, min(anomaly_score, 1))
            anomaly_score = round(anomaly_score, 3)

            machine["anomaly_score"] = anomaly_score

            # =====================================
            # FAILURE PROBABILITY
            # =====================================

            failure_probability = round(
                anomaly_score * random.uniform(0.8, 1.1),
                3
            )

            failure_probability = min(failure_probability, 1)

            machine["failure_probability"] = failure_probability

            # Frontend expects this
            machine["prediction"] = failure_probability

            # =====================================
            # HEALTH STATUS
            # =====================================

            if anomaly_score < 0.45:
                health_status = "Healthy"

            elif anomaly_score < 0.75:
                health_status = "Warning"

            else:
                health_status = "Critical"

            machine["health_status"] = health_status

            # =====================================
            # ALERTS
            # =====================================

            alerts = []

            if temperature > 305:
                alerts.append({
                    "level": "warning",
                    "message": "High temperature detected"
                })

            if vibration > 0.8:
                alerts.append({
                    "level": "warning",
                    "message": "High vibration levels"
                })

            if tool_wear > 0.8:
                alerts.append({
                    "level": "critical",
                    "message": "Tool wear extremely high"
                })

            if anomaly_score > 0.65:
                alerts.append({
                    "level": "critical",
                    "message": "Machine health critical"
                })

            machine["alerts"] = alerts

            # =====================================
            # AI EXPLANATION
            # =====================================

            machine["ai_explanation"] = (
                f"Machine health classified as {health_status}. "
                f"Anomaly score {anomaly_score} with failure probability "
                f"{failure_probability}."
            )

            # =====================================
            # ROOT CAUSE ANALYSIS
            # =====================================

            machine["root_cause"] = analyze_root_cause(machine)

            analyzed.append(machine)

        return analyzed


machine_analyzer = MachineAnalyzer()