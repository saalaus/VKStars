"""Update widget
Params: all_users, top_users, title"""

code = '''
        var all_users = %(all_users)r;
        var top_users = %(top_users)r;
        var top_users_name = [];
        var in_top = false;
        
        var user_id = Args.uid;
        var user_score = all_users[user_id];
        
        var i = 0;
        while (i < 10){
            if (top_users[i][0] == user_id){
                in_top = true;
            }
            var user = API.users.get({user_id: top_users[i][0]})[0];
            top_users_name.push(user.first_name+" "+user.last_name);
            i = i+1;
        };
        if (!user_score){
            var user = API.users.get({user_id: user_id})[0];
            top_users_name.pop();
            top_users_name.push(user.first_name+" "+user.last_name);

            top_users.pop();
            top_users.push([user.id, "Нет данных", "Нет данных"]);
        }
        if (!in_top && user_score){
            var user = API.users.get({user_id: user_id})[0];
            top_users_name.pop();
            top_users_name.push(user.first_name+" "+user.last_name);

            top_users.pop();
            var scores_and_place = user_score.split("_");
            top_users.push([user.id, scores_and_place[0], scores_and_place[1]]); 
        }


        return {
            "title": "Лидеры",
            "head": [
            {
                    "text": "Пользователь",
                    "align": "left"
            },
            {
                    "text": "Место",
                    "align": "center"
            },
            {
                    "text": %(title)r,
                    "align": "right"
            }
            ],
            "body": [
                        [
                            {
                                "icon_id": "id"+top_users[0][0],
                                "text": top_users_name[0],
                                "url": "https://vk.com/id"+top_users[0][0]
                            },
                            {
                                "text": "1"
                            },
                            {
                                "text": top_users[0][1]
                            }
                        ],
                        [
                            {
                                "text": top_users_name[1],
                                "icon_id": "id"+top_users[1][0],
                                "url": "https://vk.com/id"+top_users[1][0]
                            },
                            {
                                "text": "2"
                            },
                            {
                                "text": top_users[1][1]
                            }
                        ],
                        [
                            {
                                "text": top_users_name[2],
                                "icon_id": "id"+top_users[2][0],
                                "url": "https://vk.com/id"+top_users[2][0]
                            },
                            {
                                "text": "3"
                            },
                            {
                                "text": top_users[2][1]
                            }
                        ],
                        [
                            {
                                "text": top_users_name[3],
                                "icon_id": "id"+top_users[3][0],
                                "url": "https://vk.com/id"+top_users[3][0]
                            },
                            {
                                "text": "4"
                            },
                            {
                                "text": top_users[3][1]
                            }
                        ],
                        [
                            {
                                "text": top_users_name[4],
                                "icon_id": "id"+top_users[4][0],
                                "url": "https://vk.com/id"+top_users[4][0]
                            },
                            {
                                "text": "5"
                            },
                            {
                                "text": top_users[4][1]
                            }
                        ],
                        [
                            {
                                "text": top_users_name[5],
                                "icon_id": "id"+top_users[5][0],
                                "url": "https://vk.com/id"+top_users[5][0]
                            },
                            {
                                "text": "6"
                            },
                            {
                                "text": top_users[5][1]
                            }
                        ],
                        [
                            {
                                "text": top_users_name[6],
                                "icon_id": "id"+top_users[6][0],
                                "url": "https://vk.com/id"+top_users[6][0]
                            },
                            {
                                "text": "7"
                            },
                            {
                                "text": top_users[6][1]
                            }
                        ],
                        [
                            {
                                "text": top_users_name[7],
                                "icon_id": "id"+top_users[7][0],
                                "url": "https://vk.com/id"+top_users[7][0]
                            },
                            {
                                "text": "8"
                            },
                            {
                                "text": top_users[7][1]
                            }
                        ],
                        [
                            {
                                "text": top_users_name[8],
                                "icon_id": "id"+top_users[8][0],
                                "url": "https://vk.com/id"+top_users[8][0]
                            },
                            {
                                "text": "9"
                            },
                            {
                                "text": top_users[8][1]
                            }
                        ],
                        [
                            {
                                "text": top_users_name[9],
                                "icon_id": "id"+top_users[9][0],
                                "url": "https://vk.com/id"+top_users[9][0]
                            },
                            {
                                "text": in_top?"10":top_users[9][2]
                            },
                            {
                                "text": top_users[9][1]
                            }
                        ]
                        ]
                };
        '''