
#coding=utf-8
#求文件中数据的平均值
# import os
# os.chdir('C:\\Users\\Machenike\\Desktop\\some_number.txt')
def main():
    fileName ='C:\\Users\\Machenike\\Desktop\\some_number.txt'#input('what file are the numbers in?')
    infile=open(fileName,'r')
    sum=0.0
    count=0
    line=infile.readline()
    # print line,type(line)
    while line !="":
        sum=sum+eval(line)
        count=count+1
        line=infile.readline()
        # print line,type(line)
    print count
    print('\nThe average of the number is',float(sum)/float(count))
main()



<div id="maxwrap-reply">


<a name="1"></a><a name="pid972964633"></a>
<div class="clearfix contstxt outer-section" pk="972964633" uid="32388212" id="F1" rf="1" data-brand="0" data-brand-top="0" data-time="20170413091036">


<div class="conleft fl">
    <ul class="maxw">
        <li class="txtcenter fw">
            <a href="http://i.autohome.com.cn/32388212/home.html" target="_blank" class="c01439a" title="寂寞让人陪" xname="uname" style="vertical-align:middle;">寂寞让人陪</a><a href="/bbs/CarOwnercamp.html" class="crade" title="认证车主" onclick="return tz.checkLoginA(this,null,event)">&nbsp;</a>        </li>
            <li class="txtcenter" style="position:relative; z-index:9;">
						<div class="lv_card">
							<span class="identity "></span>
							<span class="card " data-toggle="help" data-target="32388212"><img src="http://i2.autoimg.cn/ucenter/help/card_1_26X16.png" /></span>
							<div class="clear"></div>
						</div></li>
            <li data-type="_title" class="txtcenter" style="position:relative; z-index:9;"></li>
</ul>
    <ul class="leftlist">
        <li style="padding-top: 5px;">
            <p class="imguser">
                <a target="_blank" href="http://i.autohome.com.cn/32388212/home.html" class="c01439a">
                    <img id="userprofileimg" onload="tz.userprofileimgLoaded(this)" src="http://i2.autoimg.cn/usercenter/g13/M08/6F/B9/120X120_0_q87_autohomecar__wKgH41f7QQ6ALoV0AAC23WqMfIY763.jpg" title="寂寞让人陪" alt="寂寞让人陪" onerror="fn_userImg120Error(this)" />
                </a>
            </p>
        </li>

        <li class="overflow">
            <p class="wrap_sendmessage leftxx fl ">
                <a href="http://i.autohome.com.cn/ajax/club/sendprivatemessages?userName=%bc%c5%c4%af%c8%c3%c8%cb%c5%e3" target="_blank" class="c01439a">发信息</a>
            </p>
        </li>

            <li>
                精华：0帖
            </li>
        <li>帖子：<a target="_blank" title="查看" href='http://i.autohome.com.cn/32388212/bbs.html' class="c01439a">7帖</a><span>&nbsp;|&nbsp;</span><a title="查看" target="_blank" href='http://i.autohome.com.cn/32388212/bbs/reply.html' class="c01439a">161回</a></li>

                <li>注册：2016年10月10日</li>
                <li>来自：<a title="查看该地区论坛" href="/bbs/forum-a-100012-1.html" target="_blank" class="c01439a">河南 漯河</a></li>

<li >爱车：<a class="craderz" href="/bbs/carOwnerCamp.html" target="_blank" onclick="return tz.checkLoginA(this,null,event)" title='我要申请成为认证车主'></a><a  target="_blank" title="逸动 2016款 XT 1.6L 手动俊酷型" href="/bbs/forum-c-2429-1.html#pvareaid=103121">逸动</a></li>

    <li class="leftimgs clearfix" rowIndex="0" style="z-index:1;display:">
        <div class="imgcon" data-xzid="158" data-xzname="解答达人一级勋章">
                <a target="_blank" href="http://club.autohome.com.cn/bbs/thread-o-200054-32592021-1.html" onclick="">
                    <img src="http://x.autoimg.cn/club/v1Content/images/Detail/badge/small/158.png?v=3" onerror="this.src='http://x.autoimg.cn/club/v1Content/images/Detail/badge/small/0.png?v=3'" style="cursor: pointer; width: 24px; height: 24px;"/>
                </a>
                <div class="contc" style="display: none;">
                    <div class="contcjt">
                        &nbsp;</div>
                    <div class="contcmain">
                        <div class="fl contcimg">
                            <img src="http://x.autoimg.cn/club/v1Content/images/Detail/badge/big/158.png?v=3" onerror="this.src='http://x.autoimg.cn/club/v1Content/images/Detail/badge/big/0.png?v=3'" title="解答达人一级勋章" alt="解答达人一级勋章" /></div>
                        <div class="fl userrycon">
                            <a target="_blank" href="http://club.autohome.com.cn/bbs/thread-o-200054-32592021-1.html" onclick="">
                                <h2>解答达人一级勋章</h2>
                            </a>
                            <p class="mt10">完成汽车之家&#183;知道升级任务，解答问答，并被提问者采纳为满意回答，可得解答达人一级勋章</p>
                        </div>
                    </div>
                </div>
            </div>
        <div class="imgcon" data-xzid="147" data-xzname="精华口碑勋章">
                <a target="_blank" href="http://k.autohome.com.cn/topic/2014/11" onclick="">
                    <img src="http://x.autoimg.cn/club/v1Content/images/Detail/badge/small/147.png?v=3" onerror="this.src='http://x.autoimg.cn/club/v1Content/images/Detail/badge/small/0.png?v=3'" style="cursor: pointer; width: 24px; height: 24px;"/>
                </a>
                <div class="contc" style="display: none;">
                    <div class="contcjt">
                        &nbsp;</div>
                    <div class="contcmain">
                        <div class="fl contcimg">
                            <img src="http://x.autoimg.cn/club/v1Content/images/Detail/badge/big/147.png?v=3" onerror="this.src='http://x.autoimg.cn/club/v1Content/images/Detail/badge/big/0.png?v=3'" title="精华口碑勋章" alt="精华口碑勋章" /></div>
                        <div class="fl userrycon">
                            <a target="_blank" href="http://k.autohome.com.cn/topic/2014/11" onclick="">
                                <h2>精华口碑勋章</h2>
                            </a>
                            <p class="mt10">发表1000字以上精华口碑，点评生动，以理服人，通过工作人员审核，特授予【精华口碑】专属勋章。</p>
                        </div>
                    </div>
                </div>
            </div>
        <div class="imgcon" data-xzid="260" data-xzname="掌上评车">
                <a target="_blank" href="http://club.autohome.com.cn/bbs/thread-o-200054-41548129-1.html" onclick="">
                    <img src="http://x.autoimg.cn/club/v1Content/images/Detail/badge/small/260.png?v=3" onerror="this.src='http://x.autoimg.cn/club/v1Content/images/Detail/badge/small/0.png?v=3'" style="cursor: pointer; width: 24px; height: 24px;"/>
                </a>
                <div class="contc" style="display: none;">
                    <div class="contcjt">
                        &nbsp;</div>
                    <div class="contcmain">
                        <div class="fl contcimg">
                            <img src="http://x.autoimg.cn/club/v1Content/images/Detail/badge/big/260.png?v=3" onerror="this.src='http://x.autoimg.cn/club/v1Content/images/Detail/badge/big/0.png?v=3'" title="掌上评车" alt="掌上评车" /></div>
                        <div class="fl userrycon">
                            <a target="_blank" href="http://club.autohome.com.cn/bbs/thread-o-200054-41548129-1.html" onclick="">
                                <h2>掌上评车</h2>
                            </a>
                            <p class="mt10">使用手机发表口碑，分享真实用车感受，为广大用户提供购车参考，特授予【掌上评车】专属勋章。</p>
                        </div>
                    </div>
                </div>
            </div>
    </li>

            <li class="force-out"></li>
    </ul>
