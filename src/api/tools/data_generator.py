from datetime import date
from typing import Literal
from uuid import uuid4

from faker import Faker


class DataGenerator:
    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def email(self) -> str:
        return f"taskflow-{uuid4().hex}@example.com"

    def password(self) -> str:
        return self.faker.password()

    def task_title(self) -> str:
        return f"Task: {self.faker.sentence(nb_words=4)}"[:100]

    def task_description(self) -> str:
        return self.faker.text(max_nb_chars=200)

    def task_status(self) -> Literal["todo", "in_progress", "done"]:
        return self.faker.random_element(elements=("todo", "in_progress", "done"))

    def task_due_date(self) -> date:
        return self.faker.date_this_year()


fake_en = DataGenerator(faker=Faker())
