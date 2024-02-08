from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from . models import Category, Flashcard, Challenge, FlashcardChallenge
from django.contrib.messages import constants
from django.contrib import messages

def create_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')
    if request.method == 'GET':
        categories = Category.objects.all()
        difficulties = Flashcard.DIFFICULTY_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user)
        
        category_filter = request.GET.get('category')
        difficulty_filter = request.GET.get('difficulty')

        if category_filter:
            flashcards = flashcards.filter(category__id = category_filter)

        if difficulty_filter:
            flashcards = flashcards.filter(difficulty = difficulty_filter )

        return render(request, 'create_flashcard.html', {'categories': categories, 'difficulties': difficulties, 'flashcards': flashcards})
    
    elif request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty')

        if len(question.strip()) == 0 or len(answer.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha os campos de pergunta e resposta')
            return redirect('/flashcards/create_flashcard')

        flashcard = Flashcard(
            user = request.user,
            question = question,
            answer = answer,
            category_id = category,
            difficulty = difficulty,
        )

        flashcard.save()

        messages.add_message(request, constants.SUCCESS, 'Flashcard criado com sucesso')
        return redirect('/flashcards/create_flashcard')

def delete_flashcard(request, id):

    if not request.user.is_authenticated:
        return redirect('/users/login')
    
    flashcard = Flashcard.objects.get(id=id)
    if(request.user == flashcard.user):
        flashcard.delete()
        messages.add_message(request, constants.SUCCESS, 'Flashcard deletada com sucesso')
        return redirect('/flashcards/create_flashcard/')
    else:
        messages.add_message(request, constants.ERROR, 'Acesso negado para deletar o flashcard')
        return redirect('/flashcards/create_flashcard/')
    
def create_challenge(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')
    
    if request.method == 'GET':
        categories = Category.objects.all()
        difficulties = Flashcard.DIFFICULTY_CHOICES
        return render(request, 'create_challenge.html', {'categories': categories, 'difficulties': difficulties})
    
    elif request.method == 'POST':
        title = request.POST.get('title')
        categories = request.POST.get('category')
        difficulty = request.POST.get('difficulty')
        number_questions = request.POST.get('number_questions')

        if len(title.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Escolha um título para o desafio')
            return redirect('/flashcards/create_challenge/')
        if categories is None:
            messages.add_message(request, constants.ERROR, 'Escolha ao menos uma categoria')
            return redirect('/flashcards/create_challenge/')
        if not number_questions or int(number_questions) <= 0:
            messages.add_message(request, constants.ERROR, 'Escolha um número de perguntas maior do que 0')
            return redirect('/flashcards/create_challenge/')

        flashcards = Flashcard.objects.filter(user=request.user).filter(difficulty=difficulty).filter(category_id__in=categories).order_by('?')
        
        if flashcards.count() < int(number_questions):
            messages.add_message(request, constants.ERROR, 'Nessa categoria e dificuldade há ' + str(flashcards.count()) + ' flascard(s) disponível(is)')
            return redirect('/flashcards/create_challenge/')

        challenge = Challenge(
            user = request.user,
            title = title,
            number_questions = number_questions,
            difficulty = difficulty
        )
        challenge.save()
        challenge.category.add(*categories)
        
        flashcards = flashcards[: int(number_questions)]

        for flashcard in flashcards:
            flashcard_challenge = FlashcardChallenge(
                flashcard = flashcard,
            )
            flashcard_challenge.save()
            challenge.flashcards.add(flashcard_challenge)

        challenge.save()

        return redirect('/flashcards/index_challenges/')
    
def index_challenges(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')

    challenges = Challenge.objects.filter(user=request.user)
    categories = Category.objects.all()
    difficulties = Flashcard.DIFFICULTY_CHOICES

    category_filter = request.GET.get('category')
    difficulty_filter = request.GET.get('difficulty')

    if category_filter:
        challenges = challenges.filter(category__id = category_filter)

    if difficulty_filter:
        challenges = challenges.filter(difficulty = difficulty_filter )

    # TODO: desenvolver status

    return render(request, 'index_challenges.html', {'challenges': challenges,'categories': categories, 'difficulties': difficulties})

def challenge(request, id):
    if not request.user.is_authenticated:
        return redirect('/users/login')

    challenge = Challenge.objects.get(id=id)
    if not challenge.user == request.user:
        raise Http404()

    if request.method == 'GET':
        successes = challenge.flashcards.filter(answered=True).filter(flashcard_success=True).count()
        errors  = challenge.flashcards.filter(answered=True).filter(flashcard_success=False).count()
        missing = challenge.flashcards.filter(answered=False).count()

        return render(request,'challenge.html', {'challenge': challenge, 'successes': successes, 'errors': errors, 'missing': missing})
    
def answer_flashcard(request, id):
    if not request.user.is_authenticated:
        return redirect('/users/login')

    flashcard_challenge = FlashcardChallenge.objects.get(id=id)
    flashcard_success = request.GET.get('flashcard_success')
    challenge_id = request.GET.get('challenge_id')

    if not flashcard_challenge.flashcard.user == request.user:
        raise Http404()

    flashcard_challenge.answered = True
    flashcard_challenge.flashcard_success = True if flashcard_success == '1' else False
    flashcard_challenge.save()
    return redirect(f'/flashcards/challenge/{challenge_id}/')

def report(request, id):
    challenge = Challenge.objects.get(id=id)

    successes = challenge.flashcards.filter(flashcard_success=True).count()
    errors = challenge.flashcards.filter(flashcard_success=False).count()

    data = [successes, errors]

    categories = challenge.category.all()
    category_names = [category.name for category in categories]

    data2 = []
    for category in categories:
        data2.append(challenge.flashcards.filter(flashcard__category=category).filter(flashcard_success=True).count())

    return render(request, 'report.html', {'challenge': challenge, 'data': data, 'categories': category_names, 'data2': data2})