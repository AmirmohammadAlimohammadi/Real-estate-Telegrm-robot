import telebot
import requests
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup , InputMediaPhoto
channel_id = -1002832403172
import time
token = '<token>'
bot = telebot.TeleBot(token= token)
new_files = dict()
new_accounts = dict()
search = dict()
account_searchs = dict()
user_steps = dict()
last_message_time = dict()
scores = dict()
user_mute_until = dict()
def send_final_file(bot , cid , file):
    text = f"{translate['file kind']} : {translate[file['type']]} \n{translate['prop kind']} : {translate[file['property']]} \n{translate['region']} : {file['region']}\n \
    {translate['rooms']} : {file['rooms']} \n{translate['floor']} : {file['floor']} \n{translate['elevator']} : {translate[file['elevator']]} \n{translate['parking']} : {translate[file['parking']]}\n \
    {translate['storage']} : {translate[file['storage']]} \n{translate['area']} : {file['area']} \n{translate['year']} : {file['year']}\n \
    {translate['title']} : {file['title']}\n "
    return text 
file_keys = ['type' , 'property' , 'region' , 'floor' , 'rooms' , 'elevator' , 'parking' , 'storage' , 'explain' , 'title']
translate = {'house':'مسکونی','office':'تجاری یا اداری','Yes':'دارد' , 'No':'ندارد' , 'sale': 'فروش' ,
              'rent': 'اجاره' , 'انتخاب':'انتخاب' ,'file kind':'نوع فایل' , 'prop kind':'نوع ملک' ,
                'region':'منطقه' , 'rooms':'تعداد اتاق' , 'floor':'طبقه' , 'elevator':'آسانسور' , 
                'storage':'انباری','parking':'پارکینگ' , 'area': 'متراژ' , 'year':'سال ساخت' , 'title':'عنوان'}
def is_spam(user_id):
    if user_mute_until.get(user_id) == None:
        return
    return time.time() < user_mute_until.get(user_id) + last_message_time.get(user_id)
def answer_callback_query(**kwargs):
    try :
       kwargs['bot'].answer_callback_query(callback_query_id=kwargs.get('callback_query_id')  ,text =kwargs.get('text') , show_alert =  kwargs.get('show_alert')  )
    except Exception as e:
        return    
def edit_message_text(**kwargs):
    try:
        kwargs['bot'].edit_message_text(chat_id = kwargs['chat_id'] , message_id = kwargs['message_id'] , text = kwargs['text'] , reply_markup =kwargs.get('reply_markup') )
    except Exception as e:
        return
def send_message(**kwargs):
    if is_spam(kwargs.get('user_id')):
        return
    try:
        return kwargs['bot'].send_message(chat_id = kwargs['chat_id'] , text = kwargs['text'] , reply_markup =kwargs.get('reply_markup') )
    except Exception as e:
        return
def edit_message_reply_markup(**kwargs):
    try:
        kwargs['bot'].edit_message_reply_markup(chat_id = kwargs['chat_id'] , message_id = kwargs['message_id'] , reply_markup =kwargs.get('reply_markup') )
    except Exception as e:
        return
def send_photo(**kwargs):
    try:
        return kwargs['bot'].send_photo(chat_id = kwargs['chat_id'] , caption = kwargs.get('caption') , reply_markup =kwargs.get('reply_markup') )
    except Exception as e:
        return
def edit_message_media(**kwargs):
    try:
        return kwargs['bot'].edit_message_media(chat_id = kwargs['chat_id'],message_id = kwargs['message_id'], reply_markup =kwargs.get('reply_markup') ,media = kwargs.get('media'))
    except Exception as e:
        return
def delete_message(**kwargs):
    try : 
        return kwargs['bot'].delete_message(chat_id = kwargs['chat_id'],message_id = kwargs['message_id'])
    except Exception as e:
        return
#def create_serach_markup(search):

