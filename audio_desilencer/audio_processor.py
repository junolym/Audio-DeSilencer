import os
import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence

class AudioProcessor:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path

    def save_audio(self, audio, output_path):
        audio.export(output_path, format="mp3")
        print(f"Saved audio to {output_path}")

    def process_audio(self, min_silence_len=100, threshold=-30, keep_silence=0, output_folder='output'):
        try:
            print("Reading audio:", self.input_file_path)
            audio = AudioSegment.from_file(self.input_file_path, format="mp3")

            print("Processing audio...")
            audio_chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=threshold, keep_silence=keep_silence)
            audio_non_silent = AudioSegment.empty()
            for chunk in audio_chunks:
                audio_non_silent += chunk
            
            # Create the output folder if it doesn't exist
            os.makedirs(output_folder, exist_ok=True)
            input_file_name = self.input_file_path.split('/')[-1]
            output_file_name = 'trim_' + input_file_name
            output_non_silent_path = os.path.join(output_folder, output_file_name)
            self.save_audio(audio_non_silent, output_non_silent_path)

            print("Audio processing completed.")
            print("Audio with non-silent parts saved to:", output_non_silent_path)

        except Exception as e:
            print("An error occurred:", str(e))

def main():
    parser = argparse.ArgumentParser(description="Audio processing script")
    parser.add_argument("input_file", help="Input audio file path")
    parser.add_argument("--output_folder", default=".", help="Output folder path")
    parser.add_argument("--min_silence_len", type=int, default=3000, help="Minimum silence length (in milliseconds)")
    parser.add_argument("--threshold", type=int, default=-30, help="Silence threshold in dBFS")
    parser.add_argument("--keep_silence", type=int, default=1000, help="keep_silence")

    args = parser.parse_args()

    audio_processor = AudioProcessor(args.input_file)
    audio_processor.process_audio(min_silence_len=args.min_silence_len, threshold=args.threshold, keep_silence=args.keep_silence, output_folder=args.output_folder)

if __name__ == "__main__":
    main()
