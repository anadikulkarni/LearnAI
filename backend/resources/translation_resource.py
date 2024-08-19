import http.client
import json
from flask import request
from flask_restful import Resource, fields, marshal_with
from ..models import db, Translation, LectureTranscript
from ..read_json_fields import translation_fields
# Define the fields to serialize the response

LANGUAGES = ["fr", "es", "en", "zh", "hi", "it", "ja", "kn", "ml", "ta", "te"]

class TranslationResource(Resource):
    @marshal_with(translation_fields)
    def post(self):
        data = request.json

        # Extract data from request
        lecture_transcript_id = data.get('lecture_transcript_id')
        custom_text = data.get('content')
        target_language = data.get('language')

        # Validate input data
        if not target_language or target_language not in LANGUAGES:
            return {'error': 'Valid target language is required'}, 400

        # If lecture_transcript_id is provided, fetch the content from the database
        if lecture_transcript_id is not None:
            lecture_transcript = LectureTranscript.query.get(lecture_transcript_id)
            if not lecture_transcript:
                return {'error': 'Lecture transcript not found'}, 404
            text_to_translate = lecture_transcript.content
        else:
            # Otherwise, use the custom text provided
            if not custom_text:
                return {'error': 'Content is required'}, 400
            text_to_translate = custom_text

        try:
            # Prepare the request payload and headers
            payload = json.dumps([{"Text": text_to_translate}])
            headers = {
                'x-rapidapi-key': "b2fcaf2785msh81507f68e5e85c2p1d97fejsne10a977388bb",
                'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com",
                'Content-Type': "application/json"
            }

            # Make the API request
            conn = http.client.HTTPSConnection("microsoft-translator-text.p.rapidapi.com")
            conn.request("POST", f"/translate?to={target_language}&api-version=3.0&profanityAction=NoAction&textType=plain", payload, headers)
            res = conn.getresponse()
            data = res.read()
            translated_data = json.loads(data.decode("utf-8"))

            # Extract the translated text
            translated_text = translated_data[0]['translations'][0]['text']

            # Create a new Translation object and save it to the database
            translation = Translation(
                language=target_language,
                content=translated_text,
                lecture_transcript_id=lecture_transcript_id
            )
            db.session.add(translation)
            db.session.commit()

            return translation, 201

        except Exception as e:
            # Handle translation errors
            return {'error': str(e)}, 500
