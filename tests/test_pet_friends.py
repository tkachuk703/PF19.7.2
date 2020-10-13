from api import PetFriends
import settings

pf = PetFriends()


def test_get_api_key_for_valid_user(email=settings.valid_email,
                                    password=settings.valid_password):
    """Проверяем метод GET_API_KEY с правильными данными.
    Значения переменных берутся из файла settings.py:
    Правильный EMAIL - valid_email
    Правильный PASSWORD - valid_password"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=settings.empty_filter,
                                     email=settings.valid_email,
                                     password=settings.valid_password):
    """Проверяем метод GET_API_KEY с правильными данными.
    Значения переменных берутся из файла settings.py:
    Правильный EMAIL - valid_email
    Правильный PASSWORD - valid_password
    Пустой фильтр - empty_filter"""

    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(email=settings.valid_email,
                                     password=settings.valid_password,
                                     name=settings.valid_pet_name,
                                     animal_type=settings.valid_pet_animal_type,
                                     age=settings.valid_pet_age,
                                     pet_photo=settings.valid_pet_photo):
    """Проверяем метод ADD_NEW_PET с правильными данными.
    Значения переменных берутся из файла settings.py:
    Правильный EMAIL - valid_email
    Правильный PASSWORD - valid_password
    Правильный NAME - valid_pet_name
    Правильный ANIMAL_TYPE - valid_pet_animal_type
    Правильный AGE - valid_pet_age
    Правильное PET_PHOTO - valid_pet_photo"""

    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.add_new_pet(auth_key,
                                    name=name,
                                    animal_type=animal_type,
                                    age=str(age),
                                    pet_photo=pet_photo)
    pf.delete_pet(auth_key=auth_key, pet_id=result['id'])  # Удаляем созданного питомца чтобы не захламлять БД
    assert status == 200
    assert result['name'] == name
    assert result['age'] == str(age)
    assert result['animal_type'] == animal_type


def test_delete_pet_with_valid_data(email=settings.valid_email,
                                    password=settings.valid_password,
                                    name=settings.valid_pet_name,
                                    animal_type=settings.valid_pet_animal_type,
                                    age=settings.valid_pet_age,
                                    pet_photo=settings.valid_pet_photo):
    """Проверяем метод ADD_NEW_PET с правильными данными.
    Значения переменных берутся из файла settings.py:
    Правильный EMAIL - valid_email
    Правильный PASSWORD - valid_password
    Правильный NAME - valid_pet_name
    Правильный ANIMAL_TYPE - valid_pet_animal_type
    Правильный AGE - valid_pet_age
    Правильное PET_PHOTO - valid_pet_photo"""

    _, auth_key = pf.get_api_key(email, password)
    _, pet_id = pf.add_new_pet(auth_key=auth_key,
                               name=name,
                               animal_type=animal_type,
                               age=str(age),
                               pet_photo=pet_photo)
    status = pf.delete_pet(auth_key=auth_key, pet_id=pet_id['id'])
    assert status == 200


def test_create_pet_simple_with_valid_data(email=settings.valid_email,
                                           password=settings.valid_password,
                                           name=settings.valid_pet_name,
                                           animal_type=settings.valid_pet_animal_type,
                                           age=settings.valid_pet_age):
    """Проверяем метод CREATE_PET_SIMPLE с правильными данными.
    Значения переменных берутся из файла settings.py:
    Правильный EMAIL - valid_email
    Правильный PASSWORD - valid_password
    Правильный NAME - valid_pet_name
    Правильный ANIMAL_TYPE - valid_pet_animal_type
    Правильный AGE - valid_pet_age"""

    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.create_pet_simple(auth_key=auth_key,
                                          name=name,
                                          animal_type=animal_type,
                                          age=age)
    pf.delete_pet(auth_key=auth_key, pet_id=result['id'])  # Удаляем созданного питомца чтобы не захламлять БД
    assert status == 200
    assert result['name'] == name
    assert result['age'] == str(age)
    assert result['animal_type'] == animal_type


def test_add_photo_with_valid_data(pet_photo=settings.valid_pet_photo,
                                   name=settings.valid_pet_name,
                                   animal_type=settings.valid_pet_animal_type,
                                   pet_age=settings.valid_pet_age,
                                   email=settings.valid_email,
                                   password=settings.valid_password):
    """Проверяем метод ADD_PHOTO_OF_PET с правильными данными.
    Значения переменных берутся из файла settings.py:
    Правильный EMAIL - valid_email
    Правильный PASSWORD - valid_password
    Правильный NAME - valid_pet_name
    Правильный ANIMAL_TYPE - valid_pet_animal_type
    Правильный AGE - valid_pet_age
    Правильное PET_PHOTO - valid_pet_photo"""

    _, auth_key = pf.get_api_key(email=email, password=password)
    _, result = pf.create_pet_simple(auth_key=auth_key,
                                     name=name,
                                     animal_type=animal_type,
                                     age=pet_age)
    status, result = pf.add_photo_of_pet(auth_key=auth_key,
                                         pet_id=result['id'],
                                         pet_photo=pet_photo)
    pf.delete_pet(auth_key=auth_key, pet_id=result['id'])  # Удаляем созданного питомца чтобы не захламлять БД
    assert status == 200
    assert len(result['pet_photo']) > 0


def test_get_api_key_for_valid_user_with_invalid_password(email=settings.valid_email,
                                                          password=settings.invalid_password):
    """Проверяем метод GET_API_KEY с правильным EMAIL и неправильным PASSWORD.
    Значения переменных берутся из файла settings.py:
    Правильный EMAIL - valid_email
    Неправильный PASSWORD - invalid_password"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_with_invalid_email(email=settings.invalid_email,
                                        password=settings.valid_password):
    """Проверяем метод GET_API_KEY с неправильным EMAIL и правильным PASSWORD.
    Значения переменных берутся из файла settings.py:
    Неправильный EMAIL - invalid_email
    Правильный PASSWORD - valid_password"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_with_empty_email_and_password(email=settings.empty_email,
                                                   password=settings.empty_password):
    """Проверяем метод GET_API_KEY с пустым EMAIL и пустым PASSWORD.
    Значения переменных берутся из файла settings.py:
    Пустой EMAIL - empty_email
    Пустой PASSWORD - empty_password"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_create_pet_simple_with_valid_data_and_incorrect_auth_key(name=settings.valid_pet_name,
                                                                  animal_type=settings.valid_pet_animal_type,
                                                                  age=settings.valid_pet_age):
    """Проверяем метод CREATE_PET_SIMPLE с верными данными и неправильным AUTH_KEY.
    Значения переменных берутся из файла settings.py:
    Неправильный AUTH_KEY - incorrect_auth_key
    Правильный NAME - valid_pet_name
    Правильный ANIMAL_TYPE - valid_pet_animal_type
    Правильный AGE - valid_pet_age"""

    auth_key = settings.incorrect_auth_key
    status, result = pf.create_pet_simple(auth_key=auth_key,
                                          name=name,
                                          animal_type=animal_type,
                                          age=age)
    assert status == 403


