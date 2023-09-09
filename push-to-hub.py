from datasets import load_dataset

dataset = load_dataset("imagefolder", data_dir="repo")
print(dataset["train"][0])
#dataset.push_to_hub(input("Enter which repo you'd like to push this to: "))
