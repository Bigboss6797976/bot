from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline_menu import main_menu

async def cmd_start(message: types.Message):
    welcome_text = (
        "🎰 **J88宝博国际娱乐** 🎰\n\n"
        "官方认证入口 | 全球信赖品牌\n\n"
        "📢 官方频道：@J88sportsbot\n"
        "💬 官方群组：@J88sportsbot\n"
        "👤 官方客服：@J88sportsbot\n"
        "🤖 游戏机器人：@J88sportsbot\n\n"
        "🔐 **官方认证公告**\n"
        "为全面保障会员资金与账号安全，J88宝博现公布官方唯一认证渠道：\n"
        "• 官方频道：@J88sportsbot\n"
        "• 官方群组：@J88sportsbot\n"
        "• 官方客服：@J88sportsbot\n"
        "• 游戏机器人：@J88sportsbot\n\n"
        "✅ 所有账号均为官方认证渠道，请务必核对账号名称及认证标识后再进行操作\n\n"
        "✅ **官方认证**\n"
        "身份真实 | 平台唯一，不可伪造\n"
        "资金安全 | 充值、提现全程保障\n"
        "沟通可靠 | 官方直连，杜绝中间风险\n\n"
        "⚠️ **风险提示**\n"
        "任何未带官方认证标识的账号均非J88宝博官方渠道！\n"
        "请勿向非认证账户转账，谨防冒充客服诈骗\n\n"
        "‼️ **声明**：J88宝博国际娱乐只做海外市场，从不涉及中国市场。\n\n"
        "👇 请点击下方按钮进入游戏或联系官方渠道"
    )
    photo_url = "https://via.placeholder.com/800x400.png?text=J88+BaoBo+Entertainment"
    await message.answer_photo(
        photo=photo_url,
        caption=welcome_text,
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )
