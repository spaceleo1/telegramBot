from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from datetime import datetime
import logging

from user import User

users = {}


def check_user_clear(id: int, update: Update, context: CallbackContext) -> None:
    if users[id].starting_game:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Игра отменена")
        users[id].starting_game = False


def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in users:
        users[user_id] = User(user_id)
    check_user_clear(user_id, update, context)

    context.bot.send_message(chat_id=update.effective_chat.id, text=
    """Привет, со мной можно сыграть в игру BlackJack!)
Начать игру /game
Узнать баланс /balance
Пополнить баланс /cashup
    """)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")


def game(update, context):
    id = update.message.from_user.id
    check_user_clear(id, update, context)

    context.bot.send_message(chat_id=update.effective_chat.id, text=
    """
На какую сумму будем играть?
Введите натуральное число от 1 до {} (ровно столько у вас на балансе), также вы можете отправить любое слово, и игра будет отменена
""".format(str(users[id].balance))
                             )
    users[id].starting_game = True


def balance(update, context):
    id = update.message.from_user.id

    check_user_clear(id, update, context)

    context.bot.send_message(chat_id=update.effective_chat.id, text=
    "Ваш баланс: " + str(users[id].balance))


def check_message(update, context):
    id = update.message.from_user.id
    if id not in users:
        return
    if users[id].starting_game:

        users[id].starting_game = False
        ch = True
        try:
            num = int(update.message.text)
            if 1 <= num <= users[id].balance:
                keyboard = [
                    [
                        InlineKeyboardButton("Начать игру!", callback_data='1')
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id=update.effective_chat.id, text=
                "Итак, мы готовы стартовать, игра будет проводиться по правилам BlackJack на сумму " +
                str(num) +
                " как только вы нажмете на кнопку, мы спишем данную сумму с вашего баланса, и начнем раздачу карт!",
                                         reply_markup=reply_markup)
            else:
                ch = False
        except ValueError:
            ch = False

        if ch == False:
            context.bot.send_message(chat_id=update.effective_chat.id, text=
            "Игра отменена")


def cashup(update: Update, context: CallbackContext) -> None:
    id = update.message.from_user.id

    check_user_clear(id, update, context)

    nw = datetime.now()
    total = (nw - users[id].time_cashup).total_seconds()
    cnst_sec = 300
    if (total >= cnst_sec):
        users[id].balance += 15
        users[id].time_cashup = nw
        context.bot.send_message(chat_id=update.effective_chat.id, text=
        "Баланс пополнен на 15")
    else:
        total = cnst_sec - total
        context.bot.send_message(chat_id=update.effective_chat.id, text=
        f"Баланс можно пополнять раз в 5 минут, подожди еще *{int(total/60)}* мин *{int(total)%60}* сек", parse_mode='Markdown')


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    updater = Updater(token='1862665566:AAGTBM-OTP9bGSpjlMY6nEtSzhs0TzCJsuU')
    dispatcher = updater.dispatcher

    message_handler = MessageHandler(Filters.text & (~Filters.command), check_message)
    dispatcher.add_handler(message_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    game_handler = CommandHandler('game', game)
    dispatcher.add_handler(game_handler)

    balance_handler = CommandHandler('balance', balance)
    dispatcher.add_handler(balance_handler)

    cashup_handler = CommandHandler('cashup', cashup)
    dispatcher.add_handler(cashup_handler)

    button_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(button_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()

'''
@twentyOne_Gamebot\
#еще, какой порядок выполнения, 
если сейчас уже начался какой-то процесс, 
а пользователь написал старт, что произойдет

вот, что я хочу
игра началась, как ее не прерывать
а
нихуя
я придумал
правда
хз
таймер надо будет ставить, видимо
ооо
шик
короче, мы будем изменять сообщения
смотри
он кидает /game
и мы отправляем начало игры с вопросом, на сколько мы играем
если он отправляет в ответ не число, то мы просто завершаемся
если число, то кнопка начать игру
и с счета списываются деньги
все
дальше начинается игра
по ходам
нихера)
мы это за 2 часа напишем?
погнали
игра 21
просто вытягиваешь карту из колоды
если набрал больше 21
не
у карт есть вес
2 - это 2
3 - это 3
...
10 - это 10
валет - 10
дама - 10
король 10
туз - 11, если не влезает, то 1

проиграл
если пасуешь, а у противника больше
ты проиграл


если у тебя больше чем у противника, но меньше чем 22, то ты выйграл
точнее так
ты выбираешь, тебе тянуть карту, или пасовать
а карту, которую вытянешь, прибавляешь к своему счету
такие
как нам в callback query понимать, какая колода у нас осталась, и какой счет у игроков
хотя, вроде изи





'''
