from database import *
import json
from mcq_generator import generate_evaluate_chain
from fastapi import FastAPI, Depends, HTTPException, status

async def examFind(data, db):
    print('examFind')
    examBatch = db.query(QuestionBatch).filter(
        (QuestionBatch.cefr_rank == data["cefr_level"]) &
        (QuestionBatch.interest == data["interest"]) &
        (QuestionBatch.category == data["subject"])
        
    ).first()    
    if not examBatch:
        class ExamData:
            def __init__(self, interest, cefr_level, subject):
                self.number = 5
                self.interest = interest
                self.cefr_level = cefr_level
                self.subject = subject

        data_object = ExamData(data['interest'], data['cefr_level'], data['subject'])

        await examGenerate(data_object, db)
        examBatch = db.query(QuestionBatch).filter(
            (QuestionBatch.cefr_rank == data["cefr_level"]) &
            (QuestionBatch.interest == data["interest"]) &
            (QuestionBatch.category == data["subject"])
            
        ).first()  

    if examBatch:
        questions = db.query(Question.id, Question.question_text).filter(
            Question.batch_id==examBatch.id
        ).all()

        # Konversi hasil query menjadi list of dicts
        question_list = []
        for q in questions:
            # Ambil pilihan berdasarkan question.id
            choices = db.query(Choice.id, Choice.choice_text).filter(Choice.question_id == q[0]).all()
            
            # Konversi choices ke list of dicts
            choice_list = [{"id": c[0], "text": c[1]} for c in choices]
            
            # Tambahkan choices ke dalam setiap pertanyaan
            question_list.append({
                "id": q[0],
                "text": q[1],
                "options": choice_list  # Tambahkan daftar pilihan ke dalam pertanyaan
            })

        # Buat response dictionary
        response = {
            "id": examBatch.id,
            "questions": question_list
        }
        return response
    
    
    
    return data

async def examGenerate(data, db):
    try:
        # Read the mock response from a JSON file
        with open("response.json", 'r') as f:
            response_json = json.load(f)

        try: 
            # Simulate API invocation
            api_response = generate_evaluate_chain.invoke({
                "number": data.number,
                "cefr_level": data.cefr_level,
                "interest": data.interest,
                "subject": data.subject,
                "tone": "conversational",
                "response_json": response_json
            })
            # api_response = {'number': '2', 'cefr_level': 'anything', 'interest': 'anything', 'subject': 'anything', 'tone': 'conversational', 'response_json': {'1': {'mcq': 'multiple choice question', 'options': {'a': 'choice here', 'b': 'choice here', 'c': 'choice here', 'd': 'choice here'}, 'correct': 'correct answer', 'discussion': 'feedback of when the wrong answer is chosen'}, '2': {'mcq': 'multiple choice question', 'options': {'a': 'choice here', 'b': 'choice here', 'c': 'choice here', 'd': 'choice here'}, 'correct': 'correct answer', 'discussion': 'feedback of when the wrong answer is chosen'}, '3': {'mcq': 'multiple choice question', 'options': {'a': 'choice here', 'b': 'choice here', 'c': 'choice here', 'd': 'choice here'}, 'correct': 'correct answer', 'discussion': 'feedback of when the wrong answer is chosen'}}, 'quiz': '{\n"1": {\n"mcq": "Which of the following is NOT a type of anything?",\n"options": {\n"a": "Anything",\n"b": "Something",\n"c": "Nothing",\n"d": "Everything"\n},\n"correct": "c",\n"discussion": "Anything refers to any object, concept, or idea, while nothing refers to the absence of anything. Therefore, nothing is not a type of anything."\n},\n"2": {\n"mcq": "What is the opposite of anything?",\n"options": {\n"a": "Nothing",\n"b": "Something",\n"c": "Everything",\n"d": "None of the above"\n},\n"correct": "a",\n"discussion": "Nothing is the opposite of anything because it represents the absence of anything, while something, everything, and none of the above imply the existence of something."\n}\n}'}

            print('api_response')
            print(api_response)

            # Parse the quiz data
            quiz_json_str = api_response['quiz'].strip('```json').strip('```').strip()

            quiz = json.loads(quiz_json_str)                    
        except (ValueError, KeyError) as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse quiz data: {str(e)}")
        
        question_batch = QuestionBatch(
            category=data.subject,
            cefr_rank=data.cefr_level,
            interest=data.interest,
            title='empty'
        )
        db.add(question_batch)
        db.commit()
        db.refresh(question_batch)

        # Restructure and save questions to the database
        for key, value in quiz.items():
            question_text = value["mcq"]
            correct_answer = value["correct"]
            explanation = json.dumps(value["discussion"])  # Convert dictionary to JSON string

            # Create a new question entry
            question = Question(
                batch_id=question_batch.id, 
                cefr_level=data.cefr_level,
                interest=data.interest,
                subject=data.subject,
                question_text=question_text,
                correct_answer=correct_answer,
                explanation=explanation,
            )
            db.add(question)
            db.commit()
            db.refresh(question)

            # Create choices for the question
            for option_key, option_value in value["options"].items():
                is_correct = (option_key == value["correct"])

                # Get the explanation for this choice
                explanation = value["discussion"].get(option_key, "No explanation available.")
            
                choice = Choice(
                    question_id=question.id,
                    choice_text=option_value,
                    is_correct=is_correct,
                    explanation=explanation
                )
                db.add(choice)

            db.commit()

        return {
            "message": "Questions generated and saved to the database successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")