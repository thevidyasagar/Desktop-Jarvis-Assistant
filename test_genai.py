from core.brain import client
with open("test_genai_out.txt", "w") as f:
    try:
        models = client.models.list()
        for m in models:
            f.write(m.name + "\n")
    except Exception as e:
        f.write("ERROR: " + str(e))
