#templates#
для получение шаблона нужно перейти по get ссылке http://127.0.0.1:8000/api/templates
```javascript
     "template": {
            "name": "TEST!",
            "text": "Hello #name itis ur new code #code"
        }
```
здесь name это название шаблона a содержание находится в text примечание - ( что бы добавить шаблон нужно перейти по той же ссылке только через post
только перед тем как шото добавить нужно буднт перед параметром добавить решетку )


#sendMethod#
для получения выбора метода достаточно перейти по get ссылке http://127.0.0.1:8000/api/sendMethod где получим шо то такое

```javascript
    "sendMethod": [
        {
            "nameMethod": "mail.ru"
        },
  	{
            "nameMethod": "telegram"
        }
```

примечание ( для изменение или удаление шаблона или выборМетода
переходем по put or delete (в зависемостри от сетуации)ссылке http://127.0.0.1:8000/api/templates or sendMethod
и через "/" пишем айди метода или шаблона которого хотели бы изменитб )

#notifications#
для ввода данных сообщений переходим на -> post http://127.0.0.1:8000/api/notifications/ который ждет :
```javascript
{
    "notification":{
        "params":{
                    "PARAMS1":"abdulla123123123123",
                    "PARAMS2":"dsafsadfsadfsdaf",
                    "PARAMS3":"ghdhdhfdh"
                    },
        "sendMethodID_id": 2,
        "templateID_id": 1
    }
}
```
где params это параметр который содержится в шаблонае
sendMethod - выбор типа отправки сообщений где 1 это мыло 2 - телеграм
template это шаблон сообщений как "HELLO #NAME HOW ARE U"


