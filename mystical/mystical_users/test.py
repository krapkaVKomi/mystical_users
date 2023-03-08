from faker import Faker
import random


def gen_phone():
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 888)).zfill(3)
    last = (str(random.randint(1, 9998)).zfill(4))
    phone_number = '{}-{}-{}'.format(first, second, last)


faker = Faker()

print(f'Name: {faker.name()}')
print(f'Job: {faker.job()}')
print(f'Email: {faker.email()}')
print(f'Domain name: {faker.domain_name()}')
print(f'Date of birth: {faker.date_of_birth()}')
print(f'text: {faker.text()}')
print(f'phone number: {gen_phone()}')
print(f'company name: {faker.word().title()}')