from PyHackMD import API
import pyimgur
import datetime
from config import (
    HACKMD_API_TOKEN, TODO_NOTE_ID, TEMP_NOTE_ID, IMGUR_CLIENT_ID, TEMP_NOTE_ID, AI_NOTE_ID
) 


def creat_fletting_note(message):
    api = API(HACKMD_API_TOKEN)
    data = api.create_note(
        content = f"# 靈感筆記: {message.split()[0]}\n\n  ###### tags:`靈感筆記`\n\n {message}")
    link = f"https://hackmd.io/{data['id']}"
    return link

def update_todo_note(content):
    api = API(HACKMD_API_TOKEN)
    note = api.get_note(note_id = TODO_NOTE_ID)
    ori_content = note['content']
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))).strftime("%a, %b %d, %Y %I:%M %p")
    update_content = f"{ori_content}\n- [ ] {content} [time={now}]"
    api.update_note(
        note_id = TODO_NOTE_ID,
        content = update_content
        )
    return f"已新增代辦事項{content}\n {note['publishLink']}"

def update_ai_note(question,response):
    api = API(HACKMD_API_TOKEN)
    note = api.get_note(note_id = AI_NOTE_ID)
    ori_content = note['content']
    update_content = f"{ori_content}\n---\n**Q: {question[3:]}**\n\n```\n{response}\n```\n"
    api.update_note(
        note_id = AI_NOTE_ID,
        content = update_content
        )
    return f"已備份至 {note['publishLink']}"

def get_user_image(image_content):
    path = './temp.png'
    with open(path, 'wb') as fd:
        for chunk in image_content.iter_content():
            fd.write(chunk)
    return path

def upload_img_link(imgpath):   
	im = pyimgur.Imgur(IMGUR_CLIENT_ID)
	upload_image = im.upload_image(imgpath, title="Uploaded with PyImgur")
	return upload_image.link

def add_temp_note(content):
    api = API(HACKMD_API_TOKEN)
    note_id = TEMP_NOTE_ID
    note = api.get_note(note_id = note_id)
    ori_content = note['content']
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))).strftime("%a, %b %d, %Y %I:%M %p")
    update_content = f"{ori_content}\n---\n- {content} [time={now}]"
    api.update_note(
        note_id = TEMP_NOTE_ID,
        content = update_content
        )
    return f"已新增至臨時筆記\n{content}  \n https://hackmd.io/{TEMP_NOTE_ID}"


def flex_reply_image(image):
    path = get_user_image(image)
    link = upload_img_link(path)
    add_temp_note(content=f"![]({link})")
    return {
        "type": "carousel",
        "contents": [
            {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "image",
                    "url": link,
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "gravity": "top"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "filler"
                            },
                            {
                                "type": "text",
                                "text": "Open in HackMD",
                                "color": "#ffffff",
                                "flex": 0,
                                "offsetTop": "-2px",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": f"https://hackmd.io/{TEMP_NOTE_ID}"
                                }
                            },
                            {
                                "type": "filler"
                            }
                            ],
                            "spacing": "sm"
                        },
                        {
                            "type": "filler"
                        }
                        ],
                        "borderWidth": "1px",
                        "cornerRadius": "4px",
                        "spacing": "sm",
                        "borderColor": "#ffffff",
                        "margin": "xxl",
                        "height": "40px"
                    }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "backgroundColor": "#03303Acc",
                    "paddingAll": "20px",
                    "paddingTop": "18px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "+1",
                        "color": "#ffffff",
                        "align": "center",
                        "size": "xs",
                        "offsetTop": "3px"
                    }
                    ],
                    "position": "absolute",
                    "cornerRadius": "20px",
                    "offsetTop": "18px",
                    "backgroundColor": "#ff334b",
                    "offsetStart": "18px",
                    "height": "25px",
                    "width": "53px"
                }
                ],
                "paddingAll": "0px"
            }
            }
        ]
        }
    
 