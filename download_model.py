from huggingface_hub import hf_hub_download

import os



print("--- DOWNLOADING MODEL: Magnum-v4-12b (Q6_K) ---")

print("This process may take a while depending on your internet speed...")



try:

    hf_hub_download(

        repo_id="mradermacher/Magnum-v4-12b-GGUF",

        filename="magnum-v4-12b.Q6_K.gguf", 

        local_dir=".",

        local_dir_use_symlinks=False

    )

    print("--- DOWNLOAD COMPLETE ---")

except Exception as e:

    print(f"ERROR: {e}")

    print("Trying alternative model: Q8_0 (Highest Quality)")

    try:

        hf_hub_download(

            repo_id="mradermacher/Magnum-v4-12b-GGUF",

            filename="magnum-v4-12b.Q8_0.gguf",

            local_dir=".",

            local_dir_use_symlinks=False

        )

        print("--- DOWNLOAD COMPLETE (Q8_0) ---")

    except Exception as e2:

        print(f"SECOND ERROR: {e2}")

