from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .forms import TextForm
from cryptography.fernet import Fernet
from .models import Note
import random


def index(request):
    form = TextForm()
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            key = Fernet.generate_key()
            str_key = key.decode('ascii')
            fernet = Fernet(key)
            bin_string = form.cleaned_data['text'].encode('utf-8')
            cipher_text = fernet.encrypt(bin_string)
            str_cipher_text = cipher_text.decode('ascii')
            random_number = random.randint(1000000, 9999999)
            while True:
                n = Note.objects.filter(number=random_number).first()
                if n:
                    random_number = random.randint(1000000, 9999999)
                    continue
                break
            cipher_note = Note.objects.get_or_create(number=random_number, crypto_text=str_cipher_text)

            link = f'{request.scheme}://{request.get_host()}/{random_number}/{str_key}'

            return render(request, 'structure/question.html',
                          {'random_number': random_number, 'str_key': str_key})

    return render(request, 'structure/index.html', {'form': form})


def question(request, random_number, str_key):
    link = f'{request.scheme}://{request.get_host()}/decrypt/{random_number}/{str_key}'
    return render(request, 'structure/question.html', {'link': link})


def decrypt(request, random_number, str_key):
    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer.lower() == 'зеленого' or answer.lower() == 'зеленая':
            cipher_note = get_object_or_404(Note, number=random_number)
            cipher_text = cipher_note.crypto_text.encode('ascii')
            key = str_key.encode('ascii')
            f = Fernet(key)
            text = f.decrypt(cipher_text)

            text = text.decode('utf-8')
            cipher_note.delete()
            return render(request, 'structure/decrypt.html', {'text': text})

    return redirect('question', random_number=random_number, str_key=str_key)