def create_file_markup(file):
    markup = InlineKeyboardMarkup()
    file_type = 'انتخاب'
    if file.get('type')!=None:
        file_type = file.get('type')
    markup.add(InlineKeyboardButton(text = f"{translate['file kind']} : {translate[file_type]}" , callback_data='file type'))
    prop_type = 'انتخاب'
    if file.get('property')!=None:
        prop_type = file.get('property')
    markup.add(InlineKeyboardButton(text = f"{translate['prop kind']} : {translate[prop_type]}" , callback_data='prop type'))
    
    region = 'انتخاب'
    if file.get('region')!=None:
        region = file.get('region')
    markup.add(InlineKeyboardButton(text =f"{translate['region']} : {region}" , callback_data='get region'))

    rooms = 'انتخاب'
    if file.get('rooms')!=None:
        rooms = file.get('rooms')
        if rooms == '5':
            rooms = '5 یا بیشتر'
    markup.add(InlineKeyboardButton(text = f"{translate['rooms']} : {rooms}", callback_data='get rooms'))

    floor = 'انتخاب'
    if file.get('floor')!=None:
        floor = file.get('floor')
        if floor == '31':
            floor = '31 یا بیشتر'
    markup.add(InlineKeyboardButton(text = f"{translate['floor']} : {floor}", callback_data='get floor'))

    elevator = 'انتخاب'
    if file.get('elevator')!=None:
        elevator = file.get('elevator')
    markup.add(InlineKeyboardButton(text =  f"{translate['elevator']} : {translate[elevator]}" , callback_data='elevator'))
    parking = 'انتخاب'
    if file.get('parking')!=None:
        parking = file.get('parking')
    markup.add(InlineKeyboardButton(text =  f"{translate['parking']} : {translate[parking]}" , callback_data='parking'))

    storage = 'انتخاب'
    if file.get('storage')!=None:
        storage = file.get('storage')
    markup.add(InlineKeyboardButton(text =  f"{translate['storage']} : {translate[storage]}", callback_data='storage'))
    
    area = 'انتخاب'
    if file.get('area')!=None:
        area = file.get('area')
    markup.add(InlineKeyboardButton(text= f"{translate['area']} : {area}" , callback_data='get area'))
    
    year = 'انتخاب'
    if file.get('year')!=None:
        year = file.get('year')
    markup.add(InlineKeyboardButton(text= f"{translate['year']} : {year}" , callback_data='get year') )
    
    
    title = 'انتخاب'
    if file.get('title')!=None:
        title = file.get('title')
    markup.add(InlineKeyboardButton(text = f"{translate['title']} : {title}", callback_data='title'))
    markup.add(InlineKeyboardButton(text = 'توضیحات' , callback_data='explain'))
    markup.add(InlineKeyboardButton(text = 'اضافه کردن عکس' , callback_data='add image'))
    markup.add(InlineKeyboardButton(text = 'ویرایش عکس ها عکس' , callback_data='edit image 0'))
    markup.add(InlineKeyboardButton(text = 'مرحله بعد'  , callback_data='next step'))
    return markup
@bot.callback_query_handler(func = lambda call : call.data == ' ')
def ignore(call):
    return
@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    user_id = message.from_user.id
    user_steps[user_id] = 'start'
    
    markup = ReplyKeyboardMarkup()
    markup.add('📃 ایجاد فایل جدید','🔍 جست و جوی فایل')
    markup.add('📂 فایل های من' , '🤖 تخمین قیمت خانه با هوش مصنوعی')
    markup.add('👤 اطلاعات کاربری','ثبت نام')
    markup.add('🏠 خانه')
    send_message(user_id = user_id,bot = bot, chat_id = cid , text = 'خوش آمدید', reply_markup=markup)
@bot.message_handler(func= lambda message : message.text == '🔍 جست و جوی فایل')
def start_search(message):
    cid = message.chat.id
    user_id = message.from_user.id
    search[user_id] = dict()
    #markup = make_markup_search(search[user_id])
    #bot.send_message(chat_id=cid , text='اطلاعات ملک مورد نظر خود را پر کنید' , reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == '📃 ایجاد فایل جدید')
def create_file(message):
    
    cid = message.chat.id
    user_id = message.from_user.id
    new_files[user_id] = dict()
    user_steps[user_id] = 'create first page'
    new_files[user_id]['images'] = []
    markup = create_file_markup(new_files[user_id])
    message_sent = send_message(user_id = user_id,bot = bot,chat_id=cid , text = 'اطلاعات زیر را تکمیل کنید' , reply_markup=markup)
@bot.callback_query_handler(func = lambda call : call.data == 'file type')
def get_file_type(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='فروش' , callback_data='sale'),
        InlineKeyboardButton(text='اجاره', callback_data='rent')
    )
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id=cid , message_id=mid , text='نوع فایل خود را انتخاب کنید' , reply_markup=markup)

