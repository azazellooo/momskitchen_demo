from server.settings import LISTEN_WEBHOOK

INVALID_LINK = 'Ссылка невалидна!'
USER_NOT_FOUND = 'К сожалению мы не смогли найти ваш аккаунт. ' \
                 'Пройдите регистрацию перейдя по ссылке, которую даст вам Никита.'
MAILING_OFF = 'Рассылка отключена'
MAILING_ALREADY_OFF = 'Рассылка уже отключена'
TOKEN_ALREADY_GIVEN = 'Вам уже был выделен токен.'
CANNOT_GIVE_TOKEN = 'Вы не можете получить токен, ' \
                    'пока не зарегестрируетесь по ссылке который должен был вам выдать Никита'
DATA_SAVED = 'Спасибо! Ваши данные сохранены!'
USER_ALREADY_SIGNED_UP = 'Вы уже прошли регистрацию.'
GIVE_TOKEN = f'Прекрасно, держи свой линк на профиль : {LISTEN_WEBHOOK}'
WELCOME = ['Добро пожаловать к боту! Мы успешно сохранили данные о Вас, ',
           ', но перед тем, как пойти дальше, Вы должны указать Ваше имя следующим сообщением. Оно будет использоваться для подписи контейнеров с Вашей заказанной едой. В будущем Вы в любой момент сможете его изменить.'
           ]
WELCOME_BACK = ['Привет, ', '! Рады видеть Вас снова в KitchenBot!']
ALREADY_ACTIVE = 'Рассылка уже включена.'