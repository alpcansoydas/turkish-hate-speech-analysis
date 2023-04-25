# Turkish Hate Speech Analysis 

In this work, hate speech recognition system is implemented in Turkish language.

This model is a fine-tuned version of YSKartal/bert-base-turkish-cased-turkish_offensive_trained_model and dbmdz/bert-base-turkish-cased.

Used dataset is from https://huggingface.co/datasets/Toygar/turkish-offensive-language-detection
and the dataset consists of OFFENSIVE and NOT OFFENSIVE labeled data.

Evaluation results for the limited number of data:

<img width="416" alt="Screenshot 2023-04-25 at 13 47 01" src="https://user-images.githubusercontent.com/48163702/234254382-5769bd58-a3c1-4cce-a56b-7913c79726ca.png">

*Evaluation code is seperated because of memory limitations.

You can download the turkish_offensive_language.pt file to use the model from: https://drive.google.com/file/d/19uFTLRFKNVDw3wMCnUICbuQR-JW1iI_x/view?usp=share_link
