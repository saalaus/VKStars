import time

from models import get_all, get_top_10
from exceptions import VkApiError
from VKmain import method
from const import *
import logging
logger = logging.getLogger('VKStars')
logging.basicConfig(level=logging.DEBUG)

code = '''var all_users = {};
        var top_10 = {};
        var top_10_name = [];
        var in_top_10 = false;
        var i = 0;
        while (i < 10){{
            if (top_10[i][0] == Args.uid){{
                in_top_10 = true;
            }}
            var user = API.users.get({{user_id: top_10[i][0]}})[0];
            top_10_name.push(user.first_name+" "+user.last_name);
            i = i+1;
        }};
        if (!all_users[Args.uid]){{ // если пользователя нет в базе данных
            var user = API.users.get({{user_id: Args.uid}})[0];
            top_10_name.pop(); // делаем так потому что Unable to compile code: non-variable in assignment
            top_10_name.push(user.first_name+" "+user.last_name);

            top_10.pop();
            top_10.push([user.id, "Нет данных", "Нет данных"]); // пишем user.id потому что Args.uid ПОЧЕМУ ТО НЕ РАБОТАЕТ
        }}
        if (!in_top_10 && all_users[Args.uid]){{
            var user = API.users.get({{user_id: Args.uid}})[0];
            top_10_name.pop(); // делаем так потому что Unable to compile code: non-variable in assignment
            top_10_name.push(user.first_name+" "+user.last_name);

            top_10.pop();
            var scores_and_place = all_users[Args.uid].split(" ");
            top_10.push([user.id, scores_and_place[0], scores_and_place[1]]); // пишем user.id потому что Args.uid ПОЧЕМУ ТО НЕ РАБОТАЕТ
        }}


        return {{
            "title": "Лидеры",
            "head": [
            {{
                    "text": "Пользователь",
                    "align": "left"
            }},
            {{
                    "text": "Место",
                    "align": "center"
            }},
            {{
                    "text": "{}",
                    "align": "right"
            }}
            ],
            "body": [
                        [
                            {{
                                "icon_id": "id"+top_10[0][0],
                                "text": top_10_name[0],
                                "url": "https://vk.com/id"+top_10[0][0]
                            }},
                            {{
                                "text": "1"
                            }},
                            {{
                                "text": top_10[0][1]
                            }}
                        ],
                        [
                            {{
                                "text": top_10_name[1],
                                "icon_id": "id"+top_10[1][0],
                                "url": "https://vk.com/id"+top_10[1][0]
                            }},
                            {{
                                "text": "2"
                            }},
                            {{
                                "text": top_10[1][1]
                            }}
                        ],
                        [
                            {{
                                "text": top_10_name[2],
                                "icon_id": "id"+top_10[2][0],
                                "url": "https://vk.com/id"+top_10[2][0]
                            }},
                            {{
                                "text": "3"
                            }},
                            {{
                                "text": top_10[2][1]
                            }}
                        ],
                        [
                            {{
                                "text": top_10_name[3],
                                "icon_id": "id"+top_10[3][0],
                                "url": "https://vk.com/id"+top_10[3][0]
                            }},
                            {{
                                "text": "4"
                            }},
                            {{
                                "text": top_10[3][1]
                            }}
                        ],
                        [
                            {{
                                "text": top_10_name[4],
                                "icon_id": "id"+top_10[4][0],
                                "url": "https://vk.com/id"+top_10[4][0]
                            }},
                            {{
                                "text": "5"
                            }},
                            {{
                                "text": top_10[4][1]
                            }}
                        ],
                        [
                            {{
                                "text": top_10_name[5],
                                "icon_id": "id"+top_10[5][0],
                                "url": "https://vk.com/id"+top_10[5][0]
                            }},
                            {{
                                "text": "6"
                            }},
                            {{
                                "text": top_10[5][1]
                            }}
                        ],
                        [
                            {{
                                "text": top_10_name[6],
                                "icon_id": "id"+top_10[6][0],
                                "url": "https://vk.com/id"+top_10[6][0]
                            }},
                            {{
                                "text": "7"
                            }},
                            {{
                                "text": top_10[6][1]
                            }}
                        ],
                        [
                            {{
                                "text": top_10_name[7],
                                "icon_id": "id"+top_10[7][0],
                                "url": "https://vk.com/id"+top_10[7][0]
                            }},
                            {{
                                "text": "8"
                            }},
                            {{
                                "text": top_10[7][1]
                            }}
                        ],
                        [
                            {{
                                "text": top_10_name[8],
                                "icon_id": "id"+top_10[8][0],
                                "url": "https://vk.com/id"+top_10[8][0]
                            }},
                            {{
                                "text": "9"
                            }},
                            {{
                                "text": top_10[8][1]
                            }}
                        ],
                        [
                            {{
                                "text": top_10_name[9],
                                "icon_id": "id"+top_10[9][0],
                                "url": "https://vk.com/id"+top_10[9][0]
                            }},
                            {{
                                "text": in_top_10?"10":top_10[9][2]
                            }},
                            {{
                                "text": top_10[9][1]
                            }}
                        ]
                        ]
                }};
        '''#.format(get_all(),
                   # get_top_10(),
                   # TITLE)
