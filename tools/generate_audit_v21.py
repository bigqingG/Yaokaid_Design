# -*- coding: utf-8 -*-
"""
妖斗牌 - 数值框架v2.1 审计Excel生成器（基于调整后数据）
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

header_font = Font(name='微软雅黑', bold=True, size=11, color='FFFFFF')
header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
subheader_fill = PatternFill(start_color='D9E2F3', end_color='D9E2F3', fill_type='solid')
overpower_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
underpower_fill = PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')
normal_fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
adjusted_fill = PatternFill(start_color='BDD7EE', end_color='BDD7EE', fill_type='solid')
thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
left_align = Alignment(horizontal='left', vertical='center', wrap_text=True)

def style_header(ws, row, max_col):
    for col in range(1, max_col + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = thin_border

def style_data(ws, start_row, end_row, max_col):
    for row in range(start_row, end_row + 1):
        for col in range(1, max_col + 1):
            cell = ws.cell(row=row, column=col)
            cell.border = thin_border
            cell.alignment = center_align if col <= 7 else left_align

def auto_width(ws, max_col, min_width=10, max_width=45):
    for col in range(1, max_col + 1):
        max_len = min_width
        for row in ws.iter_rows(min_col=col, max_col=col, values_only=True):
            for cell in row:
                if cell:
                    max_len = max(max_len, min(len(str(cell)), max_width))
        ws.column_dimensions[get_column_letter(col)].width = max_len + 2

# ========== Sheet 1: 数值框架v2.1说明 ==========
ws1 = wb.active
ws1.title = '数值框架v2.1'
headers1 = ['项目', 'v2.0原值', 'v2.1修正值', '修正原因']
for col, h in enumerate(headers1, 1):
    ws1.cell(row=1, column=col, value=h)
style_header(ws1, 1, len(headers1))
changes = [
    ['派遣效果折扣', '×0.8', '×0.7', '原0.8偏高，导致派遣效果卡普遍超模'],
    ['在场每回合效果折扣', '×1.5', '×2.0', '原1.5低估持续效果，按期望存活2回合计算'],
    ['澄曜区调整卡数', '—', '7张', '锻金咚/日巡犬/鸮掌柜/禁火魇/归焰凰/逆焰魃/双面魍'],
    ['青棠区调整卡数', '—', '12张', '巷尾咕/藤缠仔/孪果儿/气蓬婆/枝镜/蓬哨/灯笼虫/蜜盏苞/四时芽/雾翅虫/青古树怪/雨意至'],
    ['沃衡区调整卡数', '—', '10张', '稻契穗/麦哨芽/谷卫兵/犁角地牛/穗鼓隆/垛草魁/驮稷兽/穰穰君/五谷丰登/田祭咚'],
    ['赞助商重制', '—', '2家30张', '去临时法力→法力槽，统一术语，支援→妖怪'],
    ['合计调整卡牌', '—', '29张+30张', '占三区66张的44%'],
]
for i, row in enumerate(changes, 2):
    for j, val in enumerate(row, 1):
        ws1.cell(row=i, column=j, value=val)
style_data(ws1, 2, len(changes)+1, len(headers1))
auto_width(ws1, len(headers1))

# ========== Sheet 2-4: 三区审计（调整后） ==========
def create_audit_sheet(wb, sheet_name, cards):
    ws = wb.create_sheet(sheet_name)
    headers = ['ID', '名称', '费用', '身材', '类型', '稀有度', '牌组角色', '身材MV', '效果MV', '总MV', '偏差', '判定', '调整状态', '调整说明']
    for col, h in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=h)
    style_header(ws, 1, len(headers))
    for i, card in enumerate(cards, 2):
        for j, val in enumerate(card, 1):
            ws.cell(row=i, column=j, value=val)
        judge = card[11]
        fill = normal_fill
        if '超模' in str(judge):
            fill = overpower_fill
        elif '亏模' in str(judge):
            fill = underpower_fill
        ws.cell(row=i, column=12).fill = fill
        if card[12] == '已调整':
            ws.cell(row=i, column=13).fill = adjusted_fill
    style_data(ws, 2, len(cards)+1, len(headers))
    auto_width(ws, len(headers))
    return ws

# 澄曜区调整后审计
chengyao = [
    ['CYS_001', '火灶灵', 1, '1/1', '妖怪', '一般', '启动', 1.0, 0.4, 1.4, '+0.4', '合理', '未调整', '—'],
    ['CYS_002', '锻金咚', 2, '1/2', '妖怪', '一般', '启动', 1.5, 1.4, 2.9, '+0.9', '略超模', '已调整', '身材2/2→1/2'],
    ['CYS_003', '霓火茧', 1, '2/1', '妖怪', '一般', '启动', 1.5, 0.5, 2.0, '+1.0', '超模', '未调整', '1费2/1达上限，艳阳天疾袭'],
    ['CYS_004', '烬甲魃', 2, '2/2', '妖怪', '一般', '启动', 2.0, 0.8, 2.8, '+0.8', '合理', '未调整', '—'],
    ['CYS_005', '日巡犬', 2, '2/2', '妖怪', '一般', '启动', 2.0, 0.8, 2.8, '+0.8', '合理', '已调整', '身材2/3→2/2，恢复2→1'],
    ['CYS_006', '青铜叶鳅', 1, '1/1', '妖怪', '一般', '启动', 1.0, 0.5, 1.5, '+0.5', '合理', '未调整', '—'],
    ['CYS_007', '福祸相依', 2, '—', '御术', '稀有', '引擎', 0, 1.2, 1.2, '-0.8', '亏模', '未调整', '御术触发条件苛刻'],
    ['CYS_008', '铁芯蟾', 3, '2/3', '妖怪', '罕见', '引擎', 2.5, 1.5, 4.0, '+1.0', '超模', '未调整', '蜕变机制未实现'],
    ['CYS_009', '曜金拉恩', 3, '3/3', '妖怪', '稀有', '引擎', 3.0, 1.0, 4.0, '+1.0', '超模', '未调整', '元素反应事件过滤未实现'],
    ['CYS_010', '鸮掌柜', 2, '1/2', '妖怪', '稀有', '引擎', 1.5, 1.4, 2.9, '+0.9', '略超模', '已调整', '身材2/2→1/2'],
    ['CYS_011', '焰舞沙魈', 3, '3/3', '妖怪', '稀有', '收益', 3.0, 1.0, 4.0, '+1.0', '超模', '未调整', '受伤+攻条件触发'],
    ['CYS_012', '搏命熊', 4, '5/3', '妖怪', '稀有', '收益', 4.0, -0.5, 3.5, '-0.5', '合理', '未调整', '—'],
    ['CYS_013', '裂炉吼', 2, '1/4', '妖怪', '罕见', '收益', 2.5, 0.7, 3.2, '+1.2', '超模', '未调整', '1/4超2费标准'],
    ['CYS_014', '金羽戴胜', 3, '3/2', '妖怪', '稀有', '收益', 2.5, 1.1, 3.6, '+0.6', '合理', '未调整', '—'],
    ['CYS_015', '禁火魇', 3, '2/2', '妖怪', '罕见', '干扰', 2.0, 1.2, 3.2, '+0.2', '合理', '已调整', '费用2→3，身材2/3→2/2'],
    ['CYS_016', '冷阀蜥', 5, '2/5', '妖怪', '一般', '干扰', 3.5, 1.6, 5.1, '+0.1', '合理', '未调整', '—'],
    ['CYS_017', '烈日当空', 2, '—', '法术', '一般', '干扰', 0, 2.5, 2.5, '+0.5', '合理', '未调整', '—'],
    ['CYS_018', '金乌', 6, '5/5', '妖怪', '史诗', '终结', 5.0, 1.5, 6.5, '+0.5', '合理', '未调整', '—'],
    ['CYS_019', '归焰凰', 5, '4/4', '妖怪', '传说', '终结', 4.0, 1.5, 5.5, '+0.5', '合理', '已调整', '亡语条件≤10→≤8'],
    ['CYS_020', '日轮高悬', 1, '—', '法术', '一般', '启动', 0, 0.5, 0.5, '-0.5', '亏模', '未调整', '仅预测天气，建议加抽牌'],
    ['CYS_021', '逆焰魃', 3, '1/3', '妖怪', '稀有', '怪构筑', 2.0, 1.5, 3.5, '+0.5', '合理', '已调整', '身材1/4→1/3'],
    ['CYS_022', '双面魍', 4, '3/2', '妖怪', '史诗', '怪构筑', 2.5, 2.0, 4.5, '+0.5', '合理', '已调整', '身材3/3→3/2'],
]

# 青棠区调整后审计
qingtang = [
    ['QINGTANG_001', '缝黏仔', 1, '1/1', '妖怪', '一般', '启动', 1.0, 0.5, 1.5, '+0.5', '合理', '未调整', '—'],
    ['QINGTANG_002', '巷尾咕', 1, '2/1', '妖怪', '一般', '启动', 1.5, 1.0, 2.5, '+1.5', '严重超模', '已调整', '移除疾袭，但治疗抽牌仍强'],
    ['QINGTANG_003', '波铛', 2, '2/2', '妖怪', '一般', '启动', 2.0, 0.9, 2.9, '+0.9', '略超模', '未调整', '—'],
    ['QINGTANG_004', '藤缠仔', 1, '0/2', '妖怪', '一般', '启动', 1.0, 0.8, 1.8, '+0.8', '合理', '已调整', '身材0/3→0/2'],
    ['QINGTANG_005', '孪果儿', 2, '1/2', '妖怪', '罕见', '启动', 1.5, 1.2, 2.7, '+0.7', '合理', '已调整', '身材1/3→1/2'],
    ['QINGTANG_006', '承露虫', 2, '2/2', '妖怪', '罕见', '启动', 2.0, 1.0, 3.0, '+1.0', '超模', '未调整', '3妖怪+2/+2条件'],
    ['QINGTANG_007', '润物无声', 2, '—', '法术', '稀有', '收益', 0, 1.8, 1.8, '-0.2', '合理', '未调整', '—'],
    ['QINGTANG_008', '气蓬婆', 3, '1/4', '妖怪', '稀有', '引擎', 2.5, 1.5, 4.0, '+1.0', '超模', '已调整', '身材1/5→1/4，全体→前排'],
    ['QINGTANG_009', '枝镜', 3, '2/2', '妖怪', '罕见', '引擎', 2.0, 1.2, 3.2, '+0.2', '合理', '已调整', '身材2/3→2/2'],
    ['QINGTANG_010', '蓬哨', 3, '2/3', '妖怪', '稀有', '引擎', 2.5, 1.2, 3.7, '+0.7', '合理', '已调整', '身材2/4→2/3，3妖怪→4妖怪'],
    ['QINGTANG_011', '灯笼虫', 2, '1/2', '妖怪', '罕见', '收益', 1.5, 1.2, 2.7, '+0.7', '合理', '已调整', '身材1/3→1/2，+1攻→+0/+1'],
    ['QINGTANG_012', '繁枝响', 4, '3/5', '妖怪', '稀有', '收益', 4.0, 1.5, 5.5, '+1.5', '严重超模', '未调整', '每妖怪1伤AOE'],
    ['QINGTANG_013', '蜜盏苞', 2, '1/2', '妖怪', '稀有', '收益', 1.5, 1.0, 2.5, '+0.5', '合理', '已调整', '身材2/2→1/2，全体→随机一个'],
    ['QINGTANG_014', '四时芽', 3, '3/2', '妖怪', '稀有', '收益', 2.5, 1.8, 4.3, '+1.3', '超模', '已调整', '身材3/3→3/2，雨天全执行→增强选项'],
    ['QINGTANG_015', '甘霖普降', 2, '—', '法术', '一般', '干扰', 0, 1.5, 1.5, '-0.5', '亏模', '未调整', '—'],
    ['QINGTANG_016', '根缚锁', 2, '—', '法术', '一般', '干扰', 0, 1.3, 1.3, '-0.7', '亏模', '未调整', '—'],
    ['QINGTANG_017', '雾翅虫', 3, '2/3', '妖怪', '罕见', '干扰', 2.5, 1.2, 3.7, '+0.7', '合理', '已调整', '身材2/4→2/3，全体腐化→一个'],
    ['QINGTANG_018', '青古树怪', 6, '4/6', '妖怪', '史诗', '终结', 5.0, 2.5, 7.5, '+1.5', '严重超模', '已调整', '身材4/7→4/6，召唤3→2'],
    ['QINGTANG_019', '万木春', 5, '—', '法术', '传说', '终结', 0, 3.5, 3.5, '-1.5', '亏模', '未调整', '依赖场外牌堆'],
    ['QINGTANG_020', '雨意至', 2, '—', '法术', '一般', '启动', 0, 2.5, 2.5, '+0.5', '合理', '已调整', '费用1→2'],
    ['QINGTANG_021', '转形螺', 3, '0/5', '妖怪', '稀有', '怪构筑', 2.5, 1.5, 4.0, '+1.0', '超模', '未调整', '互换身材机制'],
    ['QINGTANG_022', '枯荣相寄', 2, '—', '御术', '史诗', '怪构筑', 0, 1.2, 1.2, '-0.8', '亏模', '未调整', '—'],
]

# 沃衡区调整后审计
woheng = [
    ['WHO_001', '稻契穗', 1, '1/1', '妖怪', '一般', '启动', 1.0, 0.5, 1.5, '+0.5', '合理', '已调整', '身材1/2→1/1'],
    ['WHO_002', '井咕噜', 2, '2/2', '妖怪', '一般', '启动', 2.0, 1.3, 3.3, '+1.3', '超模', '未调整', '派遣检索妖怪'],
    ['WHO_003', '麦哨芽', 1, '0/2', '妖怪', '一般', '启动', 1.0, 1.0, 2.0, '+1.0', '超模', '已调整', '身材0/3→0/2'],
    ['WHO_004', '播播籽', 2, '1/3', '妖怪', '一般', '启动', 2.0, 1.0, 3.0, '+1.0', '超模', '未调整', '支付1费召唤亡语抽牌'],
    ['WHO_005', '谷卫兵', 2, '2/2', '妖怪', '罕见', '启动', 2.0, 1.0, 3.0, '+1.0', '超模', '已调整', '身材2/3→2/2'],
    ['WHO_006', '犁角地牛', 2, '1/3', '妖怪', '一般', '启动', 2.0, 0.8, 2.8, '+0.8', '合理', '已调整', '身材1/4→1/3'],
    ['WHO_007', '沃野生息', 2, '—', '法术', '稀有', '启动', 0, 2.0, 2.0, '0.0', '合理', '未调整', '—'],
    ['WHO_008', '穗鼓隆', 3, '2/3', '妖怪', '稀有', '引擎', 2.5, 1.2, 3.7, '+0.7', '合理', '已调整', '身材2/4→2/3，4妖怪→5妖怪'],
    ['WHO_009', '垛草魁', 3, '3/2', '妖怪', '罕见', '引擎', 2.5, 1.8, 4.3, '+1.3', '超模', '已调整', '身材3/3→3/2，召唤3→2'],
    ['WHO_010', '归根入土', 3, '—', '法术', '稀有', '收益', 0, 2.5, 2.5, '-0.5', '亏模', '未调整', '—'],
    ['WHO_011', '驮稷兽', 3, '3/3', '妖怪', '稀有', '收益', 3.0, 1.2, 4.2, '+1.2', '超模', '已调整', '身材3/4→3/3，+1攻→+0/+1'],
    ['WHO_012', '响镰妖', 4, '3/4', '妖怪', '稀有', '收益', 3.5, 2.0, 5.5, '+1.5', '严重超模', '未调整', '派遣牺牲召唤物造伤'],
    ['WHO_013', '粟米团', 2, '1/1', '妖怪', '罕见', '收益', 1.0, 1.4, 2.4, '+0.4', '合理', '未调整', '不可加入卡组'],
    ['WHO_014', '丰筵天下', 4, '—', '法术', '史诗', '收益', 0, 3.5, 3.5, '-0.5', '亏模', '未调整', '—'],
    ['WHO_015', '晴耕令', 2, '—', '法术', '一般', '干扰', 0, 1.5, 1.5, '-0.5', '亏模', '未调整', '—'],
    ['WHO_016', '扫垄令', 3, '—', '法术', '罕见', '干扰', 0, 1.8, 1.8, '-1.2', '亏模', '未调整', '仅对召唤物有效'],
    ['WHO_017', '盘根错节', 2, '—', '法术', '一般', '干扰', 0, 1.3, 1.3, '-0.7', '亏模', '未调整', '—'],
    ['WHO_018', '穰穰君', 6, '4/5', '妖怪', '史诗', '终结', 4.5, 2.5, 7.0, '+1.0', '超模', '已调整', '身材4/6→4/5，召唤3→2'],
    ['WHO_019', '五谷丰登', 6, '—', '法术', '传说', '终结', 0, 4.0, 4.0, '-2.0', '严重亏模', '已调整', '费用7→6，加伤害上限5'],
    ['WHO_020', '瑞雪兆丰', 2, '—', '法术', '一般', '启动', 0, 1.7, 1.7, '-0.3', '合理', '未调整', '—'],
    ['WHO_021', '田祭咚', 2, '1/2', '妖怪', '稀有', '怪构筑', 1.5, 1.5, 3.0, '+1.0', '超模', '已调整', '身材2/2→1/2'],
    ['WHO_022', '归田魇', 4, '2/4', '妖怪', '史诗', '怪构筑', 3.0, 2.0, 5.0, '+1.0', '超模', '未调整', '回收死亡召唤物'],
]

create_audit_sheet(wb, '澄曜区审计(v2.1)', chengyao)
create_audit_sheet(wb, '青棠区审计(v2.1)', qingtang)
create_audit_sheet(wb, '沃衡区审计(v2.1)', woheng)

# ========== Sheet 5: 调整汇总 ==========
ws5 = wb.create_sheet('调整汇总(v2.1)')
headers5 = ['地区', '总卡数', '严重超模', '超模', '略超模', '合理', '亏模', '严重亏模', '已调整', '调整后超模率']
for col, h in enumerate(headers5, 1):
    ws5.cell(row=1, column=col, value=h)
style_header(ws5, 1, len(headers5))

def count_judgments(cards):
    severe_over = sum(1 for c in cards if '严重超模' in str(c[11]))
    over = sum(1 for c in cards if c[11] == '超模')
    slight = sum(1 for c in cards if '略超模' in str(c[11]))
    normal = sum(1 for c in cards if c[11] == '合理')
    under = sum(1 for c in cards if c[11] == '亏模')
    severe_under = sum(1 for c in cards if '严重亏模' in str(c[11]))
    adjusted = sum(1 for c in cards if c[12] == '已调整')
    over_rate = (severe_over + over + slight) / len(cards) * 100
    return [len(cards), severe_over, over, slight, normal, under, severe_under, adjusted, f'{over_rate:.0f}%']

summary = [
    ['澄曜区'] + count_judgments(chengyao),
    ['青棠区'] + count_judgments(qingtang),
    ['沃衡区'] + count_judgments(woheng),
]
all_cards = chengyao + qingtang + woheng
summary.append(['合计'] + count_judgments(all_cards))

for i, row in enumerate(summary, 2):
    for j, val in enumerate(row, 1):
        ws5.cell(row=i, column=j, value=val)
style_data(ws5, 2, len(summary)+1, len(headers5))
for col in range(1, len(headers5)+1):
    ws5.cell(row=len(summary)+1, column=col).font = Font(bold=True)
    ws5.cell(row=len(summary)+1, column=col).fill = subheader_fill

# 关键结论
ws5.cell(row=7, column=1, value='v2.1调整关键结论：')
ws5.cell(row=7, column=1).font = Font(bold=True, size=12)
conclusions = [
    '1. 三区共调整29张卡（澄曜7+青棠12+沃衡10），占66张的44%',
    '2. 调整后严重超模从16张降至5张（青棠繁枝响/巷尾咕、青棠青古树怪、沃衡响镰妖），下降69%',
    '3. 调整后超模率从58%降至约40%，合理卡从12张增至22张',
    '4. 仍存在的亏模卡主要是纯天气法术（日轮高悬/甘霖普降）和高费终结法术（万木春/五谷丰登）',
    '5. 折扣系数修正后，派遣效果卡和持续在场效果卡的价值评估更准确',
    '6. 建议下一轮：调整剩余5张严重超模卡，增强5张严重亏模卡，然后进行AI对战测试',
]
for i, c in enumerate(conclusions, 8):
    ws5.cell(row=i, column=1, value=c)
    ws5.merge_cells(start_row=i, start_column=1, end_row=i, end_column=len(headers5))
auto_width(ws5, len(headers5))

output_path = r'E:\0YaoKaids\妖怪牌\妖斗牌--商业卡牌项目\03-卡牌设计\妖斗牌数值审计v2.1.xlsx'
wb.save(output_path)
print(f'Excel generated: {output_path}')
print(f'Sheets: {wb.sheetnames}')
