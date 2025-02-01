from ProjectClass import bot, ProjectReplyKeyboard, MenuQuestionKeyboard, ListUserQuestionKeyboard, ShowAnswersOnQuestionKeyboard, SetRateAnswerKeyboard, ListUserAnswerKeyboard, ShowAnswerUserKeyboard, MenuQuestionShowKeyboard
from db import user_in_db, user_to_db, get_object, get_count_questions, answer_to_db, get_question_user_by_user_id, get_all_answer_by_question_id, user_rate, quest_to_db, delete_question_and_answer_by_q_id, get_answer_user_by_user_id, delete_answer_by_ans_id, get_all_question_without_question_user, is_valid_password
import math
AMMOUNT_QUESTION_IN_ONE_PAGE = 20


# python TGBot\telegram_bot.py


# если введена комманда start
@bot.message_handler(commands=['start'])
def welcome_func_bot(message):
    if not user_in_db('tg_id', message.from_user.id):# смотрим существует ли такой пользователь
        # если не существует, то запрашиваем логин
        
        bot.send_message(message.chat.id, 'Здравствуйте! Вы не зарегестрированы. Введите логин: ')
        bot.register_next_step_handler(message, set_login_func_bot)
    else:
        # если существует, то присылаем ему меню кнопок (каждый список обозначает одну строку)
        keyboard = ProjectReplyKeyboard(True, ['Задать вопрос', 'Список вопросов', 'Список моих вопросов', '/start', 'Мой рейтинг', 'Список моих ответов'], row_width=2)
        bot.send_message(message.chat.id, 'Здравствуйте!', reply_markup=keyboard)


# записываем логин, запрашиваем пароль
def set_login_func_bot(message):
    user_login = message.text
    bot.set_state(message.from_user.id, user_login)
    bot.send_message(message.chat.id, 'А теперь введите пароль (Должен быть не менее 6 символов, включать цифры и буквы в разных регистрах):')
    bot.register_next_step_handler(message, set_password_func_bot)


# записываем пароль, присылаем меню кнопок (каждый список обозначает одну строку)
def set_password_func_bot(message):
    user_password = message.text
    if is_valid_password(message.text):

        user_login = bot.get_state(message.from_user.id)

        user_to_db(user_login,user_password,message.from_user.id, message.chat.id)

        keyboard = ProjectReplyKeyboard(True, ['Задать вопрос', 'Список вопросов', 'Список моих вопросов', '/start', 'Мой рейтинг', 'Список моих ответов'], row_width=2)
        bot.send_message(message.chat.id, 'Вы зарегестрированы!', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Пароль не соответствует требованиям.')
        bot.register_next_step_handler(message, set_password_func_bot)


@bot.message_handler(func=lambda message: message.text == 'Список моих ответов')
def show_answers_user_func_bot(message):
    answers = get_answer_user_by_user_id(message.from_user.id)

    keyboard = ListUserAnswerKeyboard(list_answer=answers, row_width=2)
    bot.send_message(message.chat.id, 'Список ваших ответов:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.endswith('_clicked_item_list_user_answer'))
def show_answer_user_func_bot(call):
    id_answer = ListUserAnswerKeyboard.get_id_answer_by_call_text(call.data)
    answer = get_object('answer', 'ans_id', str(id_answer))
    question = get_object('quest', 'q_id', str(answer['q_id']))
    new_text = f'Вопрос:\n{question['q_text']}\nВаш ответ:\n{answer['ans_text']}'

    bot.set_state(user_id=call.from_user.id, state=str(id_answer))

    keyboard = ShowAnswerUserKeyboard(row_width=1)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_text, reply_markup=keyboard) 


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_list_user_answer')
def back_to_list_user_answer_func_bot(call):
    answers = get_answer_user_by_user_id(call.from_user.id)

    keyboard = ListUserAnswerKeyboard(list_answer=answers, row_width=2)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Список ваших ответов:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'delete_user_answer')
