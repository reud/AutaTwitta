import twitter
import APIKeyReader
import sys
import time
import traceback
import os
if os.name=='nt':
    apikeyreader=APIKeyReader.Reader(os.getcwd()+r"\SettingFiles")
else:
    apikeyreader=APIKeyReader.Reader(os.getcwd()+r"/SettingFiles")
api=apikeyreader.GetApi()
print(type(api.VerifyCredentials()))
api.PostDirectMessage("AutaTwitta 起動",screen_name=api.VerifyCredentials().screen_name)
pass
def getFFlist(followers,follows):
    fflist=[]
    for i in followers:
        for t in follows:
            if(t.screen_name==i.screen_name):
                fflist.append(t.screen_name)
                print("FF中..."+t.screen_name)
    print("getList...OK")
    return fflist
def KillFollow(endList,follows,api):
    killList=[]
    for i in follows:
        exist=False
        print("for before endList")
        for t in endList:
            if(i.screen_name==t):
                exist=True
        if(not exist):
            print(i.screen_name+"は削除されます。")
            killList.append(i.screen_name)
    for i in killList:
        try:
            print(i+"の削除を開始します。")
            api.DestroyFriendship(screen_name=i)
            print(i+"の削除をしました。")
        except:
            traceback.print_exc()          
    print("killFollow...OK")
    return len(killList)
def Sercher(api):
    #相互フォローって含んでる文をサーチ
    search=api.GetSearch(term="#followback",count=70)
    print(search)
    friends=api.GetFriendIDs()
    for i in search:
        for s in friends:
            if(str(i.user.id)==str(s)):
                search.remove(i)
                print("Already Following:"+str(i.user))
            else:
                print(str(s)+"はフォローされていません。")
    print(len(search))
    for  i in search:
        print(str(i.user.id))
        print("Follow:"+str(i.user.id))
        try:
            api.CreateFriendship(user_id=i.user.id)
            api.CreateMute(user_id=i.user.id)
        except:
            traceback.print_exc()
def GetFriend(endList,followers,api):
    followList=[]
    for i in followers:
        exist=False
        print("for before endList")
        for t in endList:
            #print(i.screen_name+" vs "+t)
            if(i.screen_name==t):
                print("比較")
                exist=True
        if(not exist):
            followList.append(i.screen_name)
    for i in followList:
        try:
            api.CreateFriendship(screen_name=i)
            api.CreateMute(screen_name=i)
        except:
            traceback.print_exc()
    return len(followList)
while(True):
    followers=api.GetFollowers()
    follows=api.GetFriends()
    endlist=getFFlist(followers,follows)
    excepts=api.GetListMembers(slug="notffbutlike",owner_screen_name=api.VerifyCredentials().screen_name)
    for user in excepts:
        print(user.screen_name+"はFFじゃなくてもフォローを継続します。")
        endlist.append(user.screen_name)
    print("appendList...OK")
    endlist=list(set(endlist))#重複要素を削除
    kills=KillFollow(endlist,follows,api)
    newFriends=GetFriend(endlist,followers,api)
    if((kills==0) and (newFriends==0)):
        pass
    else:
        api.PostDirectMessage(text="newfriend:"+str(newFriends)+"人\r\nbyefriend:"+str(kills)+"人",screen_name=api.VerifyCredentials().screen_name)
    Sercher(api)
    time.sleep(20000)