@bot.callback_query_handler(func = lambda call : call.data == 'prop type')
def get_file_type(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='مسکونی' , callback_data='house'),
        InlineKeyboardButton(text='تجاری یا اداری', callback_data='office')
    )
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot,chat_id=cid , message_id=mid , text='نوع ملک خود را انتخاب کنید' , reply_markup=markup)
@bot.callback_query_handler(func = lambda call: call.data == 'get region')
def get_region(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    for i in range(1,23,2):
        markup.add(InlineKeyboardButton(text=f'{i}' , callback_data=f'choose region {i}'),InlineKeyboardButton(text=f'{i+1}' , callback_data=f'choose region {i+1}'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'منطقه ملک خود را انتخاب کنید' , reply_markup = markup)


@bot.callback_query_handler(func = lambda call: call.data == 'get area')
def area(call):
    mid = call.message.id
    cid = call.message.chat.id
    user_id = call.from_user.id
    user_steps[user_id] = f'get area {mid}'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'متراژ ملک خود را ارسال کنید' , reply_markup = markup)
@bot.callback_query_handler(func = lambda call: call.data == 'get year')
def get_year(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    for i in range(1404,1370 , -2):
        markup.add(InlineKeyboardButton(text=f'{i}' , callback_data=f'choose year {i}'),InlineKeyboardButton(text=f'{i-1}' , callback_data=f'choose year {i-1}'))
    markup.add(InlineKeyboardButton(text=f'1370 یا قبل' , callback_data=f'choose year 1370'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'سال ساخت ملک خود را انتخاب کنید' , reply_markup = markup)
@bot.callback_query_handler(func = lambda call: call.data == 'get rooms')
def get_rooms(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    for i in range(1,5):
        markup.add(InlineKeyboardButton(text=f'{i}' , callback_data=f'choose rooms {i}'))
    markup.add(InlineKeyboardButton(text='5 یا بیشتر '  , callback_data='choose rooms 5'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'تعداد اتاق های ملک خود را انتخاب کنید' , reply_markup = markup)
@bot.callback_query_handler(func = lambda call: call.data == 'get floor')
def get_rooms(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    for i in range(1,31,2):
        markup.add(InlineKeyboardButton(text=f'{i}' , callback_data=f'choose floor {i}'),InlineKeyboardButton(text=f'{i+1}' , callback_data=f'choose floor {i+1}'))
    markup.add(InlineKeyboardButton(text='31 یا بیشتر '  , callback_data='choose floor 31'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'تعداد اتاق های ملک خود را انتخاب کنید' , reply_markup = markup)
@bot.callback_query_handler(func= lambda call : call.data == 'elevator')
def get_elevator(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'بله' , callback_data='Yes elevator') , InlineKeyboardButton(text='خیر' , callback_data='No elevator'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'آیا ملک شما آسانسور دارد' , reply_markup = markup)
#@bot.message_handler(func = lambda message: user_steps.get(message.from_user.id) == 'create first page')
#def delete_messages(message):
    #cid= message.chat.id
    #mid = message.id
    #delete_message(bot = bot , chat_id=cid , message_id=mid)
@bot.callback_query_handler(func= lambda call : call.data == 'parking')
def get_parking(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'بله' , callback_data='Yes parking') , InlineKeyboardButton(text='خیر' , callback_data='No parking'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'آیا ملک شما پارکینگ دارد' , reply_markup = markup)
@bot.callback_query_handler(func= lambda call : call.data == 'storage')
def get_storage(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'بله' , callback_data='Yes storage') , InlineKeyboardButton(text='خیر' , callback_data='No storage'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'آیا ملک شما انباری دارد' , reply_markup = markup)
@bot.callback_query_handler(func = lambda call : call.data == 'first page')
def first_page(call):
    user_id = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    user_steps[user_id] = 'create first page'
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'اطلاعات زیر را تکمیل کنید', reply_markup = markup)
@bot.callback_query_handler(func = lambda call : call.data == 'rent' or call.data == 'sale')
def file_type(call):
    user_id = call.from_user.id
    new_files[user_id]['type'] = call.data
    cid = call.message.chat.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    user_steps[user_id] = 'create first page'
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'اطلاعات زیر را تکمیل کنید', reply_markup = markup)
@bot.callback_query_handler(func = lambda call : call.data == 'house' or call.data == 'office')
def file_type(call):
    user_id = call.from_user.id
    new_files[user_id]['property'] = call.data
    cid = call.message.chat.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    user_steps[user_id] = 'create first page'
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'اطلاعات زیر را تکمیل کنید', reply_markup = markup)
@bot.callback_query_handler(func = lambda call : call.data.startswith('choose'))
def get_num(call):
    user_id = call.from_user.id
    key , value = call.data.split()[-2],call.data.split()[-1]
    new_files[user_id][key] = value
    cid = call.message.chat.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    user_steps[user_id] = 'create first page'
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'اطلاعات زیر را تکمیل کنید', reply_markup = markup)
@bot.callback_query_handler(func = lambda call : call.data.startswith('Yes') or call.data.startswith('No'))
def get_num(call):
    user_id = call.from_user.id
    key , value = call.data.split()[1],call.data.split()[0]
    new_files[user_id][key] = value
    cid = call.message.chat.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    user_steps[user_id] = 'create first page'
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'اطلاعات زیر را تکمیل کنید', reply_markup = markup)
@bot.message_handler(func = lambda message:  user_steps.get(message.from_user.id)!= None and user_steps.get(message.from_user.id).startswith('get area'))
def get_area(message):
    cid = message.chat.id
    user_id = message.from_user.id
    mid = message.id
    new_files[user_id]['area'] = message.text
    
    delete_message(bot = bot , chat_id=cid , message_id=mid)
    markup = create_file_markup(new_files[user_id])
    
    edit_message_text(bot = bot , chat_id = cid , message_id = int(user_steps[user_id].split()[-1]) , text = 'اطلاعات زیر را تکمیل کنید' , reply_markup = markup)
    user_steps[user_id] = 'create first page'
@bot.callback_query_handler(func = lambda call : call.data == 'add image')
def get_image(call):
    mid = call.message.id
    cid = call.message.chat.id
    user_id = call.from_user.id
    
    user_steps[user_id] = f'get image {mid}'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'عکس ملک خود را ارسال کنید' , reply_markup = markup)

@bot.message_handler(content_types=['photo'] ,func = lambda message: user_steps.get(message.from_user.id).startswith('get image') )
def get_image(message):
    cid = message.chat.id
    user_id = message.from_user.id
    mid = message.id
    image_id = message.photo[-1].file_id
    image_info = bot.get_file(image_id)
    image_path = image_info.file_path
    image_url = f"https://api.telegram.org/file/bot{bot.token}/{image_path}"
    image = requests.get(image_url).content
    new_files[user_id]['images'].append(image)
    delete_message(bot = bot ,chat_id=cid , message_id=mid)
    markup = create_file_markup(new_files[user_id])
    
    edit_message_text(bot = bot , chat_id = cid , message_id = int(user_steps[user_id].split()[-1]) , text = 'اطلاعات زیر را تکمیل کنید' , reply_markup = markup)
    user_steps[user_id] = 'create first page'
   
@bot.callback_query_handler(func = lambda call : call.data == 'title')
def title(call):
    mid = call.message.id
    cid = call.message.chat.id
    user_id = call.from_user.id
    user_steps[user_id] = f'get title {mid}'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = ' بین 3 تا 7 کلمه)عنوان ملک خود را ارسال کنید)' , reply_markup = markup)