def delete_user_question_func_bot(call):
    answer_id = bot.get_state(user_id=call.from_user.id)
    delete_answer_by_ans_id(answer_id)
    answers = get_answer_user_by_user_id(call.from_user.id)

    keyboard = ListUserAnswerKeyboard(list_answer=answers, row_width=2)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Список ваших ответов:', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Список моих вопросов')
def show_question_user_func_bot(message):
    questions = get_question_user_by_user_id(message.from_user.id)
    keyboard = ListUserQuestionKeyboard(list_question=questions, row_width=2)

    bot.send_message(message.chat.id, 'Список ваших вопросов:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.endswith('_clicked_item_list_user_question'))
def show_all_answers_on_user_question_func_bot(call):
    id_question = ListUserQuestionKeyboard.get_id_question_by_call_text(call.data)
    question = get_object(table='quest', column='q_id', cell=f'{id_question}')
    answers = get_all_answer_by_question_id(id_question)
    new_text = f'Вопрос:\n{question['q_text']}\n\n' + '\n\n'.join([f'Ответ {i+1}:\n{answers[i][3]}' for i in range(len(answers))])

    bot.set_state(user_id=call.from_user.id, state=str(id_question))

    keyboard = ShowAnswersOnQuestionKeyboard(row_width=1)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_list_user_question')
def back_to_list_user_question_func_bot(call):
    questions = get_question_user_by_user_id(call.from_user.id)
    keyboard = ListUserQuestionKeyboard(list_question=questions, row_width=2)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Список ваших вопросов:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'delete_user_question')
def delete_user_question_func_bot(call):
    question_id = bot.get_state(user_id=call.from_user.id)
    delete_question_and_answer_by_q_id(question_id)
    questions = get_question_user_by_user_id(call.from_user.id)
    keyboard = ListUserQuestionKeyboard(list_question=questions, row_width=2)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Список ваших вопросов:', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Мой рейтинг')
def show_user_rate_func_bot(message):
    user = get_object('users', 'tg_id', str(message.from_user.id))
    bot.send_message(chat_id=message.chat.id, text=f'Ваш рейтинг: {user['rating']}')


# Тут начинается цепочка функций бота для вопросов
@bot.message_handler(func=lambda message: message.text == 'Задать вопрос')
def ask_question_func_bot(message):
    bot.send_message(chat_id=message.chat.id, text='Введите ваш вопрос:')
    bot.register_next_step_handler(message=message, callback=set_new_question_func_bot)


def set_new_question_func_bot(message):
    quest_to_db(message.from_user.id, message.text)
    bot.send_message(chat_id=message.chat.id, text='Вопрос записан!')


# Тут начинается цепочка функций бота для ответа на вопросы
@bot.message_handler(func=lambda message: message.text == 'Список вопросов')
def show_questions_func_bot(message):
    user_id = get_object('users', 'tg_id', str(message.from_user.id))['id']
    questions = get_all_question_without_question_user(user_id)
    keyboard = MenuQuestionKeyboard(list_question=questions[:AMMOUNT_QUESTION_IN_ONE_PAGE], row_width=2)

    bot.set_state(message.from_user.id, state='1')
    bot.send_message(chat_id=message.chat.id, text=f'Список вопросов. Страница 1/{math.ceil(len(questions) / AMMOUNT_QUESTION_IN_ONE_PAGE)}', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'prev_page_quest')
