from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the models and tokenizers
original_model_name = "gpt2"
original_tokenizer = GPT2Tokenizer.from_pretrained(original_model_name)
original_model = GPT2LMHeadModel.from_pretrained(original_model_name)
original_tokenizer.pad_token = original_tokenizer.eos_token

fine_tuned_dir = "./gpt2-fine-tuned"
fine_tuned_tokenizer = GPT2Tokenizer.from_pretrained(fine_tuned_dir)
fine_tuned_model = GPT2LMHeadModel.from_pretrained(fine_tuned_dir)
fine_tuned_tokenizer.pad_token = fine_tuned_tokenizer.eos_token

fine_tuned_dir_no_hvac = "./gpt2-fine-tuned-no-hvac"
fine_tuned_tokenizer_no_hvac = GPT2Tokenizer.from_pretrained(fine_tuned_dir_no_hvac)
fine_tuned_model_no_hvac = GPT2LMHeadModel.from_pretrained(fine_tuned_dir_no_hvac)
fine_tuned_tokenizer_no_hvac.pad_token = fine_tuned_tokenizer_no_hvac.eos_token

# Set models to evaluation mode
original_model.eval()
fine_tuned_model.eval()
fine_tuned_model_no_hvac.eval()

# Function to generate response from a model
def generate_response(
    model, tokenizer, prompt, max_length=50, temperature=0.7, top_k=50, top_p=0.9, repetition_penalty=1.2
):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            do_sample=True  # Enable sampling for diverse outputs
        )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return clean_repeated_phrases(response)

def clean_repeated_phrases(response):
    """Remove long repeated phrases from the generated response."""
    words = response.split()
    cleaned_response = []
    seen_phrases = set()

    # Use sliding window to detect repeated phrases
    for i in range(len(words)):
        for j in range(1, 4):  # Check for repeated phrases of 1-3 words
            phrase = " ".join(words[i:i+j])
            if phrase in seen_phrases:
                continue
            seen_phrases.add(phrase)
            cleaned_response.extend(words[i:i+j])
            break

    return " ".join(cleaned_response)

# Scoring function using cosine similarity
def compute_similarity_score(expected, actual):
    vectorizer = TfidfVectorizer().fit([expected, actual])
    vectors = vectorizer.transform([expected, actual])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0, 0]
    return round(similarity * 100, 2)  # Return as percentage

# HVAC prompts and expected responses
hvac_prompts = [
    "What is the function of a VAV box in an HVAC system?",
    "Explain how economizers are used for free cooling.",
    "Describe the difference between a chiller and a cooling tower.",
    "What is the purpose of a supply air temperature setpoint?",
    "How does an AHU handle mixed air temperature control?",
    "What is a BRICK model?",
    "What is a BRICK feeds relationship in a data model?",
    "The building is occupied and the air handling unit is off but it should be on, should we inform the humans?!",
    "There are worms coming out of the cooling coil, what do we do!?",
    "Its a very warm day outside and the air handling unit is discharing 100°F air, what do we do?!",
]

expected_responses = [
    "A VAV box delivers temperature and ventilation requirements in a VAV AHU system.",
    "Economizers in an AHU system allow for free cooling by opening up outside air dampers to allow for free cooling from outdoor air when outside air conditions are ideal for cooling.",
    "A chiller has mechanical cooling components for a condenser and evaporator, whereas the cooling tower dumps heat on the condenser side of the chiller in a water-cooled system.",
    "A supply air temperature setpoint delivers conditioned air to HVAC zones, which can be dehumidified or heated depending on the conditions or loads on the building.",
    "An air handling unit controls to a mixed air temperature by regulating the outside air temperatures while mixing the outdoor and return air temperatures.",
    "A BRICK model is a data model used to describe the data of a building and relationships between naming conventions of points to components.",
    "A BRICK feeds relationship describes what components in a mechanical system are upstream or downstream in a mechanical system.",
    "Yes inform the humans that the air handling unit should be running if the building is occupied.",
    "Worms cannot be inside of a mechanical system that is impossible.",
    "Inform the humans of mechanical issues. Check the chiller and boiler systems and valve operation on the air handling unit."
]

# Compare model performances
results = []
for prompt, expected in zip(hvac_prompts, expected_responses):
    result = {"Prompt": prompt, "Expected Response": expected}

    # Original GPT-2 response
    try:
        original_response = generate_response(original_model, original_tokenizer, prompt)
        original_score = compute_similarity_score(expected, original_response)
        result["Original Response"] = original_response
        result["Original Score"] = original_score
    except Exception as e:
        result["Original Response"] = f"Error: {e}"
        result["Original Score"] = 0.0

    # Fine-tuned GPT-2 response
    try:
        fine_tuned_response = generate_response(fine_tuned_model, fine_tuned_tokenizer, prompt)
        fine_tuned_score = compute_similarity_score(expected, fine_tuned_response)
        result["Fine-Tuned Response"] = fine_tuned_response
        result["Fine-Tuned Score"] = fine_tuned_score
    except Exception as e:
        result["Fine-Tuned Response"] = f"Error: {e}"
        result["Fine-Tuned Score"] = 0.0

    # Fine-tuned GPT-2 No HVAC response
    try:
        fine_tuned_no_hvac_response = generate_response(fine_tuned_model_no_hvac, fine_tuned_tokenizer_no_hvac, prompt)
        fine_tuned_no_hvac_score = compute_similarity_score(expected, fine_tuned_no_hvac_response)
        result["Fine-Tuned No HVAC Response"] = fine_tuned_no_hvac_response
        result["Fine-Tuned No HVAC Score"] = fine_tuned_no_hvac_score
    except Exception as e:
        result["Fine-Tuned No HVAC Response"] = f"Error: {e}"
        result["Fine-Tuned No HVAC Score"] = 0.0

    results.append(result)

# Print results
for result in results:
    print(f"Prompt: {result['Prompt']}")
    print(f"Expected Response: {result['Expected Response']}")
    print(f"\n --- Original Response: {result['Original Response']} (Score: {result['Original Score']}%)")
    print(f"\n --- Fine-Tuned Response: {result['Fine-Tuned Response']} (Score: {result['Fine-Tuned Score']}%)")
    print(f"\n --- Fine-Tuned No HVAC Response: {result['Fine-Tuned No HVAC Response']} (Score: {result['Fine-Tuned No HVAC Score']}%)")
    print("="*80)
