import json

confessions_file = open("confessions.json", "r")
confessions_content = confessions_file.read()
confessions = json.loads(confessions_content)

fine_tune_file = []

confessions_file = open("fine-tune.jsonl", "a")
for confession in confessions:
    confessions_file.write(
        json.dumps({"prompt": "", "completion": " " + confession + " END"})
    )
    confessions_file.write("\n")

confessions_file.close()
