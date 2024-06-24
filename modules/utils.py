import random
import pandas as pd
import logging
import autogen

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('app_debug.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))

logger.addHandler(file_handler)

def generate_survey_data(num_bots, male_percentage, income_range, interests_list):
    try:
        data = [{'gender': 'male' if random.random() < male_percentage / 100 else 'female',
                 'income': random.randint(income_range[0], income_range[1]) * 1000,
                 'interests': random.sample(interests_list, k=min(len(interests_list), 3))}
                for _ in range(num_bots)]
        logger.info(f"Generated survey data: {data[:5]}...")  # Log a sample of generated data
        return data
    except Exception as e:
        logger.error(f"Error generating survey data: {str(e)}")
        raise

def simulate_demand(feature, tagline, price, num_bots, male_percentage, income_range, interests_list, progress, total_combinations, current_index):
    try:
        logger.info(f"Starting simulation for feature: {feature}, tagline: {tagline}, price: {price}")
        bot_data = generate_survey_data(num_bots, male_percentage, income_range, interests_list)
        demand_score = sum(random.randint(60, 90) for _ in bot_data) / len(bot_data)
        response_data = {
            "Feature": feature,
            "Tagline": tagline,
            "Price": float(price),
            "Demand Score": demand_score
        }
        autogen.runtime_logging.start(logger_type="file", config={"filename": "demand_simulation.log"})
        autogen.runtime_logging.log_event(name="demand_simulation", event=response_data, source="demand_meter")
        autogen.runtime_logging.stop()
        progress.progress((current_index + 1) / total_combinations)
        logger.info(f"Simulation successful for feature: {feature}, tagline: {tagline}, price: {price}")
        return response_data
    except Exception as e:
        error_data = {"Feature": feature, "Tagline": tagline, "Price": price, "Error": str(e)}
        autogen.runtime_logging.start(logger_type="file", config={"filename": "demand_simulation_errors.log"})
        autogen.runtime_logging.log_event(name="demand_simulation_error", event=error_data, source="demand_meter")
        autogen.runtime_logging.stop()
        logger.error(f"Error in simulate_demand for feature: {feature}, tagline: {tagline}, price: {price} - {str(e)}")
        return None

def process_simulation(combinations, num_bots, male_percentage, income_range, interests_list, progress):
    results = []
    total_combinations = len(combinations)
    for current_index, (feature, tagline, price) in enumerate(combinations):
        result = simulate_demand(feature, tagline, price, num_bots, male_percentage, income_range, interests_list, progress, total_combinations, current_index)
        if result:
            results.append(result)
        progress.progress((current_index + 1) / total_combinations)
    if not results:
        autogen.runtime_logging.start(logger_type="file", config={"filename": "process_simulation_errors.log"})
        autogen.runtime_logging.log_event(name="process_simulation_error", event={"Error": "No valid results returned"}, source="demand_meter")
        autogen.runtime_logging.stop()
        logger.warning("No valid results returned in process_simulation.")
    return pd.DataFrame(results)

def update_progress(progress, value):
    blocks = int(value / 5)
    blocks_html = "".join(["<div class='progress-block'></div>" for _ in range(blocks)])
    progress.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width:{value}%;">
                <div class="progress-blocks">{blocks_html}</div>
            </div>
        </div>
        <div class="progress-text">{value}%</div>
    """, unsafe_allow_html=True)

def generate_insights(assistant, user_proxy, df_dict):
    insights_prompt = f"Analyze the demand scores for the following combinations and provide insights:\n{df_dict}"
    user_proxy.initiate_chat(assistant, message=insights_prompt)
    return assistant.last_message()["content"]

def log_feedback(product_name, feedback):
    feedback_data = {"Product Name": product_name, "Feedback": feedback}
    autogen.runtime_logging.start(logger_type="file", config={"filename": "user_feedback.log"})
    autogen.runtime_logging.log_event(name="user_feedback", event=feedback_data, source="demand_meter")
    autogen.runtime_logging.stop()

def log_error(section, error_message):
    error_data = {"Section": section, "Error": error_message}
    autogen.runtime_logging.start(logger_type="file", config={"filename": "app_errors.log"})
    autogen.runtime_logging.log_event(name="app_error", event=error_data, source="omnivia_survey_platform")
    autogen.runtime_logging.stop()
    logger.error(f"Error in {section}: {error_message}")
