from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the trained model and tokenizer
model_path = "t5_summary_model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

def summarize_text(text, max_input_length=512):
    """
    Summarize the given text using the trained T5 model.
    If the text is too long, split it into smaller chunks.
    """
    input_chunks = []
    # Split text into chunks of max_input_length tokens
    while len(text) > max_input_length:
        # Find the last space within max_input_length
        split_index = text[:max_input_length].rfind(' ')
        input_chunks.append(text[:split_index])
        text = text[split_index:].strip()
    input_chunks.append(text)

    # Generate summaries for each chunk
    summaries = []
    for chunk in input_chunks:
        input_ids = tokenizer("summarize: " + chunk, return_tensors="pt").input_ids
        summary_ids = model.generate(input_ids, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summaries.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))

    # Combine all summaries
    return " ".join(summaries)
