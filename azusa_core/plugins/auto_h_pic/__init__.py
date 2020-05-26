from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from jieba import posseg

from .data_source import get_auto_h_pic

@on_command('auto_h_pic', aliases=('色图','涩图'))
async def auto_h_pic(session: CommandSession):
    wife = session.get('wife', prompt= '哈？你要谁的色图。')
    words = posseg.lcut(wife)
    # get the name from the words
    for word in words:
        if word.flag == 'nr':
            wife = word.word
            break
    wife_report = await get_auto_h_pic(wife)
    await session.send(wife_report)

@auto_h_pic.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    #print('进入参数器',stripped_arg)
    words = posseg.lcut(stripped_arg)
    name_flag = 0
    # get the name from the words
    for word in words:
        if word.flag == 'nr':
            stripped_arg = word.word
            break
   # 如果是第一次输入，分词
    if session.is_first_run:
        if stripped_arg:
            session.state['wife'] = stripped_arg
        return
   # 第二次没有内容了：
    if not stripped_arg:
        session.pause('快说快说，究竟要什么图，不说我就走了！')
    # 返回状态
    session.state[session.current_key] = stripped_arg


#@on_command('auto_h_pic2', aliases=('色图'))
#async def auto_h_pic2(session: CommandSession):
#    wife = session.get('wife', prompt= '你要谁的色图呀？')
#    wife_report = await get_auto_h_pic(wife)
#    await session.send(wife_report)
#    
#

#
#
# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language(keywords = {'色图','涩图'} )
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    print('进入NLP',stripped_msg)
    # 对消息进行分词和词性标注
    words = posseg.lcut(stripped_msg)
    # 定义一个wife
    wife = None
    # 遍历 posseg.lcut 返回的列表
    for word in words:
        # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
        if word.flag == 'nr':
            # nr 代表人名
            wife = word.word
            break

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'auto_h_pic', current_arg = wife or '')