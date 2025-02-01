from mysql.connector import connect, Error
from config import host,user_name,passw,port
import uuid
import hashlib

upper_set = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
lower_set = set('abcdefghijklmnopqrstuvwxyz')
digit_set = set('1234567890')



#проверка пароля на надежность
def is_valid_password(password):
    
    # Длина строки пароля не менее шести символов.
    if len(password) < 6:
        return False

    password_set = set(password)

    # Содержит хотя бы одну букву в верхнем регистре.
    # Содержит хотя бы одну букву в нижнем регистре.
    # Содержит хотя бы одну цифру.
    # Функция is_valid_password должна вернуть True,
    # если переданный в качестве параметра пароль отвечает требованиям надежности.
    return \
        password_set & upper_set and \
        password_set & lower_set and \
        password_set & digit_set








#создание и хэширование пароля
def hash_password(password):    
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt  
#проверка пароля
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest() 
#подключение к бд, выдаёт False если подключение провалено
def conn():
    try:
        connection = connect(host=host, 
                             user=user_name, 
                             password=passw, 
                             database=user_name, 
                             port=port,
                             charset='utf8',
                             use_unicode = True)
        return connection
    except Error as e:
        print(e)
        return False

def delete_question_and_answer_by_q_id(q_id):
    cnct = conn()
    if cnct:
        command = f'''
            DELETE FROM answer WHERE q_id = {q_id}
        '''
        with cnct.cursor() as cur:
            cur.execute(command)
            cnct.commit()
        command = f'''
            DELETE FROM quest WHERE q_id = {q_id}
            '''
        with cnct.cursor() as cur:
            cur.execute(command)
            cnct.commit()

def delete_answer_by_ans_id(ans_id):
    cnct = conn()
    if cnct:
        command = f'''
            DELETE FROM answer WHERE ans_id = {ans_id}
        '''
        with cnct.cursor() as cur:
            cur.execute(command)
            cnct.commit()

def get_question_user_by_user_id(user_tg_id):
    cnct = conn()
    if cnct:
        command = f'''
            SELECT * FROM users WHERE tg_id = {user_tg_id}
            '''
        with cnct.cursor() as cur:
            cur.execute(command)
            res = cur.fetchall()
        command = f'''
            SELECT * FROM quest WHERE user_id = {res[0][0]}
            '''
        with cnct.cursor() as cur:
            cur.execute(command)
            return cur.fetchall()

def get_answer_user_by_user_id(user_tg_id):
    cnct = conn()
    if cnct:
        command = f'''
            SELECT * FROM users WHERE tg_id = {user_tg_id}
            '''
        with cnct.cursor() as cur:
            cur.execute(command)
            res = cur.fetchall()[0][0]
        command = f'''
            SELECT * FROM answer WHERE user_id = {res}
            '''
        with cnct.cursor() as cur:
            cur.execute(command)
            res = cur.fetchall()
        return res

def get_all_answer_by_question_id(quest_id):
    cnct = conn()
    if cnct:
        command = f'''
            SELECT * FROM answer WHERE q_id = {quest_id}
            '''
        with cnct.cursor() as cur:
            cur.execute(command)
            return cur.fetchall()

#проверка: есть ли юзер в бд
def user_in_db(type,cell):
    cnct = conn()
    if cnct:
        command = f'''
            SELECT * FROM users WHERE {type} = "{cell}"
            '''
        with cnct.cursor() as cur:
            cur.execute(command)
            res = cur.fetchall()
            if len(res) > 0:
                return True
            else: 
                return False
#внесение в бд нового юзера если юзер с таким ником уже есть возвращает False 
def user_to_db(user,password,tg_id,chat_id):
    if user_in_db('name',user):
        return False
    cnct = conn()
    if cnct:
        command = f'''
        INSERT INTO users(tg_id,name,password,is_admin)
        VALUE({tg_id},'{user}','{hash_password(password)}',false)
        '''
        with cnct.cursor() as cur:
            cur.execute(command)
            cnct.commit()
#внесение в бд нового вопроса
def quest_to_db(tg_id,quest):
    cnct = conn()
    if cnct:
        
        with cnct.cursor() as cur:
            command = f'''
            SELECT id FROM users WHERE tg_id = '{tg_id}'
            '''
            cur.execute(command)
            res = cur.fetchall()
            command = f'''
            INSERT INTO quest(user_id,q_text)
            VALUE({res[0][0]},'{quest}')
            '''
            cur.execute(command)
            cnct.commit()
#внесение в бд нового ответа
def answer_to_db(tg_id,quest_id, ans_text):
    cnct = conn()
    if cnct:
        
        with cnct.cursor() as cur:
            command = f'''
            SELECT id FROM users WHERE tg_id = '{tg_id}'
            '''
            cur.execute(command)
            res = cur.fetchall()
            command = f'''
            INSERT INTO answer(user_id,q_id,ans_text)
            VALUE({res[0][0]}, {quest_id}, '{ans_text}')
            '''
            cur.execute(command)
            cnct.commit()
