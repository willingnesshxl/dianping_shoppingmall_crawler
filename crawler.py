# -*- coding: UTF-8 -*-

'''针对指定商户的评论，对其内容进行抓取（用户id ,nickname，用户等级，时间戳，三个评分，评论评分，评论内容，消费，图片） '''
__author__ = 'willingness'

import time
import random
import re
import string
from selenium import webdriver
import linecache
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")


driver = webdriver.Firefox()

k = open("sh.txt","r")
shop_id = k.readlines()
num = len(shop_id)
for i in range(16,30):
    shop_id[i] = shop_id[i][:-1]
    shopid = shop_id[i]
    print str(i)+"  /  "+ str(num)
    print "shopid:"+shopid
    driver.get('http://www.dianping.com/shop/'+str(shopid))
    page = driver.page_source
    f = open("sh/"+str(shopid)+".txt","w")
    # g = open("check_in/"+str(shopid)+".txt","w")

    # get comment
    comment_number = re.findall(" <a data-type=\"all\"(.*?)</span></a>",page)
    if comment_number != []:
        comment_number = re.findall("\((.*?)\)",comment_number[0])
        comment_number = int(comment_number[0])
    else:
        comment_number = 0

    print "comment_number : ",comment_number


    # f.write("\"comment_number\":\"%s\",\n"%str(comment_number))
    f.write("%s\n"%str(comment_number))



    if comment_number !=0:
        if comment_number %20 != 0:
            comment_pages = int(comment_number) / 20 + 1
        else:
            comment_pages = int(comment_number) / 20

        for j in range (0, comment_pages + 1):
            time.sleep(2)
            print "comment_pages = "+str(j)+"  /  "+str(comment_pages)
            driver.get("http://www.dianping.com/shop/"+str(shopid)+"/review_more?pageno="+str(j))
            page = driver.page_source

            #get user id 
            userid = re.findall("user-id=\"(.*?)\"",page)
            #get user nickname and picture num
            picture = []
            user_nickname = re.findall("title=\"\" target=\"_blank\">(.*?)</a>",page)
            for i in range(0,len(user_nickname)):
                user_nickname[i] = user_nickname[i].replace("\\","\\\\")
                user_nickname[i] = user_nickname[i].replace("*","\*")
                user_nickname[i] = user_nickname[i].replace(".","\.")
                user_nickname[i] = user_nickname[i].replace("(","\(")
                user_nickname[i] = user_nickname[i].replace(")","\)")
                user_nickname[i] = user_nickname[i].replace("^","\^")
                user_nickname[i] = user_nickname[i].replace(":","\:")
                pattern = "title=\""+'%s'%user_nickname[i]+"的图片"
                picture_num = re.findall("%s"%pattern,page)
                picture_num = len(picture_num)
                picture.append(picture_num)



            #get contribution
            user_contribution = re.findall("urr-rank(.*?)\"",page)


            #get user_info 
            user_info = re.findall("<div class=\"user-info\">(.*?)</div>",page,re.S)
            cost_num = []
            product = []
            environment = []
            service = []
            for i in range(0,len(user_info)):
                cost = re.findall("<span class=\"comm-per\">(.*?)<",user_info[i],re.S)
                if cost != []:
                    cost = re.findall("[0-9]{1,6}",cost[0])
                    cost = cost[0]
                else:
                    cost = "-1"
                cost_num.append(cost)
                p = re.findall("<span class=\"rst\">(.*?)</span>",user_info[i])
                if len(p) >= 3:
                    product1 = re.findall("[0-9]{1}",p[0])
                    product.append(product1[0])
                    environment1 = re.findall("[0-9]{1}",p[1])
                    environment.append(environment1[0])
                    service1 = re.findall("[0-9]{1}",p[2])
                    service.append(service1[0])
                else:
                    product.append("-1")
                    environment.append("-1")
                    service.append("-1")

        

            #get comment content
            comment = re.findall("<div class=\"J_brief-cont\">(.*?)</div>", page,re.S)
            #get comment rank_star
            rank_star =  re.findall('<span class="item-rank-rst irr-star(.*?)\" ',page)
            #get comment time_stamp
            comment_time = re.findall('<span class="time">(.*?)</span>',page,re.S)

            number = len(comment)
            # print user_nickname
            # print len(user_nickname)
            if number != 0:
                for i in range(0,number):
                    comment[i] = string.lstrip(comment[i])
                    comment[i] = string.rstrip(comment[i])
                    temp = re.findall("[0-9]{2}-[0-9]{2}-[0-9]{2}",comment_time[i])
                    if temp == []:
                        temp = re.findall("[0-9]{2}-[0-9]{2}",comment_time[i])
                        temp[0] = "16-"+temp[0]
                    comment_time[i] = temp[0]
                    if len(rank_star)<number:
                        for l in range(len(rank_star),number):
                            rank_star.append("-1")

                    f.write("%s,"%userid[i])
                    f.write("%s,"%user_nickname[i])
                    f.write("%s,"%user_contribution[i])
                    f.write("%s,"%rank_star[i])
                    f.write("%s,"%product[i])
                    f.write("%s,"%environment[i])
                    f.write("%s,"%service[i])
                    f.write("%s,"%cost_num[i])
                    f.write("%s,"%picture[i])
                    f.write("%s,"%comment_time[i])
                    f.write("%s"%comment[i])
                    f.write("\n")

                    # f.write("\"userid\":\"%s\","%userid[i])
                    # f.write("\"nickname\":\"%s\","%user_nickname[i])
                    # f.write("\"user_contribution\":\"%s\","%user_contribution[i])
                    # f.write("\"rank_star\":\"%s\","%rank_star[i])
                    # f.write("\"product\":\"%s\","%product[i])
                    # f.write("\"environment\":\"%s\","%environment[i])
                    # f.write("\"service\":\"%s\","%service[i])
                    # f.write("\"cost_num\":\"%s\","%cost_num[i])
                    # f.write("\"picture\":\"%s\","%picture[i])
                    # f.write("\"time_stamp\":\"%s\","%comment_time[i])
                    # f.write("\"comment\":\"%s\""%comment[i])
                    # f.write("\n")

                    # print user_info[i]
                    # print product[i],environment[i],service[i]
                    # print userid[i],comment[i],rank_star[i],comment_time[i]
                    # f.write("{\""+comment[i]+"\","+"\""+"rank_star\":\""+rank_star[i]+"\","+"\""+"time\":\""+comment_time[i]+"\"}"+"\n")    

    time.sleep(2)

    #get review_short

    # g.write('{\n')
    # driver.get('http://www.dianping.com/shop/'+str(shopid)+'/review_short?pageno=1')
    # page = driver.page_source
    # review_short_num = re.findall('<em class="col-exp">\((.*?)\)<', page)
    # if len(review_short_num) == 4:
    #     review_short_num = int(review_short_num[3])
    # elif len(review_short_num) == 0:
    #     review_short_num = 0
    #     print "review_short_num:"+'0'
    # else:
    #     review_short_num = int(review_short_num[2])
    # g.write('"review_short_num":'+'\"'+str(review_short_num)+'\"'+'\n')
    # print "review_short_num"+str(review_short_num)

    # review_short_page = review_short_num / 15 + 1
    # print 'review_short_page'+str(review_short_page)

    # for j in range(1,review_short_page + 1):
    #     print 'page='+str(j) +' / '+str(review_short_page)
    #     driver.get('http://www.dianping.com/shop/'+str(shopid)+'/review_short?pageno='+str(j))
    #     page = driver.page_source
    #     time.sleep(1)
    #     # get usrid
    #     usrid = re.findall('href="/member/(.*?)" rel', page)
    #     usrid_num = len(usrid)
    #     for i in range(1, usrid_num / 2 + 1):
    #         usrid.pop(i)
    #     # get time_stamp
    #     time_stamp = re.findall('<span class="time">(.*?)</span>', page)
    #     a = re.findall("<div class=\"comment-txt\">(.*?)</div>",page,re.S)
    #     for i in range(0, usrid_num / 2):
    #         b = re.findall("<p>(.*?)</p>",a[i],re.S)
    #         if len(b)<2:
    #             b = ""
    #         else:
    #             b = b[1]
    #         g.write('   '+'{\"usrid:'+usrid[i]+'","'+time_stamp[i]+'"'+',\"'+b+'\"}\n')
    #     time.sleep(1)
    # print "\n\n"
    # g.write('}\n')

