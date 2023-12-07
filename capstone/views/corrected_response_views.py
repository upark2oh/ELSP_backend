from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from sklearn.metrics.pairwise import cosine_similarity
from google.cloud import speech
from pydub import AudioSegment
from happytransformer import TTSettings
from transformers import T5Tokenizer, T5ForConditionalGeneration, BertTokenizer, BertModel
import os, torch, io
from myapi.settings import GOOGLE_APPLICATION_CREDENTIALS, MODEL_PATH

#수정된 답변을 반환
class CorrectionView(APIView):
    def __init__(self, *args, **kwargs):
        super(CorrectionView, self).__init__(*args, **kwargs)
        
        self.model_path = MODEL_PATH
        self.t5_model = T5ForConditionalGeneration.from_pretrained(self.model_path)
        self.t5_tokenizer = T5Tokenizer.from_pretrained(self.model_path, legacy=False)

    def post(self, request, *args, **kwargs):
        try:
            user_response = request.data.get('user_response', '')
            encoded_input = self.t5_tokenizer("grammar: " + user_response, return_tensors="pt")
            # Define TTSettings for beam search
            beam_settings = TTSettings(num_beams=5, min_length=1, max_length=100)

            with torch.no_grad():
                output = self.t5_model.generate(
                    input_ids=encoded_input["input_ids"],
                    attention_mask=encoded_input["attention_mask"],
                    num_beams=beam_settings.num_beams,
                    min_length=beam_settings.min_length,
                    max_length=beam_settings.max_length
                )
            generated_text = self.t5_tokenizer.decode(output[0], skip_special_tokens=True)        
            print(generated_text)

            return Response({'corrected_response': generated_text}, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
        except ConnectionError:
            # 서버와의 연결이 끊어진 경우에 대한 예외 처리
            return Response({'error': 'Connection to the server has been lost.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE, content_type='application/json; charset=utf-8')
        
        except Exception as e:
            # 기타 예외 처리
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json; charset=utf-8')

#유사도 계산
class SimilarityView(APIView):
    def __init__(self, *args, **kwargs):
        super(SimilarityView, self).__init__(*args, **kwargs)

        # 모델과 토크나이저 초기화
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')

    def post(self, request, *args, **kwargs):
            question = request.data.get('question', '')
            user_response = request.data.get('user_response','')

            input_tokens = self.tokenizer(question, return_tensors='pt')
            output_tokens = self.tokenizer(user_response, return_tensors='pt')

            input_embedding = self.model(**input_tokens).last_hidden_state.mean(dim=1)
            output_embedding = self.model(**output_tokens).last_hidden_state.mean(dim=1)

            similarity = cosine_similarity(input_embedding.detach(), output_embedding.detach()).item()

            return Response({'similarity': similarity}, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')

#구글API
class AudioUploadView(APIView):
    def post(self, request, *args, **kwargs):

        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
            client = speech.SpeechClient()

            m4a_content = request.body
            flac_content = convert_m4a_to_flac(m4a_content)

            audio = speech.RecognitionAudio(content=flac_content)
            
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
                sample_rate_hertz=44100,
                audio_channel_count=2,
                language_code="en-US",
                enable_word_time_offsets=True,
                enable_automatic_punctuation=True,  # 수정: 소문자로 변경
                enable_spoken_punctuation=True,
            )

            response = client.recognize(config=config, audio=audio)

            transcripts = []  # 결과를 저장할 리스트

            total_accuracy = 0  # 정확도의 합을 저장할 변수
            total_results = len(response.results)  # 전체 결과의 수


            for index, result in enumerate(response.results):
                alternative = result.alternatives[0]
                transcript = result.alternatives[0].transcript
                accuracy = result.alternatives[0].confidence

                transcripts.append(transcript)
                total_accuracy += accuracy

                for word_info in alternative.words:
                    word = word_info.word
                    start_time = word_info.start_time
                    end_time = word_info.end_time
                    
                    #print(f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}")

                #print("Transcript at index {}: {}, Accuracy: {}".format(index, transcript, accuracy))
                #print(end_time.total_seconds())
            
            average_accuracy = total_accuracy / total_results
            recording_time = str(end_time.total_seconds())
            transcripts = '. '.join(transcripts)
            print("Transcript: {}, Accuracy: {}, Time: {}".format(transcripts, average_accuracy, recording_time))
            
            return Response({'transcript': transcripts, 'accuracy': average_accuracy, 'recording_time' :recording_time}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': f'Error processing audio: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def convert_m4a_to_flac(m4a_content):
    # M4A 파일을 AudioSegment로 변환
    m4a_audio = AudioSegment.from_file(io.BytesIO(m4a_content), format="m4a")

    # FLAC로 변환
    flac_audio = m4a_audio.export(format="flac")
    
    # FLAC 파일의 content 반환
    return flac_audio.read()