#добавляет или убавляет рейтинг вопроса, rate либо '+' либо '-'
def quest_rate(q_text,rate):
    cnct = conn()
    if cnct:
        
        with cnct.cursor() as cur:
            command = f'''
            update quest set rating = rating {rate} 1 where q_text = '{q_text}'
            '''
            cur.execute(command)
            cnct.commit()
#добавляет или убавляет рейтинг юзеру, rate либо '+' либо '-'
def user_rate(tg_id,rate):
    cnct = conn()
    if cnct:
        
        with cnct.cursor() as cur:
            command = f'''
            update users set rating = rating {rate} 1 where tg_id = '{tg_id}'
            '''
            cur.execute(command)
            cnct.commit()

'''
шпакргалка по таблицам:
название          названия колонок
таблицы                  |
  |                      |
 \|/                    \|/
users(     id,   tg_id,   name, password, is_admin, rating)
quest(   q_id, user_id, q_text, rating)
answer(ans_id, user_id,   q_id, ans_text)
'''

#строки в бд в виде получение словаря
def get_object(table, column, cell):
    cnct = conn()
    if cnct:
        with cnct.cursor() as cur:
            if cell.isnumeric():
                command = f'''
                SELECT * FROM {table} WHERE {column} = {cell}
                '''
            else:
                command = f'''
                SELECT * FROM {table} WHERE {column} = '{cell}'
                '''
            cur.execute(command)
            res  = cur.fetchall()
            if len(res) == 0:
                return print('нет такой ячейки')
            
            res1 = [i for i in res[0]]
            command =f'''
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table}';
                '''
            cur.execute(command)
            res2 = [i[0] for i in cur.fetchall()]
            return dict(zip(res2,res1))


def get_all_question():
    cnct = conn()
    if cnct:
        with cnct.cursor() as cur:
            command = f'''
                    SELECT * FROM quest'''
            cur.execute(command)
            res = cur.fetchall()
            return res

def get_all_question_without_question_user(user_id):
    cnct = conn()
    if cnct:
        with cnct.cursor() as cur:
            command = f'''
                    SELECT * FROM quest WHERE user_id != {user_id}'''
            cur.execute(command)
            res = cur.fetchall()
            return res

def get_count_questions():
    cnct = conn()
    if cnct:
        with cnct.cursor() as cur:
            command = f'''
                    SELECT COUNT(q_id) FROM quest'''
            cur.execute(command)
            res = cur.fetchall()
            return res[0][0]

def get_first_quest():
    cnct = conn()
    if cnct:
        with cnct.cursor() as cur:
            command = f'''
                    SELECT * FROM quest'''
            cur.execute(command)
            res = cur.fetchall()
            return res

def add_new_quest():
    cnct = conn()
    if cnct:
        with cnct.cursor() as cur:
            for i in range(60):
                q_text = f'Question text фдфдфдф - {i}, nkzsjvnlkfzdsvnbjlkzdsbblkjz'
                command = f"INSERT INTO quest(user_id, q_text, rating) VALUE ({1}, '{q_text}', {0})"
                cur.execute(command)
                cnct.commit()

def delete_all_quest():
    cnct = conn()
    if cnct:
        with cnct.cursor() as cur:
            command = f"DELETE FROM quest"
            cur.execute(command)
            cnct.commit()

def get_all_answer():
    cnct = conn()
    if cnct:
        with cnct.cursor() as cur:
            command = f"SELECT * FROM answer"
            cur.execute(command)
            print(cur.fetchall())

def get_all_users():
    cnct = conn()
    if cnct:
        with cnct.cursor() as cur:
            command = f"SELECT * FROM users"
            cur.execute(command)
            print(cur.fetchall())

def command_sql():
    cnct = conn()
    if cnct:
        with cnct.cursor() as cur:
            command = f"SELECT * FROM users"
            cur.execute(command)
            res = cur.fetchall()

            for el in res:
                command = f"UPDATE users SET chat_id = {el[1]} WHERE tg_id = {el[1]}"
                cur.execute(command)
                cnct.commit()

if __name__ == '__main__':
    # add_new_quest()
    # command_sql()
    print(get_object('users', 'tg_id', '1846860836'))
    print(get_all_users())
    print(get_all_question())
    # =======
    '''cnct = conn()
    with cnct.cursor() as cur:
        cur.execute('select *  from users;')
        print(cur.fetchall())'''
    # >>>>>>> 420f31fcb11c024f8af8d26dfe3ae50a0f32c5f4:db.py