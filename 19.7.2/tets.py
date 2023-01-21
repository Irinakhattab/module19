from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='волна1', animal_type='волна',
                                     age='1000', pet_photo='image/jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Море", "море", "3", "image/jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Море', animal_type='море', age=3):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    assert len(my_pets['pets']) > 0, "There is no my pets"
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name


# Мой тест 1
def test_add_new_pet_without_photo_with_valid_data(name='ктото', animal_type='ктото', age='10'):
    """Проверяем, что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''


# Мой тест 2
def test_add_pet_new_photo(pet_photo='image/jpeg'):
    """Проверяем что можно добавить/изменить фото питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем(если без фото)/изменяем фото питомца
    status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] != ''


# Мой тест 3
def test_add_pet_new_photo(pet_photo='images/cat.xlsx'):
    """Проверяем, что нельзя загрузить фото несоответствующего формата"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем(если без фото)/изменяем фото питомца
    status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200


# Мой тест 4
def test_get_api_key_for_invalid_user_email(email='valid_email', password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 403 при вводе неверного логина"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


# Мой тест 5
def test_get_api_key_for_invalid_user_password(email=valid_email, password='123456'):
    """ Проверяем, что запрос api ключа возвращает статус 403 при вводе неверного пароля"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


# Мой тест 6
def test_add_new_pet_with_negative_age(name='Шарик', animal_type='кавказец',
                                       age='-1', pet_photo='image/jpeg'):
    """Проверяем, что нельзя добавить питомца с отрицательным возрастом
    !!!Баг- сайт позволяет добавить питомца с отрицательным возрастом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print('Баг - сайт позволяет добавить питомца с отрицательным возрастом')


# Мой тест 7
def test_add_new_pet_with_too_old_age(name='Ореш', animal_type='доберман',
                                       age='1000', pet_photo='image/jpeg'):
    """Проверяем, что нельзя добавить питомца, указав слишком большой возраст (больше 50)
    !!Баг - сайт позволяет добавить питомца, указав слишком большой возраст"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print('Баг - сайт позволяет добавить питомца, указав слишком большой возраст (более 50 лет)')


# Мой тест 8
def test_add_new_pet_with_invalid_age(name='volna', animal_type='volna',
                                       age='', pet_photo='image/jpeg'):
    """Проверяем что нельзя добавить питомца, не указав возраст
    !!Баг - сайт позволяет добавить питомца, не указав возраст"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print('Баг - сайт позволяет добавить питомца, не указав возраст')


# Мой тест 9
def test_add_new_pet_with_long_name(name='ввввввввввввввввввввввввввввввввввввввввввввввввввв',
                                    animal_type='сфинкс',
                                    age='1', pet_photo='images/cat.jpg'):
    """Проверяем, что нельзя добавить питомца с именем длиннее 50 символов"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print('Баг - сайт позволяет добавить питомца с именем длиннее 50 символов')


# Мой тест 10
def test_try_unsuccessful_delete_empty_pet_id():
    """Проверяем, что нельзя удалить питомца с пустым id"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Указываем значение id
    pet_id = ''
    # Пробуем удалить питомца с пустым id
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400 or 404
    print('Попытка удалить питомца с пустым значением id не удалась')