def test_delete_pet_with_incorrect_pet_id(pet_id=settings.incorrect_pet_id,
                                          email=settings.valid_email,
                                          password=settings.valid_password):
    """Проверяем метод DELETE_PET с верным AUTH KEY и неправильным PET ID.
    Значения переменных берутся из файла settings.py:
    Неправильный PET ID - incorrect_pet_id
    NOTE: При описанных входных данных возвращаемые параметры не описаны в документации.
    Ожидаем что код ответа будет не равен 200"""

    _, auth_key = pf.get_api_key(email, password)
    status = pf.delete_pet(auth_key=auth_key, pet_id=pet_id)
    assert status != 200


def test_delete_pet_with_empty_pet_id(pet_id=settings.empty_pet_id,
                                      email=settings.valid_email,
                                      password=settings.valid_password):
    """Проверяем метод DELETE_PET с верным AUTH KEY и пустым PET ID.
    Значения переменных берутся из файла settings.py:
    Пустой PET ID - empty_pet_id
    NOTE: При описанных входных данных возвращаемые параметры не описаны в документации.
    Ожидаем что код ответа будет не равен 200"""

    _, auth_key = pf.get_api_key(email, password)
    status = pf.delete_pet(auth_key=auth_key, pet_id=pet_id)
    assert status != 200


