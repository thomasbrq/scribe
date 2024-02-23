from pydub import AudioSegment
import io

class AudioService:
    """
    # Audio Service class
    """

    def __init__(self) -> None:
        pass

    def convert_bytearray_to_audio_buffer(self, array: bytearray):
        audio_bytes_io      = io.BytesIO(array)
        audio_segment       = AudioSegment.from_file(audio_bytes_io)

        audio_buffer        = io.BytesIO()
        audio_segment.export(audio_buffer, format="wav")

        return audio_buffer
