from transformers import T5Tokenizer, T5ForConditionalGeneration

def test_model(input_text, model_path="t5_summary_model"):
    # Load the trained model and tokenizer
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)

    # Prepare input
    input_ids = tokenizer("summarize: " + input_text, return_tensors="pt").input_ids

    # Generate summary
    summary_ids = model.generate(input_ids, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

if __name__ == "__main__":
    input_text = "Deep learning models like T5 and BERT are effective for text summarization. They condense long content into concise summaries."
    print("Input Text:", input_text)
    print("Generated Summary:", test_model(input_text))