def test_add_zero_size_photo(pet_photo=settings.empty_pet_photo,
                             name=settings.valid_pet_name,
                             animal_type=settings.valid_pet_animal_type,
                             pet_age=settings.valid_pet_age,
                             email=settings.valid_email,
                             password=settings.valid_password):
    """Проверяем метод ADD_PHOTO_OF_PET с пустым фото.
    Значения переменных берутся из файла settings.py:
    Правильный EMAIL - valid_email
    Правильный PASSWORD - valid_password
    Правильный NAME - valid_pet_name
    Правильный ANIMAL_TYPE - valid_pet_animal_type
    Правильный AGE - valid_pet_age
    PET_PHOTO с нулевой длиной - empty_pet_photo"""

    _, auth_key = pf.get_api_key(email=email, password=password)
    _, result = pf.create_pet_simple(auth_key=auth_key,
                                     name=name,
                                     animal_type=animal_type,
                                     age=pet_age)
    pet_id_for_delete = result['id']  # Сохраняем ID созданного питомца, для удаления по окончании теста
    status, result = pf.add_photo_of_pet(auth_key=auth_key,
                                         pet_id=result['id'],
                                         pet_photo=pet_photo)
    pf.delete_pet(auth_key=auth_key, pet_id=pet_id_for_delete)  # Удаляем созданного питомца чтобы не захламлять БД
    assert status == 400


def test_get_all_pets_with_valid_key_and_invalid_filter(filter=settings.invalid_filter,
                                                        email=settings.valid_email,
                                                        password=settings.valid_password):
    """Проверяем метод GET_ALL_PETS с верными EMAIL и PASSWORD, но неверным FILTER.
    Значения переменных берутся из файла settings.py:
    Правильный EMAIL - valid_email
    Правильный PASSWORD - valid_password
    Неправильный FILTER - invalid_filter
    NOTE: При описанных входных данных возвращаемые параметры не описаны в документации.
    Ожидаем что код ответа будет не равен 200"""

    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    print(status)
    assert status != 200


def test_add_wrong_type_photo(pet_photo=settings.wrong_type_photo,
                              name=settings.valid_pet_name,
                              animal_type=settings.valid_pet_animal_type,
                              pet_age=settings.valid_pet_age,
                              email=settings.valid_email,
                              password=settings.valid_password):
    """Проверяем метод ADD_PHOTO_OF_PET с фото в непредусмотренном формате.
    Значения переменных берутся из файла settings.py:
    Правильный EMAIL - valid_email
    Правильный PASSWORD - valid_password
    Правильный NAME - valid_pet_name
    Правильный ANIMAL_TYPE - valid_pet_animal_type
    Правильный AGE - valid_pet_age
    PET_PHOTO в непредусмотренном формате - wrong_type_photo"""

    _, auth_key = pf.get_api_key(email=email, password=password)
    _, result = pf.create_pet_simple(auth_key=auth_key,
                                     name=name,
                                     animal_type=animal_type,
                                     age=pet_age)
    pet_id_for_delete = result['id']  # Сохраняем ID созданного питомца, для удаления по окончании теста
    status, result = pf.add_photo_of_pet(auth_key=auth_key,
                                         pet_id=result['id'],
                                         pet_photo=pet_photo)
    pf.delete_pet(auth_key=auth_key, pet_id=pet_id_for_delete)  # Удаляем созданного питомца чтобы не захламлять БД
    assert status == 400
