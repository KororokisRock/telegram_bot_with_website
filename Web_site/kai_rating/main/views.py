from django.shortcuts import render
from . import  db

# Create your views here.
def home(request):
    data = db.all_db()
    req = request
    is_admin = False
    is_log=False
    massege = ''
    if req.method == 'POST':
        is_log=False
        is_admin = False
        q_count=0
        a_count=0
        name = 'Anonymus'
        rating = 0
        place = 0
        tup=[]
        q_tab=[]
        u_tab=[]
        req=req.POST
        if 'op' in req:
            com = req['op'].split()
            name = db.get_object(data,'users','name',com[-1])['name']
            password = db.get_object(data,'users','name',com[-1])['password']
            if com[1]=='del':
                db.delete(com[2],com[3],com[0])
            elif com[1]=='rate':
                db.user_rate(com[0],com[2])
            elif com[1]=='adm':
                db.user_adm(com[0])
        else:
            name = req['username']
            password = req['password']
            
        if name == 'anon':
            return render(request, 'main/awesom_1.html')
        if db.user_in_db('name',name):
            if len(password)>20:
                is_pass = password == db.get_object(data,'users','name',name)['password']
            else: 
                is_pass = db.check_password(db.get_object(data,'users','name',name)['password'],password)
            if is_pass:
                is_log=True
                is_admin = db.get_object(data,'users','name',name)['is_admin']
                user_id = db.get_object(data,'users','name',name)['id']
                rating = db.get_object(data,'users','name',name)['rating']
                name = name
                q_count=db.count_by_id('quest','user_id',user_id)
                a_count=db.count_by_id('answer','user_id',user_id)


                for c,i in enumerate(db.sort_table('users',-1)[::-1]):
                    if i[2]==name:
                        place = c+1

                for i in db.table_by_id('answer','user_id',user_id):
                    quest = db.get_object(data,'quest','q_id',i[2])
                    tup.append(tuple([quest['q_text'],i[-1],i[0]]))
                
                    

                
            else:
                massege = 'Неверный пароль.'
                
        else:
            massege = 'Пользователь с таким логином не зарегистрирован.'
        if is_admin:

            q_tab = [(i[2],db.get_object(data,'users','id',db.get_object(data,'quest','q_id',i[0])['user_id'])['name'],i[0]) for i in db.table('quest')]
            u_tab = db.table('users')
            
        context = {'mas': massege,
                   'is_admin': is_admin,
                    'is_log': is_log,
                    'name':name,
                    'q_count':q_count,
                    'a_count':a_count,
                    'rating':rating,
                    'place':place,
                    'tup':tup,
                    'q_tab':q_tab,
                    'u_tab':u_tab,
                    'password':password

                    }
        return render(request, 'main/awesom_1.html',context)
        
    

    else:
        return render(request, 'main/awesom_1.html')