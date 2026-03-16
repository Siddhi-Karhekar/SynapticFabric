# vectordb/retrieve_context.py

from digital_twin.simulator import MACHINE_MEMORY


def get_machine_context():
    """
    Build context for chatbot using LIVE digital twin machines
    """

    context = ""

    for machine_id, state in MACHINE_MEMORY.items():

        temperature = 295 + state["vibration_index"] * 10

        context += f"""
Machine ID: {machine_id}

Temperature: {round(temperature,2)} °C
Tool Wear: {round(state['tool_wear']*100,1)} %
Vibration Index: {state['vibration_index']}
Anomaly Score: {state['anomaly_score']}

"""

    return context