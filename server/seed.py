from app import app
from faker import Faker
import random
from datetime import datetime

from models import db, User, Assessment, Assessment_Response, Attendance, Chat, Class,Resource, Role, School, Student_Class

with app.app_context():
    #deleting previous records
    
    db.drop_all()
    db.create_all()

    # db.session.commit()

    fake = Faker()
    
    print('🦸‍♀️ seeding roles...')
    
    roles_data = [
        {"id": 1, "role": "Owner"},
        {"id": 2, "role": "Instructor"},
        {"id": 3, "role": "Student"}
    ]

    roles = [Role(**role_info) for role_info in roles_data]
    
    db.session.add_all(roles)
    db.session.commit()
    
    print('🦸‍♀️ Seeding users...')
    
    users =[]
    existing_emails = set()  # Keep track of used email addresses

    for _ in range(600):
        role_random = random.choice(roles)
        fake_email = fake.email()

        # email address is unique
        while fake_email in existing_emails:
            fake_email = fake.email()

        existing_emails.add(fake_email)  # Mark the email as used

        user = User(
            name=fake.name(),
            phone_number = random.randint(1000000000, 2147483647),
            photo = f'https://dummyimage.com/200x200/{random.randint(10, 100000)}',
            email_address=fake_email,
            password_hash=fake.password(),
            role_id=role_random.id
        )
        users.append(user)

    db.session.add_all(users)
    db.session.commit()  
    
    print('🦸‍♀️ Seeding schools...')
    
    owners = User.query.filter(User.role_id == 1).all()
    used_posters = set()  # Keep track of used poster URLs
    
    schools =[]
    for _ in range(800):
        random_owner = random.choice(owners)
        unique_poster = f'https://dummyimage.com/200x200/{random.randint(10, 100000)}'
        
        #  poster is unique
        while unique_poster in used_posters:
            unique_poster = f'https://dummyimage.com/200x200/{random.randint(10, 100000)}'

        used_posters.add(unique_poster)  # Mark the poster as used

        school = School(
            school_name=fake.name(),
            poster=unique_poster,
            location=fake.address(),
            owner_id=random_owner.id,
        )
        schools.append(school)

    db.session.add_all(schools)
    db.session.commit()

    
    print('🦸‍♀️ Seeding classes...')
    
    classes = []
    educator = User.query.filter_by(role_id = 2).all()
    for _ in range(400):
        school_random = random.choice(schools)
        class_bd = Class(
        class_name = fake.name(),
        educator_id = random.choice(educator).id,
        school_id = school_random.id,
        )
        classes.append(class_bd)
        
    db.session.add_all(classes)
    db.session.commit()
    
    print('🦸‍♀️ Seeding student_class...')

    
    students = User.query.filter_by(role_id = 3).all()
    student_classes =[]
    for _ in range(500):
        classes_random = random.choice(classes)
        student_class = Student_Class(
        class_id = classes_random.id,
        student_id = random.choice(students).id
        )
        student_classes.append(student_class)
        
    db.session.add_all(student_classes)
    db.session.commit()
    
    print('🦸‍♀️ Seeding attendance...')
    
    attendances= []
    for _ in range(500):
        classes_random = random.choice(classes)
        attendance = Attendance(
            class_id = classes_random.id,
            student_id = random.choice(students).id,
            date = datetime.now(),
            is_present = fake.boolean(chance_of_getting_true=75)
        )
        attendances.append(attendance)
    
    db.session.add_all(attendances)
    db.session.commit()
    
    print('🦸‍♀️ Seeding resources...')
    
    resources =[]
    for _ in range(250):
            resource = Resource(
                title = fake.name(),
                type = fake.name(),
                url = fake.url(),
                content = fake.text(),
                educator_id = random.choice(educator).id
        )
            resources.append(resource)
        
    db.session.add_all(resources)
    db.session.commit()
        
    print('🦸‍♀️ Seeding assessments...')
    
    assessments =[]
    for _ in range(250):
            classes_random = random.choice(classes)
            assesment = Assessment(
                class_id = classes_random.id,
                title = fake.name(),
                body = fake.text(),
                start_time = datetime(2023, 10, 31, 9, 0, 0),
                end_time = datetime(2023, 10, 31, 10, 0, 0),
                duration = random.randint(120, 200)
        )
            assessments.append(assesment)
        
    db.session.add_all(assessments)
    db.session.commit()
    
    print('🦸‍♀️ Seeding assessments_choice...')
    
    assessment_random = random.choice(assessments)
    responses = []
    for _ in range(650):
        response = Assessment_Response(
            assessment_id = assessment_random.id,
            student_id = random.choice(students).id,
            submitted_time = datetime(2023, 10, 31, 10, 0, 0),
            work = fake.text()
        )        
        responses.append(response)
        
    db.session.add_all(responses)
    db.session.commit()
    
    print('🦸‍♀️ Seeding chats...')
    
    chats = []
    user_random = random.choice(users)
    for _ in range(200):
        classes_random = random.choice(classes)
        chat = Chat(
            class_id = classes_random.id,
            sender = user_random.id,
            message = fake.text()
        )
        chats.append(chat)
        
    db.session.add_all(chats)
    db.session.commit()