def list_question_prev_page_func_bot(call):
    current_page = int(bot.get_state(call.from_user.id))
    current_page -= 1

    if current_page > 0:
        bot.set_state(call.from_user.id, state=str(current_page))
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text='...')
        user_id = get_object('users', 'tg_id', str(call.from_user.id))['id']
        questions = get_all_question_without_question_user(user_id)
        keyboard = MenuQuestionKeyboard(list_question=questions[(current_page - 1) * AMMOUNT_QUESTION_IN_ONE_PAGE:(current_page - 1) * AMMOUNT_QUESTION_IN_ONE_PAGE + AMMOUNT_QUESTION_IN_ONE_PAGE],
                                    row_width=2, current_page=current_page)
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text=f'Список вопросов. Страница {current_page}/{math.ceil(len(questions) / AMMOUNT_QUESTION_IN_ONE_PAGE)}', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'next_page_quest')
def list_question_next_page_func_bot(call):
    current_page = int(bot.get_state(call.from_user.id))
    current_page += 1

    if current_page <= math.ceil(get_count_questions() / AMMOUNT_QUESTION_IN_ONE_PAGE):
        bot.set_state(call.from_user.id, state=str(current_page))
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text='...')
        user_id = get_object('users', 'tg_id', str(call.from_user.id))['id']
        questions = get_all_question_without_question_user(user_id)
        keyboard = MenuQuestionKeyboard(list_question=questions[(current_page - 1) * AMMOUNT_QUESTION_IN_ONE_PAGE:(current_page - 1) * AMMOUNT_QUESTION_IN_ONE_PAGE + AMMOUNT_QUESTION_IN_ONE_PAGE],
                                    row_width=2, current_page=current_page)
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text=f'Список вопросов. Страница {current_page}/{math.ceil(len(questions) / AMMOUNT_QUESTION_IN_ONE_PAGE)}', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.endswith('_clicked_item_list_question'))
def show_menu_question_func_bot(call):
    question_index = MenuQuestionKeyboard.get_index_quest_by_call_text(call.data)
    question = get_object('quest', 'q_id', str(question_index))

    keyboard = MenuQuestionShowKeyboard(question_index=question_index, row_width=1)
    bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                          text=f'Вопрос:\n{question['q_text']}', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_list_question')
def back_to_list_question_func_bot(call):
    user_id = get_object('users', 'tg_id', str(call.from_user.id))['id']
    questions = get_all_question_without_question_user(user_id)
    current_page = int(bot.get_state(call.from_user.id))
    keyboard = MenuQuestionKeyboard(list_question=questions[(current_page - 1) * AMMOUNT_QUESTION_IN_ONE_PAGE:(current_page - 1) * AMMOUNT_QUESTION_IN_ONE_PAGE + AMMOUNT_QUESTION_IN_ONE_PAGE],
                                    row_width=2, current_page=current_page)

    bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text=f'Список вопросов. Страница {current_page}/{math.ceil(len(questions) / AMMOUNT_QUESTION_IN_ONE_PAGE)}', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.endswith('_answer_quest'))
def list_question_func_bot(call):
    bot.set_state(call.from_user.id, call.data[:call.data.index('_')])
    bot.send_message(call.from_user.id, text='Введите ответ на вопрос:')
    bot.register_next_step_handler(call.message, get_answer_from_user_func_bot)


def get_answer_from_user_func_bot(message):
    index_quest = bot.get_state(message.from_user.id)

    question = get_object('quest', 'q_id', index_quest)
    answer_to_db(message.from_user.id, question['q_id'], message.text)

    user_id_question = question['user_id']
    user_tg_id_question = get_object('users', 'id', str(user_id_question))['tg_id']
    chat_id = user_tg_id_question
    new_text = f'На ваш вопрос пришёл ещё один ответ.\nВопрос:\n{question['q_text']}\nОтвет:\n{message.text}'
    bot.set_state(user_id=int(user_tg_id_question), state=str(message.from_user.id))

    keyboard = SetRateAnswerKeyboard(row_width=2)
    bot.send_message(chat_id=chat_id, text=new_text, reply_markup=keyboard)

    bot.send_message(chat_id=message.chat.id, text='Ответ записан. Спасибо!')


@bot.callback_query_handler(func=lambda call: call.data == 'add_rate_to_user')
def add_rate_to_user_func_bot(call):
    user_id_answer = int(bot.get_state(call.from_user.id))
    user_rate(user_id_answer, '+')
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id, text='Спасибо за оценку!')


@bot.callback_query_handler(func=lambda call: call.data == 'remove_rate_to_user')
def add_rate_to_user_func_bot(call):
    user_id_answer = int(bot.get_state(call.from_user.id))
    user_rate(user_id_answer, '-')
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id, text='Спасибо за оценку!')


if __name__ == '__main__':
    print('Bot start!')
    bot.infinity_polling()