@bot.message_handler(func = lambda message:  user_steps.get(message.from_user.id)!= None and user_steps.get(message.from_user.id).startswith('get title'))
def get_title(message):
    cid = message.chat.id
    user_id = message.from_user.id
    mid = message.id
    new_files[user_id]['title'] = message.text
    
    delete_message(bot = bot , chat_id=cid , message_id=mid)
    markup = create_file_markup(new_files[user_id])
    
    edit_message_text(bot = bot , chat_id = cid , message_id = int(user_steps[user_id].split()[-1]) , text = 'اطلاعات زیر را تکمیل کنید' , reply_markup = markup)
    user_steps[user_id] = 'create first page'
@bot.callback_query_handler(func = lambda call : call.data == 'explain')
def explain(call):
    mid = call.message.id
    cid = call.message.chat.id
    user_id = call.from_user.id
    user_steps[user_id] = f'get explain {mid}'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    edit_message_text(bot = bot , chat_id = cid , message_id = mid , text = 'توضیحات ملک خود را ارسال کنید' , reply_markup = markup)
@bot.message_handler(func = lambda message:  user_steps.get(message.from_user.id)!= None and user_steps.get(message.from_user.id).startswith('get explain'))
def get_explain(message):
    
    cid = message.chat.id
    user_id = message.from_user.id
    mid = message.id
    new_files[user_id]['explain'] = message.text
    
    delete_message(bot = bot, chat_id=cid , message_id=mid)
    markup = create_file_markup(new_files[user_id])
    
    edit_message_text(bot = bot , chat_id = cid , message_id = int(user_steps[user_id].split()[-1]) , text = 'اطلاعات زیر را تکمیل کنید' , reply_markup = markup)
    user_steps[user_id] = 'create first page'
