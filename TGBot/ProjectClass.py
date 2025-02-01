import telebot
import telebot.storage
import telebot.storage.base_storage
from config import TOKEN


# обёртка бота библиотеки telebot в наш класс
class ProjectBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)


# обёртка меню кнопок под полем для ввода сообщений в наш класс
class ProjectReplyKeyboard(telebot.types.ReplyKeyboardMarkup):
    def __init__(self, resize_keyboard, keyboard, row_width=3):
        # запрашиваем будет ли телеграм менять размер кнопок для лучшего визуала
        super().__init__(resize_keyboard)
        # задаётся кол-во кнопок в поле и список кнопок
        for i in range(len(keyboard) // row_width):
            if i == len(keyboard) // row_width - 1:
                self.add(*keyboard[i*row_width :])
            else:
                self.add(*keyboard[i*row_width : i*row_width+row_width])


    # чтобы удалить клавиатуру вызываем эту функцию и результат передаём в reply_markup функции send_message
    def delete_keyboard_markup(self):
        return telebot.types.ReplyKeyboardRemove()


class ProjectInlineKeyboard(telebot.types.InlineKeyboardMarkup):
    def __init__(self, keyboard=None, row_width=3):
        super().__init__(keyboard=keyboard, row_width=row_width)
        super().__init__()
        # задаётся кол-во кнопок в поле и список кнопок
        l = []
        for i in range(len(keyboard)):
            l.append(telebot.types.InlineKeyboardButton(text=keyboard[i]['text'], callback_data=keyboard[i]['callback_data']))
            if len(l) >= row_width or i == len(keyboard) - 1:
                self.add(*l)
                l.clear()


# class MenuPageListQuestion(ProjectInlineKeyboard):
#     def __init__(self, list_question=None, row_width=3, current_page=1, ammount_question_in_one_page=20):
#         buttons = [{'text': 'Back', 'callback_data': 'back_page_list_question'},
#                {'text': 'Next', 'callback_data': 'next_page_list_question'}]
#         buttons += [{'text': list_question[i].text[:7] + '...', 'callback_data': f'{i}_clicked_element_list_question'}
#                 for i in range(current_page * ammount_question_in_one_page,
#                                current_page * ammount_question_in_one_page + ammount_question_in_one_page)
#                                if i <= len(list_question) - 1]
#         super().__init__(keyboard=buttons, row_width=row_width)
    
#     def give_current_page_by_message_text(message_text=''):
#         return int(message_text[message_text.index('Страница') + 9 : message_text.index('/')]) - 1
    
#     def give_index_question(callback_data_text=''):
#         return int(callback_data_text[:callback_data_text.index('_')])
    
#     def give_current_page_by_index_question(index_question=0, ammount_question_in_one_page=20):
#         return index_question // ammount_question_in_one_page


# class QuestionInlineKeyboard(ProjectInlineKeyboard):
#     def __init__(self, row_width=3):
#         buttons = [{'text': 'Back to list', 'callback_data': 'back_to_list_question'},
#                    {'text': '1', 'callback_data': '1'}]
#         super().__init__(keyboard=buttons, row_width=row_width)
    
#     def give_index_question_by_message_text(message_text=''):
#         return int(message_text[message_text.index('№') + 1:message_text.index(':')]) - 1


class MenuQuestionKeyboard(ProjectInlineKeyboard):
    def __init__(self, list_question=[], current_page=1, row_width=3, ammount_in_page=20):
        buttons = [{'text': 'Назад', 'callback_data': 'prev_page_quest'},
                   {'text': 'Вперёд', 'callback_data': 'next_page_quest'}] + [
                    {'text': f'{(current_page - 1) * ammount_in_page + i + 1} - {list_question[i][2][:5]}..',
                     'callback_data': f'{list_question[i][0]}_clicked_item_list_question'} for i in range(len(list_question))]
        super().__init__(keyboard=buttons, row_width=row_width)

    def get_index_quest_by_call_text(call_text):
        return int(call_text[:call_text.index('_')])
    
    def delete_keyboard():
        return telebot.types.ReplyKeyboardRemove()


class MenuQuestionShowKeyboard(ProjectInlineKeyboard):
    def __init__(self,question_index=None, row_width=3):
        buttons = [{'text': 'Ответить на вопрос', 'callback_data': f'{question_index}_answer_quest'},
                   {'text': 'Вернуться к списку', 'callback_data': 'back_to_list_question'}]
        super().__init__(keyboard=buttons, row_width=row_width)


class ListUserQuestionKeyboard(ProjectInlineKeyboard):
    def __init__(self, list_question=[], row_width=3):
        buttons = [{'text': f'{i+1} - {list_question[i][2][:5]}..', 'callback_data': f'{list_question[i][0]}_clicked_item_list_user_question'} for i in range(len(list_question))]
        super().__init__(keyboard=buttons, row_width=row_width)
    
    def get_id_question_by_call_text(call_text):
        return int(call_text[:call_text.index('_')])


class ShowAnswersOnQuestionKeyboard(ProjectInlineKeyboard):
    def __init__(self, row_width=3):
        buttons = [{'text': 'Вернуться к списку', 'callback_data': 'back_to_list_user_question'},
                   {'text': 'Удалить вопрос', 'callback_data': 'delete_user_question'}]
        super().__init__(keyboard=buttons, row_width=row_width)


class SetRateAnswerKeyboard(ProjectInlineKeyboard):
    def __init__(self, row_width=3):
        buttons = [{'text': '+', 'callback_data': 'add_rate_to_user'},
                   {'text': '-', 'callback_data': 'remove_rate_to_user'}]
        super().__init__(keyboard=buttons, row_width=row_width)


class ListUserAnswerKeyboard(ProjectInlineKeyboard):
    def __init__(self, list_answer=[], row_width=3):
        buttons = [{'text': f'{i+1} - {list_answer[i][3][:5]}..', 'callback_data': f'{list_answer[i][0]}_clicked_item_list_user_answer'} for i in range(len(list_answer))]
        super().__init__(keyboard=buttons, row_width=row_width)
    
    def get_id_answer_by_call_text(call_text):
        return int(call_text[:call_text.index('_')])


class ShowAnswerUserKeyboard(ProjectInlineKeyboard):
    def __init__(self, row_width=3):
        buttons = [{'text': 'Удалить ответ', 'callback_data': 'delete_user_answer'},
                   {'text': 'Вернуться к списку', 'callback_data': 'back_to_list_user_answer'}]
        super().__init__(keyboard=buttons, row_width=row_width)


class Question:
    def __init__(self, question_id, user_id, text, rate):
        self.question_id = question_id
        self.text = text
        self.user_id = user_id
        self.rate = rate


def remake_tuple_to_question(list_question):
    return [Question(el[0], el[1], el[2], el[3]) for el in list_question]


bot = ProjectBot(TOKEN)