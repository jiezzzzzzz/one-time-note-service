# Сервис мнговенных записок

Нашла [статью на Хабре](https://habr.com/ru/articles/486246/), захотелось повторить тот же сервис под Джанго. 

---

Это, по сути, приложение для шифрования и дешифрования вводимых пользователем данных. В теории, можно добавить возможность обмена сообщениями с разных аккаунтов и 
получится настоящий мессенджер.

---

## Как работает 

Пользователю предлагается ввести текст в специальную форму. Далее этот текст шифруется следующим образом: 

            key = Fernet.generate_key()
                        str_key = key.decode('ascii')
                        fernet = Fernet(key)
                        bin_string = form.cleaned_data['text'].encode('utf-8')
                        cipher_text = fernet.encrypt(bin_string)
                        str_cipher_text = cipher_text.decode('ascii')
                        random_number = random.randint(1000000, 9999999)
                        while True:
                                    note_object = Note.objects.filter(number=random_number).first()
                                    if note_objetc:
                                                random_number = random.randint(1000000, 9999999)
                    


После нажатия кнопки "отправить" пользователя пермещают на специальную страницу, вроде проверки "вы ли писали это сообщение", но пока это не реализовано толком и не знаю, будт ли вообще добалвено.
В случае правильного ответа и после нажатия кнопки "расшифровать" пользователь попадает на страницу с расшифрованным текстом. Расшифровывается он вот так: 


            cipher_note = get_object_or_404(Note, number=random_number)
                        cipher_text = cipher_note.crypto_text.encode('ascii')
                        key = str_key.encode('ascii')
                        fernet = Fernet(key)
                        text = fernet.decrypt(cipher_text)

                        text = text.decode('utf-8')
                        cipher_note.delete()
            

При этом сам текст в базу данных не сохраняется, только его зашифрованное представление.

### Какие ссылки можно использовать: 

- <int:random_number>/<str:str_key>/ (старница с вопросом)
- /decrypt/<int:random_number>/<str:str_key/ (страница с расшифровкой)

Для перехода по ссылкам нужен секретный ключ и рандомное число от 1000000 до 9999999, так что перейти на них просто так с главной страницы невозможно, если не знаеть
собственно ключ и число.

---

## Как запустить

 ~~ 1. не надо это запускать  ~~ 
 
 1. Скачать проект через <code>git clone</code>
 
 2. Создать файл <code>.env</code> и поместить в него секретный ключ Джанго:
 
             SECRET_KEY = 
 
 3. Накатить миграций:

            python manage.py migrate

 4.  Готово!

