# util.py

import pandas as pd
from vyzeai.models.openai import ChatOpenAI

def generate_synthetic_data(api_key, file_path, num_rows=10, chunk_size=50):
    """Generate synthetic data."""
    
    llm = ChatOpenAI(api_key)
    
    data = pd.read_excel(file_path).tail(30)
    sample_str = data.to_csv(index=False, header=False)
    
    sysp = "You are a synthetic data generator. Your output should only be CSV format without any additional text and code fences."
    
    generated_rows = []
    rows_generated = 0

    while rows_generated < num_rows:

        if generated_rows:
            current_sample_str = "\n".join([",".join(row) for row in generated_rows[-10:]])
        else:
            current_sample_str = sample_str

        rows_to_generate = min(chunk_size, num_rows - rows_generated)
        
        prompt = (f"Generate {rows_to_generate} more rows of synthetic data following this pattern:\n\n{current_sample_str}\n"
                  "\nEnsure the synthetic data does not contain column names or old data. "
                  "\nExpected Output: synthetic data as comma-separated values (',').")
        #                  "\nFor dates and time, maintain sequence. "

        generated_data = llm.run(prompt, system_message=sysp)
        
        rows = [row.split(",") for row in generated_data.strip().split("\n") if row]
        
        rows_needed = num_rows - rows_generated
        generated_rows.extend(rows[:rows_needed])
        
        rows_generated += len(rows[:rows_needed])
    
    generated_df = pd.DataFrame(generated_rows, columns=data.columns)
    
    return generated_df