@bot.callback_query_handler(func = lambda call : call.data.startswith('edit image'))
def edit_image(call):
    cid = call.message.chat.id
    mid = call.message.id
    user_id = call.from_user.id
    if len (new_files[user_id].get('images')) == 0  or new_files[user_id].get('images') == None:
        answer_callback_query(
            bot = bot,
            callback_query_id=call.id,
            text="فایل شما هیچ عکسی ندارد",
            show_alert=True
        )
        return
    index = int(call.data.split()[-1])
    edit_message_reply_markup(bot = bot,chat_id=cid , message_id=mid , reply_markup=None)
    user_steps[user_id] = f'edit image {mid}'
    markup = InlineKeyboardMarkup()
   
    
    if index > 0 and index < len(new_files[user_id]['images'])-1:
        markup.add(InlineKeyboardButton(text = 'قبلی' , callback_data=f"edit image b {index - 1}"),InlineKeyboardButton(text = 'بعدی' , callback_data=f"edit image {index + 1}"))
    
    elif index < len(new_files[user_id]['images'])-1 :
        markup.add(InlineKeyboardButton(text = 'بعدی' , callback_data=f"edit image {index + 1}"))
    elif index > 0 :
        markup.add(InlineKeyboardButton(text = 'قبلی' , callback_data=f"edit image b {index - 1}"))
    markup.add(InlineKeyboardButton(text = 'حذف این عکس' , callback_data= f'delete image {index}'))
    markup.add(InlineKeyboardButton(text = 'صفحه قبل' , callback_data=f'back to first page {mid}'))
    if index == 0 and call.data.split()[-2]!= 'b':
        send_photo(bot = bot , chat_id=cid,photo = new_files[user_id]['images'][index] , reply_markup=markup)
    else:
        edit_message_media(bot = bot, message_id=call.message.id, chat_id=cid,media = InputMediaPhoto(new_files[user_id]['images'][index]) , reply_markup=markup)
@bot.callback_query_handler(func = lambda call : call.data.startswith('delete image'))
def delete_image(call):
    cid = call.message.chat.id
    user_id = call.from_user.id
    mid = user_steps[user_id].split()[-1]
    index =  int(call.data.split()[-1])
    if len(new_files[user_id]['images']) == 0 : 
        with open('noimage.png' , 'rb') as f:
            photo = f.read()
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text = 'صفحه قبل' , callback_data=f'back to first page {mid}'))
            edit_message_media(bot = bot , chat_id=cid , message_id=call.message.id,media= InputMediaPhoto(photo) ,reply_markup= markup)
        return
    markup = InlineKeyboardMarkup()
    if index >0:
        markup.add(InlineKeyboardButton(text = 'قبلی' , callback_data=f"edit image b {index - 1}"),InlineKeyboardButton(text = 'بعدی' , callback_data=f"edit image {index + 1}"))
    if index== 0 and index < len(new_files[user_id]['images']) -1:
        markup.add(InlineKeyboardButton(text = 'بعدی' , callback_data=f"edit image {index + 1}"))
    markup.add(InlineKeyboardButton(text = 'صفحه قبل' , callback_data=f'back to first page {mid}'))
    del new_files[user_id]['images'][index]
    if index > 0:
        edit_message_media(bot = bot,chat_id=cid , message_id=call.message.id,media=InputMediaPhoto(new_files[user_id]['images'][index ]) , reply_markup=markup)      
        return
    edit_message_media(bot = bot , chat_id=cid , message_id=call.message.id,media=InputMediaPhoto(new_files[user_id]['images'][index]) , reply_markup=markup) 
