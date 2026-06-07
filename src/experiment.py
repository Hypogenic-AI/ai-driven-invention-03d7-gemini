import pandas as pd
import numpy as np
import ast
import random
import json
import os
import time
from datetime import datetime
from openai import OpenAI

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)

set_seed(42)

# Load API Key
api_key = os.getenv("OPENROUTER_KEY")
if not api_key:
    # fallback to openai if openrouter not set
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    MODEL = "gpt-4o"
else:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    MODEL = "openai/gpt-4o"

print(f"Using Model: {MODEL}")

print("Loading GNoME dataset...")
df = pd.read_csv('../datasets/gnome/stable_materials_summary.csv')

# Parse the Elements column safely
def parse_elements(x):
    try:
        # It's stored as a string representation of a list: "['S', 'Zr', 'Cs']"
        elems = ast.literal_eval(x)
        return frozenset(elems)
    except:
        return frozenset()

print("Parsing elements...")
df['Elements_Set'] = df['Elements'].apply(parse_elements)

# Filter for ternary and quaternary systems to limit scope to interesting materials
df['Num_Elements'] = df['Elements_Set'].apply(len)
df_ternary = df[df['Num_Elements'] == 3]

print(f"Total ternary materials in dataset: {len(df_ternary)}")

# Get all unique elements present in the ternary dataset
all_elements = set()
for elems in df_ternary['Elements_Set']:
    all_elements.update(elems)
all_elements = list(all_elements)

print(f"Total unique elements: {len(all_elements)}")

def evaluate_system(elements_list):
    """
    Given a list of elements like ['Li', 'O', 'Fe'],
    find the lowest Formation Energy Per Atom for materials with exactly these elements.
    Returns: min_formation_energy (float) or None if not found.
    """
    query_set = frozenset(elements_list)
    matches = df_ternary[df_ternary['Elements_Set'] == query_set]
    if len(matches) > 0:
        # Lower formation energy is more stable
        return matches['Formation Energy Per Atom'].min()
    return None

def random_search(n=30):
    print(f"\n--- Running Random Search (n={n}) ---")
    results = []
    attempts = 0
    # ensure we get n unique proposals
    proposed = set()
    
    while len(results) < n and attempts < n * 10:
        attempts += 1
        elems = frozenset(random.sample(all_elements, 3))
        if elems in proposed:
            continue
        proposed.add(elems)
        
        energy = evaluate_system(list(elems))
        results.append({
            'elements': list(elems),
            'formation_energy': energy,
            'found': energy is not None
        })
    
    hits = [r for r in results if r['found']]
    hit_rate = len(hits) / n
    avg_energy = np.mean([r['formation_energy'] for r in hits]) if hits else 0
    
    print(f"Random Search Hit Rate: {hit_rate:.2f}")
    print(f"Random Search Avg Energy: {avg_energy:.4f}")
    
    return results, hit_rate, avg_energy

def llm_zero_shot_search(n=30):
    print(f"\n--- Running LLM Zero-Shot Search (n={n}) ---")
    
    prompt = f"""
    You are an expert materials scientist and AI inventor.
    Your task is to propose {n} novel, highly stable ternary chemical systems (combinations of exactly 3 distinct elements).
    You should aim for combinations that have very low (negative) formation energies.
    
    Choose elements from the periodic table that are known to form stable crystals together (e.g., combining alkali metals, transition metals, and chalcogens/halogens).
    
    Provide your output ONLY as a JSON list of lists of strings, like this:
    [["Li", "Fe", "O"], ["Na", "Co", "P"], ...]
    
    Ensure there are exactly {n} combinations, each with exactly 3 elements.
    Do not output any other text, just the JSON array.
    """
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    content = response.choices[0].message.content.strip()
    # Strip markdown if present
    if content.startswith("```json"):
        content = content[7:-3]
    elif content.startswith("```"):
        content = content[3:-3]
        
    try:
        proposals = json.loads(content)
    except json.JSONDecodeError:
        print("Failed to parse JSON from LLM.")
        print(content)
        return [], 0, 0

    results = []
    for p in proposals[:n]:
        if len(p) != 3:
            continue
        energy = evaluate_system(p)
        results.append({
            'elements': p,
            'formation_energy': energy,
            'found': energy is not None
        })
        
    hits = [r for r in results if r['found']]
    hit_rate = len(hits) / len(proposals) if proposals else 0
    avg_energy = np.mean([r['formation_energy'] for r in hits]) if hits else 0
    
    print(f"LLM Zero-Shot Hit Rate: {hit_rate:.2f}")
    print(f"LLM Zero-Shot Avg Energy: {avg_energy:.4f}")
    
    return results, hit_rate, avg_energy

def llm_active_learning_search(steps=15):
    print(f"\n--- Running LLM Active Learning Search (steps={steps}) ---")
    
    system_prompt = """
    You are an expert materials scientist participating in an active learning loop to discover highly stable ternary materials.
    Your goal is to propose combinations of 3 elements that form highly stable crystals (having the most negative formation energy possible).
    """
    
    history = []
    results = []
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Propose a ternary elemental system (3 elements). Output ONLY JSON: [\"El1\", \"El2\", \"El3\"]."}
    ]
    
    for i in range(steps):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.5
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        try:
            p = json.loads(content)
            if not isinstance(p, list) or len(p) != 3:
                raise ValueError("Invalid format")
        except:
            print(f"Step {i}: LLM output invalid format: {content}")
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": "Invalid format. Output ONLY JSON: [\"El1\", \"El2\", \"El3\"]."})
            continue
            
        energy = evaluate_system(p)
        found = energy is not None
        
        results.append({
            'step': i,
            'elements': p,
            'formation_energy': energy,
            'found': found
        })
        
        if found:
            feedback = f"You proposed {p}. It is STABLE. Formation energy: {energy:.4f} eV/atom (lower is better). Propose another ternary system that might have an even lower formation energy. Output ONLY JSON."
        else:
            feedback = f"You proposed {p}. It was NOT FOUND in the stable materials database. Propose a different ternary system. Output ONLY JSON."
            
        print(f"Step {i}: Proposed {p} -> Found: {found}, Energy: {energy}")
        
        messages.append({"role": "assistant", "content": content})
        messages.append({"role": "user", "content": feedback})
        
    hits = [r for r in results if r['found']]
    hit_rate = len(hits) / len(results) if results else 0
    avg_energy = np.mean([r['formation_energy'] for r in hits]) if hits else 0
    
    print(f"Active Learning Hit Rate: {hit_rate:.2f}")
    print(f"Active Learning Avg Energy: {avg_energy:.4f}")
    
    return results, hit_rate, avg_energy

if __name__ == "__main__":
    os.makedirs("../results", exist_ok=True)
    
    # Run Experiments
    rand_res, rand_hr, rand_avg = random_search(n=30)
    zero_res, zero_hr, zero_avg = llm_zero_shot_search(n=30)
    al_res, al_hr, al_avg = llm_active_learning_search(steps=15)
    
    # Save Results
    summary = {
        'Random': {'Hit_Rate': rand_hr, 'Avg_Energy': rand_avg},
        'Zero_Shot': {'Hit_Rate': zero_hr, 'Avg_Energy': zero_avg},
        'Active_Learning': {'Hit_Rate': al_hr, 'Avg_Energy': al_avg}
    }
    
    with open("../results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
        
    with open("../results/all_experiments.json", "w") as f:
        json.dump({
            'random': rand_res,
            'zero_shot': zero_res,
            'active_learning': al_res
        }, f, indent=2)
        
    print("\nExperiments complete. Results saved to ../results/")
