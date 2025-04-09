import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from app.models import Profile, Tag, Question, Answer, UserRating, AnswerLike
from faker import Faker


# def chunked(iterable, chunk_size):
#     """Генератор, возвращающий чанки указанного размера."""
#     for i in range(0, len(iterable), chunk_size):
#         yield iterable[i:i + chunk_size]

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными. Использование: python manage.py fill_db [ratio]'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения сущностей')

    def handle(self, *args, **options):
        ratio = options['ratio']
        fake = Faker()

        self.stdout.write(f"Запуск заполнения БД с ratio = {ratio}")

        # Вычисляем требуемые количества записей:
        num_users = ratio  # пользователей
        num_questions = ratio * 10  # вопросов
        num_answers = ratio * 100  # ответов
        num_tags = ratio  # тегов
        num_ratings = ratio * 100  # оценок пользователей (голосов)
        num_likes = ratio * 100


        # Создание тегов
        self.stdout.write("Создание тегов...")

        tag_list = [Tag(name=f"{fake.word()}_{i}") for i in range(num_tags)]
        Tag.objects.bulk_create(tag_list, batch_size=1000)
        tags = list(Tag.objects.all())

        # Создание пользователей и профилей
        self.stdout.write("Создание пользователей и профилей...")

        profiles = []
        for i in range(num_users):
            username = 'user' + str(i),
            email = f"{username}@example.com"
            user = User.objects.create_user(username=username, email=email, password="password")
            profile = Profile(user=user)
            profiles.append(profile)
        Profile.objects.bulk_create(profiles, batch_size=1000)
        profiles = list(Profile.objects.all())

        # Создание вопросов
        self.stdout.write("Создание вопросов...")
        now = timezone.now()
        questions = []
        for i in range(num_questions):
            question = Question(
                title=f"Question {i}?",
                text=f"Text {i}?",
                author_id=random.choice(profiles),
                created_at=now
            )
            questions.append(question)
        Question.objects.bulk_create(questions, batch_size=1000)
        questions = list(Question.objects.all())

        # Назначение тегов для вопросов
        self.stdout.write("Привязка тегов к вопросам...")
        for question in questions:
            # Выбираем от 1 до 3 случайных тегов для каждого вопроса
            question_tags = random.sample(tags, k=random.randint(1, min(3, len(tags))))
            question.tags.add(*question_tags)

        # Создание ответов
        self.stdout.write("Создание ответов...")
        answer_list = []
        for i in range(num_answers):
            answer = Answer(
                text=f"Answer {i}?",
                author_id=random.choice(profiles),
                question_id=random.choice(questions),
                created_at=now
            )
            answer_list.append(answer)
        Answer.objects.bulk_create(answer_list, batch_size=1000)
        answers = list(Answer.objects.all())

        # Создание голосований (вопросов и ответов)

        self.stdout.write("Создание голосований...")
        rating_set = set()
        rating_list = []
        while len(rating_list) < num_ratings:
            user = random.choice(profiles)
            question = random.choice(questions)
            key = (user.id, question.id)
            if key not in rating_set:
                rating_set.add(key)
                rating_list.append(UserRating(
                    vote=random.choice([True, False]),
                    user_id=user,
                    question_id=question
                ))
        UserRating.objects.bulk_create(rating_list, batch_size=1000)

        answer_like_set = set()  # для контроля уникальности (user.id, answer.id)
        answerlike_list = []

        while len(answerlike_list) < num_likes:
            user = random.choice(profiles)
            answer = random.choice(answers)
            key = (user.id, answer.id)
            if key not in answer_like_set:
                answer_like_set.add(key)
                vote = random.choice([True, False])  # случайное значение голосования (лайк/дизлайк)
                answerlike_list.append(AnswerLike(user_id=user, answer_id=answer, vote=vote))

        # Массовая вставка с указанием размера чанка для оптимизации
        AnswerLike.objects.bulk_create(answerlike_list, batch_size=1000)

        print(f"Добавлено {len(answerlike_list)} оценок для ответов (AnswerLike).")

        self.stdout.write(self.style.SUCCESS("Successfully filled the database!"))