code_no_space = 'var all_users={};var top_10={};var top_10_name=[];var in_top_10=false;var i=0;while(i<10){{if(top_10[i][0]==Args.uid){{in_top_10=true;}}var user=API.users.get({{user_id:top_10[i][0]}})[0];top_10_name.push(user.first_name+" "+user.last_name);i=i+1;}};if(!all_users[Args.uid]){{var user=API.users.get({{user_id: Args.uid}})[0];top_10_name.pop();top_10_name.push(user.first_name+" "+user.last_name);top_10.pop();top_10.push([user.id,"Нет данных","Нет данных"]);}}if(!in_top_10&&all_users[Args.uid]){{var user=API.users.get({{user_id: Args.uid}})[0];top_10_name.pop();top_10_name.push(user.first_name+" "+user.last_name);top_10.pop();var scores_and_place=all_users[Args.uid].split(" ");top_10.push([user.id,scores_and_place[0],scores_and_place[1]]);}}return{{"title":"Лидеры","head":[{{"text":"Пользователь","align":"left"}},{{"text":"Место","align":"center"}},{{"text":"{}","align":"right"}}],"body": [[{{"icon_id":"id"+top_10[0][0],"text":top_10_name[0],"url":"https://vk.com/id"+top_10[0][0]}},{{"text":"1"}},{{"text":top_10[0][1]}}],[{{"text":top_10_name[1],"icon_id":"id"+top_10[1][0],"url":"https://vk.com/id"+top_10[1][0]}},{{"text":"2"}},{{"text":top_10[1][1]}}],[{{"text":top_10_name[2],"icon_id":"id"+top_10[2][0],"url":"https://vk.com/id"+top_10[2][0]}},{{"text":"3"}},{{"text":top_10[2][1]}}],[{{"text":top_10_name[3],"icon_id":"id"+top_10[3][0],"url":"https://vk.com/id"+top_10[3][0]}},{{"text":"4"}},{{"text":top_10[3][1]}}],[{{"text":top_10_name[4],"icon_id":"id"+top_10[4][0],"url":"https://vk.com/id"+top_10[4][0]}},{{"text":"5"}},{{"text":top_10[4][1]}}],[{{"text":top_10_name[5],"icon_id":"id"+top_10[5][0],"url":"https://vk.com/id"+top_10[5][0]}},{{"text":"6"}},{{"text":top_10[5][1]}}],[{{"text":top_10_name[6],"icon_id":"id"+top_10[6][0],"url":"https://vk.com/id"+top_10[6][0]}},{{"text":"7"}},{{"text":top_10[6][1]}}],[{{"text":top_10_name[7],"icon_id":"id"+top_10[7][0],"url":"https://vk.com/id"+top_10[7][0]}},{{"text":"8"}},{{"text":top_10[7][1]}}],[{{"text":top_10_name[8],"icon_id":"id"+top_10[8][0],"url":"https://vk.com/id"+top_10[8][0]}},{{"text":"9"}},{{"text":top_10[8][1]}}],[{{"text":top_10_name[9],"icon_id":"id"+top_10[9][0],"url":"https://vk.com/id"+top_10[9][0]}},{{"text":in_top_10?"10":top_10[9][2]}},{{"text":top_10[9][1]}}]]}};'



# обновление виджета каждые 5 минут
def update_widget():
    while True:
        logger.info("Updating widget")
        try:
            a = method("appWidgets.update", access_token=WIDGET_TOKEN, type="table", code=code_no_space.format(get_all(),get_top_10(),TITLE))
        except VkApiError as e:
            logger.critical(e)
        logger.info("Wait 5 minutes")
        time.sleep(300)
