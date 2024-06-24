import os
import random
from langchain_community.llms import OpenAI

# --- OpenAI API ---
llm = OpenAI(temperature=0.7)

def generate_persona(income_range, interests):
    """Generates a persona based on income and a list of interests."""
    prompt = f"""Create a persona with the following elements:
    1. Identity: Name, occupation, background
    2. Characteristics: Personality traits, communication style, beliefs, values
    3. Knowledge and expertise: Specific areas of knowledge or expertise
    4. Experiences: Relevant past experiences, achievements, or challenges
    5. Motivations: Goals, desires, or driving forces
    6. Emotional and relational aspects: Emotional state, level of empathy, approach to relationships
    7. Context: Specific setting or situation

    The persona should have an income between ${income_range[0]}k and ${income_range[1]}k. 

    {random.choice(['They like ', 'They might like ', 'They dont really care for '])} {random.sample(interests, random.randint(0, len(interests)))}

    Provide the information in a structured format.
    """

    response = llm(prompt)
    return response.strip()