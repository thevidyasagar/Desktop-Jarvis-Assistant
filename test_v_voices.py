import asyncio
import edge_tts

async def amain():
    try:
        voices = await edge_tts.VoicesManager.create()
        with open("voices_list.txt", "w", encoding="utf-8") as f:
            for v in voices.voices:
                f.write(f"{v['ShortName']} | {v['Locale']} | {v['Gender']}\n")
        print("Done writing voices_list.txt")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(amain())
