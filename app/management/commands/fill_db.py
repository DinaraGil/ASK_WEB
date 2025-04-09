import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from app.models import Profile, Tag, Question, Answer, UserRating, AnswerLike


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными для новой модели. Использование: python manage.py fill_db [ratio]'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения сущностей')

    def handle(self, *args, **options):
        ratio = options['ratio']
        self.stdout.write(f"Запуск заполнения БД с ratio = {ratio}")

        now = timezone.now()

        self.stdout.write("Создание тегов...")
        tags = []
        for i in range(ratio):
            tag = Tag(name=f"tag_{i}")
            tags.append(tag)
        Tag.objects.bulk_create(tags)
        tags = list(Tag.objects.all())

        self.stdout.write("Создание пользователей и профилей...")
        profiles = []
        for i in range(ratio):
            username = f"user_{i}"
            email = f"user_{i}@example.com"
            user = User.objects.create_user(username=username, email=email, password="password")
            profile = Profile(user=user)  # Дополнительно можно добавить аватар, если необходимо
            profiles.append(profile)
        Profile.objects.bulk_create(profiles)
        profiles = list(Profile.objects.all())

        self.stdout.write("Создание вопросов...")
        num_questions = ratio * 10
        questions = []
        for i in range(num_questions):
            author = random.choice(profiles)
            question = Question(
                author_id=author,
                title=f"Question {i}?",
                text=f"Question text {i}.",
                created_at=now - timedelta(days=random.randint(0, 365))
            )
            questions.append(question)
        Question.objects.bulk_create(questions)
        questions = list(Question.objects.all())

        self.stdout.write("Привязка тегов к вопросам...")
        for question in questions:
            question_tags = random.sample(tags, k=random.randint(1, min(3, len(tags))))
            question.tags.add(*question_tags)

        self.stdout.write("Создание ответов...")
        num_answers = ratio * 100
        answers = []
        for i in range(num_answers):
            author = random.choice(profiles)
            question = random.choice(questions)
            answer = Answer(
                author_id=author,
                question=question,
                text=f"Answer {i}. Answer text.",
                created_at=now - timedelta(days=random.randint(0, 365)),
                is_correct=False  # можно дополнительно рандомизировать правильный ответ, если нужно
            )
            answers.append(answer)
        Answer.objects.bulk_create(answers)
        answers = list(Answer.objects.all())

        self.stdout.write("Создание голосований (лайков) для вопросов и ответов...")
        num_votes = ratio * 200
        question_votes = []
        answer_votes = []

        question_vote_keys = set()
        answer_vote_keys = set()

        for i in range(num_votes):
            voter = random.choice(profiles)
            vote_value = True

            # Решаем, создаем голосование для вопроса или для ответа
            if random.choice([True, False]) and questions:
                question = random.choice(questions)
                key = (voter.id, question.id)
                if key in question_vote_keys:
                    continue
                question_vote_keys.add(key)
                rating = UserRating(
                    vote=vote_value,
                    user_id=voter,
                    question_id=question
                )
                question_votes.append(rating)
            elif answers:
                answer = random.choice(answers)
                key = (voter.id, answer.id)
                if key in answer_vote_keys:
                    continue
                answer_vote_keys.add(key)
                like = AnswerLike(
                    vote=vote_value,
                    user_id=voter,
                    answer_id=answer
                )
                answer_votes.append(like)

        if question_votes:
            UserRating.objects.bulk_create(question_votes)
        if answer_votes:
            AnswerLike.objects.bulk_create(answer_votes)

        self.stdout.write(self.style.SUCCESS("Заполнение базы данных завершено!"))