</div>

    <!--end conleft and start conright-->
    <div class="conright fl">
        <div class="rconten">
            <div class="plr26 rtopconnext">
                    <div class="fr">
                        <a data-type="_shieldon" class="rightbutlz rightbut" href="javascript:void(0)" style="display:none" onclick="_club.shieldon.command(this,1);"></a>
                        <button style="box-sizing: content-box;color: #3b5998;" title="复制本楼链接到剪贴板" data-type="_copy" name="_clipboard" class="rightbutlz" href="#" rel="1">沙发</button>
                    </div>
                                <span>发表于 </span><span xname="date">2017-4-13 09:10:36</span><span> | 来自 <a href="http://www.autohome.com.cn/apps/1.html" target="_blank">汽车之家iPhone版</a></span>            </div>


<div class="x-reply font14" xname="content">
            <div class="w740"><div layer1="text-s"></div>怎么不买6at的<div layer1="text-e"></div></div>
</div>


                <div class="qa-dm-chara07" style="display:none" name="replyuseful" id="replyuseful972964633" data-rid="972964633" data-rmid="32388212" data-tid="62208529">
                    <a href="javascript:void(0);" class="btn btn-blue btn-useful" style="display:none" id="btnuseful972964633"><i class="qa-icon qa-thumbs-white"></i><b>(</b><b id="ubtn-count972964633"></b><b>)</b></a>
                    <a class="btn btn-blue btn-confirm" id="btnconfirm972964633" style="display:none" href="javascript:void(0);"><i class="qa-icon qa-thumbs-white"></i><b>采纳答案</b></a>
                </div>
        </div>
    </div>
    <!--end conright-->
    <div class="clear" style="_height: 1px">
        &nbsp;
    </div>
    <div class="conbottoms-reply">


                <div class="conbomhf">
                <div data-id="qamember32388212" name="qamemberinfo" data-mid="32388212" style="display:none" class="qa-dm-user">

                </div>
            <div>
                <p class="fr" xname="x-ReplyOpt">
                        <a href="http://jubao.autohome.com.cn/ComplaintMain/CreateCom/?cfgid=5&appId=1002&objId=62208529&subObjId=972964633&AccusedMId=32388212" target="_blank">举报</a>
                     &nbsp;|&nbsp;
                        <a title="回复并短消息通知此楼" showtitle="回复并短消息通知此楼" hidetitle="收起回复"
                           href="#" onclick=" tz.quoteReply(this);return false; ">回复本楼</a>
                </p>
                <a href="#" target="_blank" title="广告" xname="ad-reply" xvalue="0">&nbsp;</a>
            </div>
            <div class="replycon mt15" style="display: none">
                <p class="replyjt">
                    &nbsp;
                </p>
                <div class="qt">
                    引用 寂寞让人陪 2017-04-13 09:10:36 发表于 1楼 的内容：
                </div>
                <div class="replydiv">
                    <textarea class="replytext c999"></textarea>
                </div>

                <div class="replbut">
                    <div>
                        <input name="yyhf" type="button" value="发表回复" class="cursor repbuthf cfff fr" onclick="tz.sendYY(this)" /><span class="fr">禁止发布色情、反动及广告内容！</span>
                        <p class="repbut forpic fl">
                            <a href="http://ajax.club.autohome.com.cn/NewPost/Reply?bbs=c&bbsid=2429&topicId=62208529&kshf=y" class="compatibleBj c595759" target="_blank" title="打开高级回复页面(可上传多图、插入相册图片)" onclick="return _club.ar(this);">
                                高级模式
                            </a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
			</div>