@bot.callback_query_handler(func = lambda call : call.data.startswith('back to first page'))
def back(call):
    cid = call.message.chat.id
    user_id = call.from_user.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    delete_message(bot = bot , chat_id=cid , message_id=mid)
    mid = int(user_steps[user_id].split()[-1])
    edit_message_reply_markup(bot = bot,chat_id=cid , message_id=mid , reply_markup=markup)
    return
@bot.callback_query_handler(func = lambda call : call.data == 'next step')
def get_price(call):
    cid = call.message.chat.id
    mid = call.message.id
    user_id = call.from_user.id
    for feature in file_keys:
        if new_files[user_id].get(feature) == None:
            answer_callback_query(
            bot = bot,
            callback_query_id=call.id,
            text="لطفا همه اطلاعات را تکمیل کنید",
            show_alert=True
            )
            return
        if len (new_files[user_id].get('images')) == 0 :
            answer_callback_query(
            bot = bot,
            callback_query_id=call.id,
            text="ارسال حداقل یک عکس الزامی است",
            show_alert=True
            )
            return
    bot.edit_message_reply_markup(chat_id=cid , message_id=mid , reply_markup=None)
  
    if new_files[user_id]['type'] == 'sale':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data= 'first page'))
        bot.send_message(chat_id=cid , text = 'قیمت مد نظر برای ملک خود را ارسال کنید' , reply_markup=markup)
        user_steps[user_id] = 'getting sell price'
        return
    if new_files[user_id]['type'] == 'rent':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data= 'first page'))
        bot.send_message(chat_id=cid , text = 'ودیعه مد نظر برای ملک خود را ارسال کنید' , reply_markup=markup)
        user_steps[user_id] = 'getting deposit'
        return
@bot.message_handler(func = lambda message : user_steps.get(message.from_user.id) == 'getting deposit')
def get_depos(message):
    print('here')
    user_id = message.from_user.id
    cid = message.chat.id
    new_files[user_id]['deposit'] = message.text
    user_steps[user_id] = 'getting rent'
    print('ok')
    bot.send_message(chat_id=cid , text = 'اجاره مد نظر خود را برای ملک خود ارسال کنید')
    print('k')
    return
@bot.message_handler(func = lambda message : user_steps.get(message.from_user.id) == 'getting rent')
def get_rent(message):
    user_id = message.from_user.id
    cid = message.chat.id
    new_files[user_id]['rent'] = message.text
    text = send_final_file(bot , cid , new_files[user_id])
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='تایید و ایجاد فایل' , callback_data='aproved file'))
    markup.add(InlineKeyboardButton(text='ویرایش اطلاعات ملک' , callback_data='first page'))
    markup.add(InlineKeyboardButton(text = 'ویرایش قیمت ملک' , callback_data='next step'))
    media = [InputMediaPhoto(image ) for image in new_files[user_id]['images']]
    bot.send_media_group(chat_id=cid ,media=media)
    bot.send_message(chat_id=cid , text = text , reply_markup=markup)
    print(text)
    user_steps[user_id] = 'review file'
    return
@bot.message_handler(func = lambda message : user_steps.get(message.from_user.id) == 'getting sell price')
def get_price(message):
    user_id = message.from_user.id
    cid = message.chat.id
    new_files[user_id]['price'] = message.text
    text = send_final_file(bot , cid , new_files[user_id])
    print(text)
    bot.send_message(text = text , chat_id=cid)
    user_steps[user_id] = 'review file'
@bot.message_handler(func  = lambda message: True)
def save_last_message_time(message):
    #print(message)
    time_treshold = 3
    user_id = message.from_user.id
    timestamp = message.date
    if last_message_time.get(user_id) == None:
        last_message_time[user_id] = timestamp
        scores[user_id] = 0
        user_mute_until[user_id] = 0
        return
    #print(user_mute_until[user_id])
    delta = timestamp - last_message_time[user_id]
    if delta <= 3:
        scores[user_id] +=1
        x = 1
        if scores[user_id] < 3:
            x = 0
        user_mute_until[user_id] +=  x* 2**(scores[user_id] - 3) * 60
    elif delta >= 7:
        scores[user_id] = max(scores[user_id]- delta // 7 , 0)

bot.infinity_polling()
