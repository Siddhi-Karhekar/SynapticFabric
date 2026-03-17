def analyze_root_cause(machine):

    causes = []

    temperature = machine.get("temperature", 0)
    vibration = machine.get("vibration_index", 0)
    tool_wear = machine.get("tool_wear", 0)
    torque = machine.get("torque", 0)

    # 🔥 REAL INDUSTRIAL FAILURE TYPES

    if temperature > 85:
        causes.append("Cooling system degradation (overheating risk)")

    if vibration > 0.7:
        causes.append("Bearing wear or spindle imbalance")

    if tool_wear > 0.8:
        causes.append("Cutting tool nearing failure → risk of poor surface finish")

    if torque > 60:
        causes.append("Mechanical overload → excessive cutting force")

    if not causes:
        causes.append("Machine operating within normal industrial parameters")

    return causes